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
SONG_SHIFT = 3.037               # the routine's first planned beat, now that the song starts on "'Cos I'm so messy"
DOOR = (13.0, 15.0)              # the cutaway to the journalist (Sam: hold the first dance two seconds longer)
TRIP = 17.0                      # Jenrick's foot catches: a two-second trip over his own feet (Sam, 18 Oct: one more second)
TRIP_LEN = 2.05                  # from the catch to the crash
CRASH = TRIP + TRIP_LEN          # ... he crashes into the desk at the front left
SWIPE = CRASH + 0.7              # Farage's swipe lands: the music and the strobes stop dead
FARAGE_AT = SWIPE + 0.4          # film time where Farage's first word starts
LINES = [
    dict(n=1, who='narrator', audio='shocking-1', start=2.8, at=0.4,
         text="ITV sent an undercover journalist into Reform UK's HQ, where she observed shocking behaviour."),
    dict(n=2, who='farage', audio='shocking-2', start=2.48, at=FARAGE_AT,
         text="Damn it Jenrick, if you can't stay in formation I swear to [bleep] I'll have your [bleep] ass deported."),
]
# in Farage's file seconds: Sam's first gap holds two words, so two bleeps with a short break between (Sam, 18 Oct)
BLEEPS = [(5.57, 6.04), (6.10, 6.60), (7.32, 7.99)]
DUR = BLACK_AT = round(FARAGE_AT + (8.96 - 2.48) + 1.1, 2)
# All the action after the doorway plays in the one wide shot (Sam, 18 Oct: no close-up cut to Farage).
SHOTS = [('lapel', 0.0, SLAM), ('dance', SLAM, DOOR[0]), ('door', DOOR[0], DOOR[1]), ('dance2', DOOR[1], DUR)]
# The formation (Sam, 18 Oct), as seen on screen: Farage front centre, Jenrick middle left, Braverman middle right,
# Tice back left (set a little further out than Jenrick so his face is never hidden). Floor positions in metres:
# X across (+ right), Z away from the camera (the camera brought forward towards them: Sam, 18 Oct).
SPOT = {'farage': (0.0, 2.75), 'jenrick': (-0.68, 3.35), 'braverman': (0.68, 3.35), 'tice': (-1.18, 4.0)}
DANCERS = ('tice', 'jenrick', 'braverman', 'farage')     # far to near (drawing order)
CRASH_DESK = (-2.1, -0.62, 1.55, 2.3)                    # x0, x1, z0, z1 of the desk Jenrick crashes into
# (its right end kept left of where he dances, so his feet, and the trip over them, stay in view: Sam, 18 Oct)
JENRICK_END = (-0.58, 2.43)          # where he hits the desk: its right-hand corner (he stays in shot), his hips right
# against its back edge (Sam, 18 Oct: he stopped just short of it)
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
def P(L, R, poleL='out', poleR='out', sway=0.0, dip=0.0, lean=0.0, head=0.0, chin=0.0, mood='grin', look=0.0, roll=0.0):
    pv = lambda q: V.POLES[q] if isinstance(q, str) else q
    return dict(L=L, R=R, poleL=pv(poleL), poleR=pv(poleR), sway=sway, dip=dip, lean=lean, head=head, chin=chin,
                mood=mood, look=look, roll=roll)


LOOSE_L, LOOSE_R = (-176, 400, 70), (176, 400, 70)
KEYS = {   # from the trend's original dance (Sam's clip, the woman on the right), made bigger: the whole body moves,
    # wide sways, deep dips, arms flung wider and higher (Sam, 18 Oct: more exaggerated, take up more space)
    'thumb_R': P((-230, 330, 90), (270, -90, -50), 'back', 'out', sway=-52, dip=24, head=12, lean=6),   # thumb jerked back
    'thumb_L': P((-270, -90, -50), (230, 330, 90), 'out', 'back', sway=52, dip=24, head=-12, lean=6),   # over the shoulder
    'flick': P((-320, 400, 40), (320, 400, 40), 'back', 'back', dip=46, lean=10),            # both hands flicked down, out
    'lean_up': P((-210, 430, 170), (210, 430, 170), 'back', 'back', dip=12, lean=22, chin=0.25),   # leaning right in
    'lean_dn': P((-230, 470, 180), (230, 470, 180), 'back', 'back', dip=38, lean=26, chin=0.35),   # bobbing, hunched
    'chin_R': P((-170, 320, 90), (390, 160, 60), 'out', 'down', sway=-42, dip=8, lean=-8, chin=-0.8, mood='cool'),
    'chin_L': P((-390, 160, 60), (170, 320, 90), 'down', 'out', sway=42, dip=8, lean=-8, chin=-0.8, mood='cool'),
    'sway_L': P((-290, 310, 70), (210, 360, 110), 'back', 'back', sway=-58, dip=20, head=-12),
    'sway_R': P((-210, 360, 110), (290, 310, 70), 'back', 'back', sway=58, dip=20, head=12),
    'point': P((-230, 380, 80), (60, 110, 330), 'back', 'down', sway=-32, dip=16, lean=10, head=8),    # pointing at us
    'point2': P((-230, 380, 80), (120, 170, 310), 'back', 'down', sway=-8, dip=34, lean=16, head=4),
    'chin_hand': P((-280, 360, 60), (50, -70, 150), 'back', 'down', sway=36, dip=10, head=12, chin=0.1, mood='cool'),
    'chin_hand2': P((-300, 330, 60), (90, -40, 140), 'back', 'down', sway=54, dip=26, head=12, chin=0.15, mood='cool'),
}
# The routine on the song's clock (m: seconds since the slam cut), on its beats. Sam's clip mapped onto our song bed:
# m 0-2.7 = her clip 2.76-5.45 s (thumbs back, the flick, leaning in); m 2.7- = clip two from 0.25 s (chin up with
# the arm swept out, swaying, pointing at the camera, the hand by the chin).
b = BEAT
_ROUTINE = [(0.0, 'thumb_R'), (b, 'thumb_L'), (2 * b, 'thumb_R'), (2.6 * b, 'flick'), (3.1 * b, 'lean_up'),
           (3.6 * b, 'lean_dn'), (4.1 * b, 'lean_up'), (4.6 * b, 'lean_dn'), (5.0 * b, 'chin_R'),
           (6.0 * b, 'chin_L'), (7.0 * b, 'sway_L'), (8 * b, 'sway_R'), (9 * b, 'sway_L'), (10 * b, 'sway_R'),
           (11 * b, 'sway_L'), (12 * b, 'sway_R'), (13 * b, 'point'), (13.5 * b, 'point2'), (14 * b, 'point'),
           (14.5 * b, 'point2'), (15 * b, 'chin_hand'), (15.5 * b, 'chin_hand2'), (16 * b, 'chin_hand'),
           (16.5 * b, 'chin_hand2'), (17 * b, 'chin_hand'), (17.5 * b, 'chin_hand2'), (18 * b, 'chin_hand'),
           (18.5 * b, 'chin_hand2'), (19 * b, 'chin_hand')]
# The song now starts on "'Cos I'm so messy" (Sam, 18 Oct), 3.04 s earlier in the song: an opening on its first
# beats (a sway, the thumbs, chin up), then the routine as before, moved along.
ROUTINE = ([(0.0, 'sway_R'), (0.347, 'thumb_R'), (0.885, 'thumb_L'), (1.423, 'chin_R'), (1.961, 'chin_L'),
            (2.499, 'sway_L')] + [(m + SONG_SHIFT, key) for m, key in _ROUTINE])


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


# Their faces change together every two beats through happy, groovy expressions (Sam, 18 Oct: more variety, still
# in sync). Faces snap (eyes and jokes snap); the body keeps flowing.
FACES = ['grin', 'sing', 'pout', 'grin', 'bliss', 'smug', 'sing', 'grin', 'pout', 'bliss', 'smug', 'sing']


def face_at(m):
    return FACES[int(max(0.0, m) / (2 * BEAT)) % len(FACES)]


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
    k['mood'] = face_at(m)
    return k


def build(sp, k):
    """Joints for a key pose. The sway moves the WHOLE upper body across as one piece (head, neck, jacket and arms
    together, so the neck never comes away: Sam, 18 Oct): the caller shifts the person by j['_sway']. On a big sway
    the foot on that side steps out with it and the other stays planted; the dip bends the knees. A pose may set
    the feet itself (k['feet']: the trip)."""
    j = V.standing(sp)
    sw, dip = k['sway'], k['dip']
    for side, sg in (('L', -1), ('R', 1)):
        x, y, z = j['foot' + side]
        out = max(0.0, sw * sg) * 0.55                    # the leading foot steps out with the sway
        j['foot' + side] = (x - sw + sg * out + (sw * 0.0), y - dip, z)
    for side, ft in (k.get('feet') or {}).items():
        j['foot' + side] = (ft[0] - sw, ft[1] - dip, ft[2])
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
def blend_keys(a, b2, u):
    out = {}
    for k, v in a.items():
        w = b2.get(k, v)                                   # a key only one pose has (the trip's feet) holds
        if isinstance(v, tuple) and isinstance(w, tuple):
            out[k] = tuple(x + (y - x) * u for x, y in zip(v, w))
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            out[k] = v + (w - v) * u
        else:
            out[k] = v if u < 0.5 else w
    return out


STAND = P((-176, 420, 60), (176, 420, 60), 'back', 'back', mood='neutral')
WINDUP = P((-176, 420, 60), (-40, 40, 160), 'back', 'down', mood='contempt', look=-1.0, head=-6)
SWIPED = P((-176, 420, 60), (330, 110, 60), 'back', 'out', mood='contempt', look=-1.0, head=-6)


def farage_dance_state(t):
    """Farage dances until he sees the trip (TRIP + 0.9 s): his head snaps round to our left, contempt; then the
    swipe: wind up across his chest, and the hand cuts out through the air, landing on SWIPE."""
    m = t - SLAM
    see = TRIP + 0.9
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
    react = (P((-200, 420, 50), (200, 420, 50), 'back', 'back', lean=-6, mood='alarm', look=0.6) if who == 'tice' else
             P((-176, 420, 60), (-30, 120, 120), 'back', 'down', mood='upset', look=-0.9))
    k = blend_keys(frozen, react, ease((t - SWIPE - 0.25) / 0.6)) if t > SWIPE + 0.25 else dict(frozen)
    k.update(mood='alarm' if who == 'tice' else 'upset', look=0.6 if who == 'tice' else -0.9)
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


FOOT0 = {'L': (-60.0, V.ANKLE_Y, 6.0), 'R': (60.0, V.ANKLE_Y, 6.0)}      # standing feet (V.standing)


CATCHES = (0.18, 0.62, 1.06, 1.44)    # when Jenrick's feet catch (each one checks him, never stops him)


def trip_progress(u):
    """How far along his way to the desk he is (0-1) at u s into the trip: he is never still once the first catch
    sends him off balance (Sam, 18 Oct: he slowed and steadied himself before the run): the speed surges after each
    catch and sags at the next, while rising all the way to the impact."""
    if u <= 0.18:
        return 0.0
    n = 400
    us = np.linspace(0.18, TRIP_LEN, n)
    v = (0.3 + 1.0 * ((us - 0.18) / (TRIP_LEN - 0.18)) ** 2)
    for c in CATCHES[1:]:
        v = v * (1 - 0.45 * np.exp(-((us - c) / 0.07) ** 2))              # each catch checks him, a little
    d = np.concatenate([[0.0], np.cumsum((v[1:] + v[:-1]) / 2 * np.diff(us))])
    return float(np.interp(u, us, d / d[-1]))


def trip_state(t):
    """Jenrick's trip (Sam, 18 Oct): stumbling trips, and he never finds his balance again before the desk. No deep
    lean (seen from the front it only shrank him); his balance is shown by the feet catching, the knees buckling,
    the arms flung up and out and a side-to-side wobble. 0.18 his left foot catches over his right; 0.62 the right
    over the left, knees buckle; 1.06 he stubs his left toe; 1.44 a near-tangle; then his legs run away with him,
    faster and faster, into the desk (TRIP_LEN); his speed never drops to a stop (trip_progress). Returns (X, Z, key pose)."""
    u = t - TRIP
    X0, Z0 = SPOT['jenrick']
    X1, Z1 = JENRICK_END
    if u < 0:
        return X0, Z0, None
    A = V.ANKLE_Y
    base = dance_pose(TRIP - SLAM)
    catch1 = dict(base, feet={'L': (30, A - 34, 70.0), 'R': (62, A, 6.0)}, lean=6, dip=16, mood='scared', roll=4)
    # the left arm (towards the frame's edge) reaches forward to break the fall; the right one flails UP, never out
    # behind Farage (Sam, 18 Oct: it jumped from behind him to the front in one frame when Jenrick passed him)
    stum1 = P((-180, 140, 300), (150, -210, 140), 'down', 'out', lean=8, dip=22, mood='scared', head=-8, roll=-3)
    catch2 = dict(P((-200, 220, 260), (130, -240, 170), 'down', 'out', lean=6, dip=30, mood='scared', head=8, roll=-5),
                  feet={'L': (-62, A, 6.0), 'R': (-30, A - 34, 70.0)})
    stum2 = P((-170, 60, 300), (170, -160, 150), 'down', 'out', lean=8, dip=18, mood='scared', head=-8, roll=2)
    catch3 = dict(P((-190, 180, 280), (140, -220, 180), 'down', 'out', lean=6, dip=24, mood='scared', roll=2),
                  feet={'L': (-70, A - 60, -60.0), 'R': (60, A, 20.0)})
    # then he never finds his feet again (Sam, 18 Oct: he steadied himself before the run; he must stay unbalanced
    # all the way to the desk): another stumble and a near-tangle, then his legs run away with him, wobbling side
    # to side, faster and faster, straight into the desk
    stum3 = P((-200, 120, 300), (160, -190, 150), 'down', 'out', lean=10, dip=26, mood='scared', head=8, roll=-4)
    catch4 = dict(P((-180, 230, 280), (120, -230, 180), 'down', 'out', lean=8, dip=30, mood='scared', head=-8, roll=4),
                  feet={'L': (10, A - 30, 80.0), 'R': (40, A, -10.0)})
    run1 = P((-170, 200, 300), (150, -200, 160), 'down', 'out', lean=12, dip=14, mood='scared', head=-6, roll=4)
    run2 = P((-190, 20, 260), (60, 240, 300), 'down', 'out', lean=12, dip=10, mood='scared', head=6, roll=-1)
    reach = P((-170, 330, 280), (190, 330, 260), 'down', 'out', lean=10, dip=6, mood='scared', chin=0.3, roll=-1)
    slam = P((-160, 430, 230), (190, 430, 210), 'down', 'out', lean=14, dip=4, mood='scared', chin=0.35)
    slump = P((-165, 440, 240), (200, 440, 220), 'down', 'out', lean=12, dip=6, mood='scared', chin=0.4)
    up = P((-165, 420, 200), (190, 420, 180), 'down', 'out', lean=8, dip=6, mood='scared', chin=0.2, look=1.0)
    hunch = P((-170, 430, 160), (170, 430, 160), 'back', 'back', lean=8, dip=12, mood='scared', chin=0.3, look=1.0)
    T = TRIP_LEN
    keys = [(0.0, base), (0.18, catch1), (0.42, stum1), (0.62, catch2), (0.88, stum2), (1.06, catch3), (1.26, stum3),
            (1.44, catch4), (1.64, run1), (1.82, run2), (1.94, reach), (T, slam), (T + 0.2, slump),
            (T + 0.7, slump), (T + 1.15, up), (T + 1.55, hunch)]
    k = dict(hunch)
    for (a, ka), (b2, kb) in zip(keys, keys[1:]):
        if u < b2:
            w = (u - a) / (b2 - a)
            k = blend_keys(ka, kb, w * w * w if b2 == T else ease(w))     # fast into the impact
            k.pop('feet', None)
            if 'feet' in ka or 'feet' in kb:                              # a caught foot, and back to standing
                fa, fb = ka.get('feet', FOOT0), kb.get('feet', FOOT0)
                k['feet'] = {sd: tuple(x + (y - x) * ease(w) for x, y in zip(fa[sd], fb[sd])) for sd in 'LR'}
            break
    # the catches cover little ground; from 1.06 s he accelerates all the way into the desk (no slowing before it)
    w = trip_progress(u) if u < T else 1.0
    X, Z = X0 + (X1 - X0) * w, Z0 + (Z1 - Z0) * w
    if u < T and 'feet' not in k and u > 0.18:                             # stumbling steps; faster and faster at the end
        k['step'] = (True, int(u / 0.16) % 2) if u < 1.44 else (True, int(1.44 / 0.16 + (u - 1.44) ** 1.3 * 16) % 2)
    if u >= T:                                                             # the jolt of the impact
        k['dip'] = k['dip'] + 10 * math.exp(-((u - T) / 0.06) ** 2)
    return X, Z, k


# The things on the desk he crashes into (Sam, 18 Oct: knocking stuff over): flung on the impact, falling under
# gravity, each its own size and speed; the papers flutter; everything stays where it lands.
ITEMS = [   # kind, X, Z on the desk top, launch velocity (m/s: across, up, away from us +), delay (s). He hits the
    # desk from behind, so everything is flung TOWARDS us (Sam, 18 Oct: pens had landed behind him and were drawn on
    # his legs): the mug, pot, plant and two pens fly out of the bottom of the shot; the papers flutter down and a
    # pen skids onto the carpet in front of him, to the right of the desk, never under it or behind anyone.
    ('mug', -0.92, 1.95, (0.6, 1.4, -1.2), 0.00),
    ('pot', -1.22, 2.05, (0.3, 1.8, -1.1), 0.03),
    ('plant', -1.6, 1.8, (0.2, 1.1, -0.9), 0.06),
    ('paper', -1.0, 1.75, (0.65, 2.0, 0.45), 0.00), ('paper', -1.1, 1.8, (0.6, 2.4, -0.6), 0.02),
    ('paper', -0.95, 1.85, (0.75, 1.8, 0.3), 0.04), ('paper', -1.2, 1.7, (0.2, 2.6, -0.6), 0.05),
    ('pen', -1.15, 2.0, (1.6, 1.6, 0.2), 0.03), ('pen', -1.2, 2.05, (0.9, 1.6, -1.4), 0.04),
    ('pen', -1.17, 2.02, (-0.2, 2.0, -1.5), 0.05)]
DESK_TOP = 0.74
DESK_DX = 0.0                    # (the desk stays where Sam liked it: 18 Oct)


def item_at(i, t):
    """Where item i is at time t: (X, Y, Z, angle, landed)."""
    kind, X, Z, (vx, vy, vz), delay = ITEMS[i]
    X += DESK_DX
    u = t - CRASH - delay
    if u <= 0:
        return X, DESK_TOP, Z, 0.0, False
    g = 2.2 if kind == 'paper' else 9.8                   # paper drifts down
    if kind == 'paper':
        vy *= 0.6
    land = (vy + math.sqrt(vy * vy + 2 * g * DESK_TOP)) / g   # when it reaches the floor
    uu = min(u, land)
    Xn = X + vx * uu + (0.12 * math.sin(uu * 7 + i) if kind == 'paper' else 0.0)
    Yn = DESK_TOP + vy * uu - 0.5 * g * uu * uu
    Zn = Z + vz * uu
    spin = (3 + i) * uu if kind != 'paper' else 1.4 * math.sin(uu * 5 + i)
    if u >= land:
        spin = (math.pi / 2 if kind in ('mug', 'pot') else spin)   # the mug and pot lie on their sides
    return Xn, max(0.0, Yn), Zn, spin, u >= land


def draw_item(img, cam3, i, t):
    kind = ITEMS[i][0]
    X, Y, Z, ang, landed = item_at(i, t)
    k = img.size[0] / 1080
    x, y = cam3.pt(X, Z, Y)
    sc = cam3.foc / Z * k
    d = ImageDraw.Draw(img)

    def rot(pts):
        c, s_ = math.cos(ang), math.sin(ang)
        return [(x * k + (px * c - py * s_) * sc, y * k + (px * s_ + py * c) * sc) for px, py in pts]
    if kind == 'mug':
        d.polygon(rot([(-0.045, 0), (0.045, 0), (0.045, -0.1), (-0.045, -0.1)]), fill=(250, 250, 250), outline=INK)
        d.polygon(rot([(0.045, -0.03), (0.07, -0.035), (0.07, -0.07), (0.045, -0.075)]), fill=(250, 250, 250), outline=INK)
        d.polygon(rot([(-0.03, -0.1), (0.03, -0.1), (0.03, -0.085), (-0.03, -0.085)]), fill=(110, 70, 40))
    elif kind == 'pot':
        d.polygon(rot([(-0.04, 0), (0.04, 0), (0.045, -0.1), (-0.045, -0.1)]), fill=(40, 40, 46), outline=INK)
    elif kind == 'plant':
        d.polygon(rot([(-0.06, 0), (0.06, 0), (0.07, -0.09), (-0.07, -0.09)]), fill=(196, 110, 70), outline=INK)
        for a in (-0.5, 0.0, 0.5):
            d.polygon(rot([(0, -0.09), (0.05 * math.sin(a) - 0.02, -0.2), (0.05 * math.sin(a) + 0.02, -0.2)]),
                      fill=(70, 140, 70), outline=INK)
    elif kind == 'paper':                                 # a sheet of A4 with lines of print, tumbling in 3D
        psi = 0.6 * i + 0.5 * ang
        phi = 0.0 if landed else 1.1 * math.sin(ang * 1.7 + i)

        def corner(u, v):
            a_, b_ = u * 0.105, v * 0.15
            return cam3.pt(X + a_ * math.cos(psi) - b_ * math.cos(phi) * math.sin(psi), Z + a_ * math.sin(psi)
                           + b_ * math.cos(phi) * math.cos(psi), Y + 0.004 + b_ * math.sin(phi))
        quad = [corner(-1, -1), corner(1, -1), corner(1, 1), corner(-1, 1)]
        d.polygon([(px * k, py * k) for px, py in quad], fill=(252, 252, 250), outline=INK)
        for v in (-0.6, -0.35, -0.1, 0.15, 0.4):
            (ax, ay), (bx, by) = corner(-0.7, v), corner(0.7 if v < 0.3 else 0.2, v)
            d.line([(ax * k, ay * k), (bx * k, by * k)], fill=(150, 150, 156), width=max(1, int(2 * k)))
    elif kind == 'pen':                                   # a biro: clear barrel, blue cap and end, black tip
        beta = 0.0 if landed else 0.8 * ang
        dx, dy, dz = math.cos(ang) * math.cos(beta), math.sin(beta), math.sin(ang) * math.cos(beta)
        (ax, ay), (bx, by) = (cam3.pt(X + q * 0.07 * dx, Z + q * 0.07 * dz, Y + 0.006 + q * 0.07 * dy) for q in (-1, 1))
        ax, ay, bx, by = ax * k, ay * k, bx * k, by * k
        L = math.hypot(bx - ax, by - ay) or 1.0
        nx, ny = -(by - ay) / L * 0.0065 * sc, (bx - ax) / L * 0.0065 * sc

        def seg(u0, u1, w=1.0):
            p0, p1 = (ax + (bx - ax) * u0, ay + (by - ay) * u0), (ax + (bx - ax) * u1, ay + (by - ay) * u1)
            return [(p0[0] + nx * w, p0[1] + ny * w), (p1[0] + nx * w, p1[1] + ny * w),
                    (p1[0] - nx * w, p1[1] - ny * w), (p0[0] - nx * w, p0[1] - ny * w)]
        d.polygon(seg(0.0, 1.0), fill=(232, 238, 242), outline=INK)            # the barrel
        d.polygon(seg(0.0, 0.3, 1.15), fill=(30, 60, 170), outline=INK)         # the cap
        d.polygon(seg(0.94, 1.0, 1.0), fill=(30, 60, 170), outline=INK)         # the end plug
        d.line([(ax + (bx - ax) * 0.3, ay + (by - ay) * 0.3), (ax + (bx - ax) * 0.94, ay + (by - ay) * 0.94)],
               fill=(30, 60, 170), width=max(1, int(0.003 * sc)))               # the ink tube inside


COFFEE = [   # (across: to our right, up, away from us; delay): all of it thrown to the right, landing on the carpet in
    # the clear space in front of the dancers, never on them (Sam, 18 Oct)
    (1.0, 1.0, 0.45, 0.0), (1.25, 0.8, 0.5, 0.02), (0.85, 1.2, 0.35, 0.01), (1.4, 0.9, 0.6, 0.03),
    (1.1, 0.6, 0.3, 0.04), (0.75, 0.9, 0.55, 0.02), (1.3, 1.1, 0.4, 0.05)]
COFFEE_C = (92, 54, 28)


def coffee_at(i, t):
    """A drop of coffee thrown from the mug: (X, Y, Z, landed)."""
    vx, vy, vz, dl = COFFEE[i]
    X0, Z0 = ITEMS[0][1] + DESK_DX, ITEMS[0][2]
    u = t - CRASH - dl
    if u <= 0:
        return None
    land = (vy + math.sqrt(vy * vy + 2 * 9.8 * DESK_TOP)) / 9.8
    uu = min(u, land)
    return X0 + vx * uu, max(0.0, DESK_TOP + 0.08 + vy * uu - 4.9 * uu * uu), Z0 + vz * uu, u >= land


def coffee(img, cam3, t, stains):
    """stains=True: the puddles on the carpet where the drops landed (they stay); False: the drops in flight."""
    k = img.size[0] / 1080
    d = ImageDraw.Draw(img)
    for i in range(len(COFFEE)):
        c = coffee_at(i, t)
        if c is None or c[3] != stains:
            continue
        X, Y, Z, landed = c
        x, y = cam3.pt(X, Z, Y)
        sc = cam3.foc / Z * k
        if stains:
            rng = np.random.default_rng(i)
            r = 0.07 + 0.04 * rng.random()
            pts = [(x * k + math.cos(a) * r * sc * (0.8 + 0.4 * rng.random()),
                    y * k + math.sin(a) * r * 0.35 * sc * (0.8 + 0.4 * rng.random())) for a in np.linspace(0, 6.28, 12, endpoint=False)]
            d.polygon(pts, fill=COFFEE_C)
        else:
            r = 0.022 * sc
            d.ellipse([x * k - r, y * k - r * 1.4, x * k + r, y * k + r], fill=COFFEE_C, outline=INK)


def crash_desk(img, cam3, t, top_only=None):
    """The desk at the front left that Jenrick crashes into (cut off by the frame's edge): its top with a monitor,
    keyboard and the things that go flying; its front. top_only: True = only the top, False = only the front."""
    k = img.size[0] / 1080
    d = ImageDraw.Draw(img)
    P3 = cam3.pt
    x0, x1, z0, z1 = CRASH_DESK
    shake = 0.02 * math.exp(-((t - CRASH) / 0.12) ** 2) * math.sin(t * 90) if t > CRASH - 0.05 else 0.0
    if top_only in (None, True):
        poly(d, [P3(x0, z0, DESK_TOP), P3(x1 + shake, z0, DESK_TOP), P3(x1 + shake, z1, DESK_TOP), P3(x0, z1, DESK_TOP)],
             (232, 226, 214), k)                                                               # a pale oak top
        mx = -1.45
        tip = 0.0 if t < CRASH else min(0.35, (t - CRASH) * 2.0)          # the monitor rocks back
        poly(d, [P3(mx - 0.3, z1 - 0.1, DESK_TOP + 0.08), P3(mx + 0.3, z1 - 0.1, DESK_TOP + 0.08),
                 P3(mx + 0.3, z1 - 0.1 + tip * 0.2, DESK_TOP + 0.48 - tip * 0.1), P3(mx - 0.3, z1 - 0.1 + tip * 0.2, DESK_TOP + 0.48 - tip * 0.1)],
             MONITOR, k)
        poly(d, [P3(mx - 0.22, z0 + 0.25, DESK_TOP), P3(mx + 0.22, z0 + 0.25, DESK_TOP), P3(mx + 0.22, z0 + 0.4, DESK_TOP),
                 P3(mx - 0.22, z0 + 0.4, DESK_TOP)], (60, 62, 68), k)                      # keyboard
        for i, it in enumerate(ITEMS):
            if t < CRASH + it[4]:
                draw_item(img, cam3, i, t)
    if top_only in (None, False):
        for lx, lz in ((x1 + shake - 0.05, z0 + 0.05), (x1 + shake - 0.05, z1 - 0.05)):   # steel legs
            poly(d, [P3(lx - 0.03, lz, 0.0), P3(lx + 0.03, lz, 0.0), P3(lx + 0.03, lz, DESK_TOP - 0.03),
                     P3(lx - 0.03, lz, DESK_TOP - 0.03)], (150, 152, 158), k)
        poly(d, [P3(x0, z0, DESK_TOP - 0.04), P3(x1 + shake, z0, DESK_TOP - 0.04), P3(x1 + shake, z0, DESK_TOP),
                 P3(x0, z0, DESK_TOP)], (196, 186, 168), k)                                    # the top's front edge
        poly(d, [P3(x1 + shake, z0, DESK_TOP - 0.04), P3(x1 + shake, z1, DESK_TOP - 0.04), P3(x1 + shake, z1, DESK_TOP),
                 P3(x1 + shake, z0, DESK_TOP)], (180, 170, 152), k)


# --------------------------------------------------------------------------------------------- the office people
def worker(skin, hair, hair_c, jacket, outfit, trousers, **kw):
    """An office worker dressed for a professional office (Sam, 18 Oct): suits, shirts, blouses."""
    sp = dict(skin=skin, hair=hair, hair_c=hair_c, jacket=jacket, outfit=outfit, trousers=trousers, shirt=(244, 244, 242),
              shoulders=kw.pop('shoulders', 140), hw=kw.pop('hw', 66), hh=kw.pop('hh', 88), full=True, pose='custom',
              mouth='set', jaw=kw.pop('jaw', 'soft'))
    sp.update(kw)
    return sp


# who, X, Z, facing (degrees: 45 = three-quarter towards the middle from the left; 135 = turned away, working)
WORKERS = [
    (worker(B.PALE, 'bob', (90, 60, 40), (60, 66, 84), 'blouse', (40, 42, 52), lashes=True, name='w1'), -1.7, 5.6, 45),
    (worker((240, 196, 170), 'crop', (30, 24, 22), (40, 44, 60), 'suit', (40, 44, 60), tie=(120, 30, 40), glasses=True,
            name='w2'), 1.7, 5.6, -45),
    (worker((236, 190, 162), 'side', (58, 44, 36), (70, 74, 82), 'suit', (60, 62, 70), tie=(40, 60, 110), name='w3'), -1.75, 8.2, 135),
    (worker((248, 212, 196), 'long', (200, 170, 110), (120, 40, 60), 'blouse', (34, 34, 40),
            lashes=True, name='w4'), 1.75, 8.2, -45),
    (worker(B.PALE, 'side', (170, 166, 162), (50, 54, 66), 'suit', (50, 54, 66), tie=(150, 120, 40), name='w5'), 1.75, 10.8, -135),
]
PHONE_GUY = worker(B.PALE, 'side', (110, 70, 46), (52, 60, 80), 'suit', (52, 60, 80), tie=(90, 30, 50), name='phone')
PHONE_AT = (0.84, 2.1, -135)      # front right, half in shot, turned diagonally towards Farage, filming (Sam)


def seated_worker(img, cam3, sp, X, Z, yaw, t):
    import moves
    j = moves.seated(dict(sp))
    if abs(yaw) > 90:                                       # working: hands forward on the keyboard
        for side, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, side, (sg * 80, 360.0, 260.0), 'back', 'fist')
    x, y, s = cam3.person(X, Z)
    V.person(img, B.Cam(1.0, 540, 960), x, y, s, dict(sp, blink=F.blinking(t, BLINKS.get(sp['name'], ()))), t, yaw, j)


def phone_in_hand(p, j2, t):
    """The phone held upright in his right hand (Sam, 18 Oct), its camera to the dancers and its screen towards us,
    showing what it films: the pop lights' colour, flashing with the strobe; the plain office once they stop. The
    hand is drawn again over its lower edge, so the phone sits in his grip."""
    el, wr = j2['elR'], j2['wrR']
    dx, dy = wr[0] - el[0], wr[1] - el[1]
    n = math.hypot(dx, dy) or 1.0
    hx, hy = wr[0] + dx / n * 12, wr[1] + dy / n * 12
    w, h = 30, 58
    cx, cy = hx, hy - 34
    p.poly([(cx - w, cy - h), (cx + w, cy - h), (cx + w, cy + h), (cx - w, cy + h)], (30, 32, 38), INK, 2.4)
    if music_on(t):
        m = song_clock(t)
        scr = blend_c(wash_colour(m), (255, 255, 255), 0.5 if (m % BEAT) / BEAT < 0.12 else 0.15)
    else:
        scr = (214, 220, 224)
    p.poly([(cx - w + 6, cy - h + 10), (cx + w - 6, cy - h + 10), (cx + w - 6, cy + h - 10), (cx - w + 6, cy + h - 10)],
           scr, None)
    p.ell(cx, cy + h - 22, 5, 5, (230, 40, 40), None)                                 # the record button
    p.ell(hx, hy, 26, 26, PHONE_GUY['skin'], INK, 2.4)


def blend_c(a, b, k):
    return tuple(int(x + (y - x) * k) for x, y in zip(a, b))


def phone_guy(img, cam3, t):
    """The man at the front right filming the dance on his phone (Sam, 18 Oct), seen from behind, phone held up."""
    sp = dict(PHONE_GUY)
    j = V.standing(sp)
    X, Z, yaw = PHONE_AT
    V.arm_to(j, 'R', (20.0, -150.0, 260.0), 'down', 'fist')   # the phone held up in one hand; the other hangs
    j['props'] = [lambda p, j2: phone_in_hand(p, j2, t)]
    x, y, s = cam3.person(X, Z)
    V.person(img, B.Cam(1.0, 540, 960), x, y, s, sp, t, yaw, j)


BLINKS.update({w[0]['name']: F.blinks(20 + i, 0.0, 40.0) for i, w in enumerate(WORKERS)})


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


CLIP_A = os.path.join(DATA, 'clip-a.mov')                 # Sam's screen recordings of the trend video (not on GitHub)
CLIP_B = os.path.join(DATA, 'clip-b.mov')                 # (the poorer-sounding first source: now only a back-up)
CLIP_C = os.path.join(DATA, 'clip-c.mov')                 # the beginning, from the better-sounding second source
CLIP_D = os.path.join(DATA, 'clip-d.mov')                 # the back half, from that same better source (Sam, 18 Oct)
CLIP_E = os.path.join(DATA, 'clip-e.mov')                 # the better source again, continuous from the start for 9 s
# The song bed, one continuous song from the better source only (Sam, 18 Oct: 'one second still from video 1, it
# dips'): clip E from its first sound (0.45 s, the same moment as clip C) to 8.90 s, then clip D, which matches clip E
# exactly from E 7.145 s (measured to the millisecond), from 1.755 s to 7.70 s (D drops out at 7.8). The old join
# through clip A had been skipping about 1.1 s (two beats) of the song: that was the dip.
SPLICE = ((CLIP_E, 0.45, 8.90), (CLIP_D, 8.90 - 7.145, 7.70))
XFADE = 0.03                                               # each join is a 30 ms equal-power crossfade


def _piece(clip, a, b2, pre, post):
    """A piece of a clip's sound, mono, with `pre` and `post` extra seconds either side for the crossfades."""
    import imageio_ffmpeg
    import subprocess
    t0 = max(0.0, a - pre)
    raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-ss', str(t0), '-t', str(b2 + post - t0), '-i', clip,
                          '-vn', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float64) / 32768, a - t0


def build_music():
    """The song bed from Sam's clips (SPLICE), joined without a jump. Each piece is levelled to the first (the bridge
    is from a different source), and the joins are 30 ms crossfades. Copyrighted, so kept in source/data/shocking/
    (not on GitHub; Sam, 18 Oct). Timeline unchanged by the crossfades: each join is centred on its cut."""
    h = int(XFADE / 2 * SR)
    pieces = []
    ref = None
    for i, (clip, a, b2) in enumerate(SPLICE):
        x, lead = _piece(clip, a, b2, XFADE / 2 if i else 0.0, XFADE / 2 if i < len(SPLICE) - 1 else 0.0)
        core = x[int(lead * SR):int(lead * SR) + int((b2 - a) * SR)]
        rms = math.sqrt(float(np.mean(core ** 2))) + 1e-9
        ref = rms if ref is None else ref
        pieces.append(x * (ref / rms))                       # level each piece to the first
    out = pieces[0].copy()
    n0 = int(0.006 * SR)
    out[:n0] *= np.linspace(0, 1, n0)                        # no click at the very start
    for x in pieces[1:]:
        k = min(2 * h, len(out), len(x))
        w = np.linspace(0, math.pi / 2, k)
        out[-k:] = out[-k:] * np.cos(w) + x[:k] * np.sin(w)  # equal power, over the join
        out = np.concatenate([out, x[k:]])
    out[-n0:] *= np.linspace(1, 0, n0)
    MA.write_wav(os.path.join(DATA, 'song.wav'), out)
    print(f'song bed: {len(out) / SR:.2f} s from {len(pieces)} pieces')


# --------------------------------------------------------------------------------------------- the voices
NARR_OFF = 0.4 - 2.8                                       # film time = file time + offset
FAR_OFF = FARAGE_AT - 2.48
FAR_BITS = [   # Farage's take, piece by piece (file seconds): the words, and the gaps Sam left for the bleeps
    ('Damn it Jenrick,', 2.48, 3.31), ("if you can't stay in formation I swear to", 3.45, 5.57),
    ('bloody', 5.60, 6.0), ('hell', 6.12, 6.55), ("I'll have your", 6.60, 7.32), ('bloody', 7.36, 7.95), ('ass deported.', 7.99, 8.96)]
FAR_TRACK = [(a + FAR_OFF, b2 + FAR_OFF, sh) for txt, a0, b0 in FAR_BITS
             for a, b2, sh in mouths.track(txt, [(a0, b0)])]
CAPS = [   # short chunks (two to five words), each with its first word
    (0.4, 1.5, 'ITV sent an'), (1.5, 2.9, 'undercover journalist'), (2.9, 4.3, "into Reform UK's HQ,"),
    (4.3, 5.6, 'where she observed'), (5.6, 6.9, 'shocking behaviour.'),
    (2.48 + FAR_OFF, 3.4 + FAR_OFF, 'Damn it Jenrick,'), (3.45 + FAR_OFF, 5.0 + FAR_OFF, "if you can't stay in formation"), (5.0 + FAR_OFF, 6.6 + FAR_OFF, 'I swear to ******* ******'),
    (6.6 + FAR_OFF, 7.9 + FAR_OFF, "I'll have your *****"), (7.99 + FAR_OFF, 9.4 + FAR_OFF, 'ass deported.')]


def caption_at(t):
    for a, b2, txt in CAPS:
        if a <= t < b2:
            return txt
    return None


def crash_sound(track):
    """Jenrick hitting the desk (Sam, 18 Oct: yes to the sound): a heavy thump and rattle on impact, then each thing
    clattering down where and when it lands (the mug's clink, the pot's clack, pens ticking, paper settling).
    Made here from shaped noise and tones (no outside recording)."""
    rng = np.random.default_rng(7)

    def at(sec, x, gain):
        i = int(sec * SR)
        n = min(len(x), len(track) - i)
        if n > 0:
            track[i:i + n] += x[:n] * gain
    n = int(0.45 * SR)
    tt = np.arange(n) / SR
    thump = np.sin(2 * np.pi * 70 * tt) * np.exp(-tt * 14) + 0.5 * np.sin(2 * np.pi * 120 * tt) * np.exp(-tt * 20)
    rattle = rng.standard_normal(n) * np.exp(-tt * 9)
    rattle = np.convolve(rattle, np.ones(6) / 6, 'same')
    at(CRASH, thump * 0.9 + rattle * 0.35, 0.6)
    for i, it in enumerate(ITEMS):
        kind = it[0]
        land = None
        for k in range(1, 400):
            if item_at(i, CRASH + k / 100)[4]:
                land = CRASH + k / 100
                break
        if land is None or kind == 'paper':
            continue
        m = int(0.25 * SR)
        tt = np.arange(m) / SR
        if kind == 'mug':
            x = (np.sin(2 * np.pi * 2300 * tt) + 0.6 * np.sin(2 * np.pi * 3700 * tt)) * np.exp(-tt * 30)
            x += rng.standard_normal(m) * np.exp(-tt * 60) * 0.5
            g = 0.3
        elif kind in ('pot', 'plant'):
            x = rng.standard_normal(m) * np.exp(-tt * 40) + np.sin(2 * np.pi * 400 * tt) * np.exp(-tt * 30)
            g = 0.25
        else:
            x = rng.standard_normal(m) * np.exp(-tt * 120)
            g = 0.12
        at(land, x, g)
    m = int(0.6 * SR)                                       # the papers settling
    at(CRASH + 0.9, np.convolve(rng.standard_normal(m), np.ones(30) / 30, 'same') * np.exp(-np.arange(m) / SR * 5), 0.08)


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
    crash_sound(rest)
    song = load_song() * 0.75                            # loud: it never plays under a voice (Sam: louder)
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
    for i in range(len(SCOOTERS)):                         # packed tight along the kerb, nose-out (Claude's addition)
        scooter(d, 110 + i * 200 + (i % 3) * 12, 2320 + (i % 2) * 10, i)   # on the paving, the cycle lane in front
    d.line([(1460, 2300), (1460, 1300)], fill=(40, 42, 46), width=14)                   # a lamp post
    d.rectangle([1444, 1280, 1476, 1310], fill=(40, 42, 46))
    _PLATE['img'] = img
    return img


SCOOTERS = [   # (body colour, kind, lean) left to right, as parked outside Millbank Tower (ref millbank-scooters)
    ((206, 208, 212), 'scooter', -4), ((176, 178, 184), 'scooter', 3), ((40, 40, 44), 'scooter', -2),
    ((52, 30, 30), 'motorbike', 5), ((34, 34, 38), 'scooter', -3), ((26, 26, 30), 'motorbike', 2),
    ((96, 98, 104), 'scooter', -5), ((214, 214, 212), 'scooter', 4)]


def scooter(d, x, y, i):
    """A scooter or motorbike parked nose-out towards the road, seen from the front (ref millbank-scooters, Sam
    18 Oct: authentic colour and position): front wheel and mudguard, the front shield with its headlights, a tall
    tinted windscreen, handlebars with mirrors, a black leg cover, a top box behind; the motorbikes are naked bikes
    with a red frame and a round lamp. Packed tight, each leaning a little on its stand."""
    body, kind, lean = SCOOTERS[i % len(SCOOTERS)]
    s_ = math.sin(math.radians(lean))
    sh = lambda px, py: (x + px + (y + 170 - py) * -s_, py)            # lean about the tyre's contact
    poly_ = lambda pts, fill, w=3: d.polygon([sh(px, py) for px, py in pts], fill=fill, outline=INK, width=w)
    if kind == 'motorbike':
        poly_([(-60, y - 120), (60, y - 120), (70, y - 40), (-70, y - 40)], (30, 30, 34))           # tank and seat
        poly_([(-14, y - 40), (14, y - 40), (18, y + 90), (-18, y + 90)], (200, 50, 40))             # the red frame/fork
        poly_([(-22, y + 40), (22, y + 40), (22, y + 170), (-22, y + 170)], (24, 24, 26))           # tyre, head-on
        poly_([(-30, y + 30), (30, y + 30), (24, y + 60), (-24, y + 60)], body)                     # mudguard
        d.ellipse([sh(-26, y - 60)[0], y - 60, sh(26, y - 60)[0], y - 8], fill=(250, 246, 214), outline=INK, width=3)
        d.line([sh(-90, y - 70), sh(90, y - 70)], fill=(30, 30, 34), width=7)                       # bars
        for mx in (-90, 90):
            d.ellipse([sh(mx - 14, y - 110)[0], y - 110, sh(mx + 14, y - 110)[0], y - 92], fill=(90, 100, 110), outline=INK, width=2)
        return
    poly_([(-74, y - 210), (74, y - 210), (78, y - 150), (-78, y - 150)], (28, 28, 32))               # top box behind
    poly_([(-96, y - 30), (96, y - 30), (80, y + 120), (-80, y + 120)], (30, 30, 34))               # leg cover
    poly_([(-26, y + 60), (26, y + 60), (26, y + 170), (-26, y + 170)], (24, 24, 26))               # tyre, head-on
    d.ellipse([sh(-14, y + 90)[0], y + 90, sh(14, y + 90)[0], y + 130], fill=(170, 172, 176), outline=INK, width=2)
    poly_([(-40, y + 46), (40, y + 46), (32, y + 80), (-32, y + 80)], body)                         # mudguard
    poly_([(-70, y - 130), (70, y - 130), (78, y - 40), (40, y + 30), (-40, y + 30), (-78, y - 40)], body)   # shield
    poly_([(-54, y - 104), (54, y - 104), (40, y - 86), (-40, y - 86)], (244, 242, 220), 2)        # one wide headlight
    for hx in (-66, 66):                                                                             # indicators
        poly_([(hx - 9, y - 70), (hx + 9, y - 70), (hx + 7, y - 58), (hx - 7, y - 58)], (236, 150, 50), 2)
    poly_([(-44, y - 262), (0, y - 270), (44, y - 262), (64, y - 130), (-64, y - 130)], (120, 132, 142))   # tall tinted screen
    d.line([sh(-110, y - 140), sh(110, y - 140)], fill=(30, 30, 34), width=7)                        # bars
    for mx in (-110, 110):                                                                           # mirrors
        d.line([sh(mx, y - 140), sh(mx * 0.9, y - 190)], fill=(30, 30, 34), width=4)
        d.ellipse([sh(mx * 0.9 - 16, y - 210)[0], y - 210, sh(mx * 0.9 + 16, y - 210)[0], y - 186], fill=(90, 100, 110), outline=INK, width=2)


def lapel_view(t):
    """The part of the Millbank plate the lapel camera sees at t (box) and its tilt (degrees, PIL's rotate)."""
    u = t / SLAM
    z = 1.0 + 0.55 * u * u * 0.6 + 0.25 * u                # walking closer: the entrance grows
    step = math.sin(2 * math.pi * 1.9 * t)                 # two steps a second
    roll = -4.0 + 1.8 * step
    cx, cy = 810 + 30 * math.sin(2 * math.pi * 0.95 * t), 1750 - 260 * u + 14 * abs(step)
    w, h = 1080 / z / 1.5 * 1.5, 1920 / z / 1.5 * 1.5
    return (cx - w / 2 * 1.5, cy - h / 2 * 1.5, cx + w / 2 * 1.5, cy + h / 2 * 1.5), roll


def plate_to_frame(px, py, t):
    """A point on the Millbank plate to where it shows on the 1080 x 1920 frame at t."""
    (x0, y0, x1, y1), roll = lapel_view(t)
    x, y = (px - x0) / (x1 - x0) * 1080, (py - y0) / (y1 - y0) * 1920
    a = math.radians(roll)                                 # PIL turns the picture anticlockwise about its middle
    dx, dy = x - 540, y - 960
    return 540 + dx * math.cos(a) + dy * math.sin(a), 960 - dx * math.sin(a) + dy * math.cos(a)


def sign_box(t):
    """The MILLBANK TOWER lettering on the canopy, on the frame (for the Hook Text check)."""
    if t >= SLAM:
        return None
    font = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans.ttf'), 92)
    l, tp, r, b = ImageDraw.Draw(Image.new('L', (1, 1))).textbbox((810, 1652), 'M I L L B A N K   T O W E R',
                                                                    font=font, anchor='mm')
    pts = [plate_to_frame(x, y, t) for x in (l, r) for y in (tp, b)]
    return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))


HOOK = ('Reform HQ: EXPOSED!', {'y': 560, 'x': 700})        # as finish.py is given it (Sam, 18 Oct: on the windows)
KEEP_CLEAR = [('the MILLBANK TOWER sign', sign_box),
              ('the ITV / REC readout', lambda t: (70, 480, 440, 640) if t < SLAM else None)]


def lapel_frame(t):
    """Shot 1: the walk up to the doors through her lapel camera (refs undercover-1, 2): chest height, looking up,
    crooked and swaying with each step, a cheap soft picture with washed-out colour and a pink-grey cast, grain, her
    jacket's dark edge smudging one corner, and the REC readout (Sam, 18 Oct: yes to REC)."""
    plate = millbank_plate()
    box, roll = lapel_view(t)
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
    f0 = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), 46 * S)
    d.text((x, y - 62 * S), 'ITV', font=f0, fill=(250, 250, 250), stroke_width=2 * S, stroke_fill=(30, 30, 30))   # (Sam, 18 Oct)
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


def jenrick_layer(img, cam3, X, Z, k, t, legs=True):
    """Jenrick drawn whole, or without his legs (after the desk he crashed into, so his body lies over its top while
    his legs stay behind it). When he is falling (k['roll']) he is drawn on a layer of his own and tipped sideways
    about his feet, so the trip reads from the front (Sam, 18 Oct: it looked as if he just ran forward)."""
    roll = k.get('roll', 0.0)
    target = img
    if abs(roll) > 0.5:
        target = Image.new('RGBA', img.size, (0, 0, 0, 0))
    keep = V.leg
    if not legs:
        V.leg = lambda *a, **kw: None                      # (restored below)
    try:
        r = make_person(target, cam3, 'jenrick', X, Z, k, t, step=k.get('step') if legs else None)
    finally:
        V.leg = keep
    if target is not img:
        fx, fy = cam3.pt(X, Z)
        k2 = img.size[0] / 1080
        img.alpha_composite(target.rotate(roll, resample=Image.BICUBIC, center=(fx * k2, fy * k2)))
    return r


def desk_top_mask(size, cam3):
    """The desk top's outline on screen, as a mask: the only place Jenrick's second pass may draw."""
    from PIL import ImageDraw as _D
    k = size[0] / 1080
    x0, x1, z0, z1 = CRASH_DESK
    pts = [cam3.pt(x0, z0, DESK_TOP), cam3.pt(x1 + 0.05, z0, DESK_TOP), cam3.pt(x1 + 0.05, z1, DESK_TOP), cam3.pt(x0, z1, DESK_TOP)]
    m = Image.new('L', size, 0)
    _D.Draw(m).polygon([(x * k, y * k) for x, y in pts], fill=255)
    return m


def over_desk_top(img, cam3, jen, t):
    """Jenrick's upper body laid over the desk top he has fallen on, clipped to the desk top, so the second pass
    can never paint him over anyone else (it once put his arm in front of Farage's)."""
    lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    jenrick_layer(lay, cam3, *jen, t, legs=False)
    a = lay.split()[3]
    from PIL import ImageChops
    lay.putalpha(ImageChops.multiply(a, desk_top_mask(img.size, cam3)))
    img.alpha_composite(lay)


def dance_frame(t, cam3=DANCE_CAM):
    """Shots 2 and 4, one wide shot (Sam, 18 Oct): the four of them dancing under the pop lights; office workers at
    the desks watching or working; a man at the front right filming it on his phone; Jenrick's trip and crash into
    the desk at the front left; the swipe; the outburst and everyone's reactions."""
    img = room(cam3)
    on = music_on(t)
    if on:
        pop_lights(img, t, cam3)
        ring_lights(img, cam3, song_clock(t))
    coffee(img, cam3, t, stains=True)                       # puddles are part of the floor: drawn before anyone
    for sp, X, Z, yaw in sorted(WORKERS, key=lambda w: -w[2]):
        seated_worker(img, cam3, sp, X, Z, yaw, t)
    people = []
    jen = None
    for who in DANCERS:
        X, Z = SPOT[who]
        extra = {}
        if who == 'farage':
            X, Z = farage_pos(t)
            if t < FARAGE_AT:
                k = farage_dance_state(t)
            else:
                k, extra = farage_shout_state(t)
        elif who == 'jenrick':
            if t >= TRIP:
                X, Z, k = trip_state(t)
            else:
                k = dance_pose(t - SLAM)
            jen = (X, Z, k)
        else:
            k = other_dance_state(who, t)
        people.append((Z, who, X, k, extra))
    for Z, who, X, k, extra in sorted(people, key=lambda q: -q[0]):
        if who == 'jenrick':
            jenrick_layer(img, cam3, X, Z, k, t)
        else:
            x, y, s = make_person(img, cam3, who, X, Z, k, t, extra=extra,
                                  step=farage_step(t) if who == 'farage' else None)
            if who == 'farage' and t >= FARAGE_AT:
                spit_at(img, x, y - 150 * s + 70 * s, s, t)
    crash_desk(img, cam3, t, top_only=True)
    if jen and jen[1] < 3.0:                                 # at the desk: his body over its top, legs behind it,
        over_desk_top(img, cam3, jen, t)                     # drawn again ONLY where the desk top is (Sam, 18 Oct)
    crash_desk(img, cam3, t, top_only=False)
    for i, it in enumerate(ITEMS):
        if t >= CRASH + it[4]:
            draw_item(img, cam3, i, t)
    coffee(img, cam3, t, stains=False)
    phone_guy(img, cam3, t)
    if on:                                                  # the coloured light falls over everyone too
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
    # a wide double doorway (Sam, 18 Oct: wider, and seen from a little further back)
    poly(d, [(110, 420), (970, 420), (970, 1920), (110, 1920)], (236, 236, 232), k)            # the frame
    poly(d, [(150, 460), (930, 460), (930, 1920), (150, 1920)], (150, 156, 164), k)            # the corridor
    poly(d, [(150, 1560), (930, 1560), (930, 1920), (150, 1920)], (120, 124, 130), k)
    # one proper lift (Sam, 18 Oct): a steel surround, two leaves meeting in the middle, call button, floor display
    poly(d, [(560, 700), (880, 700), (880, 1560), (560, 1560)], (120, 124, 132), k)
    poly(d, [(585, 730), (855, 730), (855, 1560), (585, 1560)], (196, 202, 208), k)
    d.line([(720 * k, 730 * k), (720 * k, 1560 * k)], fill=INK, width=max(1, int(3 * k)))
    poly(d, [(660, 640), (780, 640), (780, 684), (660, 684)], (30, 30, 34), k)
    f0 = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), int(30 * k))
    d.text((720 * k, 662 * k), '4', font=f0, fill=(240, 120, 60), anchor='mm')
    poly(d, [(896, 1080), (924, 1080), (924, 1140), (896, 1140)], (150, 154, 160), k)
    d.ellipse([903 * k, 1098 * k, 917 * k, 1112 * k], fill=(240, 200, 90), outline=INK)
    for x0 in (150, 930):                                                                        # the doors, open
        poly(d, [(x0, 460), (x0 + (60 if x0 < 500 else -60), 500), (x0 + (60 if x0 < 500 else -60), 1900), (x0, 1920)],
             (214, 216, 214), k)
    poly(d, [(480, 300), (600, 300), (600, 360), (480, 360)], (40, 160, 80), k)                 # EXIT sign
    f = ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), int(34 * k))
    d.text((540 * k, 330 * k), 'EXIT', font=f, fill=(250, 250, 250), anchor='mm')
    poly(d, [(40, 900), (80, 900), (80, 960), (40, 960)], (246, 246, 244), k)                   # light switch
    sp = dict(C.JOURNALIST, mood='wtf', look=-0.1)
    u = t - DOOR[0]
    sp['blink'] = any(b <= t < b + 0.42 for b in DOOR_BLINKS)                                 # slow blinks
    sp['gape'] = 0.8 + 0.2 * ease(u / 0.6)
    j = V.standing(sp)
    j['props'] = [lambda p, j2: C.handbag(p, sp)]            # the bag on its strap, over the sleeve
    V.person(img, B.Cam(1.0, 540, 960), 540, 820, 0.96, sp, t, 0, j)
    m = song_clock(t)                                       # the pop lights spill over her from the room
    img.alpha_composite(Image.new('RGBA', img.size, wash_colour(m) + (40,)))
    if (m % BEAT) / BEAT < 0.12:
        img.alpha_composite(Image.new('RGBA', img.size, (255, 255, 255, 90)))
    return img


# --------------------------------------------------------------------------------------------- shots 5 and 6: the outburst
JAB = [3.6, 4.4, 5.2, 6.7, 8.2]                             # file seconds of his stressed words: a finger jab on each


# After the swipe Farage strides over to Jenrick at the desk and rants right in his face (Sam, 18 Oct: 'I did enjoy
# how Farage ended up shouting and spitting straight in his face'), close but never through him (collision_faults).
FARAGE_IN = (-0.17, 2.7)
WALK_IN = (SWIPE + 0.45, SWIPE + 1.25)


def farage_pos(t):
    X0, Z0 = SPOT['farage']
    u = ease((t - WALK_IN[0]) / (WALK_IN[1] - WALK_IN[0]))
    return X0 + (FARAGE_IN[0] - X0) * u, Z0 + (FARAGE_IN[1] - Z0) * u


def farage_step(t):
    return (True, int(t / 0.2) % 2) if WALK_IN[0] < t < WALK_IN[1] else None


def farage_shout_state(t):
    m = mouths.at(FAR_TRACK, t)
    talking_now = m != 'rest'
    jab = max((math.exp(-((t - (j + FAR_OFF)) / 0.12) ** 2) for j in JAB), default=0.0)
    k = P((-280 - 40 * jab, 120 - 30 * jab, 220 + 40 * jab), (176, 420, 60), 'down', 'back', mood='fury', look=-1.0,
          head=-8, lean=4 + 4 * jab, chin=0.15)
    extra = dict(mood='fury', strength=1.4, red=1.0, look=-1.0, turn=-0.3)
    if talking_now:
        extra['mouth'] = 'v:' + m
    return k, extra


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


# --------------------------------------------------------------------------------------------- the checks
BODY_R = 0.22                   # a person's half-width on the floor plan (metres)


def floor_positions(t):
    """Where everyone stands on the floor at time t (metres)."""
    pos = {'farage': farage_pos(t), 'tice': SPOT['tice'], 'braverman': SPOT['braverman'],
           'jenrick': trip_state(t)[:2] if t >= TRIP else SPOT['jenrick'], 'phone man': PHONE_AT[:2]}
    for sp, X, Z, yaw in WORKERS:
        pos[sp['name']] = (X, Z)
    return pos


def collision_faults():
    """Nobody passes through anybody, or into the desk (Sam, 18 Oct: Jenrick clipped straight through Farage). On
    every frame of the office shots, the floor-plan distance between any two people must be at least two body
    half-widths, and no one's body may enter the desk Jenrick crashes into (his hands reach it; his body stops at
    its edge). Returns faults, the first frame of each pair only."""
    faults, seen = [], set()
    x0, x1, z0, z1 = CRASH_DESK
    for i in range(int(SLAM * FPS), int(DUR * FPS)):
        t = i / FPS
        if shot_of(t) not in ('dance', 'dance2'):
            continue
        pos = floor_positions(t)
        names = list(pos)
        for a in range(len(names)):
            Xa, Za = pos[names[a]]
            for b in range(a + 1, len(names)):
                Xb, Zb = pos[names[b]]
                d = math.hypot(Xa - Xb, Za - Zb)
                if d < 2 * BODY_R and (names[a], names[b]) not in seen:
                    seen.add((names[a], names[b]))
                    faults.append(f'{t:.2f} s: {names[a]} passes through {names[b]} ({d:.2f} m apart)')
            dd = math.hypot(max(x0 - Xa, 0.0, Xa - x1), max(z0 - Za, 0.0, Za - z1))
            if dd < 0.10 and (names[a], 'desk') not in seen:      # hips may touch its edge, never enter it
                seen.add((names[a], 'desk'))
                faults.append(f'{t:.2f} s: {names[a]} walks into the desk ({dd:.2f} m from its edge)')
    return faults


def frame_faults():
    """Jenrick's whole trip and impact stay in shot (Sam, 18 Oct): his drawing never touches the frame's edge."""
    faults = []
    keep = B.SS
    B.SS = 1
    t = TRIP - 0.2
    while t <= CRASH + 1.5:
        X, Z, k = trip_state(t) if t >= TRIP else (*SPOT['jenrick'], dance_pose(t - SLAM))
        lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
        jenrick_layer(lay, DANCE_CAM, X, Z, k, t, legs=True)
        bb = lay.getbbox()
        if bb and (bb[0] <= 0 or bb[2] >= 1080 or bb[1] <= 0):
            faults.append(f'{t:.2f} s: Jenrick runs off the edge of the frame {bb}')
            break
        t += 1 / FPS
    B.SS = keep
    return faults


def layering_faults():
    """Drawing order (Sam, 18 Oct: Jenrick's arm showed in front of Farage although he was further away): on every
    frame where Jenrick is drawn a second time over the desk, the extra pixels must lie on the desk top only."""
    faults = []
    keep = B.SS
    B.SS = 1
    m = desk_top_mask((1080, 1920), DANCE_CAM)
    import numpy as _np
    mask = _np.asarray(m) > 0
    t = TRIP
    while t <= DUR:
        X, Z, k = trip_state(t)
        if Z < 3.0:
            lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
            over_desk_top(lay, DANCE_CAM, (X, Z, k), t)
            drawn = _np.asarray(lay.split()[3]) > 0
            if (drawn & ~mask).any():
                faults.append(f"{t:.2f} s: Jenrick's second pass draws outside the desk top")
                break
        t += 3 / FPS
    B.SS = keep
    return faults


def item_faults():
    """The things knocked off the desk (Sam, 18 Oct: pens had landed behind Jenrick and were drawn on his legs). They
    are drawn after the people, so on every frame each one must be nearer the camera than anyone it covers on
    screen, and nothing may come to rest under the desk where it would show through it."""
    faults, seen = [], set()
    x0, x1, z0, z1 = CRASH_DESK
    for n in range(int(CRASH * FPS), int(DUR * FPS)):
        t = n / FPS
        pos = floor_positions(t)
        for i in range(len(ITEMS)):
            X, Y, Z, ang, landed = item_at(i, t)
            x, y = DANCE_CAM.pt(X, Z, Y)
            if not (0 <= x <= 1080 and 0 <= y <= 1920):
                continue
            if landed and x0 < X < x1 and z0 < Z < z1 and (i, 'desk') not in seen:
                seen.add((i, 'desk'))
                faults.append(f'{t:.2f} s: the {ITEMS[i][0]} lands under the desk')
            for who, (PX, PZ) in pos.items():
                px, py, ps = DANCE_CAM.person(PX, PZ)
                inside = abs(x - px) < 210 * ps and py - 330 * ps < y < py + 960 * ps
                if inside and Z > PZ - 0.05 and (i, who) not in seen:
                    seen.add((i, who))
                    faults.append(f'{t:.2f} s: the {ITEMS[i][0]} is behind {who} but drawn over them')
    return faults


# --------------------------------------------------------------------------------------------- the shared clip check
# clipcheck.py (Sam, 18 Oct: nothing passes through anything): every dancer's body as solids, the desk, everything
# flung off it; the pieces drawn separately as layers; the deliberate contacts and the trip's physics.
def dancer_states(t):
    """(who, X, Z, key pose, extra, step) for the four dancers at t, as dance_frame draws them."""
    out = []
    for who in DANCERS:
        X, Z = SPOT[who]
        extra, step = {}, None
        if who == 'farage':
            X, Z = farage_pos(t)
            k, extra = (farage_dance_state(t), {}) if t < FARAGE_AT else farage_shout_state(t)
            step = farage_step(t)
        elif who == 'jenrick':
            X, Z, k = trip_state(t) if t >= TRIP else (X, Z, dance_pose(t - SLAM))
            step = k.get('step')
        else:
            k = other_dance_state(who, t)
        out.append((who, X, Z, k, extra, step))
    return out


def _joints(who, k, step):
    sp = dict(C.CAST[who])
    j = build(sp, k)
    if step and step[0]:
        side = 'L' if step[1] else 'R'
        x, y, z = j['foot' + side]
        j['foot' + side] = (x - 30, y - 40, z + 60)
    return sp, j


def solids(t):
    import clipcheck as CC
    if shot_of(t) not in ('dance', 'dance2'):
        return []
    out = []
    for who, X, Z, k, extra, step in dancer_states(t):
        sp, j = _joints(who, k, step)
        out += CC.person_solids(who, j, X, Z, 0.0, sp, roll=k.get('roll', 0.0) if who == 'jenrick' else 0.0)
    X, Z, yaw = PHONE_AT
    out.append(CC.capsule('phone man', 'body', (X, 0.1, Z), (X, 1.5, Z), 0.2))
    x0, x1, z0, z1 = CRASH_DESK
    out.append(CC.box('desk', 'top', (x0, 0.0, z0), (x1, DESK_TOP, z1)))
    for i, (kind, *_r) in enumerate(ITEMS):
        X, Y, Z, ang, landed = item_at(i, t)
        r = {'mug': 0.05, 'pot': 0.05, 'plant': 0.07, 'paper': 0.03, 'pen': 0.012}[kind]
        out.append(CC.sphere(f'item:{kind}{i}', 'item', (X, Y + r, Z), r))
    return out


def layers(t):
    """The pieces drawn separately, in drawing order (the dancers far to near, then the desk, the things flung
    off it, the phone man)."""
    if shot_of(t) not in ('dance', 'dance2'):
        return []
    cam3 = DANCE_CAM
    out = []
    for who, X, Z, k, extra, step in sorted(dancer_states(t), key=lambda q: -q[2]):
        if who == 'jenrick':
            out.append((who, Z, lambda im, X=X, Z=Z, k=k: jenrick_layer(im, cam3, X, Z, k, t)))
        else:
            out.append((who, Z, lambda im, who=who, X=X, Z=Z, k=k, e=extra, st=step:
                        make_person(im, cam3, who, X, Z, k, t, extra=e, step=st)))
    out.append(('desk', CRASH_DESK[2:], lambda im: crash_desk(im, cam3, t)))
    for i, it in enumerate(ITEMS):
        if t >= CRASH + it[4]:
            out.append((f'{it[0]} {i}', item_at(i, t)[2], lambda im, i=i: draw_item(im, cam3, i, t)))
    out.append(('phone man', PHONE_AT[1], lambda im: phone_guy(im, cam3, t)))
    return out


def LINE_SUBJECTS():
    """Each of the cast alone, large, for the line-work check (linecheck.py)."""
    out = []
    for who in ('tice', 'jenrick', 'farage', 'braverman', 'journalist'):
        def d(im, who=who):
            sp = dict(C.CAST[who], mood='neutral')
            j = V.standing(sp)
            if who == 'journalist':
                j['props'] = [lambda p, j2, sp=sp: C.handbag(p, sp)]
            V.person(im, B.Cam(1.0, 540, 960), 540, 420, 1.45, sp, 0.0, 0, j)
        out.append((who, d))
    return out


# The other shared checks (sizes.py, landmarks.py): props at their real size (the lift door's shape is judged
# alone: its depth beyond the doorway is not set), and the clothes against the body's landmarks.
PROP_SIZES = [('the paper', 'A4 paper', 0.21, 0.297, None), ('a pen', 'biro', 0.14, 0.012, None),
              ('the mug', 'mug', 0.09, 0.10, None), ('the crash desk', 'desk', CRASH_DESK[1] - CRASH_DESK[0], DESK_TOP, None),
              ('the doorway', 'double doorway', 860, 1291, 0.96 / V.M_PER_UNIT),
              ('the lift door', 'lift door opening', 270, 830, 0)]
OUTFIT = {'braverman': {'cropped jacket hem': 430, 'skirt top': 400, 'skirt hem': 745},
          'journalist': {'skirt top': 392, 'skirt hem': 745}}


CLIP_SPAN = (SLAM, DUR)
ALLOWED = [('jenrick', 'desk', CRASH - 0.15, DUR),                  # he crashes into it and lies against it
           ('item:*', 'desk', 0.0, DUR), ('item:*', 'item:*', 0.0, DUR),   # things sit on the desk, side by side
           ('jenrick', 'item:*', CRASH - 0.15, CRASH + 0.3)]          # he knocks them flying
IN_SHOT = [('jenrick', TRIP - 0.2, CRASH + 1.5)]
CONTACTS = [('jenrick.body', 'desk', CRASH)]                              # Sam, 18 Oct: he stopped just short of it
MOMENTUM = [('jenrick', TRIP + 0.25, CRASH - 0.02, 0.12)]            # Sam, 18 Oct: he must not steady himself
PUSHES = [('jenrick', CRASH, [f'item:{it[0]}{i}' for i, it in enumerate(ITEMS) if it[0] != 'paper'])]  # (paper floats)


def checks():
    """The film's own plan checks (run by preflight.py): collisions, Jenrick staying in shot, drawing order."""
    faults = collision_faults() + frame_faults() + layering_faults() + item_faults()
    print('collision, framing and layering checks:', 'clean' if not faults else f'{len(faults)} fault(s)')
    if faults:
        raise ValueError('check: ' + '; '.join(faults))


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
    return door_frame(t)


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
            if who == 'journalist':
                j['props'] = [lambda p, j2, sp=sp: C.handbag(p, sp)]
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
    elif a[0] == 'check':
        checks()
    elif a[0] == 'sheet':
        stills_sheet(a[1], [float(x) for x in a[2:]])
    elif a[0] == 'final':
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=overlay, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None)


# The smoother limbs used since Cry Minister and Bingo Bingo (Sam, 18 Oct: no boxy arms and legs): the arm checker on,
# then limbs.install for the arms (one tapered sleeve coming from behind the shoulder); the bending legs drawn by
# views get the same shaping (fuller thigh, in at the knee, a little calf, slim ankle).
F.guard(B)
import limbs                     # noqa: E402
limbs.install(B)


def shaped_leg(p, j, side, yaw, sp):
    hip3, foot3 = j['hip' + side], j['foot' + side]
    knee3 = V.knee_of(j, side)
    hip, knee, foot = (V.project(q, yaw)[0] for q in (hip3, knee3, foot3))
    lerp2 = lambda a, b2, u: (a[0] + (b2[0] - a[0]) * u, a[1] + (b2[1] - a[1]) * u)
    pts = [hip, lerp2(hip, knee, 0.45), knee, lerp2(knee, foot, 0.32), lerp2(knee, foot, 0.8), foot]
    V.tube(p, pts, [50, 45, 33, 37, 26, 25], sp.get('trousers', (40, 40, 46)))
    fx, fy, fz = foot3
    a = math.radians(j.get('toe' + side, 0.0))

    def foot_pt(dx, dy, dz):
        return (fx + dx, fy + dy - dz * math.sin(a), fz + dz * math.cos(a))
    box = [foot_pt(sx, sy, sz) for sx in (-28, 28) for sy in (0, 36) for sz in (-28, 92)]
    hull = V._hull([V.project(q, yaw)[0] for q in box])
    p.poly(curve(hull, 3), sp.get('shoe', (22, 20, 22)), INK, 2.4)


V.leg = shaped_leg

if __name__ == '__main__':
    main()
