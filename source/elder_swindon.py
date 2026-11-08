#!/usr/bin/env python3
"""Elder Scrolls: Swindon. A parody of the Elder Scrolls VI teaser: wind over soil uncovers a golden Elder Scroll by a
drooling man face down by his lager; a Staffie clamps on his ankle; the camera rockets up to the Magic Roundabout,
Swindon; SWINDON burns in. From satire_template.py (rule 58: no voices, no rooms). Notes: notes/elder-swindon.md.

MAP (rule 61)
- 45: STORY: shots and hits, HOOK, HAS, SHOT_CAST, the timings of every beat (gusts, scroll, packet, dog, climb)
- 95: cameras per shot: shot 1 glide can -> face, shot 2 along the scroll, shot 3 packet, shot 4 straight down,
      shot 5 the climb (width and centre eased; near-real hands over to flat 16.8-17.1), shot 6 held (aerial.held_cam)
- 150: the man (leg jerks when the dog tugs), the dog (charge, clamp, tug, shake), the scroll, the packet's tumble
- 215: picture(t): near-real (comp.near_real's parts) or flat (aerial.draw + the man layer), blended at the hand-over
- 280: overlay (title from elder_swindon_title), draw_order, scene, checks, main
Parts: world and props source/elder_swindon_comp.py; ground source/elder_swindon_ground.py; roundabout
source/elder_swindon_aerial.py; title source/elder_swindon_title.py.

    python3 source/elder_swindon.py stills OUT_DIR T [T ...]
    python3 source/elder_swindon.py final OUT.mp4 [--small] [--span T0 T1] [--reuse --redo SHOT]
"""
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B                    # noqa: E402
import film_engine as E                # noqa: E402
import mossad_audio as MA              # noqa: E402
import lying as L                      # noqa: E402
import elder_swindon_comp as C         # noqa: E402
import elder_swindon_ground as G       # noqa: E402
import elder_swindon_aerial as A       # noqa: E402
import elder_swindon_title as T        # noqa: E402

FPS, SR = 12, MA.SR

# =============================================== STORY ===============================================
NAME = 'elder-swindon'
HAS = {'people', 'effects', 'props'}
HOOK = (C.HOOK, {'y': 1240, 'until': 4.0})           # finish.py reads it (rule 75); clear of the can and his face
SUBTITLES_AT_FINISH = True
SUBS_IN_PICTURE = False
LINES = []                                           # no voices
AUDIO = os.path.join(os.path.dirname(HERE), 'music', 'sentinel-teaser-audio.m4a')
HITS = [1.07, 2.49, 6.57, 7.37, 7.79, 11.43, 13.86, 15.08, 17.45, 19.86, 21.93, 24.76, 27.19]
SHOTS = [('1', 0.0, 7.37), ('2', 7.37, 13.86), ('3', 13.86, 15.08), ('4', 15.08, 16.50), ('5', 16.50, 17.45),
         ('6', 17.45, 30.04)]
DUR = 30.04
SHOT_CAST = {'1': ['DROOLER'], '2': ['DROOLER'], '4': ['DROOLER', 'STAFFIE'], '5': ['DROOLER', 'STAFFIE'],
             '6': ['DROOLER']}
GUSTS = [1.07, 2.49, 6.57, 7.37]                    # dust blows harder on these hits
SCROLL_T = (7.37, 9.2)                               # the gust strips the soil off it
GLINT_T = 7.79                                       # the gold catches the sun
DOG_IN, DOG_CLAMP = 15.30, 15.85                     # charges in; clamps on his left ankle
CLIMB = (16.50, 17.45)                               # the camera rockets up, lands on the hit
HANDOVER = (16.80, 17.10)                            # near-real gives way to flat (Showstopper element 5)
W0, W1 = 2.6, 118.0                                  # frame width (metres) straight down at the start and end
# =====================================================================================================


def sm(a, b, t):
    u = min(1.0, max(0.0, (t - a) / (b - a)))
    return u * u * (3 - 2 * u)


def shot_of(t):
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


# ------------------------------------------------------------------------------------------------ cameras
def climb_u(t):
    """0..1 through the climb: slow start (the dog reads), fast middle, eased stop on 17.45."""
    u = min(1.0, max(0.0, (t - CLIMB[0]) / (CLIMB[1] - CLIMB[0])))
    return u ** 2.2 * (3 - 2 * u) if u < 1 else 1.0


def top_cam(t):
    u = climb_u(t)
    width = W0 * (W1 / W0) ** u
    end = A.held_cam(CLIMB[1]).at
    g = (width - W0) / (W1 - W0)
    x = 0.0 + (end[0] - 0.0) * g
    z = -0.3 + (end[2] + 0.3) * g
    d = width * 3.0 / W0
    return C.S.Cam((x, d, z + d * math.cos(math.radians(89.6))), (x, 0.0, z), focal=1080 * d / width)


def cam_for(t):
    s = shot_of(t)
    if s == '1':                                         # from the can and his splayed hand along the arm to his face
        u = sm(0.3, 3.6, t)
        at = (-0.62 + 0.52 * u, -0.98 + 0.30 * u)
        return C.orbit(at, 225, 70, 0.9 + 0.1 * u, 0.62 + 0.12 * u)
    if s == '2':                                         # along the scroll: spiked tip, grips, the case, the end cap
        u = sm(8.2, 13.6, t)
        return C.orbit((-0.80, -0.50 - 0.64 * u), 225 + 8 * u, 70, 0.9, 0.62)
    if s == '3':                                         # the packet tumbling past the scroll
        u = (t - 13.86) / 1.22
        return C.orbit((-0.78, -0.95 + 0.25 * u), 230, 70, 1.0, 0.8)
    if s in ('4', '5'):
        return top_cam(t)
    return A.held_cam(t)


# ------------------------------------------------------------------------------------------------ the man, the dog
def man_at(t):
    """The man face down, out cold; only his left leg jerks as the dog tugs."""
    k, surf = C.man()
    k = {a: (np.array(b, float).copy() if hasattr(b, '__len__') else b) for a, b in k.items()}
    p = dog_state(t)
    if p and p['clamped']:
        a = math.radians(p['heading'])
        pull = np.array([math.cos(a), 0, math.sin(a)]) * 0.05 * p['tug']
        k['anL'] = k['anL'] + pull
        k['knL'] = k['knL'] + pull * 0.45
    return k, surf


def dog_state(t):
    if t < DOG_IN:
        return None
    k0, _ = C.man()
    an = np.array(k0['anL'], float)
    heading = 50.0
    clamp_at = (an[0] + 0.02, an[2] + 0.04)
    if t < DOG_CLAMP:                                    # charging in head first from the bottom left
        u = (t - DOG_IN) / (DOG_CLAMP - DOG_IN)
        dist = 2.6 * (1 - u) ** 1.3
        a = math.radians(heading)
        at = (clamp_at[0] + math.cos(a) * dist, clamp_at[1] + math.sin(a) * dist)
        return dict(at=at, heading=heading + 6 * math.sin(t * 20), pull=0.0, run=t * 26, clamped=False, tug=0.0)
    s = t - DOG_CLAMP                                    # clamped: tugging back, shaking its head side to side
    tug = 0.5 + 0.5 * math.sin(s * 9.0)
    a = math.radians(heading)
    back = 0.05 * tug
    at = (clamp_at[0] + math.cos(a) * back, clamp_at[1] + math.sin(a) * back)
    return dict(at=at, heading=heading + 14 * math.sin(s * 13.0), pull=tug, run=None, clamped=True, tug=tug)


def draw_dog(pil, cam, t):
    p = dog_state(t)
    if p:
        C.dog(pil, cam, p['at'], p['heading'], p['pull'], run=p['run'])


# ------------------------------------------------------------------------------------------------ props
def scroll_bury(t):
    if t < SCROLL_T[0]:
        return 1.0
    return 1.0 - 0.55 * sm(SCROLL_T[0], SCROLL_T[0] + 0.4, t) - 0.45 * sm(SCROLL_T[0] + 0.4, 11.0, t)


def packet_at(t):
    """The sandwich packet: lying still, then tumbling end over end past the scroll (13.86-15.0) on the wind, then
    lying where it lands."""
    x0, z0, a0 = C.PACKET
    if t < 13.86:
        return (x0, z0, a0, 1.0)
    u = min(1.0, (t - 13.86) / 1.1)
    x, z = x0 - 0.2 * u, z0 - 1.05 * u
    spin = a0 + 540 * u
    flip = math.cos(u * 3 * math.pi)                      # end over end: it narrows as it flips
    return (x, z, spin, flip)


# ------------------------------------------------------------------------------------------------ picture
def near(cam, t):
    ss = B.SS
    img, H = G.soil(cam, ss=ss, grass=0.45)
    img = G.litter(img, cam, ss, C.LITTER)
    img = C.lying_rev(img, cam, C.CAN[0], C.CAN[1], C._prof_can, C.can_mat, bury=0.35, seed=2)
    b = scroll_bury(t)
    if b < 1:
        img = C.lying_rev(img, cam, C.SCROLL[1], C.SCROLL[0], C._prof_scroll, C.scroll_mat, bury=b, seed=3)  # uncovered from the end by his hand
    pil = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).convert('RGBA')
    px, pz, pa, flip = packet_at(t)
    C.packet(pil, cam, px, pz, pa)
    k, surf = man_at(t)
    L.draw(pil, cam, k, C.MAN, t, surfaces=[(p0, n) for _, p0, n in surf])
    C.drool(pil, cam, k)
    draw_dog(pil, cam, t)
    out = np.asarray(pil.convert('RGB'), float) / 255
    gust = max([math.exp(-((t - g) / 0.5) ** 2) for g in GUSTS] + [0.0])
    out = G.dust(out, cam, ss, t, strength=0.7 + 1.2 * gust)
    if GLINT_T - 0.2 < t < GLINT_T + 0.8 and b < 1:      # the gold catches the sun: a soft flare on the case
        (gx, gy), _ = cam.project((C.SCROLL[0][0] * 0.8 + C.SCROLL[1][0] * 0.2, 0.03, C.SCROLL[0][1] * 0.8 + C.SCROLL[1][1] * 0.2))
        hh, ww, _ = out.shape
        yy, xx = np.mgrid[0:hh, 0:ww]
        a = math.exp(-((t - GLINT_T - 0.1) / 0.25) ** 2)
        r2 = ((xx - gx * ss) ** 2 + (yy - gy * ss) ** 2) / (60 * ss) ** 2
        out = out + a * 0.8 * np.exp(-r2)[..., None] * np.array([1.0, 0.85, 0.5])
    hh, ww, _ = out.shape                                # a warm, moody vignette
    yy, xx = np.mgrid[0:hh, 0:ww]
    v = 1 - 0.55 * np.clip(((xx - ww / 2) / ww) ** 2 * 2.2 + ((yy - hh / 2) / hh) ** 2 * 2.2, 0, 1)
    out = out * v[..., None]
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).convert('RGBA')


def flat(cam, t):
    pil = Image.new('RGBA', (B.W * B.SS, B.H * B.SS))

    def man_layer(p):
        v = A.View(p, cam)
        sx0, sy0 = A.X0 - C.SCROLL[0][0], C.SCROLL[0][1] - A.Z0
        sx1, sy1 = A.X0 - C.SCROLL[1][0], C.SCROLL[1][1] - A.Z0
        v.line([(sx0, sy0), (sx1, sy1)], (30, 24, 16), w_m=0.07)       # the scroll: gold, outlined
        v.line([(sx0, sy0), (sx1, sy1)], (226, 184, 100), w_m=0.045)
        cx, cz = (C.CAN[0][0] + C.CAN[1][0]) / 2, (C.CAN[0][1] + C.CAN[1][1]) / 2
        v.poly(A.rrect(A.X0 - cx, cz - A.Z0, 0.16, 0.07, 90, 0.02, 2), (200, 40, 40))
        px, pz, pa, _ = packet_at(t)
        v.poly(A.rrect(A.X0 - px, pz - A.Z0, 0.18, 0.12, pa, 0.01, 2), (236, 236, 228))
        k, surf = man_at(t)
        L.draw(p, cam, k, C.MAN, t, surfaces=[(p0, n) for _, p0, n in surf])
        draw_dog(p, cam, t)
    A.draw(pil, cam, t, man_layer=man_layer)
    return pil


def picture(t):
    cam = cam_for(t)
    s = shot_of(t)
    if s in ('1', '2', '3', '4') or t < HANDOVER[0]:
        return near(cam, t)
    if t >= HANDOVER[1]:
        return flat(cam, t)
    a = sm(HANDOVER[0], HANDOVER[1], t)
    return Image.blend(near(cam, t), flat(cam, t), a)


def overlay(img, t):
    T.title(img, t)
    return img


def draw_order(t):
    s = shot_of(t)
    base = ['soil', 'litter', 'can', 'scroll', 'packet', 'DROOLER', 'drool']
    if s in ('4', '5') and t >= DOG_IN:
        base.append('STAFFIE')
    if s == '6':
        return ['roundabout', 'burnt car', 'DROOLER', 'e-bikes', 'traffic', 'walkers', 'fight', 'lamp post']
    return base


def soundtrack(stems=False):
    import subprocess
    import tempfile
    wav = os.path.join(tempfile.mkdtemp(), 'a.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', AUDIO, '-ac', '1', '-ar', str(SR), wav], check=True)
    import wave
    with wave.open(wav) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
    n = int((DUR + 0.3) * SR)
    mix = np.zeros(n)
    mix[:min(n, len(x))] = x[:n]
    return (mix, np.zeros(n), mix) if stems else mix


def main():
    a = sys.argv[1:]

    def set_ss(v):
        B.SS = v
        C.SS = v
        A.SS = v
    if a[0] == 'stills':
        set_ss(1)
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            overlay(picture(float(x)), float(x)).convert('RGB').save(os.path.join(a[1], f't{x}.jpg'), quality=88)
    elif a[0] == 'final':
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=set_ss, crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None,
                 stamp=False if '--nostamp' in a else None)


if __name__ == '__main__':
    main()
