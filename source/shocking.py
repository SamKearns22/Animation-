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
         ('farage', FARAGE_AT, 21.3), ('wide', 21.3, 25.0)]
DUR = BLACK_AT = 25.0
# The formation (Sam, 18 Oct), as seen on screen: Farage front centre, Jenrick middle left, Braverman middle right,
# Tice back left (set a little further out than Jenrick so his face is never hidden). Floor positions in metres:
# X across (+ right), Z away from the camera.
SPOT = {'farage': (0.0, 4.2), 'jenrick': (-1.0, 5.2), 'braverman': (1.0, 5.2), 'tice': (-1.75, 6.3)}
DANCERS = ('tice', 'jenrick', 'braverman', 'farage')     # far to near (drawing order)
# ====================================================================================================================


# --------------------------------------------------------------------------------------------- the office camera
FOC, CAM_H, HORIZON = 1400.0, 1.6, 900.0       # focal length (px), camera height (m), horizon row
M_UNIT = V.M_PER_UNIT


def floor_pt(X, Z, Y=0.0):
    """A point in the office (metres; Y up from the floor) on screen (px)."""
    return 540 + FOC * X / Z, HORIZON + FOC * (CAM_H - Y) / Z


def person_at(X, Z):
    """Neck base on screen and the person's scale, for someone standing at (X, Z)."""
    s = FOC / Z * M_UNIT
    fx, fy = floor_pt(X, Z)
    return fx, fy - V.ANKLE_Y * s - 36 * s, s


# --------------------------------------------------------------------------------------------- the dance
def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    if isinstance(a, tuple):
        return tuple(x + (y - x) * u for x, y in zip(a, b))
    return a + (b - a) * u


# A key pose: hand targets for the screen-left (L) and screen-right (R) hands in the body's frame (x across, y down
# from the neck, z towards us), the elbow direction, plus sway (hips and shoulders across, feet planted), dip (knees
# bend), lean (degrees forward), head tilt (head across), chin (head up -, down +), and the face.
def P(L, R, poleL='out', poleR='out', sway=0.0, dip=0.0, lean=0.0, head=0.0, chin=0.0, mood='grin', look=0.0):
    return dict(L=L, R=R, poleL=poleL, poleR=poleR, sway=sway, dip=dip, lean=lean, head=head, chin=chin, mood=mood,
                look=look)


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
MOVE = 0.16                      # each move snaps into its pose over this long, landing on the beat


def routine_pose(m):
    """The key pose blend at song time m: each new pose arrives over MOVE seconds, landing on its beat."""
    if m <= ROUTINE[0][0]:
        return KEYS[ROUTINE[0][1]]
    for (t0, a), (t1, b2) in zip(ROUTINE, ROUTINE[1:]):
        if m < t1:
            u = ease((m - (t1 - MOVE)) / MOVE) if m > t1 - MOVE else 0.0
            return blend_keys(KEYS[a], KEYS[b2], u)
    return KEYS[ROUTINE[-1][1]]


def blend_keys(a, b2, u):
    out = {}
    for k, v in a.items():
        out[k] = lerp(v, b2[k], u) if isinstance(v, (tuple, float, int)) and not isinstance(v, bool) else (v if u < 0.5 else b2[k])
    return out


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
        V.arm_to(j, side, k[side], k['pole' + side], 'fist')
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


if __name__ == '__main__':
    main()
