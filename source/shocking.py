#!/usr/bin/env python3
"""Shocking Behaviour (TikTok satire, Sam 18 Oct): ITV's undercover journalist walks into Reform UK's Millbank Tower
HQ ... where Farage, Jenrick, Tice and Braverman are doing a perfectly synchronised TikTok dance to "Messy" under pop
lights. Jenrick trips; Farage cuts the music with a swipe and screams at him (bleeped). Notes: notes/shocking.md.
People: source/shocking_cast.py. Guide: guides/satire.md.

    python3 source/shocking.py cast OUT.jpg              the cast sheet (every view used, the dance keys, strengths)
    python3 source/shocking.py stills OUT_DIR T [T ...]  stills at these times (seconds)
    python3 source/shocking.py sheet OUT.jpg T [T ...]   several stills side by side on one sheet
    python3 source/shocking.py music                     rebuild the song bed from Sam's two screen recordings
    python3 source/shocking.py check                     every check and the audit (also run by preflight.py)
    python3 source/shocking.py final OUT.mp4 [--small] [--reuse --redo SHOT,SHOT]
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import shocking_cast as C        # noqa: E402  (installs the five heads and outfits into burnham)
import views as V                # noqa: E402
import figure as F               # noqa: E402
import mouths                    # noqa: E402
import mossad_audio as MA        # noqa: E402
import peepee as PP              # noqa: E402
import filmkit                   # noqa: E402
import film_engine as E          # noqa: E402
from ed import INK, curve, oval  # noqa: E402
from satire_style import rough, install_circle_hands   # noqa: E402

install_circle_hands(B)
FPS, SR = 12, MA.SR
NAME = 'shocking'
DATA = os.path.join(HERE, 'data', NAME)

# =============================================== STORY ==============================================================
# Sam's takes: shocking-1 the narrator (speech 2.8-9.2 s in the file), shocking-2 Farage (2.48-9.0 s, with Sam's two
# gaps for the bleeps at 5.57-6.60 and 7.32-7.99 in the file).
SLAM = 7.0                       # the slam cut into the dance; the song starts here
BEAT = 0.539                     # the song's beat (111 bpm, measured)
DOOR = (11.0, 13.0)              # the cutaway to the journalist in the doorway
TRIP = 16.0                      # three seconds into the second dance shot, Jenrick trips
SWIPE = 17.0                     # Farage's swipe lands: the music and the strobes stop dead
FARAGE_AT = 17.4                 # film time where Farage's first word starts
LINES = [
    dict(n=1, who='narrator', audio='shocking-1', start=2.8, at=0.4,
         text="ITV sent an undercover journalist into Reform UK's HQ, where she observed shocking behaviour."),
    dict(n=2, who='farage', audio='shocking-2', start=2.48, at=FARAGE_AT,
         text="Damn it Jenrick, if you can't stay in formation I swear to [bleep] I'll have your [bleep] ass deported."),
]
BLEEPS = [(5.57, 6.60), (7.32, 7.99)]          # in Farage's file seconds
SHOTS = [('lapel', 0.0, SLAM), ('dance', SLAM, DOOR[0]), ('door', DOOR[0], DOOR[1]), ('dance2', DOOR[1], FARAGE_AT),
         ('farage', FARAGE_AT, 21.6), ('wide', 21.6, 25.0)]     # the cut to the wide falls after the first bleep
DUR = BLACK_AT = 25.0
# The formation (Sam, 18 Oct), as seen on screen: Farage front centre, Jenrick middle left, Braverman middle right,
# Tice back left (set a little further out than Jenrick so his face is never hidden). Floor positions in metres:
# X across (+ right), Z away from the camera.
SPOT = {'farage': (0.0, 3.0), 'jenrick': (-0.75, 3.7), 'braverman': (0.75, 3.7), 'tice': (-1.3, 4.4)}
DANCERS = ('tice', 'jenrick', 'braverman', 'farage')     # far to near (drawing order)
# ====================================================================================================================


# --------------------------------------------------------------------------------------------- the office camera
M_UNIT = V.M_PER_UNIT
SOLE = 928.0                     # person units, neck to soles


class Cam3:
    """A simple camera in the office: focal length (px), height (m), horizon row; X across, Z away, Y up (metres)."""
    def __init__(self, foc=1400.0, h=1.6, horizon=900.0, cx=540.0):
        self.foc, self.h, self.horizon, self.cx = foc, h, horizon, cx

    def pt(self, X, Z, Y=0.0):
        return self.cx + self.foc * X / Z, self.horizon + self.foc * (self.h - Y) / Z

    def person(self, X, Z):
        """Neck base on screen and the person's scale for someone standing at (X, Z)."""
        s = self.foc / Z * M_UNIT
        x, y = self.pt(X, Z)
        return x, y - SOLE * s, s


DANCE_CAM = Cam3(1400.0, horizon=820.0)
WIDE_CAM = Cam3(1000.0, horizon=820.0)        # the reaction shot: a wider lens, so Jenrick is in it after his stumble


# --------------------------------------------------------------------------------------------- the dance
def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    if isinstance(a, tuple):
        return tuple(x + (y - x) * u for x, y in zip(a, b))
    return a + (b - a) * u


# A key pose: hand targets for the screen-left (L) and screen-right (R) hands in the body's frame (x across, y down
# from the neck, z towards us), the elbow direction, plus sway (the whole upper body across, feet planted), dip
# (knees bend), lean (degrees forward), head tilt (head across), chin (head up -, down +), and the face.
def P(L, R, poleL='out', poleR='out', sway=0.0, dip=0.0, lean=0.0, head=0.0, chin=0.0, mood='grin', look=0.0):
    pv = lambda q: V.POLES[q] if isinstance(q, str) else q
    return dict(L=L, R=R, poleL=pv(poleL), poleR=pv(poleR), sway=sway, dip=dip, lean=lean, head=head, chin=chin,
                mood=mood, look=look)


LOOSE_L, LOOSE_R = (-176, 400, 70), (176, 400, 70)
KEYS = {   # from the trend's original dance (Sam's clip, the woman on the right), frame by frame
    'thumb_R': P((-170, 390, 80), (240, -40, -60), 'back', 'out', sway=-20, dip=8, head=8),       # thumb jerked back over the shoulder
    'thumb_L': P((-240, -40, -60), (170, 390, 80), 'out', 'back', sway=20, dip=8, head=-8),
    'flick': P((-232, 440, 40), (232, 440, 40), 'back', 'back', dip=14),                       # both hands flicked down and out
    'lean_up': P((-150, 470, 120), (150, 470, 120), 'back', 'back', dip=4, lean=13, chin=0.2), # leaning in to the camera,
    'lean_dn': P((-150, 480, 130), (150, 480, 130), 'back', 'back', dip=16, lean=15, chin=0.3),  # shoulders hunched, bobbing
    'chin_R': P((-150, 350, 80), (330, 300, 70), 'out', 'down', sway=-12, chin=-0.7, mood='cool'),   # chin up, arm swept out
    'chin_L': P((-330, 300, 70), (150, 350, 80), 'down', 'out', sway=12, chin=-0.7, mood='cool'),
    'sway_L': P((-190, 390, 60), (170, 380, 80), 'back', 'back', sway=-22, dip=6, head=-12),
    'sway_R': P((-170, 380, 80), (190, 390, 60), 'back', 'back', sway=22, dip=6, head=12),
    'point': P((-176, 400, 70), (70, 160, 300), 'back', 'down', sway=-10, dip=6, head=6),       # finger pointed at us
    'point2': P((-176, 400, 70), (90, 190, 290), 'back', 'down', sway=-4, dip=12, head=4),
    'chin_hand': P((-180, 400, 70), (50, -70, 150), 'back', 'down', sway=10, head=10, chin=0.1, mood='cool'),   # hand by
    'chin_hand2': P((-180, 400, 70), (80, -50, 140), 'back', 'down', sway=16, head=14, chin=0.15, mood='cool'),  # the chin
}
# The routine on the song's clock (m: seconds since the slam cut), on its beats. Sam's clip mapped onto our song bed:
# m 0-2.7 = her clip 2.76-5.45 s (thumbs back, the flick, leaning in); m 2.7- = clip two from 0.25 s (chin up with
# the arm swept out, swaying, pointing at the camera, the hand by the chin).
b = BEAT
ROUTINE = [(0.0, 'thumb_R'), (b, 'thumb_L'), (2 * b, 'thumb_R'), (2.6 * b, 'flick'), (3.1 * b, 'lean_up'),
           (3.6 * b, 'lean_dn'), (4.1 * b, 'lean_up'), (4.6 * b, 'lean_dn'), (5.0 * b, 'chin_R'),
           (6.0 * b, 'chin_L'), (7.0 * b, 'sway_L'), (8 * b, 'sway_R'), (9 * b, 'sway_L'), (10 * b, 'sway_R'),
           (11 * b, 'sway_L'), (12 * b, 'sway_R'), (13 * b, 'point'), (13.5 * b, 'point2'), (14 * b, 'point'),
           (14.5 * b, 'point2'), (15 * b, 'chin_hand'), (15.5 * b, 'chin_hand2'), (16 * b, 'chin_hand'),
           (16.5 * b, 'chin_hand2'), (17 * b, 'chin_hand'), (17.5 * b, 'chin_hand2'), (18 * b, 'chin_hand'),
           (18.5 * b, 'chin_hand2'), (19 * b, 'chin_hand')]


def _cr(p0, p1, p2, p3, u):
    """Catmull-Rom: a smooth curve through the key poses (no stopping dead between beats)."""
    u2, u3 = u * u, u * u * u
    return 0.5 * (2 * p1 + (p2 - p0) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u2 + (3 * p1 - p0 - 3 * p2 + p3) * u3)


def _mix(ks, u):
    """Blend four key poses along the curve; words (the face) switch half way."""
    out = {}
    for k, v in ks[1].items():
        if isinstance(v, tuple):
            out[k] = tuple(_cr(*(kk[k][i] for kk in ks), u) for i in range(len(v)))
        elif isinstance(v, (int, float)):
            out[k] = _cr(*(kk[k] for kk in ks), u)
        else:
            out[k] = v if u < 0.5 else ks[2][k]
    return out


def routine_pose(m):
    """The dance at song time m: a smooth path through the key poses, each landing on its beat, so the body is
    always moving (Sam, 18 Oct: fluid and expressive). Each move eases out of one pose and into the next."""
    keys = ROUTINE
    if m <= keys[0][0]:
        return dict(KEYS[keys[0][1]])
    for i in range(len(keys) - 1):
        t0, t1 = keys[i][0], keys[i + 1][0]
        if m < t1:
            u = ease((m - t0) / (t1 - t0)) * 0.5 + (m - t0) / (t1 - t0) * 0.5   # a little ease into each beat
            ks = [KEYS[keys[max(0, i - 1)][1]], KEYS[keys[i][1]], KEYS[keys[i + 1][1]],
                  KEYS[keys[min(len(keys) - 1, i + 2)][1]]]
            return _mix(ks, u)
    return dict(KEYS[keys[-1][1]])


def dance_pose(m):
    """The pose with follow-through: the body leads; the hands arrive 0.06 s later and the head 0.09 s later
    (overlapping action), and a bounce in the knees on every beat."""
    k = routine_pose(m)
    arms = routine_pose(m - 0.06)
    head = routine_pose(m - 0.09)
    for f in ('L', 'R', 'poleL', 'poleR'):
        k[f] = arms[f]
    k['head'], k['chin'] = head['head'], head['chin']
    k['dip'] += 7 * (0.5 - 0.5 * math.cos(2 * math.pi * m / BEAT))
    return k


def build(sp, k):
    """Joints for a key pose. The sway moves the WHOLE upper body across as one piece (head, neck, jacket and arms
    together, so the neck never comes away: Sam, 18 Oct): the caller shifts the person by j['_sway'] and the feet
    are moved back the other way so they stay planted. The dip bends the knees."""
    j = V.standing(sp)
    sw, dip = k['sway'], k['dip']
    for side in 'LR':
        x, y, z = j['foot' + side]
        j['foot' + side] = (x - sw, y - dip, z)
    for side in 'LR':
        sx, sy, sz = j['sh' + side]
        tx, ty, tz = k[side]
        d = math.sqrt((tx - sx) ** 2 + (ty - sy) ** 2 + (tz - sz) ** 2)
        if d < 180:                                       # never fold the elbow tighter than a real one can
            f = 180 / max(d, 1e-6)
            tx, ty, tz = sx + (tx - sx) * f, sy + (ty - sy) * f, sz + (tz - sz) * f
        V.arm_to(j, side, (tx, ty, tz), k['pole' + side], 'fist')
    j['lean'] = k['lean']
    j['bob'] = dip
    j['head_dy'] = 30 * max(0.0, k['chin'])
    j['_sway'] = sw
    return j


def face_of(sp, k):
    sp['mood'] = k['mood']
    sp['head_dx'] = max(-12.0, min(12.0, k['head']))       # a small tilt only: the head stays on its neck
    sp['down'] = k['chin']
    sp['look'] = k.get('look', 0.0)


# --------------------------------------------------------------------------------------------- who does what, when
def trip_state(t):
    """Jenrick's trip (film seconds from TRIP): the foot catches, he lurches forward and to our left, arms flung up,
    stumbles three quick steps to the edge of the floor and catches himself, bent over; then straightens, hunched and
    scared. Returns (X, Z, key pose, extra face)."""
    u = t - TRIP
    X0, Z0 = SPOT['jenrick']
    X1, Z1 = -1.3, 3.1                                    # where he ends up (half out of the dance shot)
    if u < 0:
        return X0, Z0, None, {}
    flail = P((-300, -40, 60), (300, -60, 60), 'out', 'out', lean=20, mood='scared', head=-8)
    flail2 = P((-260, 60, 80), (280, -100, 40), 'out', 'out', lean=24, mood='scared', head=8)
    caught = P((-110, 520, 140), (110, 520, 140), 'back', 'back', lean=28, dip=40, mood='scared', chin=0.2)
    hunch = P((-150, 440, 90), (150, 440, 90), 'back', 'back', lean=8, dip=10, mood='scared', chin=0.3, look=1.0)
    keys = [(0.0, flail), (0.25, flail2), (0.5, flail), (0.75, caught), (1.3, caught), (1.8, hunch)]
    for (a, ka), (b2, kb) in zip(keys, keys[1:]):
        if u < b2:
            k = blend_keys(ka, kb, ease((u - a) / (b2 - a)))
            break
    else:
        k = dict(hunch)
    w = ease(min(1.0, u / 0.75))
    X, Z = X0 + (X1 - X0) * w, Z0 + (Z1 - Z0) * w
    k['step'] = (u < 0.75, int(u / 0.18) % 2)              # quick stumbling steps while travelling
    return X, Z, k, {}


def blend_keys(a, b2, u):
    out = {}
    for k, v in a.items():
        if isinstance(v, tuple):
            out[k] = tuple(x + (y - x) * u for x, y in zip(v, b2[k]))
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            out[k] = v + (b2[k] - v) * u
        else:
            out[k] = v if u < 0.5 else b2[k]
    return out


STAND = P((-176, 420, 60), (176, 420, 60), 'back', 'back', mood='neutral')
WINDUP = P((-176, 420, 60), (-40, 40, 160), 'back', 'down', mood='contempt', look=-1.0, head=-6)
SWIPED = P((-176, 420, 60), (330, 110, 60), 'back', 'out', mood='contempt', look=-1.0, head=-6)


def farage_dance_state(t):
    """Farage dances until he sees the trip (TRIP + 0.35 s): his head snaps round to our left, contempt; then the
    swipe: wind up across his chest, and the hand cuts out through the air, landing on SWIPE."""
    m = t - SLAM
    see = TRIP + 0.35
    if t < see:
        return dance_pose(m)
    if t < SWIPE - 0.3:
        k = blend_keys(dance_pose(see - SLAM), STAND, ease((t - see) / 0.35))
        k.update(mood='contempt', look=-1.0, head=-6)
        return k
    if t < SWIPE - 0.12:
        return blend_keys(STAND, WINDUP, ease((t - (SWIPE - 0.3)) / 0.18))
    if t < SWIPE:
        u = (t - (SWIPE - 0.12)) / 0.12
        return blend_keys(WINDUP, SWIPED, u * u * u)       # fast into the cut
    return blend_keys(SWIPED, STAND, ease((t - SWIPE - 0.5) / 0.5)) if t > SWIPE + 0.5 else dict(SWIPED)


def other_dance_state(who, t):
    """Tice and Braverman dance on until the swipe, freeze on it, then let their arms drop and look round."""
    if t < SWIPE:
        return dance_pose(t - SLAM)
    frozen = dance_pose(SWIPE - SLAM)
    k = blend_keys(frozen, STAND, ease((t - SWIPE - 0.25) / 0.45)) if t > SWIPE + 0.25 else dict(frozen)
    k.update(mood='alarm' if who == 'tice' else 'upset', look=-0.8 if who == 'braverman' else 0.6)
    return k


def make_person(img, cam3, who, X, Z, k, t, extra=None, step=None):
    """Draw one person at (X, Z) in a key pose k, front view."""
    sp = dict(C.CAST[who])
    j = build(sp, k)
    if step and step[0]:                                   # a stumbling step: one foot lifted forward
        side = 'L' if step[1] else 'R'
        x, y, z = j['foot' + side]
        j['foot' + side] = (x - 30, y - 40, z + 60)
    face_of(sp, k)
    sp['blink'] = F.blinking(t, BLINKS.get(who, ()))
    sp.update(extra or {})
    x, y, s = cam3.person(X, Z)
    V.person(img, B.Cam(1.0, 540, 960), x + j['_sway'] * s, y, s, sp, t, 0, j)
    return x, y, s


BLINKS = {w: F.blinks(i + 3, 0.0, DUR) for i, w in enumerate(DANCERS)}


# --------------------------------------------------------------------------------------------- lights and sound
def song_clock(t):
    return t - SLAM


def music_on(t):
    return SLAM <= t < SWIPE


WASH = [(232, 40, 168), (40, 206, 232), (150, 64, 236), (250, 170, 40)]


def wash_colour(m):
    bar = int(m / (BEAT * 2)) % len(WASH)
    return WASH[bar]


def pop_lights(img, t, cam3, strength=1.0):
    """The full pop performance (Sam, 18 Oct): the office lights down, a colour wash changing every two beats,
    sweeping coloured beams from the ring lights, pools of colour on the floor, and a strobe flash on the beat.
    Flat translucent shapes, no glows."""
    m = song_clock(t)
    W, H = img.size
    k = W / 1080
    dim = Image.new('RGBA', img.size, (14, 10, 30, int(80 * strength)))
    img.alpha_composite(dim)
    c = wash_colour(m)
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in range(5):                                    # sweeping beams from above
        cx = (180 + 180 * i) * k
        ang = math.sin(m * 2.1 + i * 1.3) * 0.5
        top = (cx, 520 * k)
        ln = 1500 * k
        w = 120 * k
        bx = cx + math.sin(ang) * ln
        by = 520 * k + math.cos(ang) * ln
        col = WASH[(i + int(m / BEAT)) % len(WASH)]
        d.polygon([top, (bx - w, by), (bx + w, by)], fill=col + (int(60 * strength),))
    for i, (X, Z) in enumerate(SPOT.values()):            # pools of colour on the floor
        x, y = cam3.pt(X, Z)
        rx, ry = 0.7 * cam3.foc / Z * k, 0.22 * cam3.foc / Z * k
        col = WASH[(i + int(m / (BEAT * 2))) % len(WASH)]
        d.ellipse([x * k - rx, y * k - ry, x * k + rx, y * k + ry], fill=col + (int(70 * strength),))
    img.alpha_composite(lay)
    tint = Image.new('RGBA', img.size, c + (int(26 * strength),))
    img.alpha_composite(tint)
    ph = (m % BEAT) / BEAT
    if ph < 0.12:                                         # the strobe, on the beat
        img.alpha_composite(Image.new('RGBA', img.size, (255, 255, 255, int(110 * strength))))


def load_song():
    path = os.path.join(DATA, 'song.wav')
    if not os.path.exists(path):
        raise FileNotFoundError("the song bed is missing: run `python3 source/shocking.py music` with Sam's clips")
    import wave
    with wave.open(path) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768
    return x


CLIP_A = os.path.join(DATA, 'clip-a.mov')                 # Sam's two screen recordings of the trend video (not on GitHub)
CLIP_B = os.path.join(DATA, 'clip-b.mov')
SPLICE = ((2.757, 5.447), (0.245, 8.2))                    # each half's music, cut on the beat (measured: 111 bpm)


def build_music():
    """The song bed from Sam's two halves, joined on a beat: half A 2.757-5.447 s (five beats), then half B from
    0.245 s. Copyrighted, so kept in source/data/shocking/ (not on GitHub; Sam, 18 Oct)."""
    import imageio_ffmpeg
    import subprocess
    out = []
    for clip, (a, b2) in zip((CLIP_A, CLIP_B), SPLICE):
        raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-ss', str(a), '-t', str(b2 - a), '-i', clip,
                              '-vn', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.int16).astype(np.float64) / 32768
        f = int(0.008 * SR)                                # no click at the join
        x[:f] *= np.linspace(0, 1, f)
        x[-f:] *= np.linspace(1, 0, f)
        out.append(x)
    MA.write_wav(os.path.join(DATA, 'song.wav'), np.concatenate(out))


# --------------------------------------------------------------------------------------------- the voices
NARR_OFF = 0.4 - 2.8                                       # film time = file time + offset
FAR_OFF = FARAGE_AT - 2.48
FAR_BITS = [   # Farage's take, piece by piece (file seconds): the words, and the gaps Sam left for the bleeps
    ('Damn it Jenrick,', 2.48, 3.31), ("if you can't stay in formation I swear to", 3.45, 5.57),
    ('bloody hell', 5.60, 6.55), ("I'll have your", 6.60, 7.32), ('bloody', 7.36, 7.95), ('ass deported.', 7.99, 8.96)]
FAR_TRACK = [(a + FAR_OFF, b2 + FAR_OFF, sh) for txt, a0, b0 in FAR_BITS
             for a, b2, sh in mouths.track(txt, [(a0, b0)])]
CAPS = [   # short chunks (two to five words), each with its first word
    (0.4, 1.5, 'ITV sent an'), (1.5, 2.9, 'undercover journalist'), (2.9, 4.3, "into Reform UK's HQ,"),
    (4.3, 5.6, 'where she observed'), (5.6, 6.9, 'shocking behaviour.'),
    (2.48 + FAR_OFF, 3.4 + FAR_OFF, 'Damn it Jenrick,'), (3.45 + FAR_OFF, 5.0 + FAR_OFF, "if you can't stay in formation"), (5.0 + FAR_OFF, 6.6 + FAR_OFF, 'I swear to ****'),
    (6.6 + FAR_OFF, 7.9 + FAR_OFF, "I'll have your ****"), (7.99 + FAR_OFF, 9.4 + FAR_OFF, 'ass deported.')]


def caption_at(t):
    for a, b2, txt in CAPS:
        if a <= t < b2:
            return txt
    return None


def soundtrack(stems=False):
    n = int((DUR + 0.3) * SR)
    voice, rest = np.zeros(n), np.zeros(n)
    for name, off in (('shocking-1', NARR_OFF), ('shocking-2', FAR_OFF)):
        v = MA.line(name)
        cut = int(max(0.0, -off) * SR) if off < 0 else 0
        s = int(max(0.0, off) * SR)
        seg = v[cut:cut + n - s]
        if name == 'shocking-1':                           # Sam's take ends with handling noise after 9.3 s: stop there
            seg = seg[:int((9.35 - (cut / SR)) * SR)]
            f = int(0.05 * SR)
            seg[-f:] *= np.linspace(1, 0, f)
        voice[s:s + len(seg)] += seg
    for a, b2 in BLEEPS:                                   # the censor bleeps fill Sam's gaps exactly
        s0, s1 = int((a + FAR_OFF) * SR), int((b2 + FAR_OFF) * SR)
        tt = np.arange(s1 - s0) / SR
        tone = 0.32 * np.sin(2 * np.pi * 1000 * tt)
        f = int(0.006 * SR)
        tone[:f] *= np.linspace(0, 1, f)
        tone[-f:] *= np.linspace(1, 0, f)
        voice[s0:s1] += tone
    song = load_song() * 0.36                            # sits just under the voices' loudness
    s0, s1 = int(SLAM * SR), int(SWIPE * SR)               # the song stops dead on the swipe
    seg = song[:s1 - s0].copy()
    f = int(0.012 * SR)
    seg[-f:] *= np.linspace(1, 0, f)
    rest[s0:s0 + len(seg)] += seg
    mix = voice + rest
    end = int(BLACK_AT * SR)
    mix, g = MA.master(mix, end)
    voice, rest = voice * g, rest * g
    mix[end:] = 0
    return (mix, voice, rest) if stems else mix


# --------------------------------------------------------------------------------------------- shot 1: the lapel camera
SKY, GLASS, GLASS_D, FRAME_C = (176, 204, 226), (120, 150, 170), (70, 92, 110), (214, 218, 220)
CANOPY, STONE, PAVE = (34, 40, 58), (206, 200, 186), (176, 172, 166)
_PLATE = {}


def millbank_plate():
    """Millbank Tower's entrance as the lapel camera sees it (refs millbank-1..4): from the pavement, low, looking up.
    Drawn once large; the walk zooms into it. Flat colour, one outline."""
    if 'img' in _PLATE:
        return _PLATE['img']
    W2, H2 = 1620, 2880
    img = Image.new('RGBA', (W2, H2), SKY + (255,))
    d = ImageDraw.Draw(img)
    rng = np.random.default_rng(5)
    for _ in range(6):                                     # a few flat clouds
        x, y = rng.uniform(0, W2), rng.uniform(60, 500)
        for k in range(4):
            r = rng.uniform(40, 90)
            d.ellipse([x + k * 60 - r, y - r * 0.6, x + k * 60 + r, y + r * 0.6], fill=(236, 240, 244))
    # the tower: converging upward (we look up at it)
    base_y, top_y = 1720, -200
    bl, br = 40, 1580
    tl, tr = 300, 1320
    d.polygon([(bl, base_y), (br, base_y), (tr, top_y), (tl, top_y)], fill=GLASS, outline=INK)
    rows = 26
    for r in range(rows + 1):                              # floors: stone bands between glass
        u = r / rows
        y = base_y + (top_y - base_y) * (1 - (1 - u) ** 1.35)
        xl, xr = bl + (tl - bl) * (base_y - y) / (base_y - top_y), br + (tr - br) * (base_y - y) / (base_y - top_y)
        d.line([(xl, y), (xr, y)], fill=STONE, width=max(2, int(16 * (1 - u))))
    cols = 14
    for c in range(cols + 1):                              # window mullions
        u = c / cols
        d.line([(bl + (br - bl) * u, base_y), (tl + (tr - tl) * u, top_y)], fill=FRAME_C, width=5)
    for _ in range(40):                                    # sky reflected in a few panes
        c = rng.integers(0, cols)
        r = rng.integers(2, rows)
        u0, u1 = c / cols, (c + 1) / cols
        y0 = base_y + (top_y - base_y) * (1 - (1 - r / rows) ** 1.35)
        y1 = base_y + (top_y - base_y) * (1 - (1 - (r + 1) / rows) ** 1.35)
        f = lambda y, u: (bl + (br - bl) * u) + ((tl + (tr - tl) * u) - (bl + (br - bl) * u)) * (base_y - y) / (base_y - top_y)
        d.polygon([(f(y0, u0) + 6, y0 - 8), (f(y0, u1) - 6, y0 - 8), (f(y1, u1) - 6, y1 + 8), (f(y1, u0) + 6, y1 + 8)],
                  fill=(150, 182, 204))
    # the ground floor: dark glass doors under the deep canopy
    d.rectangle([0, 1720, W2, 2160], fill=GLASS_D, outline=INK, width=3)
    for x in range(60, W2, 170):
        d.line([(x, 1720), (x, 2160)], fill=(30, 34, 40), width=8)
    d.rectangle([620, 1840, 1000, 2160], fill=(46, 56, 66), outline=INK, width=4)     # the revolving door
    d.line([(810, 1840), (810, 2160)], fill=(150, 160, 170), width=6)
    for x in (300, 1240):                                  # lights glowing inside the lobby (flat)
        d.rectangle([x, 1880, x + 110, 1960], fill=(210, 196, 150))
    # the canopy with its lettering
    d.polygon([(-40, 1560), (W2 + 40, 1560), (W2 + 40, 1740), (-40, 1740)], fill=CANOPY, outline=INK)
    d.polygon([(-40, 1740), (W2 + 40, 1740), (W2 + 40, 1790), (-40, 1790)], fill=(22, 26, 36))
    font = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans.ttf'), 92)
    txt = 'M I L L B A N K   T O W E R'
    d.text((W2 / 2, 1652), txt, font=font, fill=(214, 216, 220), anchor='mm')
    # steps and the pavement with its blue cycle lane
    for k in range(3):
        y = 2160 + 46 * k
        d.rectangle([-20, y, W2 + 20, y + 46], fill=STONE if k % 2 == 0 else (190, 184, 170), outline=INK)
    d.rectangle([-20, 2298, W2 + 20, H2], fill=PAVE)
    for y in range(2340, H2, 110):
        d.line([(0, y), (W2, y + 30)], fill=(160, 156, 150), width=3)
    d.polygon([(-20, 2560), (W2 + 20, 2520), (W2 + 20, 2640), (-20, 2690)], fill=(70, 130, 200))
    for i, x in enumerate(range(90, W2, 260)):             # parked scooters along the kerb (Claude's addition)
        y = 2470 + (i % 2) * 14
        col = [(30, 30, 34), (200, 200, 204), (60, 62, 70)][i % 3]
        d.ellipse([x, y + 60, x + 70, y + 130], fill=(24, 24, 26), outline=INK, width=3)
        d.ellipse([x + 160, y + 60, x + 230, y + 130], fill=(24, 24, 26), outline=INK, width=3)
        d.polygon([(x + 30, y + 70), (x + 70, y), (x + 170, y + 10), (x + 210, y + 80), (x + 120, y + 96)], fill=col,
                  outline=INK)
        d.rectangle([x + 60, y - 30, x + 150, y + 4], fill=(28, 28, 30), outline=INK, width=2)
    d.line([(1460, 2300), (1460, 1300)], fill=(40, 42, 46), width=14)                   # a lamp post
    d.rectangle([1444, 1280, 1476, 1310], fill=(40, 42, 46))
    _PLATE['img'] = img
    return img


def lapel_frame(t):
    """Shot 1: the walk up to the doors through her lapel camera (refs undercover-1, 2): chest height, looking up,
    crooked and swaying with each step, a cheap soft picture with washed-out colour and a pink-grey cast, grain, her
    jacket's dark edge smudging one corner, and the REC readout (Sam, 18 Oct: yes to REC)."""
    plate = millbank_plate()
    u = t / SLAM
    z = 1.0 + 0.55 * u * u * 0.6 + 0.25 * u                # walking closer: the entrance grows
    step = math.sin(2 * math.pi * 1.9 * t)                 # two steps a second
    roll = -4.0 + 1.8 * step
    cx, cy = 810 + 30 * math.sin(2 * math.pi * 0.95 * t), 1750 - 260 * u + 14 * abs(step)
    w, h = 1080 / z / 1.5 * 1.5, 1920 / z / 1.5 * 1.5
    box = (cx - w / 2 * 1.5, cy - h / 2 * 1.5, cx + w / 2 * 1.5, cy + h / 2 * 1.5)
    W, H = B.W * B.SS, B.H * B.SS
    im = plate.transform((W, H), Image.EXTENT, box, Image.BILINEAR).rotate(roll, Image.BILINEAR, expand=False,
                                                                           fillcolor=SKY + (255,))
    return degrade(im, t)


def degrade(im, t):
    """The cheap hidden camera: soft and low in detail, washed out with a pink-grey cast, grain, a dark smudge."""
    W, H = im.size
    small = im.convert('RGB').resize((W // 5, H // 5), Image.BILINEAR).filter(ImageFilter.GaussianBlur(0.8))
    a = np.asarray(small, np.float32)
    g = a.mean(axis=2, keepdims=True)
    a = g + (a - g) * 0.6                                  # washed out
    a = a * 0.86 + np.array([30, 18, 22]) * 1.0            # lifted blacks, a pink-grey cast
    rng = np.random.default_rng(int(t * 120))
    a += rng.normal(0, 6, a.shape[:2])[..., None]          # grain
    hh, ww = a.shape[:2]
    yy, xx = np.mgrid[0:hh, 0:ww]
    blob = np.exp(-(((xx - 0.02 * ww) / (0.32 * ww)) ** 2 + ((yy - 0.98 * hh) / (0.22 * hh)) ** 2))
    a = a * (1 - 0.85 * blob[..., None]) + np.array([24, 20, 22]) * 0.85 * blob[..., None]   # her jacket's edge
    vig = 1 - 0.35 * (((xx - ww / 2) / (ww / 2)) ** 2 + ((yy - hh / 2) / (hh / 2)) ** 2) / 2
    a *= vig[..., None]
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    return out.convert('RGBA')


def rec_overlay(img, t):
    S = B.SS
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 40 * S)
    x, y = 80 * S, 560 * S
    if int(t * 2) % 2 == 0:                                # the dot blinks once a second
        d.ellipse([x, y, x + 34 * S, y + 34 * S], fill=(230, 30, 36))
    d.text((x + 50 * S, y + 17 * S), 'REC', font=f, fill=(250, 250, 250), anchor='lm', stroke_width=2 * S,
           stroke_fill=(30, 30, 30))
    secs = 41 * 60 + 7 + int(t)
    f2 = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans.ttf'), 32 * S)
    d.text((x, y + 70 * S), f'18/10/2026  09:{secs // 60 % 60:02d}:{secs % 60:02d}', font=f2, fill=(250, 250, 250),
           stroke_width=2 * S, stroke_fill=(30, 30, 30))


# --------------------------------------------------------------------------------------------- the office
CEIL, WALL, CARPET = (222, 224, 224), (236, 236, 232), (112, 116, 124)
DESK, MONITOR, CHAIR, SCREEN = (244, 244, 240), (26, 28, 32), (34, 34, 38), (52, 84, 186)


def poly(d, pts, fill, k, outline=INK, w=2):
    d.polygon([(x * k, y * k) for x, y in pts], fill=fill, outline=outline, width=max(1, int(w * k)))


def office(img, cam3, lit=True):
    """The open-plan office (refs office-1..8): we look straight down the long middle of the floor to a wall of
    windows; long white desk rows on both sides with black monitors, chairs and blue padded divider screens; a
    ceiling grid of panel and strip lights; grey carpet; plants; a green sofa; glass meeting rooms at the far
    right; the two ring lights hanging over the dance floor. Flat colour, one outline."""
    k = img.size[0] / 1080
    d = ImageDraw.Draw(img)
    P3 = cam3.pt
    ZF, XW, YC = 15.0, 4.6, 2.8
    # ceiling, walls, far wall, floor
    poly(d, [P3(-XW, 1.0, YC), P3(XW, 1.0, YC), P3(XW, ZF, YC), P3(-XW, ZF, YC)], CEIL, k)
    poly(d, [P3(-XW, 1.0, 0), P3(-XW, ZF, 0), P3(-XW, ZF, YC), P3(-XW, 1.0, YC)], WALL, k)
    poly(d, [P3(XW, 1.0, 0), P3(XW, ZF, 0), P3(XW, ZF, YC), P3(XW, 1.0, YC)], WALL, k)
    poly(d, [P3(-XW, 1.0, 0), P3(XW, 1.0, 0), P3(XW, ZF, 0), P3(-XW, ZF, 0)], CARPET, k)
    for z in np.arange(1.5, ZF, 1.2):                      # carpet tiles and ceiling grid
        d.line([tuple(v * k for v in P3(-XW, z, 0)), tuple(v * k for v in P3(XW, z, 0))], fill=(104, 108, 116), width=max(1, int(k)))
        d.line([tuple(v * k for v in P3(-XW, z, YC)), tuple(v * k for v in P3(XW, z, YC))], fill=(204, 206, 206), width=max(1, int(k)))
    for x in np.arange(-XW, XW + 0.1, 1.2):
        d.line([tuple(v * k for v in P3(x, 1.0, YC)), tuple(v * k for v in P3(x, ZF, YC))], fill=(204, 206, 206), width=max(1, int(k)))
    for z in np.arange(2.0, ZF - 0.5, 2.4):                # panel lights and strips
        for x in (-2.4, 2.4):
            poly(d, [P3(x - 0.5, z, YC), P3(x + 0.5, z, YC), P3(x + 0.5, z + 1.2, YC), P3(x - 0.5, z + 1.2, YC)],
                 (252, 252, 246) if lit else (190, 192, 196), k, None)
    for x in (-0.8, 0.8):
        d.line([tuple(v * k for v in P3(x, 1.5, YC)), tuple(v * k for v in P3(x, ZF - 1, YC))],
               fill=(252, 252, 246) if lit else (190, 192, 196), width=max(2, int(5 * k)))
    # the far wall: floor-to-ceiling windows on the city
    fl, fr = P3(-XW, ZF, 0), P3(XW, ZF, YC)
    poly(d, [P3(-XW, ZF, 0), P3(XW, ZF, 0), P3(XW, ZF, YC), P3(-XW, ZF, YC)], (190, 214, 232), k)
    rng = np.random.default_rng(2)
    x = fl[0]
    while x < fr[0]:                                        # a flat skyline
        w = rng.uniform(14, 40)
        h = rng.uniform(20, 70)
        d.rectangle([x * k, (fl[1] - h) * k, (x + w) * k, fl[1] * k], fill=(150, 170, 190))
        x += w + rng.uniform(0, 8)
    for xx in np.linspace(-XW, XW, 9):
        d.line([tuple(v * k for v in P3(xx, ZF, 0)), tuple(v * k for v in P3(xx, ZF, YC))], fill=(60, 64, 70), width=max(2, int(4 * k)))
    # glass meeting rooms down the far right, a door and EXIT sign on the left wall
    for z0 in (10.0, 12.4):
        poly(d, [P3(XW - 1.6, z0, 0), P3(XW - 1.6, z0 + 2.0, 0), P3(XW - 1.6, z0 + 2.0, YC), P3(XW - 1.6, z0, YC)],
             (200, 220, 230), k)
    poly(d, [P3(-XW, 11.0, 0), P3(-XW, 12.0, 0), P3(-XW, 12.0, 2.1), P3(-XW, 11.0, 2.1)], (196, 196, 190), k)
    poly(d, [P3(-XW, 11.2, 2.25), P3(-XW, 11.8, 2.25), P3(-XW, 11.8, 2.45), P3(-XW, 11.2, 2.45)], (40, 160, 80), k)
    # the desk rows, far to near, both sides
    for z0 in np.arange(13.0, 1.4, -2.6):
        for side in (-1, 1):
            if side < 0 and 8.6 < z0 < 10.5:
                sofa(d, P3, k, -3.2, z0 + 0.4)
                continue
            desk_block(d, P3, k, side, z0)
    for X, Z in ((-4.2, 13.8), (4.0, 9.4), (-4.1, 6.0), (4.2, 3.4)):     # plants
        plant(d, P3, k, X, Z)
    ring_lights(img, cam3, None)


def desk_block(d, P3, k, side, z0):
    """Two facing desks with a blue padded divider between, monitors and chairs, at depth z0."""
    x0, x1 = (1.7, 4.2) if side > 0 else (-4.2, -1.7)
    zz = (z0, z0 + 1.6)
    top = 0.74
    for z in (zz[1], zz[0]):                                # chairs at the aisle end
        cx = x0 - 0.0 if side > 0 else x1
        poly(d, [P3(cx - 0.25 * side, z + 0.3, 0.45), P3(cx + 0.2 * side, z + 0.3, 0.45),
                 P3(cx + 0.2 * side, z + 0.3, 1.0), P3(cx - 0.25 * side, z + 0.3, 1.0)], CHAIR, k)
    poly(d, [P3(x0, zz[0], top), P3(x1, zz[0], top), P3(x1, zz[1], top), P3(x0, zz[1], top)], DESK, k)
    poly(d, [P3(x0, zz[0], top - 0.05), P3(x1, zz[0], top - 0.05), P3(x1, zz[0], top), P3(x0, zz[0], top)], (210, 210, 206), k)
    for x in (x0 + 0.05, x1 - 0.05):
        d.line([tuple(v * k for v in P3(x, zz[0], 0)), tuple(v * k for v in P3(x, zz[0], top))], fill=(150, 150, 150), width=max(2, int(4 * k)))
    zm = (zz[0] + zz[1]) / 2                                # the divider screen (rounded-topped, blue)
    poly(d, [P3(x0, zm, top), P3(x1, zm, top), P3(x1, zm, top + 0.42), P3(x0, zm, top + 0.42)], SCREEN, k)
    for i in range(2):                                      # monitors facing the aisle-side seats
        xm = x0 + (x1 - x0) * (0.3 + 0.4 * i)
        poly(d, [P3(xm - 0.28, zm - 0.12, top + 0.12), P3(xm + 0.28, zm - 0.12, top + 0.12),
                 P3(xm + 0.28, zm - 0.12, top + 0.5), P3(xm - 0.28, zm - 0.12, top + 0.5)], MONITOR, k)
        cup = P3(xm + 0.4, zz[0] + 0.2, top)
        d.rectangle([cup[0] * k - 4 * k, cup[1] * k - 14 * k, cup[0] * k + 4 * k, cup[1] * k], fill=(250, 250, 250),
                    outline=INK)


def sofa(d, P3, k, X, Z):
    poly(d, [P3(X - 0.9, Z, 0.42), P3(X + 0.9, Z, 0.42), P3(X + 0.9, Z + 0.8, 0.42), P3(X - 0.9, Z + 0.8, 0.42)], (110, 130, 84), k)
    poly(d, [P3(X - 0.9, Z + 0.8, 0.42), P3(X + 0.9, Z + 0.8, 0.42), P3(X + 0.9, Z + 0.8, 0.85), P3(X - 0.9, Z + 0.8, 0.85)], (96, 116, 72), k)
    poly(d, [P3(X - 0.9, Z, 0.0), P3(X + 0.9, Z, 0.0), P3(X + 0.9, Z, 0.42), P3(X - 0.9, Z, 0.42)], (96, 116, 72), k)
    for i in (-0.5, 0.4):
        poly(d, [P3(X + i, Z + 0.7, 0.45), P3(X + i + 0.35, Z + 0.7, 0.45), P3(X + i + 0.35, Z + 0.7, 0.75),
                 P3(X + i, Z + 0.7, 0.75)], (170, 90, 60), k)


def plant(d, P3, k, X, Z):
    poly(d, [P3(X - 0.2, Z, 0), P3(X + 0.2, Z, 0), P3(X + 0.17, Z, 0.4), P3(X - 0.17, Z, 0.4)], (240, 240, 236), k)
    cx, cy = P3(X, Z, 0.9)
    r = 0.45 * 1400 / Z
    for i in range(7):
        a = i / 7 * math.pi * 2
        d.ellipse([(cx + math.cos(a) * r * 0.5 - r * 0.45) * k, (cy + math.sin(a) * r * 0.5 - r * 0.45) * k,
                   (cx + math.cos(a) * r * 0.5 + r * 0.45) * k, (cy + math.sin(a) * r * 0.5 + r * 0.45) * k],
                  fill=(70, 130, 70) if i % 2 else (90, 150, 80), outline=INK)


def ring_lights(img, cam3, m):
    """Two big round ring lights hanging over the dance floor (ref office-3): white when the office is lit; during
    the dance they glow in the wash colours and pulse on the beat (Claude's addition, Sam OK'd 18 Oct)."""
    k = img.size[0] / 1080
    d = ImageDraw.Draw(img)
    for i, Z in enumerate((3.6, 6.0)):
        cx, cy = cam3.pt(0.0, Z, 2.6)
        rx, ry = 0.75 * cam3.foc / Z, 0.1 * cam3.foc / Z
        top = cam3.pt(0.0, Z, 2.8)
        d.line([(cx * k, top[1] * k), (cx * k, (cy - ry) * k)], fill=(60, 60, 64), width=max(1, int(2 * k)))
        if m is None:
            col = (250, 250, 244)
        else:
            col = WASH[(i + int(m / BEAT)) % len(WASH)]
            if (m % BEAT) / BEAT < 0.2:
                col = tuple(min(255, c + 80) for c in col)
        w = max(3, int(10 * k * 5 / Z))
        d.ellipse([(cx - rx) * k, (cy - ry) * k, (cx + rx) * k, (cy + ry) * k], outline=INK, width=w + 4)
        d.ellipse([(cx - rx) * k, (cy - ry) * k, (cx + rx) * k, (cy + ry) * k], outline=col, width=w)


_ROOM = {}


def room(cam3, lit=True):
    """The office drawn once per camera (it never changes) and reused."""
    key = (cam3.foc, cam3.horizon, lit, B.SS)
    if key not in _ROOM:
        img = B.canvas(WALL)
        office(img, cam3, lit)
        _ROOM[key] = img
    return _ROOM[key].copy()


def dance_frame(t, cam3=DANCE_CAM):
    """Shots 2 and 4: the four of them on the dance floor; the pop lights until the swipe."""
    img = room(cam3)
    on = music_on(t)
    if on:
        pop_lights(img, t, cam3)
        ring_lights(img, cam3, song_clock(t))
    people = []
    for who in DANCERS:
        X, Z = SPOT[who]
        step = None
        if who == 'farage':
            k = farage_dance_state(t)
        elif who == 'jenrick':
            if t >= TRIP:
                X, Z, k, _ = trip_state(t)
                step = k.get('step')
            else:
                k = dance_pose(t - SLAM)
        else:
            k = other_dance_state(who, t)
        people.append((Z, who, X, k, step))
    for Z, who, X, k, step in sorted(people, key=lambda q: -q[0]):
        make_person(img, cam3, who, X, Z, k, t, step=step)
    if on:                                                  # the coloured light falls over the dancers too
        tint = Image.new('RGBA', img.size, wash_colour(song_clock(t)) + (22,))
        img.alpha_composite(tint)
        if (song_clock(t) % BEAT) / BEAT < 0.12:
            img.alpha_composite(Image.new('RGBA', img.size, (255, 255, 255, 70)))
    return img


# --------------------------------------------------------------------------------------------- shot 3: the doorway
DOOR_BLINKS = (DOOR[0] + 0.55, DOOR[0] + 1.35)


def door_frame(t):
    """Shot 3: the journalist standing in a side doorway of the same office, the pop lights flickering over her;
    South Park shock (Sam, 18 Oct); two slow, disbelieving blinks. The music carries on."""
    img = B.canvas((70, 74, 84))
    k = img.size[0] / 1080
    d = ImageDraw.Draw(img)
    poly(d, [(0, 0), (1080, 0), (1080, 1920), (0, 1920)], WALL, k)
    poly(d, [(250, 240), (830, 240), (830, 1920), (250, 1920)], (236, 236, 232), k)           # the frame
    poly(d, [(290, 280), (790, 280), (790, 1920), (290, 1920)], (150, 156, 164), k)            # the corridor
    poly(d, [(290, 1500), (790, 1500), (790, 1920), (290, 1920)], (120, 124, 130), k)
    poly(d, [(560, 520), (760, 520), (760, 1500), (560, 1500)], (190, 196, 200), k)             # the lift doors
    d.line([(660 * k, 520 * k), (660 * k, 1500 * k)], fill=INK, width=max(1, int(2 * k)))
    poly(d, [(480, 120), (600, 120), (600, 180), (480, 180)], (40, 160, 80), k)                 # EXIT sign
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), int(34 * k))
    d.text((540 * k, 150 * k), 'EXIT', font=f, fill=(250, 250, 250), anchor='mm')
    sp = dict(C.JOURNALIST, mood='wtf', look=-0.1)
    u = t - DOOR[0]
    sp['blink'] = any(b <= t < b + 0.42 for b in DOOR_BLINKS)                                 # slow blinks
    sp['gape'] = 0.8 + 0.2 * ease(u / 0.6)
    j = V.standing(sp)
    V.person(img, B.Cam(1.0, 540, 960), 540, 640, 1.18, sp, t, 0, j)
    m = song_clock(t)                                       # the pop lights spill over her from the room
    img.alpha_composite(Image.new('RGBA', img.size, wash_colour(m) + (40,)))
    if (m % BEAT) / BEAT < 0.12:
        img.alpha_composite(Image.new('RGBA', img.size, (255, 255, 255, 90)))
    return img


# --------------------------------------------------------------------------------------------- shots 5 and 6: the outburst
JAB = [3.6, 4.4, 5.2, 6.7, 8.2]                             # file seconds of his stressed words: a finger jab on each


def farage_shout_state(t):
    m = mouths.at(FAR_TRACK, t)
    talking_now = m != 'rest'
    jab = max((math.exp(-((t - (j + FAR_OFF)) / 0.12) ** 2) for j in JAB), default=0.0)
    k = P((-260 - 40 * jab, 40 - 30 * jab, 200 + 40 * jab), (176, 420, 60), 'down', 'back', mood='fury', look=-1.0,
          head=-8, lean=4 + 4 * jab)
    extra = dict(mood='fury', strength=1.4, red=1.0, look=-1.0, turn=-0.3)
    if talking_now:
        extra['mouth'] = 'v:' + m
    return k, extra


def spit(img, cam, x, y, s, t):
    """Spit flying from his mouth on the loudest words (Claude's addition): small drops thrown towards Jenrick,
    falling under gravity, gone after half a second."""
    k = img.size[0] / 1080
    d = ImageDraw.Draw(img)
    for j in JAB:
        u = t - (j + FAR_OFF)
        if 0 <= u < 0.5:
            rng = np.random.default_rng(int(j * 100))
            for _ in range(7):
                vx, vy = -rng.uniform(260, 520), -rng.uniform(40, 200)
                px = x + (-10 + vx * u) * s * cam.z
                py = y + (-80 + vy * u + 900 * u * u) * s * cam.z
                r = rng.uniform(2.0, 4.0) * s * cam.z * 1.6
                d.ellipse([(px - r) * k, (py - r) * k, (px + r) * k, (py + r) * k], fill=(236, 244, 250), outline=INK)


def farage_close_frame(t):
    """Shot 5: close on Farage, screaming at Jenrick (off to our left); office lights back to normal."""
    cam3 = DANCE_CAM
    img = room(cam3)
    X, Z = SPOT['farage']
    k, extra = farage_shout_state(t)
    big = Image.new('RGBA', img.size, (0, 0, 0, 0))
    big.alpha_composite(img)
    x, y, s = cam3.person(X, Z)
    z = 2.3
    cam = B.Cam(z, x, y - 120 * s)
    bg = img.transform(img.size, Image.EXTENT, ((x - 540 / z) * B.SS, (y - 120 * s - 960 / z) * B.SS,
                                                (x + 540 / z) * B.SS, (y - 120 * s + 960 / z) * B.SS), Image.BILINEAR)
    sp = dict(C.FARAGE)
    j = build(sp, k)
    face_of(sp, k)
    sp.update(extra)
    sp['blink'] = F.blinking(t, BLINKS['farage'])
    V.person(bg, cam, x, y, s, sp, t, 0, j)
    spit(bg, cam, 540 + 0, 960 + (y - (y - 120 * s)) * 0 - (120 * s - 0) * z * 0, s, t) if False else None
    hx, hy = cam.P(x, y - 150 * s + 60 * s)
    spit_at(bg, hx / B.SS, hy / B.SS, s * z, t)
    return bg


def spit_at(img, mx, my, sc, t):
    k = img.size[0] / 1080
    d = ImageDraw.Draw(img)
    for j in JAB:
        u = t - (j + FAR_OFF)
        if 0 <= u < 0.5:
            rng = np.random.default_rng(int(j * 100))
            for _ in range(7):
                vx, vy = -rng.uniform(260, 520), -rng.uniform(40, 200)
                px = mx + (vx * u) * sc
                py = my + (vy * u + 900 * u * u) * sc
                r = rng.uniform(2.0, 4.0) * sc
                d.ellipse([(px - r) * k, (py - r) * k, (px + r) * k, (py + r) * k], fill=(236, 244, 250), outline=INK)


REACT = {'jenrick': ((-1.3, 3.1), P((-150, 440, 90), (150, 440, 90), 'back', 'back', lean=8, dip=10, mood='scared',
                                         chin=0.3, look=1.0)),
         'tice': ((-1.3, 4.4), P((-190, 420, 50), (190, 420, 50), 'back', 'back', lean=-5, mood='alarm', look=0.7)),
         'braverman': ((0.75, 3.7), P((-176, 420, 60), (-30, 120, 120), 'back', 'down', mood='upset', look=-0.9))}


def wide_frame(t):
    """Shot 6: everyone, wider: Farage finishing his rant at Jenrick; Jenrick scared and miserable at the edge of
    the floor; Tice mildly alarmed, leaning back; Braverman shocked and upset, hand to her chest."""
    cam3 = WIDE_CAM
    img = room(cam3)
    people = []
    for who in DANCERS:
        if who == 'farage':
            k, extra = farage_shout_state(t)
            (X, Z) = SPOT['farage']
        else:
            (X, Z), k = REACT[who]
            extra = {}
        people.append((Z, who, X, k, extra))
    for Z, who, X, k, extra in sorted(people, key=lambda q: -q[0]):
        x, y, s = make_person(img, cam3, who, X, Z, k, t, extra=extra)
        if who == 'farage':
            spit_at(img, x, y - 150 * s + 60 * s, s, t)
    return img


# --------------------------------------------------------------------------------------------- the film
def shot_of(t):
    return next((s[0] for s in SHOTS if s[1] <= t < s[2]), SHOTS[-1][0])


def picture(t):
    if t >= BLACK_AT:
        return B.canvas((0, 0, 0))
    s = shot_of(t)
    if s == 'lapel':
        return lapel_frame(t)
    if s in ('dance', 'dance2'):
        return dance_frame(t)
    if s == 'door':
        return door_frame(t)
    if s == 'farage':
        return farage_close_frame(t)
    return wide_frame(t)


def overlay(img, t):
    if t < BLACK_AT:
        if shot_of(t) == 'lapel':
            rec_overlay(img, t)
        c = caption_at(t)
        if c:
            PP.caption(img, c)
    return img


def frame_image(t):
    return overlay(picture(t), t)


def stills_sheet(out, times, w=360):
    B.SS = 1
    h = w * 16 // 9
    sheet = Image.new('RGB', (w * len(times), h + 40), (20, 20, 20))
    for i, t in enumerate(times):
        im = frame_image(t).convert('RGB').resize((w, h), Image.LANCZOS)
        sheet.paste(im, (w * i, 40))
        label(sheet, w * i + 10, 4, f'{t:.1f}s {shot_of(t)}', 24)
    sheet.save(out, quality=86)


# --------------------------------------------------------------------------------------------- cast sheet
def label(img, x, y, txt, size=30):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), size)
    d.text((x, y), txt, font=f, fill=(250, 250, 250), stroke_width=3, stroke_fill=(20, 20, 20))


def panel(draw, w=400, h=700, z=1.0, cy=960, bg=(226, 222, 216)):
    img = B.canvas(bg)
    cam = B.Cam(z, 540, cy)
    draw(img, cam)
    hh = int(h * 1080 / w)
    return img.convert('RGB').crop((0, 960 - hh // 2, 1080, 960 + hh // 2)).resize((w, h), Image.LANCZOS)


def dancer(img, cam, who, key, x=540, y=760, s=0.62, extra=None):
    sp = dict(C.CAST[who])
    k = KEYS[key] if isinstance(key, str) else key
    j = build(sp, k)
    face_of(sp, k)
    sp.update(extra or {})
    V.person(img, cam, x + j['_sway'] * s, y, s, sp, 0.0, 0, j)


def cast_sheet(out):
    """Row 1: the four dancers and the journalist, standing. Row 2: the dance's key poses (on Farage). Row 3: the
    outburst faces close (Farage's fury at strengths 1-4 for Sam to pick; Jenrick scared; Tice alarmed; Braverman
    upset); the journalist's 'what am I looking at'."""
    B.SS = 1
    W1 = 400
    sheet = Image.new('RGB', (W1 * 5, 700 * 2 + 520 * 2), (30, 26, 24))
    for i, who in enumerate(('tice', 'jenrick', 'farage', 'braverman', 'journalist')):
        def d(im, cam, who=who):
            sp = dict(C.CAST[who], mood='neutral')
            j = V.standing(sp)
            V.person(im, cam, 540, 640, 0.9, sp, 0.0, 0, j)
        sheet.paste(panel(d), (W1 * i, 0))
        label(sheet, W1 * i + 12, 10, who.title())
    keys = ['thumb_R', 'flick', 'lean_dn', 'chin_R', 'sway_L', 'point', 'chin_hand', 'thumb_L', 'sway_R', 'chin_hand2']
    for i, key in enumerate(keys[:5]):
        sheet.paste(panel(lambda im, cam, key=key: dancer(im, cam, 'farage', key, y=640, s=0.9)), (W1 * i, 700))
        label(sheet, W1 * i + 12, 710, f'dance: {key}', 26)
    faces = [('farage', dict(mood='fury', strength=0.5, red=0.3, look=-0.8), 'Farage fury 1'),
             ('farage', dict(mood='fury', strength=1.0, red=0.7, look=-0.8), 'Farage fury 2'),
             ('farage', dict(mood='fury', strength=1.4, red=1.0, look=-0.8, mouth='v:AI'), 'Farage fury 3 (shouting)'),
             ('farage', dict(mood='contempt', look=-0.9), 'Farage contempt (sees trip)'),
             ('journalist', dict(mood='wtf'), 'Journalist: what?!'),
             ('jenrick', dict(mood='scared', look=0.7, gaze_dy=-2), 'Jenrick scared'),
             ('tice', dict(mood='alarm', look=0.4), 'Tice mildly alarmed'),
             ('braverman', dict(mood='upset', look=-0.5), 'Braverman shocked, upset'),
             ('jenrick', dict(mood='grin'), 'Jenrick dancing'),
             ('braverman', dict(mood='cool'), 'Braverman dancing')]
    for i, (who, ex, name) in enumerate(faces):
        def d(im, cam, who=who, ex=ex):
            sp = dict(C.CAST[who], **ex)
            V.person(im, cam, 540, 1100, 1.0, sp, 0.0, 0, V.standing(sp))
        r, c = divmod(i, 5)
        sheet.paste(panel(d, w=W1, h=520, z=2.2, cy=1020), (W1 * c, 1400 + 520 * r))
        label(sheet, W1 * c + 12, 1410 + 520 * r, name, 24)
    sheet.save(out, quality=88)


def main():
    a = sys.argv[1:]
    if a[0] == 'cast':
        cast_sheet(a[1])
    elif a[0] == 'music':
        build_music()
    elif a[0] == 'stills':
        B.SS = 1
        os.makedirs(a[1], exist_ok=True)
        for x in a[2:]:
            frame_image(float(x)).convert('RGB').save(os.path.join(a[1], f't{x}.jpg'), quality=88)
    elif a[0] == 'sheet':
        stills_sheet(a[1], [float(x) for x in a[2:]])
    elif a[0] == 'final':
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else ())


if __name__ == '__main__':
    main()
