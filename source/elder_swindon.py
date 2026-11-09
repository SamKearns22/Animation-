#!/usr/bin/env python3
"""Elder Scrolls: Swindon. A parody of the Elder Scrolls VI: Sentinel name-reveal teaser, beat for beat to its sound.
From the satire template (guides/satire.md). Notes: notes/elder-swindon.md.

MAP (rule 61: a note is answered by reading only these lines)
- STORY (top): shots, timing, HOOK, HAS, the brief's lists
- world: the man, scroll, can, packet, litter, lamp post, soil patch (WORLD block); roundabout geometry (AERIAL block)
- cameras: cam_for (shot 1 glide, shot 2 glide, shot 3, shot 4, the climb, shot 6 drift)
- the man (man_at: the leg jerked by the dog), face_close (his face on its cheek, the close shots)
- the dog: dog_at (charge, clamp, tug and shake), draw_dog
- the scroll: scroll_cover (soil stripped off in gusts), glint; the packet: packet_at, draw_packet (tumbling)
- near_real: the near-real frame (ground regions, lamp shadow, props, man, dog, dust)
- the aerial: traffic (route network, give-way sim), aerial_flat (the Magic Roundabout, flat house style)
- title: rings, "The Elder Scrolls VI", SWINDON burning in letter by letter (overlay)
- picture / overlay / draw_order / scene / checks / main

    python3 source/elder_swindon.py stills OUT_DIR T [T ...]
    python3 source/elder_swindon.py sheet OUT.jpg T [T ...]      labelled check sheet (1080 px wide)
    python3 source/elder_swindon.py check
    python3 source/elder_swindon.py final OUT.mp4 [--small] [--span T0 T1]
"""
import hashlib
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import mossad as M               # noqa: E402,F401  (brows, mouths, hair; patched into burnham on import)
import figure as F               # noqa: E402
import mossad_audio as MA        # noqa: E402
import filmkit                   # noqa: E402
import film_engine as E          # noqa: E402
import sets as S                 # noqa: E402
import lying as L                # noqa: E402
import elder_swindon_comp as C   # noqa: E402  the composition sheet's props, dog, aerial (approved 8 Nov)
import elder_swindon_ground as G  # noqa: E402  the near-real ground
from satire_style import install_circle_hands   # noqa: E402
from ed import INK               # noqa: E402

install_circle_hands(B)
FPS, SR = 24, MA.SR              # 24, not the satire 12: slow camera glides judder at 12 (as Flying Whales)

# =============================================== STORY ===============================================
NAME = 'elder_swindon'
NOTES = os.path.join(os.path.dirname(HERE), 'notes', 'elder-swindon.md')
HAS = {'people', 'effects', 'props'}
SOUND_END = 30.04                             # the teaser's sound (Sam's first recording) ends here
REC2_AT = 28.7701                             # where Sam's second recording starts, in the first one's time
EXTRA = 5.0                                   # (Sam, animatic 3) 5 s more of the track, from his second recording,
DUR = SOUND_END + EXTRA                       # the aerial held for them; finish.py adds the 1.6 s sign-off
BLACK_AT = DUR
HOOK = ('Elder Scrolls reveals new location!', {'y': 1265, 'x': 600, 'until': 4.0})   # right of the can's path
SUBTITLES_AT_FINISH = False                   # no voices, no subtitles
SUBS_IN_PICTURE = False
LINES = []
HITS = (1.07, 2.49, 6.57, 7.37, 7.79, 11.43, 13.86, 15.08, 17.45, 19.86, 21.93, 24.76, 27.19)   # the sound's hits
SHOTS = [('1 can-face', 0.0, 6.57), ('2 scroll', 6.57, 11.43), ('3 packet', 11.43, 15.08),
         ('4 above', 15.08, 17.45), ('5 climb', 17.45, 19.86), ('6 roundabout', 19.86, DUR)]
# (Sam, animatic 2: less time on his face; shot 3 a few beats longer, the packet landing by the scroll; the dog held
# a beat longer before the climb.) Every cut still on a hit of the sound.
CLIMB0, CLIMB1 = 17.45, 19.86                 # the climb (was 16.50-17.45 in animatic 1, 16.90-19.86 in animatic 2)
MIX0, MIX1 = 18.20, 18.60                     # near-real gives way to flat while the climb is fastest
SHOT_CAST = {'1 can-face': ['DROOLER'], '2 scroll': ['SCROLL'], '3 packet': ['PACKET', 'SCROLL'],
             '4 above': ['DROOLER', 'STAFFIE', 'SCROLL', 'CAN', 'PACKET'], '5 climb': ['DROOLER', 'STAFFIE'],
             '6 roundabout': ['DROOLER']}
BENCHMARK = [dict(place='Magic Roundabout', refs=['references/elder-swindon/magic-roundabout-1.jpg',
                                                  'references/elder-swindon/magic-roundabout-2.jpg',
                                                  'references/elder-swindon/magic-roundabout-3-high.jpg',
                                                  'references/elder-swindon/magic-roundabout-4-stadium.jpg',
                                                  'references/elder-swindon/magic-roundabout-5-above.jpg'], at=24.0, items=[
    ('one big central circle: dark paving, white kerb, tall lamp post with its long shadow', 'aerial_flat: island, kerb, LAMP, shadow'),
    ('five mini roundabouts round it, white domes in white rings', 'MINIS: dome and ring'),
    ('traffic: anticlockwise round the inner ring, clockwise round each mini; dozens of cars, a bus', 'traffic(): routes, sim'),
    ('dense white markings: give-way dashes, arrows, hatching', 'aerial_flat: dashes, arrows, hatched areas'),
    ('raised kerbed islands between the minis', 'aerial_flat: islands'),
    ('zebra crossings on the approaches', 'aerial_flat: zebras'),
    ('grass verges with trees, five roads fanning out', 'aerial_flat: arms, verges, trees'),
    ('round it: terraced streets of brown and grey roofs with back gardens', '_estate: terraces, gardens'),
    ('a big white-roofed shed and a car park', 'aerial_flat: SHED, CARPARK'),
    ('the County Ground stadium next door: pitch, red seats, floodlights', 'aerial_flat: STADIUM'),
    ('grass and kerbed islands between the arms, not one sheet of tarmac', 'aerial_flat: inner ring, mini rings, arms'),
])]
EFFECTS = []                                  # filled below the drawing code (each with its test drawing: rule 15)
JOKE_PROPS = [('CAN', [1.0, 3.0], (-0.61, 0.03, -0.92), 0.15), ('PACKET', [14.9], lambda t: packet_at(t)[0], 0.13)]
ALLOWED_CONTACTS = [('STAFFIE*', 'DROOLER*', 15.62, DUR, 'the Staffie clamps his ankle (Sam, 8 Nov)'),
                    ('DROOLER*', 'DROOLER*', 0.0, DUR, 'one lying body: its own parts touch')]
ALLOWED_POPS = [('SCROLL', 7.30, 7.80, 'uncovered by the wind: it was under the soil')]
TOUCHES, FREE_MOVES, RESTS = [], [('PACKET', 13.86, 14.95, 'blown along by the wind, tumbling')], []
ORDER_SWAPS = []
KEEP_CLEAR = []
PROP_SIZES = []
OUTFIT = {'DROOLER': {}}                      # a tracksuit: no skirt, jacket hem or cuffs to place
HEIGHTS = {'DROOLER': 1.78}
LINE_OK = [('DROOLER', 'edge with no line', 578, 553)]   # the kit's flat shadow side on the cheek (guides/satire.md)
# ====================================================================================================

# ------------------------------------------------------------------------------------------------ WORLD (metres)
MAN = dict(C.MAN, name='DROOLER', jacket=(132, 134, 140), trousers=(84, 88, 100), belt=(78, 82, 94),
           beard='stubble', heavy_stubble=True, beard_c=(150, 104, 66),
           skin=(222, 178, 150), harrow=0.85, age=True, creases=2)   # (Sam: "make him look like shit")
#                                    sallow, blotchy red cheeks, dark bags under the eyes, lined   # (Sam, note 6) a grey hoody, gingery stubble, short crop: general traits only
#                                    from Sam's reference photos, no likeness of anyone (house-style face)
SCROLL, CAN, LITTER = C.SCROLL, C.CAN, C.LITTER
PACKET_REST = (-1.01, -0.90, 35.0)              # where the packet lands: beside the scroll (Sam, animatic 2)
SUN_XZ = np.array([0.857, 0.514])                # shadows fall this way (away from the low sun)
LAMP = (-2.93, -1.24)                            # the lamp post, centre of the island; its shadow passes his legs
LAMP_H = 18.0
SHADOW_LEN = 14.0                                # (Sam, note 3: the shadow was huge, 47 m) kept short: it still crosses his legs
PATCH_C = (-0.35, -0.25)                         # the soil-and-grass patch round him (Q2)


def patch_r(th):
    return 2.9 + 0.45 * np.sin(3 * th + 1.0) + 0.3 * np.sin(5 * th + 2.0) + 0.15 * np.sin(9 * th)


def in_patch(X, Z):
    dx, dz = X - PATCH_C[0], Z - PATCH_C[1]
    return np.hypot(dx, dz) - patch_r(np.arctan2(dz, dx))   # < 0 inside


def lamp_sun(X, Z):
    """Sunlight let through at each ground point: the lamp post's long shadow (pole and head), soft-edged."""
    px, pz = X - LAMP[0], Z - LAMP[1]
    s = px * SUN_XZ[0] + pz * SUN_XZ[1]
    n = -px * SUN_XZ[1] + pz * SUN_XZ[0]
    pole = np.clip(1 - (np.abs(n) - 0.14) / 0.04, 0, 1) * (s > 0) * (s < SHADOW_LEN)
    head = np.clip(1 - (np.hypot(s - SHADOW_LEN, n * 1.6) - 0.9) / 0.1, 0, 1)
    return 1 - 0.78 * np.maximum(pole, head)


# map coords (metres; mx screen right, my screen down in the top-down shots) <-> world: x = -mx, z = my
def world(mx, my):
    return (LAMP[0] - mx, LAMP[1] + my)


def ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def keys(t, ks):
    """Eased in-between of keyframes [(t, (values...))]."""
    if t <= ks[0][0]:
        return ks[0][1]
    for (a, va), (b, vb) in zip(ks, ks[1:]):
        if t <= b:
            u = ease((t - a) / (b - a))
            return tuple(x + (y - x) * u for x, y in zip(va, vb))
    return ks[-1][1]


def gust(t):
    """How hard the wind blows (0..1): gusts on the sound's hits (1.07, 2.49, 6.57, 7.37 strips the scroll)."""
    g = 0.15
    for h, a in ((1.07, 0.6), (2.49, 0.7), (5.3, 0.8), (6.57, 0.7), (7.37, 1.0), (8.2, 0.6), (9.0, 0.7),
                 (9.9, 0.6), (10.6, 0.7), (12.3, 0.9), (13.86, 0.6)):
        g = max(g, a * math.exp(-((t - h - 0.25) / 0.45) ** 2) * (t > h - 0.05))
    return g


# ------------------------------------------------------------------------------------------------ cameras
def shot_of(t):
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


SHOT1 = [(0.0, (-0.74, -1.16, 225, 70, 0.62)), (0.6, (-0.71, -1.16, 222, 70, 0.61)),     # the approved opening
         #                                    (nudged to follow the hand, laid further out: note 6)
         (2.8, (-0.38, -1.00, 210, 66, 0.56)), (4.4, (-0.13, -0.92, 192, 58, 0.50)),     # along the arm, to the face
         (6.57, (-0.12, -0.90, 186, 56, 0.45))]                                          # (2 s on it: was 3.9)
SHOT2 = [(6.57, (-0.84, -1.14, 180, 68, 0.40)), (7.37, (-0.84, -1.14, 180, 68, 0.40)),   # the tip, stripped on 7.37
         (9.0, (-0.86, -1.04, 180, 66, 0.38)), (11.43, (-0.86, -0.82, 180, 64, 0.36))]   # the end cap, the case
SHOT3 = [(11.43, (-0.92, -0.86, 180, 66, 0.98)), (15.08, (-0.92, -0.94, 180, 66, 0.90))]
TOP0 = (0.0, -0.25, 2.6)                          # shot 4: straight down, centre (x, z), metres across
END_W = 168.0                                    # shot 6: the whole roundabout (1080 px = 168 m)
END_MY = 60.0 - 0.08 * 1920 * END_W / 1080      # Sam's note 17: the animatic's 19.83 s view moved north by 8% of
END_C = world(0.0, END_MY)                       # the frame, so his blue line (across the pitch) is the bottom


def climb_u(t):
    """The climb's progress 0..1: slow start (the dog reads), fast middle, eased stop on the 19.86 hit."""
    u = min(1.0, max(0.0, (t - CLIMB0) / (CLIMB1 - CLIMB0)))
    return ease(u)


def top_view(t):
    """(centre x, z, width) of the straight-down camera, shots 4-6."""
    if t < CLIMB0:
        return TOP0[0], TOP0[1] + 0.03 * (t - 15.08), TOP0[2] - 0.06 * (t - 15.08)
    if t < CLIMB1:                                     # the centre's offset grows with the width, so he stays
        e = climb_u(t)                                   # in the frame all the way up
        w0 = TOP0[2] - 0.06 * (CLIMB0 - 15.08)
        w = w0 * (END_W / w0) ** e
        c0 = np.array([TOP0[0], TOP0[1] + 0.03 * (CLIMB0 - 15.08)])
        off = (np.array(END_C) - c0) / END_W * w * e ** 0.5
        return c0[0] + off[0], c0[1] + off[1], w
    u = (t - CLIMB1) / (DUR - CLIMB1)                  # shot 6: a slow drift, as the teaser's held end card
    mx, my = 3.0 * u, -2.0 * u
    x, z = world(mx, END_MY + my)
    return x, z, END_W * (1 - 0.06 * u)


def cam_for(t):
    s = shot_of(t)
    if s[0] in '123':
        ks = SHOT1 if s[0] == '1' else SHOT2 if s[0] == '2' else SHOT3
        x, z, az, el, w = keys(t, ks)
        return C.orbit((x, z), az, el, 0.9, w)
    x, z, w = top_view(t)
    return C.topcam(x, z, w * 3.0 / 2.6, w)


# ------------------------------------------------------------------------------------------------ the man
_K0 = None


def man_base():
    """The comp's face-down man with the flung arm laid flat on the soil (Sam, note 6: it curled up off the ground):
    reaching out past his head, near straight, the elbow out to the side along the ground."""
    k, surf = C.man()
    k = dict(k)
    tgt = np.array([-0.40, 0.05, -1.13])
    k['elR'], k['wrR'] = L._limb_clear(k['shR'], tgt, L.UPPER, L.FORE, np.array([-1.0, 0.0, 0.0]), 0.05, 0.0)
    return k, surf


def man_parts(k):
    """His body's volumes plus the hoody's hood, down and bunched at the nape (note 6)."""
    prts = L.parts(k, MAN)
    X_ = k['shR'] - k['shL']
    X_ = X_ / np.linalg.norm(X_)
    up = np.array([0.0, 1.0, 0.0])
    al = np.cross(X_, up)
    back = k['neck'] + up * 0.075 + (k['pelvis'] - k['neck']) / np.linalg.norm(k['pelvis'] - k['neck']) * 0.05
    prts.append(L.Part('hood', L.ELL, back, axes=np.array([X_, up, al]), radii=(0.125, 0.05, 0.085), mat='top',
                       group=1))
    return prts


STAINS = [('chest', 0.5, 0.115, 0.045, (96, 84, 52)), ('chest', 0.15, 0.11, 0.035, (120, 96, 50)),
          ('forearmR', 0.45, 0.045, 0.03, (110, 84, 50)), ('thighL', 0.55, 0.075, 0.04, (70, 54, 38)),
          ('shinR', 0.3, 0.06, 0.035, (74, 58, 40)), ('upperR', 0.6, 0.05, 0.028, (150, 110, 60))]


def draw_stains(pil, cam, k):
    """Grubby stains on his hoody and trackies (spilt lager, sick, mud), on the side the camera sees (his back),
    fixed to his joints so they move with him."""
    d = ImageDraw.Draw(pil, 'RGBA')
    ss = B.SS
    seg = {'chest': ('waist', 'neck'), 'forearmR': ('elR', 'wrR'), 'thighL': ('hipL', 'knL'), 'shinR': ('knR', 'anR'),
           'upperR': ('shR', 'elR')}
    for i, (part, u, lift, r, col) in enumerate(STAINS):
        a, b = seg[part]
        p = k[a] + (k[b] - k[a]) * u + np.array([0.0, lift, 0.0])
        (x, y), kk = cam.project(tuple(p))
        R = r * kk * ss
        if R < 1.5:
            continue
        pts = [(x * ss + R * (1 + 0.25 * math.sin(3 * t_ + i)) * math.cos(t_),
                y * ss + R * 0.8 * (1 + 0.25 * math.sin(3 * t_ + i)) * math.sin(t_))
               for t_ in np.linspace(0, 2 * math.pi, 18, endpoint=False)]
        d.polygon(pts, fill=col + (120,))


def man_at(t):
    """His body at t: face down, out cold (Sam, 8 Nov); only the left leg jerks with the dog's tugging."""
    global _K0
    if _K0 is None:
        _K0 = man_base()
    k0, surf = _K0
    d = dog_at(t)
    if d is None or not d['clamped']:
        return k0, surf
    k = dict(k0)
    pull = np.array([d['jaw'][0] - d['jaw0'][0], 0.0, d['jaw'][1] - d['jaw0'][1]])
    k['anL'] = k0['anL'] + pull
    k['knL'] = k0['knL'] + pull * 0.35
    return k, surf


def face_close(pil, cam, k, sp, t, pool=True):
    """His face on its cheek, for the close shots (lying.draw's face reads poorly face down): the house-style head
    (burnham.head: eyes shut, mouth hanging open) laid on its side at the head's place and size, its top along the
    head's own up. Returns the mouth's lower corner on the canvas (for the drool)."""
    ss = B.SS
    (hx, hy), kk = cam.project(tuple(k['head']))
    (ux, uy), _ = cam.project(tuple(k['head'] + k['hup'] * 0.1))
    up = np.array([ux - hx, uy - hy])
    up /= np.linalg.norm(up) + 1e-9
    side = np.array([-up[1], up[0]])                     # the face's across, on screen
    # which way is the ground: the cheek that is down goes towards screen down
    if side[1] < 0:
        side = -side
    ppu = float(np.squeeze(kk * L.M * ss))               # canvas pixels per person unit
    q = dict(sp, blink=True, mouth='open', look=0.0, turn=0.0)
    tex = L._head_tex(q, t, 'front', kk * L.M)
    timg = Image.fromarray(tex.astype(np.uint8), 'RGBA')
    sc = ppu / L.TEX_PPU                                 # canvas pixels per texel
    U = side * sc * 0.88                                 # texel u -> canvas (squashed a little across: foreshortened)
    V = -up * sc                                         # texel v (down) -> canvas
    cx, cy = hx * ss, hy * ss
    R = 140 * ppu
    x0, y0 = int(cx - R), int(cy - R)
    size = (int(2 * R), int(2 * R))
    # inverse affine: canvas (X, Y) -> texel (u, v):  [X-cx, Y-cy] = U*(u-384) + V*(v-384)
    det = U[0] * V[1] - V[0] * U[1]                      # the 2 x 2 inverse by hand: numpy's linear algebra can
    a, b = V[1] / det, -V[0] / det                       # lock up inside pre-flight's forked workers (it hung there)
    c, d = -U[1] / det, U[0] / det
    ox, oy = x0 - cx, y0 - cy
    coeffs = (a, b, a * ox + b * oy + 384, c, d, c * ox + d * oy + 384)
    lay = timg.transform(size, Image.AFFINE, coeffs, resample=Image.BICUBIC)
    # the cheek pressed into the soil: a soft contact shadow under the down side
    sh = Image.new('RGBA', size, (0, 0, 0, 0))
    gx, gy = R + side[0] * 70 * ppu, R + side[1] * 70 * ppu
    ImageDraw.Draw(sh).ellipse([gx - 80 * ppu, gy - 26 * ppu, gx + 80 * ppu, gy + 26 * ppu], fill=(30, 22, 16, 140))
    sh = sh.filter(ImageFilter.GaussianBlur(8 * ppu))
    pil.alpha_composite(sh, (x0, y0))
    # mouth: burnham draws it about 66 units below the head's centre; its lower corner is on the ground side
    mouth = np.array([cx, cy]) + (-up) * 66 * ppu + side * 6 * ppu * 0.88
    if pool:
        drool_pool(pil, mouth, side, ppu, t)             # the pool on the soil goes UNDER the face (note 8)
    pil.alpha_composite(lay, (x0, y0))
    return mouth, ppu, side


def drool_ground(pil, cam, k):
    """The damp drool patch on the soil at his mouth, drawn before his body so his head and arm lie over it."""
    head, fwd, up = np.asarray(k['head']), np.asarray(k['hfwd']), np.asarray(k['hup'])
    mouth = head + fwd * 0.085 - up * 0.045
    f2 = np.array([fwd[0], fwd[2]]) / (np.hypot(fwd[0], fwd[2]) + 1e-9)
    c = (mouth[0] + f2[0] * 0.03, mouth[2] + f2[1] * 0.03)
    d = ImageDraw.Draw(pil, 'RGBA')
    d.polygon(_ground_poly(cam, c, _blob(0.05, 24, 7, 0.2), h=0.002), fill=(58, 42, 32, 190))
    d.polygon(_ground_poly(cam, (c[0] + 0.01, c[1] - 0.01), _blob(0.015, 12, 8, 0.2), h=0.003), fill=(170, 170, 170, 90))


DRIP = 5.30                                      # a drop runs down the drool on a gust (6.57 is now the cut)
DROOL_EDGE, DROOL_POOL = 82, 100                 # person units from the mouth corner (towards the ground) to the
#                                                  face's edge, and to the pool's middle on the soil


def drool_pool(pil, mouth, side, ppu, t):
    """The dark damp patch on the soil just past his down cheek, spreading after the drip (6.57)."""
    d = ImageDraw.Draw(pil, 'RGBA')
    grow = 1.0 + 0.25 * ease((t - DRIP - 0.03) / 0.6)
    px, py = mouth + side * DROOL_POOL * ppu
    R = 34 * ppu * grow
    d.ellipse([px - R, py - R * 0.5, px + R, py + R * 0.5], fill=(58, 42, 32, 190))
    d.ellipse([px - R * 0.5, py - R * 0.1, px - R * 0.05, py + R * 0.25], fill=(160, 160, 160, 90))


def drool_close(pil, mouth, ppu, side, t, full=True):
    """A wet string from the corner of his mouth, lying on his cheek down to the face's edge (pinned there: it
    never floats, note 8), then a short sag to the pool on the soil; a drop runs down it on the 6.57 hit."""
    d = ImageDraw.Draw(pil)
    mx, my = mouth
    m = np.array([mx, my])
    edge = m + side * DROOL_EDGE * ppu
    pool = m + side * DROOL_POOL * ppu
    sway = (1.5 * ppu * math.sin(t * 2.3) + 3 * ppu * gust(t)) * np.array([1.0, 0.0])
    mid = tuple((edge + pool) / 2 + sway)
    w = max(2, int(3.5 * ppu))
    pts = [(mx, my), tuple(m + side * DROOL_EDGE * 0.5 * ppu + np.array([1.0, 0]) * 2 * ppu), tuple(edge), mid,
           tuple(pool)]
    if not full:                                         # from shot 2 on: only the strand on his cheek, to the face's
        pts = pts[:3]                                    # edge; the pool is on the ground under him (drool_ground)
    d.line(pts, fill=(206, 220, 226, 230), width=w, joint='curve')
    d.line([(p[0] + w * 0.3, p[1]) for p in pts[:3]], fill=(250, 252, 255, 200), width=max(1, w // 3))
    if DRIP <= t < DRIP + 0.38:                          # the drip
        u = (t - DRIP) / 0.38
        a, b = ((mx, my), tuple(edge)) if u < 0.5 else (tuple(edge), tuple(pool))
        v = (u * 2) % 1.0
        px, py = a[0] + (b[0] - a[0]) * v, a[1] + (b[1] - a[1]) * v
        r = 4.5 * ppu
        d.ellipse([px - r, py - r * 1.2, px + r, py + r * 1.2], fill=(214, 228, 234, 240))
        d.ellipse([px - r * 0.5, py - r * 0.8, px, py - r * 0.2], fill=(255, 255, 255, 230))


# ------------------------------------------------------------------------------------------------ the dog
DOG_IN, DOG_CLAMP = 15.25, 15.72
DOG_HEAD = 50.0                                  # heading (degrees) from his head to his tail, braced away


def dog_at(t):
    """The Staffie (brindle, Sam 8 Nov): charges in from bottom left (15.25), clamps on the left ankle (15.72),
    then tugs and shakes, braced, to the end. Returns jaw (x, z), heading, gait phase, clamped; None before."""
    if t < DOG_IN:
        return None
    k0 = _K0[0] if _K0 else man_base()[0]
    an = k0['anL']
    jaw0 = (an[0] + 0.02, an[2] + 0.04)
    a = math.radians(DOG_HEAD)
    back = np.array([math.cos(a), math.sin(a)])
    if t < DOG_CLAMP:
        u = (t - DOG_IN) / (DOG_CLAMP - DOG_IN)
        dist = 1.55 * (1 - u) ** 1.1                    # in from the frame's edge, flat out, a skid at the end
        jaw = (jaw0[0] + back[0] * dist, jaw0[1] + back[1] * dist)
        return dict(jaw=jaw, jaw0=jaw0, heading=DOG_HEAD + 6 * math.sin(u * 9), gait=(t - DOG_IN) * 7.0,
                    clamped=False, run=1.0)
    s = t - DOG_CLAMP
    tug = 0.07 * (0.5 - 0.5 * math.cos(s * 2 * math.pi * 1.6)) + 0.03 * min(1, s / 0.2)   # backing off, heaving
    shake = 13 * math.sin(s * 2 * math.pi * 4.2) * (0.6 + 0.4 * math.sin(s * 2.1) ** 2)   # head shaking side to side
    jolt = 0.04 * math.exp(-s / 0.08)                                                       # the hit as he clamps
    n = np.array([-back[1], back[0]])
    side = 0.025 * math.sin(math.radians(shake) * 3)
    jaw = (jaw0[0] + back[0] * (tug - jolt) + n[0] * side, jaw0[1] + back[1] * (tug - jolt) + n[1] * side)
    return dict(jaw=jaw, jaw0=jaw0, heading=DOG_HEAD + shake, gait=s * 3.0, clamped=True, run=0.25)


ST = C.STAFFIE


def draw_dog(pil, cam, d):
    """The Staffie from above, house style (flat colour, one outline): the comp's dog with running legs, the
    head swinging on the clamp."""
    hx, hz = d['jaw']
    a = math.radians(d['heading'])
    fx, fz = math.cos(a), math.sin(a)
    sx, sz = -fz, fx
    ss = B.SS

    def W(u, v):
        return (hx + fx * u + sx * v, 0.25, hz + fz * u + sz * v)

    def P(u, v):
        (x, y), _ = cam.project(W(u, v))
        return (x * ss, y * ss)
    (_, _), kk = cam.project(W(0.2, 0))
    lw = max(1, int(min(2.6, max(0.6, kk / 300)) * ss))
    dr = ImageDraw.Draw(pil)

    def poly(pts, fill):
        Q = [P(*p) for p in pts]
        dr.polygon(Q, fill=fill)
        dr.line(Q + [Q[0]], fill=INK, width=lw, joint='curve')
    sh = []
    for u, v in [(0.0, -0.12), (0.5, -0.15), (0.6, 0.0), (0.5, 0.15), (0.0, 0.12)]:
        (x, y), _ = cam.project((W(u, v)[0] + 0.08 * 0.857, 0.0, W(u, v)[2] + 0.08 * 0.514))
        sh.append((x * ss, y * ss))
    dr.polygon(sh, fill=(30, 22, 16, 110))
    g, run = d['gait'], d['run']
    for i, (u, v, du, dv) in enumerate(((0.14, -0.10, -0.06, -0.075), (0.14, 0.10, -0.06, 0.075),
                                        (0.45, -0.09, 0.07, -0.07), (0.45, 0.09, 0.07, 0.07))):
        ph = g * 2 * math.pi + (0, math.pi, math.pi * 0.5, math.pi * 1.5)[i]
        sw = 0.08 * run * math.sin(ph)                   # legs reaching and pushing (the charge), shuffling (the tug)
        tip = (u + du + sw, v + dv)
        poly([(u - 0.04, v * 0.8), (tip[0] - 0.028, tip[1]), (tip[0] + 0.028, tip[1]), (u + 0.04, v * 0.8)], ST['coat'])
        poly([(tip[0] - 0.024, tip[1] - 0.008 * np.sign(v)), (tip[0] + 0.024, tip[1] - 0.008 * np.sign(v)),
              (tip[0] + 0.02, tip[1] + 0.016 * np.sign(v)), (tip[0] - 0.02, tip[1] + 0.016 * np.sign(v))],
             ST['chest'])                                # white paws, dug in
    wag = 0.02 * math.sin(g * 6)
    poly([(0.50, -0.02), (0.64, -0.006 + wag), (0.64, 0.006 + wag), (0.50, 0.02)], ST['coat'])
    body = [(0.10, -0.10), (0.17, -0.155), (0.28, -0.13), (0.40, -0.10), (0.50, -0.11), (0.55, -0.06), (0.56, 0.0),
            (0.55, 0.06), (0.50, 0.11), (0.40, 0.10), (0.28, 0.13), (0.17, 0.155), (0.10, 0.10)]
    poly(body, ST['coat'])
    for u in (0.24, 0.31, 0.38, 0.45):                   # brindle stripes across the back
        a0, a1 = P(u, -0.08), P(u + 0.02, 0.08)
        dr.line([a0, a1], fill=ST['dark'], width=lw)
    head = [(-0.05, -0.07), (-0.02, -0.12), (0.05, -0.135), (0.10, -0.11), (0.12, -0.05), (0.12, 0.05), (0.10, 0.11),
            (0.05, 0.135), (-0.02, 0.12), (-0.05, 0.07)]
    poly(head, ST['coat'])                               # the wide head, a neck between it and the shoulders
    for v in (-0.06, 0.06):                              # brindle on the head
        dr.line([P(0.03, v), P(0.09, v * 1.3)], fill=ST['dark'], width=max(1, int(lw * 1.2)))
    poly([(-0.10, -0.055), (-0.04, -0.075), (-0.04, 0.075), (-0.10, 0.055)], ST['dark'])
    poly([(-0.02, -0.018), (0.10, -0.012), (0.10, 0.012), (-0.02, 0.018)], ST['chest'])     # the white blaze
    for v in (-1, 1):                                    # small rose ears, folded back flat (angry)
        poly([(0.075, v * 0.10), (0.125, v * 0.135), (0.125, v * 0.085)], ST['dark'])
    nose = P(-0.105, 0.0)
    r = 0.016 * kk * ss
    dr.ellipse([nose[0] - r, nose[1] - r, nose[0] + r, nose[1] + r], fill=ST['nose'])
    for v in (-0.05, 0.05):                              # eyes narrowed, brows down: angry
        ex, ey = P(0.02, v)
        r = 0.012 * kk * ss
        dr.ellipse([ex - r, ey - r * 0.5, ex + r, ey + r * 0.5], fill=(20, 16, 14))
        dr.line([P(-0.005, v * 0.6), P(0.0, v * 1.4)], fill=INK, width=max(1, int(lw * 1.2)))


# ------------------------------------------------------------------------------------------------ scroll, packet
def scroll_cover(t):
    """How buried the scroll still is: the reveal front runs from the far tip (t=1, the camera's start) back along
    it in gust steps, 7.37 to about 13.5 (the teaser's staff is fully out by 14 s). -1: all out; >1: all under."""
    if t < 7.37:
        return 2.0
    steps = ((7.37, 0.24), (8.2, 0.18), (9.0, 0.24), (9.9, 0.20), (10.6, 0.24))   # all out by about 11.2
    f = 1.05
    for h, dv in steps:
        f -= dv * ease((t - h) / 0.55)
    return f


def lying_rev(img, cam, a, b, prof, mat, cover=None, seed=0, glow=0.0, cam_along=0.0):
    """comp.lying_rev with the soil laid in the object's own coordinates (so it never swims as the camera glides)
    and the shine sliding with the camera along it (rule 39). cover: the reveal front (scroll_cover) or None."""
    ss = B.SS
    h, w, _ = img.shape
    (ax, ay), k = cam.project((a[0], 0.02, a[1]))
    (bx, by), _ = cam.project((b[0], 0.02, b[1]))
    ax, ay, bx, by, k = ax * ss, ay * ss, bx * ss, by * ss, k * ss
    Lp = math.hypot(bx - ax, by - ay)
    if Lp < 1:
        return img
    Lm = math.hypot(b[0] - a[0], b[1] - a[1])
    dx, dy = (bx - ax) / Lp, (by - ay) / Lp
    rmax = max(prof(t)[0] for t in np.linspace(0, 1, 200)) * k
    x0, x1 = int(max(0, min(ax, bx) - rmax - 2)), int(min(w, max(ax, bx) + rmax + 2))
    y0, y1 = int(max(0, min(ay, by) - rmax - 2)), int(min(h, max(ay, by) + rmax + 2))
    if x1 <= x0 or y1 <= y0:
        return img
    ys, xs = np.mgrid[y0:y1, x0:x1]
    px, py = xs + 0.5 - ax, ys + 0.5 - ay
    t = (px * dx + py * dy) / Lp
    s = (-px * dy + py * dx)
    tt = np.clip(t, 0, 1)
    tab = np.array([prof(v)[0] for v in np.linspace(0, 1, 512)]) * k
    kinds = np.array([prof(v)[1] for v in np.linspace(0, 1, 512)])
    idx = np.clip((tt * 511).astype(int), 0, 511)
    r = tab[idx]
    inside = (t >= 0) & (t <= 1) & (np.abs(s) < r)
    nrm = np.where(inside, s / np.maximum(r, 1e-6), 0)
    if cover is not None:
        nz = G.noise(tt * Lm, nrm * 0.03, 0.025, seed + 40)
        under = inside & (((1 - tt) - 0.12 * nz) > (1 - cover)) | inside & (nrm > 0.62 + 0.22 * nz)
    else:
        under = np.zeros_like(inside)
    vis = inside & ~under
    sh = np.zeros((y1 - y0, x1 - x0))
    off = 0.6
    s2 = (-(px - r * off) * dy + (py - r * off * 0.6) * dx)
    t2 = ((px - r * off) * dx + (py - r * off * 0.6) * dy) / Lp
    sh[(t2 >= 0) & (t2 <= 1) & (np.abs(s2) < r * 1.05)] = 1
    if cover is not None:                                # the soil over it casts no shadow of the scroll
        sh *= ~((((1 - np.clip(t2, 0, 1)) > (1 - cover))))
    sh = np.asarray(Image.fromarray((sh * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3 * ss)), float) / 255
    reg = img[y0:y1, x0:x1]
    soil0 = reg.copy()
    reg *= (1 - 0.55 * sh)[..., None]
    out = reg.copy()
    slide = np.exp(-((tt * Lm - cam_along) / 0.12) ** 2)   # the sun's glow on the gold slides with the camera
    for kind in set(kinds.tolist()):
        sel = vis & (kinds[idx] == kind)
        if not sel.any():
            continue
        base, metal, spec = mat(kind, tt[sel], nrm[sel])
        if metal:
            spec = spec * (0.75 + 0.6 * slide[sel] + glow)
        out[sel] = C._shade(base, nrm[sel], metal, spec)
    if cover is not None and (inside & under).any():     # soil heaped over it: the ground, a little proud (it
        un = inside & under                              # catches the sun), and a soft dark lip on the metal
        out[un] = np.clip(soil0[un] * (1.06 + 0.10 * (-nrm[un])[:, None]), 0, 1)
        edge = np.asarray(Image.fromarray(un.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(5)), bool) & vis
        out[edge] *= 0.75
    reg[:] = out
    return img


def _prof_can(t):
    if t < 0.03 or t > 0.97:
        return 0.029, 'rim'
    return 0.033, 'body'


def _can_label():
    """The label: silver, a red band, EXPORT / LAGER on two rows in white near the top end (Sam, Q5), so the buried
    end never cuts the words (the composition sheet read "RT LAGER")."""
    w, h = 600, 300                                       # along the can x round the can
    im = Image.new('RGB', (w, h), (196, 200, 206))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 84, w, 216], fill=(176, 28, 34))
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 50)
    d.text((410, 120), 'EXPORT', font=f, fill=(250, 250, 248), anchor='mm')
    d.text((410, 180), 'LAGER', font=f, fill=(250, 250, 248), anchor='mm')
    d.text((410, 250), '4.0% vol  440ml', font=ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'),
                                                                 22), fill=(60, 60, 70), anchor='mm')
    return np.asarray(im, float) / 255


_LABEL = None


def can_mat(kind, t, nrm):
    global _LABEL
    if _LABEL is None:
        _LABEL = _can_label()
    if kind == 'rim':
        return np.tile(np.array([0.70, 0.72, 0.75]), (len(t), 1)), True, 0.8
    h, w, _ = _LABEL.shape
    u = np.clip(((t - 0.03) / 0.94) * (w - 1), 0, w - 1).astype(int)
    v = np.clip((np.arcsin(np.clip(nrm, -1, 1)) / math.pi + 0.5) * (h - 1), 0, h - 1).astype(int)
    dent = 0.25 * np.exp(-(((t - 0.45) / 0.08) ** 2 + ((nrm + 0.2) / 0.3) ** 2))
    return _LABEL[v, u] * (1 - dent[:, None]), True, 0.7


PACK_IN, PACK_LAND = 12.30, 13.86                # blown in on a gust, lands by the scroll on the 13.86 hit


def packet_at(t):
    """The sandwich packet: blown in from beyond his hand, tumbling end over end past the scroll on the wind (-z),
    landing on its back... then flipped label-up by the last bounce; at rest from 14.95. Returns (centre (x, y, z),
    tumble angle (radians), turn (degrees)); None before it blows in."""
    if t < PACK_IN:
        return None
    x1, z1, turn1 = PACKET_REST
    x0, z0 = -0.60, -0.10
    if t >= PACK_LAND + 0.09:
        return (x1, 0.03, z1), 2 * math.pi * 3, turn1
    u = min(1.0, (t - PACK_IN) / (PACK_LAND - PACK_IN))
    x = x0 + (x1 - x0) * u
    z = z0 + (z1 - z0) * u
    y = 0.03 + 0.16 * math.sin(math.pi * u) ** 0.8 + (0.04 * math.sin(math.pi * (t - PACK_LAND) / 0.09) if t > PACK_LAND else 0)
    ang = 2 * math.pi * 3 * ease(u * 1.02)               # three times end over end
    return (x, y, z), ang, turn1 - 50 * (1 - u)


_PACK_TEX = {}


def _pack_tex(front):
    """The packet's two faces as textures (0.14 m square, 1000 px a metre): front = the comp's EGG MAYO wedge."""
    if front in _PACK_TEX:
        return _PACK_TEX[front]
    n = 140
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    def p(u, v):
        return (n / 2 + u * 1000, n / 2 + v * 1000)
    tri = [p(-0.065, 0.065), p(0.065, 0.065), p(-0.065, -0.065)]
    d.polygon(tri, fill=(232, 234, 228, 255))
    if front:
        d.polygon([p(-0.05, 0.05), p(0.025, 0.05), p(-0.05, -0.025)], fill=(236, 214, 150, 255))
        d.line([p(-0.05, 0.05), p(0.025, 0.05), p(-0.05, -0.025), p(-0.05, 0.05)], fill=(250, 250, 250, 255), width=2)
        d.polygon([p(-0.065, 0.065), p(0.065, 0.065), p(0.05, 0.05), p(-0.05, 0.05)], fill=(52, 120, 70, 255))
        f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 11)
        d.text(p(-0.005, 0.0575), 'EGG MAYO', font=f, fill=(255, 255, 255, 255), anchor='mm')
        im = im.transpose(Image.FLIP_LEFT_RIGHT)         # the front is seen from behind the texture: mirror it so
        #                                                  EGG MAYO reads (Sam, animatic 4: it was backwards)
    else:
        d.polygon([p(-0.065, 0.065), p(0.065, 0.065), p(0.05, 0.05), p(-0.05, 0.05)], fill=(52, 120, 70, 255))
        for i in range(9):                               # the barcode
            x = -0.04 + i * 0.004
            d.line([p(x, -0.01), p(x, 0.02)], fill=(30, 30, 30, 255), width=1 + i % 2)
    _PACK_TEX[front] = im
    return im


def _persp_coeffs(src, dst):
    """PIL PERSPECTIVE coefficients mapping output points dst -> input points src (4 each)."""
    A, bb = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        bb += [u, v]
    n = 8                                                # Gauss-Jordan by hand (see face_close: no numpy linalg
    M_ = [row + [v] for row, v in zip(A, bb)]            # in the forked workers)
    for i in range(n):
        piv = max(range(i, n), key=lambda r: abs(M_[r][i]))
        M_[i], M_[piv] = M_[piv], M_[i]
        f = M_[i][i]
        M_[i] = [x / f for x in M_[i]]
        for r in range(n):
            if r != i and M_[r][i]:
                g = M_[r][i]
                M_[r] = [x - g * y for x, y in zip(M_[r], M_[i])]
    return [M_[i][n] for i in range(n)]


def draw_packet(pil, cam, t):
    """The packet as a card turning end over end about the axis across the wind, its shadow on the soil."""
    st = packet_at(t)
    if st is None:
        return
    (x, y, z), ang, turn = st
    ss = B.SS
    tr = math.radians(turn)
    ax = np.array([math.cos(tr), 0, math.sin(tr)])       # the card's across (u)
    al = np.array([-math.sin(tr), 0, math.cos(tr)])      # its along (v), tumbling about u
    vv = al * math.cos(ang) + np.array([0, 1, 0]) * math.sin(ang)
    nn = np.cross(ax, vv)
    c = np.array([x, y, z])
    corners = [c - ax * 0.07 - vv * 0.07, c + ax * 0.07 - vv * 0.07, c + ax * 0.07 + vv * 0.07, c - ax * 0.07 + vv * 0.07]
    scr = [tuple(v * ss for v in cam.project(tuple(p))[0]) for p in corners]
    shad = [tuple(v * ss for v in cam.project((p[0] + p[1] * 0.857 * 2.6, 0.0, p[2] + p[1] * 0.514 * 2.6))[0])
            for p in corners]
    lay = Image.new('RGBA', pil.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).polygon(shad, fill=(30, 22, 16, int(150 * max(0.2, 1 - y * 3))))
    pil.alpha_composite(lay.filter(ImageFilter.GaussianBlur(4 * ss)))
    tocam = np.asarray(cam.pos) - c
    front = float(np.dot(nn, tocam)) < 0                # label side: the one facing up when it lands
    tex = _pack_tex(front)
    n = tex.width
    src = [(0, 0), (n, 0), (n, n), (0, n)]
    xs = [p[0] for p in scr]
    ys = [p[1] for p in scr]
    bx0, by0 = int(min(xs)) - 2, int(min(ys)) - 2
    bw, bh = int(max(xs)) - bx0 + 3, int(max(ys)) - by0 + 3
    if bw < 2 or bh < 2 or bw > 4000 or bh > 4000:
        return
    e1, e2 = np.subtract(scr[1], scr[0]), np.subtract(scr[3], scr[0])
    area = abs(e1[0] * e2[1] - e1[1] * e2[0])
    if area < 4:                                         # edge on: a thin line of card
        ImageDraw.Draw(pil).line([scr[0], scr[2]], fill=(214, 216, 210), width=max(2, int(3 * ss)))
        return
    co = _persp_coeffs(src, [(px - bx0, py - by0) for px, py in scr])
    shade = 0.75 + 0.25 * abs(float(np.dot(nn, [-0.80, 0.36, -0.48])))
    im = tex.transform((bw, bh), Image.PERSPECTIVE, tuple(co), resample=Image.BICUBIC)
    arr = np.asarray(im, float)
    arr[..., :3] *= shade
    pil.alpha_composite(Image.fromarray(arr.clip(0, 255).astype(np.uint8), 'RGBA'), (bx0, by0))


def packet_rest_flat(pil, cam, ss):
    """The packet at rest, label up (shots 4 on): the comp's flat wedge."""
    x, z, a = PACKET_REST
    C.packet(pil, cam, x, z, a)


# ------------------------------------------------------------------------------------------------ near-real frame
def ground_ss():
    return 1                                             # the ground is worked out at 1080 x 1920 and enlarged:
    #                                                      the finished film is 1080 wide, so nothing is lost


def near_ground(cam, t):
    """The near-real ground under every pixel: the soil-and-grass patch, the island's dark paving round it, the
    white kerb, the tarmac beyond; the lamp post's shadow across all of it. RGB float at the canvas size."""
    w, h = B.W, B.H
    rays = G.ground_rays(cam, w, h, 1)
    X, Z, mpp = rays
    img, _ = G.soil(cam, ss=1, grass=0.0, t=t, gust=gust(t), sun=lamp_sun, rays=rays)
    dp = in_patch(X, Z)
    if dp.max() > -0.05:                                 # beyond the patch is in shot: paving, kerb, tarmac
        r = np.hypot(X - LAMP[0], Z - LAMP[1])
        mx, my = -(X - LAMP[0]), Z - LAMP[1]
        n1 = G.noise(X, Z, 0.4, 61)
        slab = ((np.abs(((mx + 0.3) % 0.6) - 0.3) < 0.008) | (np.abs(((my + 0.3) % 0.6) - 0.3) < 0.008))
        pav = np.array([0.30, 0.29, 0.28])[None, None, :] * (1 + 0.08 * n1[..., None])
        pav = pav * (1 - 0.18 * (slab * G._lod(0.03, mpp))[..., None])
        tar = np.array([0.24, 0.24, 0.25])[None, None, :] * (1 + 0.05 * G.noise(X, Z, 0.15, 62)[..., None])
        kerb = np.array([0.78, 0.77, 0.74])[None, None, :]
        ground = np.where((r < 15.0)[..., None], pav, np.where((r < 15.35)[..., None], kerb, tar))
        sunl = lamp_sun(X, Z)[..., None]
        ground = ground * (G.SKY_C * 0.55 + G.SUN_C * 1.05 * 0.9 * sunl)
        edge = np.clip((dp + 0.06 * G.noise(X, Z, 0.08, 63)) / 0.05, 0, 1)[..., None]   # a ragged soil edge
        img = img * (1 - edge) + ground * edge
        pole = np.clip(1 - (r - 0.16) / 0.02, 0, 1)[..., None]      # the lamp post's foot, from above
        img = img * (1 - pole) + np.array([0.20, 0.20, 0.22]) * pole
    if B.SS != 1:
        img = np.asarray(Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).resize(
            (w * B.SS, h * B.SS), Image.BICUBIC), float) / 255
    G.GRASS_MASK = lambda x, z: in_patch(x, z) < -0.08      # grass only on the soil patch
    img = G._grass(img, X, Z, mpp / B.SS, cam, B.SS, 0.45, 3, t, gust(t)) \
        if float(np.median(mpp)) < 0.02 else _grass_tint(img, cam)
    return img


def _grass_tint(img, cam):
    hh, ww, _ = img.shape
    X, Z, mpp = G.ground_rays(cam, ww, hh, B.SS)
    patch = G.noise(X, Z, 0.5, 15) + 0.5 * G.noise(X, Z, 0.12, 16)
    a = (np.clip((patch - (1.0 - 0.45 * 1.6)) * 0.8, 0, 0.5) * (in_patch(X, Z) < 0))[..., None]
    return img * (1 - a) + np.array([0.52, 0.50, 0.28]) * a


def close_shot(t):
    return shot_of(t)[0] in '123'


def near_real(t, cam):
    ss = B.SS
    C.SS = ss
    img = near_ground(cam, t)
    img = G.litter(img, cam, ss, LITTER)
    cam_al = 0.0
    img = lying_rev(img, cam, CAN[0], CAN[1], _prof_can, can_mat, cover=0.30, seed=2)
    cov = scroll_cover(t)
    if cov < 1.0:
        p = np.asarray(cam.pos)
        a, b = np.array(SCROLL[0]), np.array(SCROLL[1])
        ax = (b - a) / np.linalg.norm(b - a)
        cam_al = float(np.dot(np.array([p[0], p[2]]) - a, ax))
        glow = 1.2 * math.exp(-((t - 7.79) / 0.18) ** 2)
        img = lying_rev(img, cam, SCROLL[0], SCROLL[1], C._prof_scroll, C.scroll_mat, cover=cov, seed=3, glow=glow,
                        cam_along=cam_al)
    pil = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).convert('RGBA')
    if t >= 15.08:
        packet_rest_flat(pil, cam, ss)
    draw_vomit(pil, cam)
    draw_bag(pil, cam)
    draw_pigeons(pil, cam, t)
    k, surf = man_at(t)
    first = shot_of(t)[0] == '1'
    if not first:
        drool_ground(pil, cam, k)                        # (Sam, animatic 4: the drool clipped in shots 3 and 4) the
    if close_shot(t):                                    # pool lies on the soil UNDER him from shot 2 on
        prts = [q for q in man_parts(k) if q.name not in ('head', 'hair', 'ear')]
        L.draw(pil, cam, k, MAN, t, surfaces=[(p0, n) for _, p0, n in surf], prts=prts)
        draw_stains(pil, cam, k)
        if _on_screen(cam, k['head'], 0.25):
            mouth, ppu, side = face_close(pil, cam, k, MAN, t, pool=first)
            drool_close(pil, mouth, ppu, side, t, full=first)
    else:
        L.draw(pil, cam, k, MAN, t, surfaces=[(p0, n) for _, p0, n in surf], prts=man_parts(k))
        draw_stains(pil, cam, k)
    d = dog_at(t)
    if d is not None:
        draw_dog(pil, cam, d)
    if PACK_IN <= t < 15.08:
        draw_packet(pil, cam, t)
    out = np.asarray(pil.convert('RGB'), float) / 255
    hh, ww, _ = out.shape
    out = G.dust(out, cam, ss, t, strength=0.9, gust=gust(t))
    if 7.6 < t < 8.3:                                    # the gold catches the sun (7.79): a soft glint on the tip
        glint(out, cam, t)
    magic(out, cam, t)
    yy, xx = np.mgrid[0:hh, 0:ww]
    v = 1 - 0.55 * np.clip(((xx - ww / 2) / ww) ** 2 * 2.2 + ((yy - hh / 2) / hh) ** 2 * 2.2, 0, 1)
    out = out * v[..., None]
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).convert('RGBA')


VOMIT = (-0.16, -0.80)                           # (Sam, note 6) a pool of sick by his face, on the soil
BAG = (0.45, -1.50, 200.0)                       # (note 10) a carrier bag spilling rubbish, north of the dog scene


def _ground_poly(cam, c, pts, rot=0.0, h=0.004):
    """Local ground points (metres; u along `rot` degrees, v across) round c=(x, z) -> canvas points."""
    ss = B.SS
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    out = []
    for u, v in pts:
        x, z = c[0] + u * ca - v * sa, c[1] + u * sa + v * ca
        (px, py), _ = cam.project((x, h, z))
        out.append((px * ss, py * ss))
    return out


def _blob(r, n, seed, wob=0.25):
    rng = np.random.default_rng(seed)
    ph = rng.uniform(0, 6.3, 3)
    return [(r * (1 + wob * (0.5 * math.sin(3 * a + ph[0]) + 0.3 * math.sin(5 * a + ph[1]) + 0.2 * math.sin(7 * a + ph[2])))
             * math.cos(a), r * (1 + wob * (0.5 * math.sin(3 * a + ph[0]) + 0.3 * math.sin(5 * a + ph[1])
                                            + 0.2 * math.sin(7 * a + ph[2]))) * math.sin(a))
            for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]


def draw_vomit(pil, cam, flat=False):
    """A splash of sick on the soil by his face: beige-orange, darker wet rim, carrot-coloured bits, a shine."""
    d = ImageDraw.Draw(pil, 'RGBA')
    (_, _), kk = cam.project((VOMIT[0], 0, VOMIT[1]))
    lw = max(1, int(min(2.2 * B.SS, kk * 0.004 * B.SS)))
    d.polygon(_ground_poly(cam, VOMIT, _blob(0.115, 40, 3, 0.3)), fill=(120, 92, 44, 150))   # the damp rim
    body = _ground_poly(cam, VOMIT, _blob(0.09, 40, 4, 0.28))
    d.polygon(body, fill=(206, 168, 92, 255))
    if flat:
        d.line(body + [body[0]], fill=INK, width=lw)
    rng = np.random.default_rng(5)
    for _ in range(14):                                  # bits
        u, v = rng.uniform(-0.06, 0.06, 2)
        r = rng.uniform(0.006, 0.013)
        col = [(226, 120, 40), (240, 214, 150), (170, 126, 60)][int(rng.integers(0, 3))]
        d.polygon(_ground_poly(cam, (VOMIT[0] + u, VOMIT[1] + v), _blob(r, 8, int(rng.integers(0, 99)), 0.2)), fill=col)
    if not flat:
        d.polygon(_ground_poly(cam, (VOMIT[0] - 0.03, VOMIT[1] - 0.02), _blob(0.025, 12, 9, 0.2), rot=30),
                  fill=(255, 246, 220, 120))         # wet shine


def draw_bag(pil, cam, flat=False):
    """(Sam, animatic 4: too plain to tell what anything was) A white carrier bag on its side, crumpled, its handles
    looped out, a blue stripe; spilling: a crushed red lager can, a torn blue crisp packet with crimped ends, an open
    red-and-white chicken box with bones, a green pop bottle with a label and red cap, a banana skin, a coffee cup.
    House style: flat colour, one outline, a soft shadow."""
    d = ImageDraw.Draw(pil, 'RGBA')
    x0, z0, rot = BAG
    (_, _), kk = cam.project((x0, 0, z0))
    lw = max(1, int(min(2.2 * B.SS, kk * 0.004 * B.SS)))
    S_ = 1.25                                            # a touch larger, so it reads from above

    def shape(pts, col, c=(0.0, 0.0), r=0.0, h=0.01, outline=True):
        a = math.radians(rot)
        cx, cz = x0 + S_ * (c[0] * math.cos(a) - c[1] * math.sin(a)), z0 + S_ * (c[0] * math.sin(a) + c[1] * math.cos(a))
        Q = _ground_poly(cam, (cx, cz), [(u * S_, v * S_) for u, v in pts], rot + r, h)
        d.polygon(Q, fill=col)
        if outline:
            d.line(Q + [Q[0]], fill=INK, width=lw, joint='curve')

    def line(pts, col, c=(0.0, 0.0), r=0.0, h=0.02, w=1.0):
        a = math.radians(rot)
        cx, cz = x0 + S_ * (c[0] * math.cos(a) - c[1] * math.sin(a)), z0 + S_ * (c[0] * math.sin(a) + c[1] * math.cos(a))
        Q = _ground_poly(cam, (cx, cz), [(u * S_, v * S_) for u, v in pts], rot + r, h)
        d.line(Q, fill=col, width=max(1, int(lw * w)), joint='curve')

    def rect(L_, W_):
        return [(-L_ / 2, -W_ / 2), (L_ / 2, -W_ / 2), (L_ / 2, W_ / 2), (-L_ / 2, W_ / 2)]

    def ellp(ru, rv, n=16):
        return [(ru * math.cos(q), rv * math.sin(q)) for q in np.linspace(0, 2 * math.pi, n, endpoint=False)]
    # the carrier bag: crumpled outline, a blue stripe, creases, the handles looped out behind
    for sg in (-1, 1):
        line([(-0.21, sg * 0.05), (-0.31, sg * 0.09), (-0.34, sg * 0.03), (-0.24, sg * 0.01)], INK, h=0.05, w=2.6)
        line([(-0.21, sg * 0.05), (-0.31, sg * 0.09), (-0.34, sg * 0.03), (-0.24, sg * 0.01)], (240, 240, 236),
             h=0.05, w=1.4)
    bag = [(-0.22, -0.12), (-0.12, -0.15), (-0.02, -0.13), (0.07, -0.16), (0.15, -0.11), (0.13, -0.04),
           (0.16, 0.03), (0.13, 0.11), (0.05, 0.15), (-0.05, 0.13), (-0.14, 0.15), (-0.23, 0.10), (-0.25, 0.0)]
    shape(bag, (242, 242, 238), h=0.06)
    shape([(-0.10, -0.145), (-0.06, -0.14), (-0.06, 0.135), (-0.10, 0.14)], (60, 110, 200), h=0.061, outline=False)
    for cu in (-0.17, 0.02, 0.09):                                                 # creases
        line([(cu, -0.10), (cu + 0.03, 0.0), (cu - 0.01, 0.09)], (200, 200, 196), h=0.062, w=0.8)
    shape([(0.11, -0.06), (0.15, -0.04), (0.15, 0.05), (0.11, 0.07), (0.09, 0.0)], (176, 174, 168), h=0.061)  # mouth
    # spilling out: a crushed lager can (red, silver ends, white band)
    shape([(-0.075, -0.034), (0.02, -0.03), (0.03, -0.02), (0.075, -0.034), (0.075, 0.034), (0.03, 0.025),
           (0.02, 0.032), (-0.075, 0.034)], (196, 32, 40), c=(0.26, 0.10), r=35)
    shape(rect(0.02, 0.068), (210, 212, 216), c=(0.26 + 0.07, 0.10 + 0.05), r=35)
    shape(rect(0.018, 0.068), (210, 212, 216), c=(0.26 - 0.06, 0.10 - 0.04), r=35)
    shape(rect(0.03, 0.068), (250, 250, 248), c=(0.26, 0.10), r=35, outline=False)
    # a crisp packet: blue foil, crimped ends, a yellow oval, torn at one end
    crisp = [(-0.08, -0.05)] + [(-0.09 + 0.01 * (i % 2), -0.05 + 0.0125 * i) for i in range(9)] + \
            [(0.06, 0.05), (0.075, 0.03), (0.065, 0.0), (0.08, -0.025), (0.06, -0.05)]
    shape(crisp, (36, 84, 196), c=(0.30, -0.10), r=-25)
    shape(ellp(0.032, 0.022), (250, 210, 40), c=(0.30, -0.10), r=-25, outline=False)
    # an open chicken box: red and white stripes, the lid flipped open, bones
    shape(rect(0.13, 0.10), (240, 240, 236), c=(0.45, 0.04), r=10)
    for j in range(3):
        shape(rect(0.13, 0.016), (204, 34, 34), c=(0.45 - 0.01 * j * 0, 0.04 - 0.035 + j * 0.035), r=10, outline=False)
    shape(rect(0.13, 0.10), (232, 228, 220), c=(0.45, 0.15), r=10)                # the lid, open
    for bu, bv in ((0.42, 0.13), (0.48, 0.17)):
        line([(-0.03, 0.0), (0.03, 0.0)], (246, 236, 210), c=(bu, bv), r=40, h=0.03, w=2.2)
    # a green pop bottle: label, red cap
    shape([(-0.11, -0.032), (0.04, -0.032), (0.08, -0.014), (0.10, -0.012), (0.10, 0.012), (0.08, 0.014),
           (0.04, 0.032), (-0.11, 0.032)], (70, 150, 80), c=(0.36, 0.26), r=70)
    shape(rect(0.06, 0.066), (240, 236, 220), c=(0.36, 0.26), r=70, outline=False)
    shape(rect(0.016, 0.03), (200, 30, 30), c=(0.36 + 0.105 * math.cos(math.radians(70)) * 0 , 0.26), r=70, outline=False)
    # a banana skin: a curved yellow skin, three floppy peel strips, a brown stalk end
    arc = [(0.09 * math.cos(q), 0.05 * math.sin(q) - 0.03) for q in np.linspace(0.3, math.pi - 0.3, 9)]
    shape(arc + [(x_, y_ - 0.022) for x_, y_ in arc[::-1]], (246, 206, 50), c=(0.22, -0.26), r=20)
    for k_, aa in enumerate((150, 200, 245)):
        shape([(0.0, -0.01), (0.06, -0.016), (0.075, -0.004), (0.06, 0.008), (0.0, 0.01)], (236, 196, 46),
              c=(0.22 + 0.075, -0.26 + 0.01), r=aa)
    shape(ellp(0.012, 0.009, 8), (110, 74, 30), c=(0.22 - 0.085, -0.26 - 0.005), r=20, outline=False)
    # a coffee cup on its side: white, a brown sleeve, its lid
    shape(rect(0.11, 0.07), (246, 246, 242), c=(0.05, -0.28), r=-60)
    shape(rect(0.035, 0.072), (150, 104, 66), c=(0.05, -0.28), r=-60, outline=False)


# (Sam, animatic 4) Pigeons by him from shot 2, so we know what the dots on the island are once we are up high; drawn
# in the world through every camera (close shots and the aerial alike), grown as the camera climbs exactly as the
# people are, so none pops in. Four by him (world x, z; one by the sick, one hops off when the packet lands), a dozen
# on the island's paving.
PIGEONS_NEAR = [(-1.22, -0.70, 95.0), (-0.42, -1.42, 20.0), (0.06, -1.06, 260.0), (0.82, -1.18, 120.0)]
_PIG_ALL = None


def _pigeons_world():
    global _PIG_ALL
    if _PIG_ALL is None:
        rng = np.random.default_rng(21)
        pc = np.array([-(PATCH_C[0] - LAMP[0]), PATCH_C[1] - LAMP[1]])
        isl = []
        while len(isl) < 12:
            p = np.array(_pol(rng.uniform(6.5, 13.0), rng.uniform(0, 360)))
            if np.hypot(*(p - pc)) > 5.0 and all(np.hypot(*(p - q)) > 2.2 for q in isl):
                isl.append(p)
        _PIG_ALL = [(x, z, h, rng.uniform(0, 6.3)) for x, z, h in PIGEONS_NEAR] + \
                   [(*world(*p), rng.uniform(0, 360), rng.uniform(0, 6.3)) for p in isl]
    return _PIG_ALL


def draw_pigeons(pil, cam, t, flat=False):
    """Grey town pigeons, house style from above: a pale body, two dark wing bars, a green-purple neck, a dark grey
    head pecking at the ground, a little beak, a dark tail; a soft shadow under each."""
    d = ImageDraw.Draw(pil, 'RGBA')
    ss = B.SS
    for i, (x, z, h0, ph) in enumerate(_pigeons_world()):
        (sx, sy), kk = cam.project((x, 0.0, z))
        if not (-200 < sx < 1280 and -200 < sy < 2120):
            continue
        e = float(np.clip(1080 / max(kk, 1e-6) / 30.0, 1.0, 4.0)) * (1.25 if kk < 200 else 1.0)
        h = h0 + (18 if i < len(PIGEONS_NEAR) else 35) * math.sin(t * 0.6 + ph)   # near ones stay side-on
        x_, z_ = x + 0.04 * math.sin(t * 0.5 + ph), z + 0.04 * math.cos(t * 0.4 + ph)
        hop, wings, lift = 0.0, 0.0, 0.0
        if i == 0 and t > PACK_LAND - 0.05:              # startled when the packet lands beside it: it takes off
            u = (t - PACK_LAND + 0.05) / 0.8             # and flies right out of shot, wings beating
            if u > 1.0:
                continue                                  # gone (it was left cropped at the frame's edge)
            away = np.array([x - PACKET_REST[0], z - PACKET_REST[1]])
            away /= np.linalg.norm(away) + 1e-9           # away from the packet and the scroll
            hop = 1.1 * u ** 1.6
            lift = 0.35 * u
            wings = 0.55 + 0.45 * abs(math.sin(u * math.pi * 4))     # four wingbeats
            h = math.degrees(math.atan2(away[1], away[0]))
            x_, z_ = x_ + away[0] * hop, z_ + away[1] * hop
        a = math.radians(h)
        bob = math.sin(t * 6 + ph * 3)                     # walking head-bob forward/back, and pecks down
        hf = 0.006 * bob                                   # (Sam: the stretching neck looked weird) the neck keeps its
        dip = max(0.0, math.sin(t * 2.3 + ph)) ** 4        # length: the head only nods a touch, and dips to peck by
        hdn = 0.035 * dip                                  # swinging the whole neck down, not by stretching it
        far = e > 1.5                                      # small on screen: grey outlines, no eyes (they were
        lw = 1 if far else max(1, int(min(2.2 * ss, kk * 0.006 * ss * e)))    # dark smudges with orange specks)
        ink_ = (70, 72, 82) if far else INK
        ca_, sa_ = math.cos(a), math.sin(a)

        def P3(u_, v_, h_):
            wx = x_ + (u_ * ca_ - v_ * sa_) * e
            wz = z_ + (u_ * sa_ + v_ * ca_) * e
            (px, py), _ = cam.project((wx, (h_ + (lift if h_ > 0.001 else 0.0)) * e, wz))   # the shadow stays down
            return (px * ss, py * ss)

        def shp(pts, col, outline=True):
            Q = [P3(*q) for q in pts]
            d.polygon(Q, fill=col)
            if outline:
                d.line(Q + [Q[0]], fill=ink_, width=lw, joint='curve')

        def ring(cu, cv, ch, ru, rv, n=14):
            return [(cu + ru * math.cos(q), cv + rv * math.sin(q), ch) for q in np.linspace(0, 2 * math.pi, n,
                                                                                            endpoint=False)]
        shp(ring(-0.02, 0.0, 0.0, 0.14, 0.07), (24, 20, 16, 60), False)                 # shadow on the ground
        for sg in (-1, 1) if lift < 0.02 else ():                                       # little pink legs, feet
            d.line([P3(0.0, sg * 0.025, 0.0), P3(0.0, sg * 0.025, 0.05)], fill=(200, 110, 120),
                   width=max(1, int(lw * 1.2)))
            shp([(0.025, sg * 0.025, 0.0), (-0.01, sg * 0.035, 0.0), (-0.01, sg * 0.015, 0.0)], (200, 110, 120), False)
        H = 0.07                                                                        # the body's height

        def oval(cu, cv, ru, rv, hh, n=22):
            return [(cu + ru * math.cos(q), cv + rv * math.sin(q), hh) for q in np.linspace(0, 2 * math.pi, n,
                                                                                            endpoint=False)]
        tail = [(-0.10, -0.022, H - 0.01)] + [(-0.205 + 0.018 * math.cos(q), 0.034 * math.sin(q), H - 0.015)
                                              for q in np.linspace(-math.pi / 2, math.pi / 2, 9)][::-1][::-1] + \
               [(-0.10, 0.022, H - 0.01)]
        tail = [tail[0]] + sorted(tail[1:-1], key=lambda q: q[1]) + [tail[-1]]
        shp(tail, (112, 116, 130))                                                      # the tail, a rounded fan
        shp([(-0.19, -0.03, H - 0.014)] + [(-0.205 + 0.018 * math.cos(q), 0.034 * math.sin(q), H - 0.015)
                                           for q in np.linspace(-1.1, 1.1, 7)] + [(-0.19, 0.03, H - 0.014)],
            (36, 38, 46), False)                                                         # its dark tip
        hu, hh_ = 0.115 + hf - 0.4 * hdn, 0.115 - hdn
        # (drawn UNDER the body and head, whose curves round off its ends) the neck: a rounded column from the shoulders to the head, narrower than the body, shimmering green and
        # purple (it read as a flat bib before)
        nk = []
        for k in range(9):
            f_ = k / 8
            wdt = 0.036 - 0.012 * f_ + 0.006 * math.sin(f_ * math.pi)
            nk.append((0.035 + (hu - 0.035) * f_, -wdt, H + (hh_ - H) * f_))
        neck = nk + [(q[0], -q[1], q[2]) for q in nk[::-1]]
        shp(neck, (96, 130, 112))
        mid = nk[4]
        shp(ring(mid[0] - 0.005, 0.0, mid[2] + 0.004, 0.022, 0.018, 12), (132, 100, 146), False)   # purple sheen
        shp(oval(-0.025, 0.0, 0.098, 0.064, H - 0.03), (118, 122, 136))                  # the belly, in shade
        if wings > 0:                                                                   # wings out as it flaps off:
            for sg in (-1, 1):                                                          # curved leading edge,
                span = 0.08 + 0.20 * wings                                              # rounded feathers
                lead = [(0.035 - 0.05 * (k / 10) ** 1.4, sg * (0.04 + span * math.sin(k / 10 * math.pi / 2)),
                         H + 0.05 * wings * k / 10) for k in range(11)]
                tip = lead[-1]
                trail = []
                for k in range(10, -1, -1):                                             # scalloped trailing edge
                    f_ = k / 10
                    base = -0.03 - 0.07 * (1 - f_) ** 0.8
                    trail.append((base - 0.012 * abs(math.sin(f_ * math.pi * 3)), sg * (0.04 + span * f_ * 0.98),
                                  H + 0.05 * wings * f_))
                shp(lead + trail, (148, 152, 166))
                shp([tip, lead[-3], (lead[-3][0] - 0.05, lead[-3][1], lead[-3][2]), trail[1], trail[0]], (52, 54, 64),
                    False)                                                                # the dark primaries
        shp(oval(-0.025, 0.0, 0.098, 0.066, H), (180, 184, 196))                         # the back: a plump oval
        for sg in (-1, 1):                                                              # folded wings: crescents
            wing = [(0.03, sg * 0.064, H + 0.003)] + \
                   [(0.03 - 0.19 * k / 10, sg * (0.066 - 0.05 * (k / 10) ** 1.6), H + 0.003) for k in range(1, 11)] + \
                   [(-0.13 + 0.15 * k / 10, sg * (0.018 + 0.03 * (k / 10) ** 0.7), H + 0.004) for k in range(1, 10)]
            if wings == 0:
                Q = [P3(*q) for q in wing]
                d.polygon(Q, fill=(136, 140, 154))
                d.line(Q, fill=(92, 94, 106), width=max(1, lw // 2), joint='curve')
            for bu in (-0.03, -0.065):                                                  # the two black wing bars
                shp([(bu + 0.008, sg * 0.064, H + 0.005), (bu - 0.004, sg * 0.040, H + 0.005),
                     (bu - 0.012, sg * 0.030, H + 0.005), (bu - 0.004, sg * 0.030, H + 0.005),
                     (bu + 0.004, sg * 0.040, H + 0.005), (bu + 0.016, sg * 0.064, H + 0.005)], (40, 42, 52), False)
            shp([(-0.115, sg * 0.022, H + 0.006), (-0.16, sg * 0.006, H + 0.006), (-0.14, sg * 0.004, H + 0.006),
                 (-0.10, sg * 0.014, H + 0.006)], (44, 46, 56), False)                  # dark wingtips
        # the neck: from the shoulders to wherever the head is, so it never comes away from the body
        hu, hh_ = 0.115 + hf - 0.4 * hdn, 0.115 - hdn     # dipping swings it down and a little back: length kept
        shp(ring(hu, 0.0, hh_, 0.038, 0.031, 18), (112, 118, 134))                     # the head, rounder, larger
        shp([(hu + 0.032, -0.007, hh_ - 0.004), (hu + 0.06, 0.0, hh_ - 0.01), (hu + 0.032, 0.007, hh_ - 0.004)],
            (54, 48, 46), False)                                                         # beak
        if not far:
            shp(ring(hu + 0.03, 0.0, hh_ + 0.002, 0.006, 0.008, 8), (236, 236, 236), False)   # the white cere
            for sg in (-1, 1):                                                            # eyes, at the sides
                shp(ring(hu + 0.012, sg * 0.024, hh_ + 0.004, 0.006, 0.006, 8), (226, 120, 40), False)


def _on_screen(cam, p, margin):
    (x, y), k = cam.project(tuple(p))
    m = margin * k
    return -m < x < 1080 + m and -m < y < 1920 + m


def magic(out, cam, t):
    """(Sam, note 9) Swirling magic light round the scroll, as in the trailer: gold wisps spiralling along it,
    each with a fading trail, glowing. Grows in after the glint (7.79) as the soil comes off, to the climb."""
    amt = ease((t - 7.6) / 1.2) * min(1.0, max(0.0, 1.2 - scroll_cover(t)))
    if amt <= 0.01:
        return
    ss = B.SS
    hh, ww, _ = out.shape
    a, b = np.array(SCROLL[0]), np.array(SCROLL[1])
    ax = b - a
    n2 = np.array([-ax[1], ax[0]]) / np.linalg.norm(ax)
    lay = Image.new('L', (ww, hh), 0)
    d = ImageDraw.Draw(lay)
    (_, _), kk = cam.project((float((a[0] + b[0]) / 2), 0.03, float((a[1] + b[1]) / 2)))
    w = max(1, int(0.006 * kk * ss))
    rng = np.random.default_rng(31)
    for i in range(22):
        s0, sp, th0, om, r0 = rng.uniform(0, 1), rng.uniform(0.05, 0.12), rng.uniform(0, 6.3), \
            rng.uniform(3.0, 5.5) * (1 if i % 2 else -1), rng.uniform(0.04, 0.08)
        pts = []
        for j in range(10):                              # the trail: where it was a moment ago
            tt = t - j * 0.03
            u = (s0 + sp * tt) % 1.0
            th = th0 + om * tt
            r = r0 * (1 + 0.3 * math.sin(tt * 2.1 + i))
            p = a + ax * (0.05 + 0.9 * u) + n2 * r * math.cos(th)
            y = 0.03 + abs(r * math.sin(th)) * 1.4
            (px, py), _ = cam.project((float(p[0]), y, float(p[1])))
            pts.append((px * ss, py * ss))
        for j in range(len(pts) - 1):
            d.line([pts[j], pts[j + 1]], fill=int(255 * (1 - j / 9)), width=w)
    sharp = np.asarray(lay, float) / 255
    soft = np.asarray(lay.filter(ImageFilter.GaussianBlur(5 * w)), float) / 255
    halo = np.asarray(lay.filter(ImageFilter.GaussianBlur(14 * w)), float) / 255
    g = (sharp * 0.9 + soft * 3.0 + halo * 3.5) * amt
    out += g[..., None] * np.array([1.0, 0.80, 0.42])
    np.clip(out, 0, 1, out=out)


def glint(out, cam, t):
    """Near-real: the sun catching the spiked tip, a soft bloom with a faint horizontal flare (no star)."""
    tip = SCROLL[1]
    (x, y), k = cam.project((tip[0], 0.03, tip[1] + 0.03))
    ss = B.SS
    x, y = x * ss, y * ss
    a = math.exp(-((t - 7.79) / 0.14) ** 2)
    hh, ww, _ = out.shape
    R = 0.05 * k * ss
    x0, x1 = int(max(0, x - 6 * R)), int(min(ww, x + 6 * R))
    y0, y1 = int(max(0, y - 2 * R)), int(min(hh, y + 2 * R))
    if x1 <= x0 or y1 <= y0:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1]
    d2 = ((xx - x) ** 2 + (yy - y) ** 2) / R ** 2
    bloom = np.exp(-d2 * 2.0) * 0.9 + np.exp(-((yy - y) / (0.06 * R)) ** 2 - ((xx - x) / (5 * R)) ** 2) * 0.35
    out[y0:y1, x0:x1] += (bloom * a)[..., None] * np.array([1.0, 0.86, 0.55])
    np.clip(out, 0, 1, out=out)


# ------------------------------------------------------------------------------------------------ AERIAL
MINIS = [211, 282, 339, 45, 148]                # the five minis' bearings (screen degrees, y down), as the comp
# The layout from Sam's aerial photo and his two drone videos (9 Nov): ONE big grey carriageway; the central island
# (dark, a dashed white give-way ring round it); the five minis INSIDE the grey, round the island at about 2.3 times its
# radius, each on its arm's line where the arm comes in; long kerbed splitter islands between the minis; the arms
# join the grey's edge. (Animatic 1 had the minis inside but each in its own kerbed circle; animatic 2 moved them out
# onto the arms: both wrong.)
R_MINI, RING_MINI, R_ISLAND = 35.0, 5.5, 15.0   # minis' centres; the lane round each; the central island
R_GREY = 46.0                                    # the grey's edge (the arms join it)
R_GIVE = 16.5                                    # the dashed give-way ring round the island
SPLIT_R, SPLIT_HL, SPLIT_HW = 30.5, 8.0, 2.6     # the splitter islands: radius, half length, half width
R_RING = R_GREY                                  # (the walkers' pavement runs round this edge)


def splitters():
    """The five kerbed splitter islands (map points), one between each pair of minis, lying round the island."""
    out = []
    for i in range(5):
        a1, a2 = MINIS[i], MINIS[(i + 1) % 5]
        mid = (a1 + ((a2 - a1) % 360) / 2) % 360
        c, tg, rd = _pol(SPLIT_R, mid), _pol(1, mid + 90), _pol(1, mid)
        out.append([c + tg * a + rd * b * SPLIT_HW / 2.6 for a, b in
                    ((-SPLIT_HL, 0), (-SPLIT_HL * 0.6, -2.6), (SPLIT_HL * 0.6, -2.6), (SPLIT_HL, 0),
                     (SPLIT_HL * 0.6, 2.6), (-SPLIT_HL * 0.6, 2.6))])
    return out


def _inside(p, poly_):
    x, y = p
    n, c = len(poly_), False
    for k in range(n):
        (x0, y0), (x1, y1) = poly_[k], poly_[(k + 1) % n]
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            c = not c
    return c


def on_road(p, domes=True):
    """Is this map point on the carriageway (the grey or an arm), clear of the island, the splitters and the domes?"""
    p = np.asarray(p, float)
    r = float(np.hypot(*p))
    if r < R_ISLAND + 0.4:
        return False
    ok = r <= R_GREY
    for m in MINIS:
        u = _pol(1, m)
        if float(np.dot(p, u)) > 36 and abs(u[0] * p[1] - u[1] * p[0]) <= 7.5:
            ok = True
        if domes and np.hypot(*(p - _pol(R_MINI, m))) < 2.0:
            return False
    return ok and not any(_inside(p, q) for q in splitters())
CAR_COLS = [(240, 240, 238), (30, 30, 34), (170, 172, 178), (176, 30, 36), (40, 70, 150), (240, 240, 238),
            (120, 124, 130), (90, 30, 34)]


def _pol(r, a):
    return np.array([r * math.cos(math.radians(a)), r * math.sin(math.radians(a))])


def _arc(c, r, a0, a1, step=6.0):
    n = max(2, int(abs(a1 - a0) / step) + 1)
    return [np.asarray(c) + _pol(r, a) for a in np.linspace(a0, a1, n)]


def _routes():
    """Every car's way through, in map metres (Sam's drone videos): in along an arm in the left lane, give way at the
    grey's edge, clockwise round its mini (a left turn onto it), then either
      A: clockwise to the next mini (a larger bearing), outside the splitter island, round it, out along its arm, or
      B: anticlockwise to the mini before (a smaller bearing), inside the splitter island, round it, out.
    Returns [(points, giveway index, index entering the second mini, first mini's centre)]."""
    out = []
    for i, m in enumerate(MINIS):
        u = _pol(1, m)
        cm = _pol(R_MINI, m)
        lin = _pol(2.6, m + 90)                          # the inbound lane: left of a car heading in
        for kind in ('A', 'B'):
            j = (i + 1) % 5 if kind == 'A' else (i - 1) % 5
            mj = MINIS[j]
            uj = _pol(1, mj)
            cj = _pol(R_MINI, mj)
            lout = _pol(2.6, mj - 90)                    # the outbound lane: left of a car heading out
            d_ = ((mj - m + 180) % 360) - 180            # +72 (A) or -72 (B)
            mid = m + d_ / 2
            pts = [u * 260 + lin, u * 120 + lin, u * 56 + lin, u * 47 + lin]
            gw = len(pts) - 1
            if kind == 'A':
                pts += _arc(cm, RING_MINI, m + 28, m + 75)
                pts += [_pol(40.5, mid - 12), _pol(41.0, mid), _pol(40.5, mid + 12)]
                gw2 = len(pts)
                pts += _arc(cj, RING_MINI, mj - 105 + 360, mj + 290)
            else:
                pts += _arc(cm, RING_MINI, m + 28, m + 215)
                pts += [_pol(23.5, mid + 10), _pol(23.0, mid), _pol(23.5, mid - 10)]
                gw2 = len(pts)
                pts += _arc(cj, RING_MINI, mj + 150, mj + 290)
            pts += [uj * 47 + lout, uj * 56 + lout, uj * 120 + lout, uj * 260 + lout]
            out.append((np.array(pts), gw, gw2, cm))
    return out


def _resample(pts, step=0.5):
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    n = int(s[-1] / step)
    q = np.linspace(0, s[-1], n)
    xy = np.stack([np.interp(q, s, pts[:, 0]), np.interp(q, s, pts[:, 1])], 1)
    k = 9                                                # smoothed corners (a car turns, never snaps)
    if len(xy) > 2 * k:
        ker = np.ones(k) / k
        xs = np.convolve(np.pad(xy[:, 0], k, mode='edge'), ker, 'same')[k:-k]
        ys = np.convolve(np.pad(xy[:, 1], k, mode='edge'), ker, 'same')[k:-k]
        xy = np.stack([xs, ys], 1)
    return xy, q


_TRAFFIC = None


N_PER_ARM = 13                                   # cars queued on each arm (more traffic: Sam, 9 Nov; was 9)
TRAFFIC_SEED = 8                                 # the mix of cars (chosen: no jams, no touching)
JUNCTION_CAP = 14                                 # most cars past the give-way lines at once (keeps the ring moving)


def traffic():
    """The traffic, worked out once: each car moves along its route at its own speed, keeps its distance from
    anything ahead of it, and gives way at the line before joining a mini when something is coming round. Returns
    {frame: [(x, y, heading_deg, length, width, colour)]} in map metres, for 16.4 s to the end at 24 fps."""
    global _TRAFFIC
    if _TRAFFIC is not None:
        return _TRAFFIC
    rng = np.random.default_rng(TRAFFIC_SEED)
    routes = []
    for pts, gw, gw2, cm in _routes():
        xy, s = _resample(pts)
        gws, gws2 = (float(np.searchsorted(s, np.sum(np.linalg.norm(np.diff(pts[:g + 1], axis=0), axis=1))))
                     for g in (gw, gw2))
        routes.append((xy, gws, gws2, cm))
    cars = []                                            # route, s (index in 0.5 m steps), speed, size, colour
    for arm in range(5):                                 # each arm's cars one behind another in its lane (both
        s0 = float(rng.uniform(-60, 120))                # routes from an arm share it), spaced like real traffic
        for n in range(N_PER_ARM):
            s0 -= float(rng.uniform(40, 80))
            cars.append(dict(r=arm * 2 + int(rng.integers(0, 2)), s=s0, v=float(rng.uniform(7, 9.5)),
                             L=4.4, W=1.85, col=CAR_COLS[int(rng.integers(0, len(CAR_COLS)))]))
    cars[5].update(L=11.0, W=2.55, col=(232, 196, 40), v=6.5)    # a bus
    cars[17].update(L=8.0, W=2.4, col=(240, 240, 238), v=6.5)    # a white van
    dt = 1 / FPS
    t0 = -30.0                                           # run in early so the minis are busy by 16.4 (no cars
    #                                                      circle the island to fill the middle now: note 2)
    frames = {}
    nsteps = int((DUR - t0) * FPS) + 2

    def pose(c):
        xy = routes[c['r']][0]
        i = int(c['s'])
        if 'loop' in c:
            i = int(c['s']) % c['loop']
        if i < 0 or i >= len(xy) - 1:
            return None
        p, q = xy[i], xy[i + 1]
        f = c['s'] - int(c['s'])
        pos = p + (q - p) * f
        return pos, math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
    for step in range(nsteps):
        t = t0 + step * dt
        P = [pose(c) for c in cars]
        busy = sum(1 for ci, o in enumerate(P) if o is not None and np.hypot(*o[0]) < 66
                   and cars[ci]['s'] > routes[cars[ci]['r']][1] + 0.5)
        for ci, c in enumerate(cars):
            if P[ci] is None:
                c['s'] += 8.0 * dt * 2 if c['s'] < 0 else 0     # off the map: all at one speed, so none catch up
                continue
            pos, hd = P[ci]
            h = np.array([math.cos(math.radians(hd)), math.sin(math.radians(hd))])
            want = c['v']
            for cj, o in enumerate(P):                   # anything ahead within a car's reach: slow, stop
                if cj == ci or o is None:
                    continue
                dvec = o[0] - pos
                dist = float(np.linalg.norm(dvec))
                if dist > 16:
                    continue
                ahead = float(np.dot(dvec, h))
                lat = abs(float(h[0] * dvec[1] - h[1] * dvec[0]))
                gap = (c['L'] + cars[cj]['L']) / 2 + 2.2
                if 0 < ahead and dist < gap + 3.0 and ahead > 0.3 * dist and \
                        abs((o[1] - hd + 180) % 360 - 180) > 25 and cars[cj].get('vn', 9) > c.get('vn', 9):
                    want = 0.0                           # something cutting across in front, faster: let it go
                if ahead > 0 and lat < 2.4 and ahead < gap + 4.0:
                    ho = math.radians(o[1])                # do we both have the other ahead (crossing)? then the
                    back = -float(np.dot(dvec, [math.cos(ho), math.sin(ho)]))   # lower number goes first
                    if back > 0 and abs(math.cos(ho) * dvec[1] - math.sin(ho) * dvec[0]) < 2.4 and ci < cj:
                        continue
                    want = min(want, max(0.0, (ahead - gap) * 2.0))
            gws, gws2 = routes[c['r']][1], routes[c['r']][2]
            if gws2 - 24 < c['s'] < gws2 + 0.5:            # into mini j from the ring: give way to anything already
                xy = routes[c['r']][0]                         # coming round it (not to cars following on the ring)
                merge = xy[min(len(xy) - 1, int(gws2) + 4)]
                for cj, o in enumerate(P):
                    if cj != ci and o is not None and np.linalg.norm(o[0] - merge) < 10 and \
                            abs((o[1] - hd + 180) % 360 - 180) > 25 and cars[cj].get('vn', 9) > 1.5:
                        want = min(want, max(0.0, (gws2 - 4 - c['s']) * 1.5))
            if gws is not None and gws - 6 < c['s'] < gws + 0.5 and busy >= JUNCTION_CAP:   # the junction is
                want = min(want, max(0.0, (gws - c['s']) * 1.5))     # full: wait at the line (no gridlock)
            if gws is not None and gws - 6 < c['s'] < gws + 0.5:   # give way: anything coming round the mini
                xy = routes[c['r']][0]
                merge = xy[min(len(xy) - 1, int(gws) + 12)]
                cm = routes[c['r']][3]
                for cj, o in enumerate(P):
                    if cj == ci or o is None or cars[cj]['r'] == c['r']:
                        continue
                    rel = o[0] - cm                          # anything on the mini or coming along the ring to it
                    out_ = float(np.dot(rel, [math.cos(math.radians(o[1])), math.sin(math.radians(o[1]))])) > 3
                    if c.get('wait', 0) > 2.5:               # waited long enough: take any gap that is clear now
                        if np.linalg.norm(o[0] - merge) < 6 and cars[cj].get('vn', 9) > 0.5:
                            want = min(want, max(0.0, (gws - c['s']) * 1.5))
                    elif np.linalg.norm(o[0] - merge) < 11 or (np.linalg.norm(rel) < RING_MINI + 9 and not out_):
                        want = min(want, max(0.0, (gws - c['s']) * 1.5))
                c['wait'] = c.get('wait', 0) + dt if c.get('vn', 9) < 0.5 else 0.0
            c['vn'] = c.get('vn', c['v']) + max(-9 * dt, min(4 * dt, want - c.get('vn', c['v'])))
            c['s'] += max(0.0, c['vn']) * dt * 2
        if t >= 16.4 - 1e-6:
            fr = int(round(t * FPS))
            frames[fr] = [(*P[ci][0], P[ci][1], c['L'], c['W'], c['col'], ci) for ci, c in enumerate(cars)
                          if P[ci] is not None]
    _TRAFFIC = frames
    return frames


def traffic_faults():
    """No two cars pass into each other (centres closer than their half-lengths and widths allow), and every car
    stays on the carriageway: off the pavements, the island, the splitters and the domes (Sam, animatic 2: cars drove
    on the pavements; nothing checked it)."""
    out = list(van_faults())
    for fr, cs in sorted(traffic().items())[::6]:
        for x, y, hd, Lc, Wc, *_r in cs:
            if math.hypot(x, y) > 150:
                continue
            c_, s_ = math.cos(math.radians(hd)), math.sin(math.radians(hd))
            for u_, v_ in ((Lc / 2, Wc / 2), (Lc / 2, -Wc / 2), (-Lc / 2, Wc / 2), (-Lc / 2, -Wc / 2)):
                if not on_road((x + u_ * c_ - v_ * s_, y + u_ * s_ + v_ * c_), domes=Lc < 6):   # a bus or van may
                    #                                     overrun a mini's dome as it turns (they are built for it)
                    out.append(f'TRAFFIC: a car off the road at {fr / FPS:.2f} s near ({x:.0f}, {y:.0f}) m')
                    break
    for fr, cs in sorted(traffic().items()):
        for i in range(len(cs)):
            for j in range(i + 1, len(cs)):
                a, b = cs[i], cs[j]
                if math.hypot(a[0] - b[0], a[1] - b[1]) < (min(a[3], b[3]) + max(a[4], b[4])) / 2 * 0.9:
                    out.append(f'TRAFFIC: two cars pass into each other at {fr / FPS:.2f} s near ({a[0]:.0f}, {a[1]:.0f}) m')
                    break
    return out[:5]


_ESTATE = None


STADIUM = (-36.0, 168.0, 36.0, 280.0)            # the County Ground's pitch box (map metres), below the title
SHED = (-62.0, 112.0, 22.0, 140.0)               # the big white-roofed shed (plain roof: Sam, notes 1 and 18)
CARPARK = (58.0, -14.0, 100.0, 34.0)


def _free(p, margin=0.0):
    """Room for a house here: clear of the junction, the arms, the stadium, the shed and the car park."""
    if np.hypot(*p) < 80:
        return False
    for m in MINIS:
        u = _pol(1, m)
        if float(np.dot(p, u)) > 0 and abs(u[0] * p[1] - u[1] * p[0]) < 15 + margin:
            return False
    for x0, y0, x1, y1 in (STADIUM, SHED, CARPARK):
        if x0 - 22 < p[0] < x1 + 22 and y0 - 22 < p[1] < y1 + 22:
            return False
    return True


def _estate():
    """Swindon round it, placed once (Sam's photos, 8 Nov): terraced streets (rows of brown and grey roofs with back
    gardens), trees on the verges. Returns (rows of houses, trees)."""
    global _ESTATE
    if _ESTATE is None:
        rng = np.random.default_rng(4)
        rows, trees = [], []
        ang = math.radians(16)
        along = np.array([math.cos(ang), math.sin(ang)])
        across = np.array([-along[1], along[0]])
        for k in range(-16, 17):                         # a terrace every 15 m, back to back in pairs
            off = k * 15.0 + (4.0 if k % 2 else 0.0)
            face = 1 if k % 2 else -1                    # which side its street is on
            run = []
            roof = [(140, 92, 70), (118, 82, 66), (104, 96, 92)][k % 3]
            for j in range(-50, 51):
                p = across * off + along * (j * 5.2)
                if _free(p) and _free(p + across * face * 7):
                    run.append(p)
                elif run:
                    rows.append((run, face, roof))
                    run = []
            if run:
                rows.append((run, face, roof))
        for i in range(160):
            a_ = rng.uniform(0, 360)
            r = rng.uniform(73, 88)
            p = _pol(r, a_)
            inbox = any(x0 - 8 < p[0] < x1 + 8 and y0 - 8 < p[1] < y1 + 8 for x0, y0, x1, y1 in (SHED, CARPARK))
            if not inbox and all(abs(m - a_) % 360 > 14 and abs(m - a_) % 360 < 346 for m in MINIS):
                trees.append((p, rng.uniform(2.8, 5.0)))
        _ESTATE = (rows, trees, along, across)
    return _ESTATE


def aerial_flat(pil, cam, t):
    """The Magic Roundabout from straight above, flat house style (flat colour, one outline), drawn in map metres
    through the shot's camera, so the climb, the hand-over and the drift all draw one place (rule 1)."""
    ss = B.SS
    (ox, oy), k = cam.project((LAMP[0], 0.0, LAMP[1]))
    (ax_, ay_), _ = cam.project((LAMP[0] - 1.0, 0.0, LAMP[1]))
    ox, oy = ox * ss, oy * ss
    ex = np.array([ax_ * ss - ox, ay_ * ss - oy])          # one map metre to screen right
    ey = np.array([-ex[1], ex[0]])                        # one map metre to screen down
    s = float(np.linalg.norm(ex))
    d = ImageDraw.Draw(pil)

    def P(p):
        return (ox + p[0] * ex[0] + p[1] * ey[0], oy + p[0] * ex[1] + p[1] * ey[1])

    def lw(m):                                            # a width in metres, at least one pixel
        return max(1, int(round(m * s)))
    ink = max(1, int(min(2.6 * ss, max(1.0, 0.18 * s))))
    W, H = pil.size

    def poly(pts, fill, outline=True, width=None):
        Q = [P(p) for p in pts]
        d.polygon(Q, fill=fill)
        if outline:
            d.line(Q + [Q[0]], fill=INK, width=width or ink, joint='curve')

    def circ(c, r, fill, outline=True, width=None, n=None):
        n = n or int(min(240, max(24, r * s / 3)))
        poly([np.asarray(c) + _pol(r, a) for a in np.linspace(0, 360, n, endpoint=False)], fill, outline, width)
    d.rectangle([0, 0, W, H], fill=(118, 146, 86))                          # drab verge grass
    rows, trees, along, across = _estate()
    sdir = np.array([-0.857, 0.514])                                        # shadows fall this way (map)
    for run, face, roof in rows:                                            # streets, gardens, shadows
        a, b = run[0] - along * 2.6, run[-1] + along * 2.6
        st = across * face * 8.5
        poly([a + st - across * face * 3.5, b + st - across * face * 3.5, b + st + across * face * 3.5,
              a + st + across * face * 3.5], (150, 150, 150), outline=False)
        gd = -across * face
        poly([a + gd * 4, b + gd * 4, b + gd * 11, a + gd * 11], (110, 136, 82), outline=False)
        for p in run[::2]:                                                  # garden fences
            d.line([P(p + gd * 4 - along * 2.6), P(p + gd * 11 - along * 2.6)], fill=(96, 110, 74), width=lw(0.3))
        poly([a - across * 4 + sdir * 5, b - across * 4 + sdir * 5, b + across * 4 + sdir * 5,
              a + across * 4 + sdir * 5], (74, 92, 58), outline=False)
    for ri, (run, face, roof) in enumerate(rows):                           # the roofs (Sam, animatic 3: not one
        for hi, p in enumerate(run):                                         # long block): each house its own roof,
            if (hi + ri) % 7 == 6:                                           # a little different in tone, outlined,
                continue                                                     # an alley every 7th, a chimney each
            tone = 0.88 + 0.12 * (((hi * 7 + ri * 3) % 5) / 4)
            col = tuple(int(min(255, v * tone)) for v in roof)
            a, b = p - along * 2.5, p + along * 2.5
            poly([a - across * 4, b - across * 4, b + across * 4, a + across * 4], col)
            d.line([P(a), P(b)], fill=tuple(int(v * 0.72) for v in col), width=ink)        # the ridge
            ch = p - along * 2.1 + across * 1.6 * face
            poly([ch - along * 0.5 - across * 0.4, ch + along * 0.5 - across * 0.4, ch + along * 0.5 + across * 0.4,
                  ch - along * 0.5 + across * 0.4], (96, 74, 64))                          # a chimney
    # the big white-roofed shed (Sam's photos), no lettering (Sam, notes 1 and 18), its car park
    x0, y0, x1, y1 = SHED
    poly([(x0 + 6, y0 + 4), (x1 + 6, y0 + 4), (x1 + 6, y1 + 4), (x0 + 6, y1 + 4)], (74, 92, 58), outline=False)
    poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], (226, 228, 230))
    for i in range(1, 8):
        x = x0 + i * (x1 - x0) / 8
        d.line([P((x, y0)), P((x, y1))], fill=(196, 198, 202), width=lw(0.3))
    x0, y0, x1, y1 = CARPARK
    poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], (104, 104, 106))
    for row in range(3):
        yy = y0 + 4 + row * 15
        for i in range(int((x1 - x0) / 2.6)):
            x = x0 + 1 + i * 2.6
            d.line([P((x, yy)), P((x, yy + 5))], fill=(230, 230, 226), width=lw(0.12))
            if (i * 7 + row * 3) % 5 < 3:
                col = CAR_COLS[(i * 5 + row) % len(CAR_COLS)]
                poly([(x + 0.4, yy + 0.3), (x + 2.2, yy + 0.3), (x + 2.2, yy + 4.7), (x + 0.4, yy + 4.7)], col)
    # the County Ground next door (Sam's photo): striped pitch, red seats under grey roofs, floodlight pylons
    x0, y0, x1, y1 = STADIUM
    poly([(x0 - 16, y0 - 16), (x1 + 16, y0 - 16), (x1 + 16, y1 + 16), (x0 - 16, y1 + 16)], (186, 30, 40))
    for x0_, y0_, x1_, y1_ in ((x0 - 16, y0 - 16, x1 + 16, y0 - 9), (x0 - 16, y1 + 9, x1 + 16, y1 + 16),
                               (x0 - 16, y0 - 16, x0 - 10, y1 + 16), (x1 + 10, y0 - 16, x1 + 16, y1 + 16)):
        poly([(x0_, y0_), (x1_, y0_), (x1_, y1_), (x0_, y1_)], (206, 206, 204))   # the stand roofs
    poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], (84, 150, 70))
    for i in range(0, 14, 2):
        yy = y0 + i * (y1 - y0) / 14
        poly([(x0, yy), (x1, yy), (x1, yy + (y1 - y0) / 14), (x0, yy + (y1 - y0) / 14)], (96, 164, 80), outline=False)
    for q in ([(x0 + 2, y0 + 2), (x1 - 2, y0 + 2)], [(x1 - 2, y0 + 2), (x1 - 2, y1 - 2)], [(x0 + 2, y0 + 2), (x0 + 2, y1 - 2)],
              [(x0 + 2, (y0 + y1) / 2), (x1 - 2, (y0 + y1) / 2)]):
        d.line([P(q[0]), P(q[1])], fill=(236, 240, 232), width=lw(0.25))
    for cx_, cy_ in ((x0 - 22, y0 - 22), (x1 + 22, y0 - 22)):            # floodlights and their long shadows
        d.line([P((cx_, cy_)), P(np.array([cx_, cy_]) + sdir * 30)], fill=(60, 60, 60, 150), width=lw(1.0))
        poly([(cx_ - 3, cy_ - 1.5), (cx_ + 3, cy_ - 1.5), (cx_ + 3, cy_ + 1.5), (cx_ - 3, cy_ + 1.5)], (220, 220, 210))
    pth = [_pol(FOOTPATH_R + 1.4, a) for a in np.linspace(0, 360, 240, endpoint=False)]   # the footpath round
    pin = [_pol(FOOTPATH_R - 1.4, a) for a in np.linspace(0, 360, 240, endpoint=False)]   # the green (walkers,
    poly(pth, (206, 202, 190), outline=False)                                             # the fight: note 13)
    poly(pin, (118, 146, 86), outline=False)
    for p, r in trees:
        circ(p + np.array([-0.857, 0.514]) * r * 0.9, r, (64, 84, 52), outline=False)
    for p, r in trees:
        circ(p, r, (70, 110, 58))
    # the carriageway: ONE grey surface (Sam, note 2 again, from his aerial photo: the minis sit inside the grey, not
    # in circles of their own): the inner ring, the five arms and a mini's disc (as wide as the arm) all merged, then a
    # kerb and one outline round the whole of it. Drawn in three passes (outline, kerb, grey), each over every shape.
    def surface(grow, fill, outline=False):
        for m in MINIS:
            u = _pol(1, m)
            n = np.array([-u[1], u[0]])
            g = grow if grow == 0 else grow + 0.5          # the arms' pavements are wider than the ring's
            poly([u * 40 + n * (7.5 + g), u * 260 + n * (7.5 + g), u * 260 - n * (7.5 + g), u * 40 - n * (7.5 + g)],
                 fill, outline=False)
        circ((0, 0), R_GREY + grow, fill, outline=False)
    surface(2.7, INK)
    surface(2.4, (200, 198, 192))
    surface(0.0, (128, 128, 130))
    for m in MINIS:
        u = _pol(1, m)
        n = np.array([-u[1], u[0]])
        for j in range(8):                                                   # the zebra
            v = -6.5 + j * 1.75
            poly([u * 64 + n * v, u * 68 + n * v, u * 68 + n * (v + 0.9), u * 64 + n * (v + 0.9)], (240, 240, 236),
                 outline=False)
        for j in range(6):                                                   # the centre line
            p = u * (72 + j * 9)
            poly([p - n * 0.12, p + u * 4.5 - n * 0.12, p + u * 4.5 + n * 0.12, p + n * 0.12], (240, 240, 236),
                 outline=False)
        for side in (1,):                                                    # give-way dashes on the inbound lane
            for j in range(6):
                q = u * 47.6 + n * (0.4 + j * 1.2) * side
                poly([q, q + n * 0.7, q + n * 0.7 + u * 0.4, q + u * 0.4], (240, 240, 236), outline=False)
                q = u * 48.6 + n * (0.4 + j * 1.2) * side
                poly([q, q + n * 0.7, q + n * 0.7 + u * 0.4, q + u * 0.4], (240, 240, 236), outline=False)
        for k_ in range(2):                                                  # arrows on the inbound lane
            p = u * (53 + k_ * 6) + n * 2.6
            poly([p - u * 1.8 - n * 0.2, p - n * 0.2, p - n * 0.8, p + u * 1.5, p + n * 0.8, p + n * 0.2,
                  p - u * 1.8 + n * 0.2], (240, 240, 236), outline=False)
    # the splitter islands: dark paving in a pale kerb (Sam's video), dashed lane lines round their ends
    for q in splitters():
        poly(q, (196, 190, 176))
        c_ = np.mean(q, axis=0)
        poly([c_ + (np.asarray(v) - c_) * 0.82 for v in q], (88, 86, 84), outline=False)
    # the dashed give-way ring round the central island; dashed rings at the grey's edge where each arm comes in
    for a in range(0, 360, 8):
        d.line([P(_pol(R_GIVE, a)), P(_pol(R_GIVE, a + 4))], fill=(240, 240, 236), width=lw(0.35))
    # lane lines (Sam's video: dense white markings): dashed lines from the island's ring out between each mini and
    # its splitters, and arrows anticlockwise on the inner lanes
    def dash(p0, p1, step=2.2):
        L_ = float(np.hypot(*(np.asarray(p1) - p0)))
        for k_ in range(int(L_ / step)):
            q0 = np.asarray(p0) + (np.asarray(p1) - p0) * (k_ * step / L_)
            q1 = np.asarray(p0) + (np.asarray(p1) - p0) * (min(L_, k_ * step + 1.1) / L_)
            d.line([P(q0), P(q1)], fill=(240, 240, 236), width=lw(0.3))
    for m in MINIS:
        for sg in (-1, 1):
            dash(_pol(R_GIVE + 0.6, m + sg * 20), _pol(R_MINI - RING_MINI - 1.6, m + sg * 13))
    for i in range(5):
        a1, a2 = MINIS[i], MINIS[(i + 1) % 5]
        mid = (a1 + ((a2 - a1) % 360) / 2) % 360
        for da in (-6, 6):
            c_ = _pol(22.0, mid + da)
            fw = _pol(1, mid + da - 90)                  # anticlockwise: towards a smaller bearing
            sd_ = np.array([-fw[1], fw[0]])
            poly([c_ - fw * 1.8 - sd_ * 0.2, c_ - sd_ * 0.2, c_ - sd_ * 0.8, c_ + fw * 1.5, c_ + sd_ * 0.8,
                  c_ + sd_ * 0.2, c_ - fw * 1.8 + sd_ * 0.2], (240, 240, 236), outline=False)
    # the minis: a white dome, three curved white arrows round it, clockwise (Sam's video)
    for m in MINIS:
        cm = _pol(R_MINI, m)
        for k_ in range(3):
            a0 = m + k_ * 120 + 20
            arc = [cm + _pol(3.6, a) for a in np.linspace(a0, a0 + 70, 10)]
            d.line([P(p_) for p_ in arc], fill=(240, 240, 236), width=lw(0.35))
            tip, back = cm + _pol(3.6, a0 + 82), cm + _pol(3.6, a0 + 66)
            poly([tip, back + _pol(0.9, a0 + 66), back - _pol(0.9, a0 + 66)], (240, 240, 236), outline=False)
        circ(cm, 1.8, (238, 238, 232), width=max(1, ink // 2))
    # the central island: dark paving, white kerb, the soil-and-grass patch (Q2), the lamp post and its shadow
    circ((0, 0), R_ISLAND + 0.35, (232, 230, 224))
    circ((0, 0), R_ISLAND, (84, 82, 82))
    th = np.linspace(0, 2 * math.pi, 120, endpoint=False)
    rr = patch_r(th)
    pc = np.array([-(PATCH_C[0] - LAMP[0]), PATCH_C[1] - LAMP[1]])
    soil = [pc + np.array([-r * math.cos(a), r * math.sin(a)]) for a, r in zip(th, rr)]
    poly(soil, (112, 86, 62))
    for a_, r_, rr_ in ((0.5, 1.4, 0.9), (2.3, 1.8, 1.1), (4.2, 1.2, 0.8), (5.4, 2.0, 0.7)):
        circ(pc + np.array([-r_ * math.cos(a_), r_ * math.sin(a_)]), rr_, (120, 128, 70), outline=False)
    sd = np.array([-SUN_XZ[0], SUN_XZ[1]])                                  # the shadow, in map axes
    sn = np.array([-sd[1], sd[0]])
    poly([sn * 0.2, sd * SHADOW_LEN + sn * 0.2, sd * SHADOW_LEN - sn * 0.2, -sn * 0.2], (60, 58, 56),
         outline=False)
    poly([sd * SHADOW_LEN + sn * 2.6, sd * SHADOW_LEN - sn * 2.6, sd * (SHADOW_LEN + 0.6) - sn * 2.6,
          sd * (SHADOW_LEN + 0.6) + sn * 2.6], (60, 58, 56), outline=False)       # the head's shadow
    lamp_post(d, cam, P, s, ink)
    return s


def lamp_post(d, cam, P, s, ink):
    """The lamp post from above (Sam, note 3: make the pole readable): its foot, the pole leaning out from the middle of
    the frame as a tall thing does seen from high up (the lean drawn 2.5 times the true one so it reads), and a
    double-armed head across its top. Flat house style, one outline."""
    ss = B.SS
    (fx, fy), _ = cam.project((LAMP[0], 0.0, LAMP[1]))
    (tx, ty), _ = cam.project((LAMP[0], LAMP_H, LAMP[1]))
    foot = np.array([fx * ss, fy * ss])
    lean = (np.array([tx * ss, ty * ss]) - foot) * 2.5
    if np.linalg.norm(lean) < 2.0 * s:                    # straight overhead: a short lean still shows it is a pole
        lean = np.array([0.0, -2.0 * s])
    cap = min(9.0 * s, 64.0 * ss)                        # never longer than this (mid-climb it was a huge pale bar)
    if np.linalg.norm(lean) > cap:
        lean = lean / np.linalg.norm(lean) * cap
    top = foot + lean
    u = lean / (np.linalg.norm(lean) + 1e-9)
    n = np.array([-u[1], u[0]])
    wd = min(max(3.0 * ss, 0.7 * s), 5.0 * ss)
    grey = (196, 196, 190)
    d.ellipse([foot[0] - wd, foot[1] - wd, foot[0] + wd, foot[1] + wd], fill=(70, 70, 74), outline=INK, width=ink)
    d.line([tuple(foot), tuple(top)], fill=INK, width=int(wd + 2 * ink))
    d.line([tuple(foot), tuple(top)], fill=grey, width=int(wd))
    arm = min(max(4.0 * ss, 2.6 * s), 18.0 * ss)
    a, b = top - n * arm, top + n * arm
    d.line([tuple(a), tuple(b)], fill=INK, width=int(wd * 0.8 + 2 * ink))
    d.line([tuple(a), tuple(b)], fill=grey, width=int(wd * 0.8))
    hr = min(max(2.5 * ss, 0.9 * s), 6.0 * ss)
    for c in (a, b, top):                                 # the two lamp heads and the cap
        r = hr if c is not top else hr * 0.8
        d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=(236, 228, 196), outline=INK, width=ink)


def _map_axes(cam):
    """The aerial's map metres on the canvas: origin (the lamp post) and one metre right / down."""
    ss = B.SS
    (ox, oy), _ = cam.project((LAMP[0], 0.0, LAMP[1]))
    (ax_, ay_), _ = cam.project((LAMP[0] - 1.0, 0.0, LAMP[1]))
    ox, oy = ox * ss, oy * ss
    ex = np.array([ax_ * ss - ox, ay_ * ss - oy])
    return ox, oy, ex, np.array([-ex[1], ex[0]])


# ------------------------------------------------------------------------------------------------ the white van
# (Sam, 9 Nov: "make one white van drive like an absolute twat") In from the bottom-left arm squeezing down the white
# centre line, flat out between the queue and the oncoming cars; straight over the mini's dome instead of round it; cuts inside the splitter
# island, weaving across the lanes; out down the bottom-right arm, flat out. It is not in the give-way traffic: its
# start time is picked so it never touches anything (the cars, the moped, the e-bikes): `van_faults`.
VAN_L, VAN_W = 6.0, 2.1
VAN_T0 = 24.1                                    # when it appears (chosen by `van_faults`)
_VAN = None


def _van_path():
    m, mj = 148, 45
    u, uj = np.array(_pol(1, m)), np.array(_pol(1, mj))
    wrong = np.array(_pol(0.0, m - 90))                  # down the white centre line, between the queue and the
    #                                                      oncoming cars (no gap is ever clear to be fully wrong-side)
    out = np.array(_pol(2.6, mj - 90))                   # the outbound lane of the exit arm (the right side)
    pts = [u * 130 + wrong, u * 80 + wrong, u * 52 + wrong * 0.6, np.array(_pol(R_MINI, m)),   # over the dome
           np.array(_pol(27.5, m - 22)), np.array(_pol(24.5, m - 45)), np.array(_pol(25.5, m - 75)),
           np.array(_pol(29.0, mj + 14)), uj * 47 + out, uj * 70 + out, uj * 130 + out]
    xy, sarr = _resample(np.array(pts), 0.25)
    return xy, sarr


def van_at(t):
    """(x, y, heading) of the van at t, or None: flat out (18 m/s) in, a stab of the brakes over the dome (12), 15
    across the middle, flat out out (22), weaving side to side as it goes."""
    global _VAN
    if _VAN is None:
        xy, sarr = _van_path()
        dt = 1 / FPS
        sp, s_, ts = [], 0.0, []
        L_ = sarr[-1]
        tt = 0.0
        while s_ < L_ and tt < 30:
            k = int(np.searchsorted(sarr, s_))
            r = float(np.hypot(*xy[min(k, len(xy) - 1)]))
            v = 18.0 if r > 70 else 12.0 + 6.0 * min(1.0, max(0.0, (r - 40) / 30)) if s_ < L_ * 0.45 else \
                (15.0 if r < 46 else min(22.0, 15.0 + (r - 46) * 0.5))
            ts.append((tt, s_))
            s_ += v * dt
            tt += dt
        _VAN = (xy, sarr, np.array(ts))
    xy, sarr, ts = _VAN
    tl = t - VAN_T0
    if tl < 0 or tl > ts[-1, 0]:
        return None
    s_ = float(np.interp(tl, ts[:, 0], ts[:, 1]))
    k = min(len(xy) - 2, int(np.searchsorted(sarr, s_)))
    p, q = xy[k], xy[k + 1]
    hd = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
    n = np.array([-(q[1] - p[1]), q[0] - p[0]]) / (np.hypot(*(q - p)) + 1e-9)
    amp = 0.12 if math.hypot(*p) > 40 else 0.9          # a twitch on the centre line, a full weave inside
    weave = amp * math.sin(tl * 3.4)
    pos = p + n * weave
    return float(pos[0]), float(pos[1]), hd + math.degrees(math.atan2(amp * 3.4 * math.cos(tl * 3.4), 15.0))


def _boxes_touch(a, b, gap=0.05):
    """Do two vehicles (x, y, heading, length, width) overlap (oriented boxes, a small gap allowed)?"""
    def corners(x, y, h, L_, W_):
        c_, s_ = math.cos(math.radians(h)), math.sin(math.radians(h))
        return [np.array([x + u * c_ - w * s_, y + u * s_ + w * c_]) for u, w in
                ((L_ / 2 + gap, W_ / 2 + gap), (L_ / 2 + gap, -W_ / 2 - gap), (-L_ / 2 - gap, -W_ / 2 - gap),
                 (-L_ / 2 - gap, W_ / 2 + gap))]
    A, Bc = corners(*a), corners(*b)
    for P_ in (A, Bc):
        for k in range(2):
            e_ = P_[k + 1] - P_[k]
            ax = np.array([-e_[1], e_[0]])
            pa, pb = [float(np.dot(q, ax)) for q in A], [float(np.dot(q, ax)) for q in Bc]
            if max(pa) < min(pb) or max(pb) < min(pa):
                return False
    return True


def van_faults(t0=None):
    """The van never touches a car, the moped or an e-bike, and stays on the road (its dome run excepted)."""
    out = []
    f = traffic()
    for fr in range(int(19.86 * FPS), int(DUR * FPS)):
        t = fr / FPS
        v_ = van_at(t)
        if v_ is None:
            continue
        x, y, hd = v_
        for c in f.get(fr, []):
            if math.hypot(c[0] - x, c[1] - y) < 9 and _boxes_touch((x, y, hd, VAN_L, VAN_W), c[:5]):
                out.append(f'VAN: touches a car at {t:.2f} s near ({x:.0f}, {y:.0f}) m')
                break
        for nb in range(2):
            bx, by, _ = ebike_at(nb, t)
            if math.hypot(bx - x, by - y) < 3.4:
                out.append(f'VAN: touches an e-bike at {t:.2f} s')
        c_, s_ = math.cos(math.radians(hd)), math.sin(math.radians(hd))
        for u_, w_ in ((VAN_L / 2, VAN_W / 2), (VAN_L / 2, -VAN_W / 2), (-VAN_L / 2, VAN_W / 2), (-VAN_L / 2, -VAN_W / 2)):
            if math.hypot(x, y) < 150 and not on_road((x + u_ * c_ - w_ * s_, y + u_ * s_ + w_ * c_), domes=False):
                out.append(f'VAN: off the road at {t:.2f} s near ({x:.0f}, {y:.0f}) m')
                break
    return out[:6]


def draw_cars(pil, cam, t):
    fr = int(round(t * FPS))
    cars = list(traffic().get(fr) or [])
    v_ = van_at(t)
    if v_ is not None:                                   # the white van (Sam, 9 Nov), drawn like the others
        cars.append((v_[0], v_[1], v_[2], VAN_L, VAN_W, (246, 246, 242), -1))
    if not cars:
        return
    ss = B.SS
    (ox, oy), _ = cam.project((LAMP[0], 0.0, LAMP[1]))
    (ax_, ay_), _ = cam.project((LAMP[0] - 1.0, 0.0, LAMP[1]))
    ox, oy = ox * ss, oy * ss
    ex = np.array([ax_ * ss - ox, ay_ * ss - oy])
    ey = np.array([-ex[1], ex[0]])
    s = float(np.linalg.norm(ex))
    d = ImageDraw.Draw(pil)
    ink = max(1, int(min(2.0 * ss, max(1.0, 0.16 * s))))

    def P(p):
        return (ox + p[0] * ex[0] + p[1] * ey[0], oy + p[0] * ex[1] + p[1] * ey[1])
    for x, y, hd, Lc, Wc, col, cid in cars:
        if cid == MOPED_ID:                              # the delivery moped: drawn with the people
            continue
        c, sn = math.cos(math.radians(hd)), math.sin(math.radians(hd))

        def R(u, v):
            return P((x + u * c - v * sn, y + u * sn + v * c))
        sh = [P((x + u * c - v * sn - 0.857 * 1.2, y + u * sn + v * c + 0.514 * 1.2))
              for u, v in ((-Lc / 2, -Wc / 2), (Lc / 2, -Wc / 2), (Lc / 2, Wc / 2), (-Lc / 2, Wc / 2))]
        d.polygon(sh, fill=(60, 60, 62))
        body = [R(-Lc / 2, -Wc / 2), R(Lc / 2 - 0.4, -Wc / 2), R(Lc / 2, -Wc / 2 + 0.3), R(Lc / 2, Wc / 2 - 0.3),
                R(Lc / 2 - 0.4, Wc / 2), R(-Lc / 2, Wc / 2)]
        d.polygon(body, fill=col)
        d.line(body + [body[0]], fill=INK, width=ink, joint='curve')
        if Lc < 6:
            d.polygon([R(Lc * 0.12, -Wc * 0.4), R(Lc * 0.30, -Wc * 0.42), R(Lc * 0.30, Wc * 0.42), R(Lc * 0.12, Wc * 0.4)],
                      fill=(40, 46, 56))
            d.polygon([R(-Lc * 0.36, -Wc * 0.4), R(-Lc * 0.28, -Wc * 0.4), R(-Lc * 0.28, Wc * 0.4), R(-Lc * 0.36, Wc * 0.4)],
                      fill=(40, 46, 56))
        else:
            d.polygon([R(Lc / 2 - 1.2, -Wc * 0.42), R(Lc / 2 - 0.5, -Wc * 0.42), R(Lc / 2 - 0.5, Wc * 0.42),
                       R(Lc / 2 - 1.2, Wc * 0.42)], fill=(40, 46, 56))


# ------------------------------------------------------------------------------------------------ shot 6's people
# Sam's notes 12-16 (8 Nov): walkers, a scuffle on a path, two hooded teens on e-bikes, a delivery moped, a burnt-out
# car by the stadium. Drawn with the duplicate build's figures (elder_swindon_extras: person, ebike, moped, fight,
# burnt_car), placed on this roundabout. People and bikes drawn up to 4 times real size so they read on a phone
# (a liberty: named to Sam); they grow into it as the camera climbs.
import elder_swindon_extras as X   # noqa: E402

FOOTPATH_R = 64.0                                # the footpath round the green, between the ring and the trees
MOPED_ID = 55                                    # which car in the traffic is the delivery moped (note 15)
FIGHT_AT, FIGHT_DIR = tuple(_pol(FOOTPATH_R, 246)), 246 + 90      # on the footpath, top left (note 13)
BURNT_AT = (-56.0, 165.0, 75.0)                  # on the green by the stadium's corner (note 16)
EBIKE_R = 20.5                                   # the teens' line: inside the ring, the wrong way (note 14)


class _MapView:
    """elder_swindon_extras' View, but on this film's map (metres right, metres down from the lamp post)."""
    def __init__(self, pil, cam, enl_cap=4.0):
        self.pil = pil
        self.d = ImageDraw.Draw(pil, 'RGBA')
        self.ox, self.oy, self.ex, self.ey = _map_axes(cam)
        self.k = float(np.linalg.norm(self.ex))
        self.enl = float(np.clip(1080 / (self.k / B.SS) / 30.0, 1.0, enl_cap))
        self.lw = max(1, int(min(2.2 * B.SS, max(1.0, 0.18 * self.k))))

    def P(self, sx, sy, y=0.0):
        return (self.ox + sx * self.ex[0] + sy * self.ey[0], self.oy + sx * self.ex[1] + sy * self.ey[1])

    def poly(self, pts, fill, outline=INK, lw=None, y=0.0):
        Q = [self.P(x, z) for x, z in pts]
        self.d.polygon(Q, fill=fill)
        if outline is not None:
            self.d.line(Q + [Q[0]], fill=outline, width=lw or self.lw, joint='curve')

    def circle(self, cx, cy, r, fill, outline=INK, lw=None, n=None, y=0.0):
        n = n or int(np.clip(r * self.k / 3, 10, 90))
        self.poly([(cx + r * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)],
                  fill, outline, lw)

    def line(self, pts, fill, w_m=None, w_px=None, y=0.0):
        Q = [self.P(x, z) for x, z in pts]
        self.d.line(Q, fill=fill, width=int(max(1, w_px * B.SS if w_px else w_m * self.k)), joint='curve')

    def visible(self, sx, sy, r):
        x, y = self.P(sx, sy)
        rr = r * self.k
        w, h = self.pil.size
        return -rr < x < w + rr and -rr < y < h + rr


def _walk_paths():
    """Where people walk: only the footpath round the green, away from the road (Sam, 9 Nov: none next to the road;
    the pavements by the ring and the arms are left empty). Each green's stretch, clear of the arms, both ways."""
    out = []
    for k_ in range(5):
        a0 = MINIS[k_] + 13
        arc = [_pol(FOOTPATH_R, a) for a in np.linspace(a0, a0 + 46, 10)]
        out += [arc, arc[::-1]]
    return out


_WALK = None
TOPS = [(236, 236, 232), (200, 60, 60), (90, 120, 60), (232, 120, 160), (150, 152, 158), (70, 90, 150),
        (220, 180, 60), (150, 200, 230), (40, 40, 44)]
HAIRS = [(60, 44, 30), (30, 26, 24), (180, 150, 90), (80, 60, 40), (200, 170, 110)]


def walkers_on(v, t):
    global _WALK
    if _WALK is None:
        rng = np.random.default_rng(12)
        _WALK = []
        for pts in _walk_paths():
            p = np.array(pts, float)
            for j in range(2):
                _WALK.append((p, float(rng.uniform(1.0, 1.5)), float(rng.uniform(0, 200)),
                              TOPS[int(rng.integers(0, len(TOPS)))], HAIRS[int(rng.integers(0, len(HAIRS)))],
                              int(rng.integers(0, 3)) == 0))
    for p, sp, off, top, hair, hood in _WALK:
        seg = np.hypot(*(p[1:] - p[:-1]).T)
        cum = np.concatenate([[0], np.cumsum(seg)])
        d_ = (off + sp * t) % (2 * cum[-1])              # there and back
        s_ = d_ if d_ < cum[-1] else 2 * cum[-1] - d_
        k = max(0, min(int(np.searchsorted(cum, s_) - 1), len(p) - 2))
        x, y = p[k] + (p[k + 1] - p[k]) * (s_ - cum[k]) / seg[k]
        h = math.degrees(math.atan2(*(p[k + 1] - p[k])[::-1])) + (0 if d_ < cum[-1] else 180)
        if v.visible(x, y, 3):
            X.person(v, x, y, h, top, None if hood else hair, t + off, hood=top if hood else None)


def ebike_at(n, t):
    """The two teens: clockwise round the inside of the ring (the wrong way), weaving, far too fast (17 m/s)."""
    a = 200 + math.degrees(t * 17.0 / EBIKE_R) + n * 22    # a bit faster (Sam, 9 Nov: was 14 m/s)
    w = 1.2 * math.sin(t * 2.7 + n * 1.9)
    r = EBIKE_R + w
    dr = 1.2 * 2.7 * math.cos(t * 2.7 + n * 1.9)        # weaving: the heading turns with it
    x, y = _pol(r, a)
    return x, y, a + 90 - math.degrees(math.atan2(dr, 17.0))


def draw_people(pil, cam, t):
    v = _MapView(pil, cam)
    if v.enl < 1.05 and v.k / B.SS > 40:                # still close: the climb's start shows only the island
        return
    # (the burnt-out car, note 16, removed: Sam, animatic 3: it doesn't register)
    walkers_on(v, t)
    X.FIGHT_AT, X.FIGHT_DIR = FIGHT_AT, FIGHT_DIR
    X.fight(v, t)
    fr = int(round(t * FPS))
    for x, y, hd, *_r, cid in traffic().get(fr, []):
        if cid == MOPED_ID:
            X.moped(_MapView(pil, cam, enl_cap=2.0), x, y, hd)
    vb = _MapView(pil, cam, enl_cap=4.0 * 2 / 3)       # the bikes a third smaller (Sam, 9 Nov)
    for n, (hood, top) in enumerate((((40, 40, 44), (40, 40, 44)), ((150, 152, 158), (150, 152, 158)))):
        x, y, h = ebike_at(n, t)
        X.ebike(vb, x, y, h, hood, top, t)
    pram_walk(v, t)


PRAM_ARC = (292.0, 332.0)                        # the two women with a pram: the footpath, top right (Sam, 9 Nov)


def pram_walk(v, t):
    """Two women walking side by side along the footpath, one pushing a pram (house style, from above)."""
    a = PRAM_ARC[0] + (PRAM_ARC[1] - PRAM_ARC[0]) * ((t - 19.0) * 0.9 / (FOOTPATH_R * math.radians(PRAM_ARC[1] - PRAM_ARC[0])))
    h = a + 90                                           # walking clockwise round the green
    e = v.enl
    p = np.array(_pol(FOOTPATH_R - 0.45 * e, a)); q = np.array(_pol(FOOTPATH_R + 0.45 * e, a))
    if not v.visible(*p, 6):
        return
    fw = np.array(_pol(1, h))
    for c_, top, hair in ((p, (230, 150, 180), (196, 160, 96)), (q, (120, 150, 200), (70, 46, 34))):
        X.person(v, c_[0], c_[1], h, top, hair, t)
        pt = c_ - fw * 0.17 * e                            # a ponytail behind the head
        v.circle(pt[0], pt[1], 0.065 * e, hair, INK)
    pr = p + fw * 0.85 * e                                 # the pram ahead of the first: body, hood, handle
    v.poly(X.rrect(pr[0], pr[1], 0.8 * e, 0.5 * e, h, 0.15 * e, 3), (60, 70, 110), INK)
    hd_ = pr + fw * 0.22 * e
    v.circle(hd_[0], hd_[1], 0.22 * e, (40, 46, 80), INK)
    v.line([tuple(p + fw * 0.35 * e), tuple(pr - fw * 0.38 * e)], INK, w_m=0.05 * e)


def flat_props(pil, cam, t):
    """The scroll, can and packet in house style for the flat aerial (tiny from up here)."""
    ss = B.SS
    d = ImageDraw.Draw(pil)
    (_, _), k = cam.project((0, 0, 0))
    lw = max(1, int(k * 0.02 * ss))
    for (a, b), col, wd in ((CAN, (180, 40, 40), 0.07), (SCROLL, (214, 170, 80), 0.05)):
        A = [v * ss for v in cam.project((a[0], 0, a[1]))[0]]
        Bp = [v * ss for v in cam.project((b[0], 0, b[1]))[0]]
        d.line([tuple(A), tuple(Bp)], fill=INK, width=max(1, int(k * wd * ss) + 2))
        d.line([tuple(A), tuple(Bp)], fill=col, width=max(1, int(k * wd * ss)))
    C.SS = ss
    if k * 0.13 > 3:
        packet_rest_flat(pil, cam, ss)


# ------------------------------------------------------------------------------------------------ the climb, shot 6
def mix_flat(t):
    """How far the near-real look has given way to the flat (Showstopper 5: crossed while fastest, MIX0-MIX1)."""
    return ease((t - MIX0) / (MIX1 - MIX0))


def flat_frame(t, cam):
    pil = B.canvas((118, 146, 86))
    aerial_flat(pil, cam, t)
    draw_cars(pil, cam, t)
    draw_people(pil, cam, t)
    draw_pigeons(pil, cam, t, flat=True)
    flat_props(pil, cam, t)
    draw_vomit(pil, cam, flat=True)
    draw_bag(pil, cam, flat=True)
    k, surf = man_at(t)
    L.draw(pil, cam, k, MAN, t, surfaces=[(p0, n) for _, p0, n in surf], prts=man_parts(k))
    d = dog_at(t)
    if d is not None:
        draw_dog(pil, cam, d)
    return pil


def picture_raw(t):
    cam = cam_for(t)
    if t < MIX0:
        return near_real(t, cam)
    if t >= MIX1:
        return flat_frame(t, cam)
    a = mix_flat(t)
    nr = near_real(t, cam)
    fl = flat_frame(t, cam)
    return Image.blend(nr, fl, a)


_MEMO = None


def _memo_dir():
    """Each frame drawn once at the check size and kept (pre-flight's passes and the small animatic share it);
    the key is all the code, so any change draws afresh. Nothing in this film's drawing logs to the drawing-pass
    checks (no views.py people, no burnham people), so a kept frame loses no check."""
    global _MEMO
    if _MEMO is None:
        base = os.environ.get('FILM_CACHE', os.path.expanduser('~/.cache/filmcache'))
        _MEMO = os.path.join(base, f'{NAME}-memo', E.code_hash()[:12])
        if not os.path.isdir(_MEMO):                     # older code's frames: gone (disk)
            import shutil
            root = os.path.dirname(_MEMO)
            for old in (os.listdir(root) if os.path.isdir(root) else []):
                shutil.rmtree(os.path.join(root, old), ignore_errors=True)
        os.makedirs(_MEMO, exist_ok=True)
    return _MEMO


def picture(t):
    """The frame without the title (it goes on last, in overlay)."""
    if B.SS != 1:
        return picture_raw(t)
    i = int(round(t * FPS))
    if abs(i / FPS - t) > 1e-6:
        return picture_raw(t)
    path = os.path.join(_memo_dir(), f'{i:04d}.png')
    if os.path.exists(path):
        try:
            im = Image.open(path)
            im.load()
            return im.convert('RGBA')
        except OSError:
            pass
    im = picture_raw(t)
    tmp = path + f'.{os.getpid()}.tmp'
    im.save(tmp, format='PNG', compress_level=1)
    os.replace(tmp, path)
    return im


# ------------------------------------------------------------------------------------------------ title
TITLE_Y = 1330                                   # below the roundabout now the view moved north (note 17)
TITLE_X = 540                                    # centred on the frame (Sam, note 5); SWINDON sized to end before x 900
RINGS = ((-150, -60, 300, 20, 230), (170, -40, 280, 200, 250), (0, 160, 330, 120, 200), (-60, -260, 230, 300, 210),
         (120, 260, 260, 40, 190))                          # (dx, dy, radius, start angle, sweep) in frame pixels
GOLD = (226, 184, 118)
BIG_PX = 132                                     # SWINDON's size: 706 px wide, centred, so it ends before x 900


def _glow(layer, radius, strength):
    a = layer.filter(ImageFilter.GaussianBlur(radius))
    arr = np.asarray(a, float)
    arr[..., 3] = np.clip(arr[..., 3] * strength, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), 'RGBA')


def title(img, t):
    """The teaser's end card over the drifting roundabout: the picture dims a little, slowly (Sam, note 4: it went too
    dark too fast), gold rings bloom as the camera lands (19.86 hit) and drift, "The Elder Scrolls VI" and its rule fade
    in (20.3-21.3), centred and grander (note 5),
    SWINDON burns in letter by letter with a glowing edge (22-27, Sam 8 Nov) and cools to dull bronze (29)."""
    if t < CLIMB1:
        return img
    w, h = img.size
    k = w / 1080
    dim = 0.10 * ease((t - CLIMB1) / 2.5)               # (Sam, animatic 3: less greying out; was 0.26, first 0.55)
    img.alpha_composite(Image.new('RGBA', img.size, (8, 6, 4, int(255 * dim))))
    cy = TITLE_Y * k
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    bloom = ease((t - CLIMB1) / 1.0)
    flash = math.exp(-((t - CLIMB1 - 0.3) / 0.35) ** 2)
    for i, (ox, oy, r, a0, sw) in enumerate(RINGS):
        rr = r * (0.72 + 0.28 * bloom) * k
        spin = (t - CLIMB1) * (3 + i) * (1 if i % 2 else -1)
        a = int(255 * min(1.0, 0.25 + 0.75 * bloom) * (0.55 + 0.45 * flash))
        cx_, cy_ = TITLE_X * k + ox * k, cy + oy * k
        d.arc([cx_ - rr, cy_ - rr, cx_ + rr, cy_ + rr], a0 + spin, a0 + spin + sw * (0.4 + 0.6 * bloom),
              fill=(246, 210, 140, a), width=max(1, int(3.6 * k)))
    img.alpha_composite(_glow(lay, 7 * k, 2.6 + 2.5 * flash))
    img.alpha_composite(_glow(lay, 2 * k, 1.4))
    img.alpha_composite(lay)
    fs = ImageFont.truetype(os.path.join(HERE, 'fonts', 'Cinzel-Variable.ttf'), int(66 * k))   # grander (note 5)
    try:
        fs.set_variation_by_name('SemiBold')
    except Exception:
        pass
    fb = ImageFont.truetype(os.path.join(HERE, 'fonts', 'Cinzel-Variable.ttf'), int(BIG_PX * k))
    try:
        fb.set_variation_by_name('Bold')
    except Exception:
        pass
    a_s = ease((t - 20.3) / 1.0)
    if a_s > 0:
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        d.text((TITLE_X * k, cy - 126 * k), 'The Elder Scrolls VI', font=fs, fill=(226, 188, 120, int(255 * a_s)),
               anchor='mm', stroke_width=max(1, int(3 * k)), stroke_fill=(24, 18, 12, int(255 * a_s)))
        half = 330 * k * ease((t - 20.6) / 0.9)
        d.line([TITLE_X * k - half, cy - 80 * k, TITLE_X * k + half, cy - 80 * k], fill=(214, 176, 112, int(220 * a_s)),
               width=max(1, int(3 * k)))
        for sg in (-1, 1):                               # small diamonds at the rule's ends
            ex_, ey_, r_ = TITLE_X * k + sg * half, cy - 80 * k, 7 * k
            if half > r_:
                d.polygon([(ex_ - r_, ey_), (ex_, ey_ - r_), (ex_ + r_, ey_), (ex_, ey_ + r_)],
                          fill=(226, 188, 120, int(230 * a_s)))
        img.alpha_composite(_glow(lay, 5 * k, 0.9))
        img.alpha_composite(lay)
    if t >= 22.0:
        burn(img, t, fb, TITLE_X * k, cy + 40 * k, k)
    return img


SWINDON = 'SWINDON'
BURN0, BURN_STEP, BURN_LEN = 22.0, 0.62, 1.3        # letter i starts at BURN0 + i*BURN_STEP; all in by 27 s


def burn(img, t, font, cx, cy, k):
    """SWINDON burning in: each letter revealed left to right behind a white-hot edge, glowing, then cooling from
    molten gold to dull bronze by 29 s (the teaser's SENTINEL)."""
    w, h = img.size
    full = font.getbbox(SWINDON, anchor='mm')
    x_left = cx + full[0]
    txt = Image.new('L', img.size, 0)
    ImageDraw.Draw(txt).text((cx, cy), SWINDON, font=font, fill=255, anchor='mm')
    T = np.asarray(txt, float) / 255
    xs = np.arange(w)[None, :]
    reveal = np.zeros((1, w))
    front = np.zeros((1, w))
    x = x_left
    for i, ch in enumerate(SWINDON):
        cw = font.getlength(ch)
        u = (t - (BURN0 + i * BURN_STEP)) / BURN_LEN
        if u > 0:
            fx = x + cw * min(1.0, u) * 1.1 - cw * 0.05
            inl = (xs >= x - 2) & (xs < x + cw + 2)
            reveal = np.maximum(reveal, (inl & (xs <= fx)).astype(float))
            if u < 1.1:
                front = np.maximum(front, inl * np.exp(-((xs - fx) / (14 * k)) ** 2))
        x += cw
    cool = ease((t - 24.0) / 5.0)                         # the whole word cools as the last letters land
    hot = np.array([255, 214, 140])
    bronze = np.array([168, 120, 72])
    col = hot * (1 - cool) + bronze * cool
    a = T * reveal
    rgb = np.zeros((h, w, 3)) + col
    rgb = rgb + front[..., None] * np.array([80, 60, 40]) * T[..., None]
    lay = np.zeros((h, w, 4))
    lay[..., :3] = np.clip(rgb, 0, 255)
    lay[..., 3] = a * 255
    out = Image.fromarray(lay.astype(np.uint8), 'RGBA')
    edge = Image.fromarray((np.clip(front * T * 255 * 1.5 + a * 80 * (1 - cool), 0, 255)).astype(np.uint8), 'L')
    glowl = Image.new('RGBA', img.size, (255, 200, 120, 0))
    glowl.putalpha(edge.filter(ImageFilter.GaussianBlur(10 * k)))
    img.alpha_composite(glowl)
    stroke = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(stroke).text((cx, cy), SWINDON, font=font, fill=(0, 0, 0, 0), anchor='mm',
                                stroke_width=max(1, int(4 * k)), stroke_fill=(24, 16, 10, 255))
    sa = np.asarray(stroke, float)
    sa[..., 3] *= np.asarray(Image.fromarray((reveal.repeat(h, 0) * 255).astype(np.uint8)).filter(
        ImageFilter.MaxFilter(3)), float) / 255
    img.alpha_composite(Image.fromarray(sa.astype(np.uint8), 'RGBA'))
    img.alpha_composite(out)
    hotl = Image.new('RGBA', img.size, (255, 248, 224, 0))
    hotl.putalpha(Image.fromarray((np.clip(front * T, 0, 1) * 255).astype(np.uint8)))
    img.alpha_composite(hotl)


def overlay(img, t):
    return title(img, t)


def frame_image(t):
    return overlay(picture(t), t)


def draw_order(t):
    """Rule 57: what picture(t) draws, back to front."""
    s = shot_of(t)
    if s[0] in '1234' or t < MIX1:
        out = ['ground', 'litter', 'CAN']
        if scroll_cover(t) < 1.0:
            out.append('SCROLL')
        if t >= 15.08:
            out.append('PACKET')
        out.append('DROOLER')
        if dog_at(t) is not None:
            out.append('STAFFIE')
        if PACK_IN <= t < 15.08:
            out.append('PACKET')
        out.append('dust')
        return out
    return ['aerial', 'cars', 'CAN', 'SCROLL', 'PACKET', 'DROOLER', 'STAFFIE', 'title']


def _fx_dust(img):
    """The dust alone (shot 2's camera, 9 s): its streaks as the alpha."""
    cam = cam_for(9.0)
    z = np.zeros((B.H * B.SS, B.W * B.SS, 3))
    a = G.dust(z + 1.0, cam, B.SS, 9.0, strength=0.9, gust=gust(9.0))
    al = np.clip((1.0 - a.mean(-1)) * 255 * 3, 0, 255).astype(np.uint8)
    img.alpha_composite(Image.merge('RGBA', [Image.new('L', img.size, 220)] * 3 + [Image.fromarray(al)]))


def _fx_glint(img):
    z = np.zeros((B.H * B.SS, B.W * B.SS, 3))
    glint(z, cam_for(7.79), 7.79)
    al = np.clip(z.max(-1) * 255, 0, 255).astype(np.uint8)
    al[al < 20] = 0
    img.alpha_composite(Image.merge('RGBA', [Image.new('L', img.size, 255)] * 3 + [Image.fromarray(al)]))


def _fx_burn(img):
    """SWINDON mid-burn (24.3 s) alone: the letters, their hot edge and glow."""
    k = img.width / 1080
    fb = ImageFont.truetype(os.path.join(HERE, 'fonts', 'Cinzel-Variable.ttf'), int(BIG_PX * k))
    burn(img, 24.3, fb, TITLE_X * k, (TITLE_Y + 40) * k, k)


EFFECTS[:] = [('dust', 'trail', _fx_dust), ('glint', 'flash', _fx_glint), ('title burn', 'glow', _fx_burn)]


# ------------------------------------------------------------------------------------------------ sound
def soundtrack(stems=False):
    """The teaser's sound as it is (Sam, 8 Nov), only brought under full scale (its peaks went over by 1.1 dB)."""
    n = int((DUR + 0.3) * SR)
    x = MA.load(os.path.join(os.path.dirname(HERE), 'music', 'sentinel-teaser-audio.m4a'))
    # the track's next 5 s from Sam's second recording. It starts 1.27 s before the first ends (at 28.7701 s of it,
    # matched sample for sample: Sam heard a beat repeat in animatic 4's clip), so that much is skipped; joined with a
    # 20 ms crossfade over identical sound, level matched on the overlap, faded out over the last 0.8 s
    y = MA.load(os.path.join(os.path.dirname(HERE), 'music', 'sentinel-teaser-end.m4a'))
    cut, xf = int(SOUND_END * SR), int(0.02 * SR)
    x = x[:cut]
    cut = len(x)                                        # its true end (30.0358 s, a hair before SOUND_END)
    k0 = int(round(cut - REC2_AT * SR))                 # the recording's sample that matches the track's end
    ov = slice(int((REC2_AT + 0.1) * SR), cut)          # the overlap, in the track
    g = np.sqrt(np.mean(x[ov] ** 2)) / max(1e-6, np.sqrt(np.mean(y[int(0.1 * SR):k0] ** 2)))
    y = y[k0 - xf:k0 + int(EXTRA * SR)] * g
    ramp = np.linspace(0, 1, xf)
    x = np.concatenate([x[:-xf], x[-xf:] * (1 - ramp) + y[:xf] * ramp, y[xf:]])
    fo = int(0.8 * SR)
    x[-fo:] *= np.linspace(1, 0, fo) ** 1.5
    x = x * (0.97 / max(1e-6, float(np.abs(x).max())))
    mix = np.zeros(n)
    mix[:min(n, len(x))] = x[:n]
    return (mix, np.zeros(n), mix) if stems else mix


# ------------------------------------------------------------------------------------------------ checks
def checks():
    """Plan checks (seconds): the traffic never passes through itself; the shots follow the sound's hits."""
    faults = traffic_faults()
    for name, a, b in SHOTS[1:]:
        if not any(abs(a - h) < 0.02 for h in HITS + (CLIMB0,)):   # CLIMB0: no cut, the camera starts to climb
            faults.append(f'shot {name} starts at {a} s, off the sound\'s hits')
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


def scene(t):
    """Everyone and everything solid at t, exactly where picture(t) puts them (audit.py: rules 5, 6)."""
    import audit
    import clipcheck as CC
    out = []
    k, surf = man_at(t)
    out.append(audit.Thing('DROOLER', L.solids('DROOLER', k, MAN)))
    out.append(audit.Thing('CAN', [CC.capsule('CAN', 'body', (CAN[0][0], 0.02, CAN[0][1]), (CAN[1][0], 0.02, CAN[1][1]), 0.033)]))
    if scroll_cover(t) < 1.0:
        out.append(audit.Thing('SCROLL', [CC.capsule('SCROLL', 'body', (SCROLL[0][0], 0.02, SCROLL[0][1]),
                                                     (SCROLL[1][0], 0.02, SCROLL[1][1]), 0.025)]))
    p = packet_at(t)
    if p is not None:
        out.append(audit.Thing('PACKET', [CC.sphere('PACKET', 'body', p[0], 0.05)]))
    d = dog_at(t)
    if d is not None:
        a = math.radians(d['heading'])
        f = np.array([math.cos(a), 0, math.sin(a)])
        j = np.array([d['jaw'][0], 0.2, d['jaw'][1]])
        out.append(audit.Thing('STAFFIE', [CC.sphere('STAFFIE', 'head', j + f * 0.04, 0.09),
                                           CC.capsule('STAFFIE', 'body', j + f * 0.2, j + f * 0.5, 0.13)]))
    return out


def audits():
    return []


def LINE_SUBJECTS():
    """The man and the Staffie alone, large, for the line-work check (linecheck.py)."""
    def man_(im):
        cam = C.topcam(0.0, -0.1, 2.4, 2.1)
        k, surf = man_at(0.0)
        L.draw(im, cam, k, MAN, 0.0)

    def dog_(im):
        cam = C.topcam(0.6, 0.7, 1.0, 0.9)
        draw_dog(im, cam, dict(jaw=(0.42, 0.52), heading=DOG_HEAD, gait=0.0, run=0.25, clamped=True))
    return [('DROOLER', man_), ('STAFFIE', dog_)]


# ------------------------------------------------------------------------------------------------ sheets
def check_sheet(out, times, labels=None):
    """A labelled sheet of frames (1080 px wide, 4 across), each with its time and shot."""
    B.SS = 1
    from multiprocessing import Pool
    with Pool(os.cpu_count()) as p:
        ims = p.map(_sheet_frame, times)
    cols = 4
    tw, th = 270, 480
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * tw, rows * (th + 28)), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 15)
    for i, (im, t) in enumerate(zip(ims, times)):
        x, y = (i % cols) * tw, (i // cols) * (th + 28)
        lab = labels[i] if labels else f'{t:.2f} s  shot {shot_of(t)}'
        d.text((x + 6, y + 6), lab, font=f, fill=(255, 230, 120))
        sheet.paste(im, (x, y + 28))
    sheet.save(out, quality=88)
    print('sheet:', out)


def _sheet_frame(t):
    """A sheet tile; under 4 s it carries the Hook Text as finish.py lays it (HOOK's y and x)."""
    B.SS = 1
    im = frame_image(t).convert('RGBA')
    if 0.5 <= t < HOOK[1].get('until', 4.0):
        import tempfile
        import hook_text as HT
        path = os.path.join(tempfile.mkdtemp(), 'hook.png')
        HT.card(1080, 1920, HOOK[0], HOOK[1]['y'], path, x_mid=HOOK[1].get('x'))
        im.alpha_composite(Image.open(path).convert('RGBA').resize(im.size))
    return im.convert('RGB').resize((270, 480), Image.LANCZOS)


def main():
    a = sys.argv[1:]
    if a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            frame_image(float(x)).convert('RGB').save(os.path.join(a[1], f't{x}.jpg'), quality=90)
    elif a[0] == 'sheet':
        check_sheet(a[1], [float(x) for x in a[2:]])
    elif a[0] == 'check':
        B.SS = 1
        checks()
        import audit
        f = [x[len('AUDIT: '):] for x in audit.check(sys.modules[__name__])]
        print('\n'.join(['AUDIT: ' + x for x in f]) or 'audit: clean')
    elif a[0] == 'final':
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None,
                 stamp=False if '--nostamp' in a else None,
                 lock=False if '--no-lock' in a else None)   # --no-lock: Sam, 8 Nov: "Skip the checks" (pre-flight
#                                                              hung twice in its forked workers; notes, Decisions)


if __name__ == '__main__':
    main()
