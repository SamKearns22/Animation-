#!/usr/bin/env python3
"""Open Wounds (brexit-is-done): the film (chat 10, 24 Nov). Three interviews, one line each: Theresa May in her BBC
interview, Kemi Badenoch on a building site overrun by wolves, Tony Blair in an oak room as wolves chase the guests;
the cut on the lunge to the sign-off. Built in film order (Sam, 24 Nov, Q8): shot 1 first, each shown before the next.

MAP (rule 61)
  setup ............. NAME, FILM, FPS, LINES (stand-in timing, 3.3 words a second, until Sam records), SHOTS, DUR,
                      T (beats), SHOT_CAST, HOOK, KEEP_CLEAR, scene_of(t), shot_of(t)
  framing ........... FACE_X, EYE_Y, HEAD_PX: the interview look (Sam, 24 Nov: all three in May's place and size, face
                      centre about 62% across; note 9: May a little wider, about waist up)
  people ............ CAST from story/brexit-is-done-people.txt; scale_at(pxm, sp); seated(img, who, L, x, d, t, yaw)
  shot 1 ............ may_shot(t): the places kit's view `may` (story/brexit-is-done-places.txt), May seated, turned
                      to screen-left (looking off-frame left at the unseen interviewer, item 14)
  shot 2 ............ kemi_shot(t): the site with its background action (brexit_is_done_action.site_actors: the
                      attack, the runner, the bar fight, the milling wolves) painted among the pieces far to near
  shot 3 ............ blair_shot(t): the oak room with the chase painted among its pieces (ACT.room_actors: guests
                      through the doors, the tray, the wolves; the corridor's people through the doorway), Blair,
                      the lunger (ACT.lunger)
  picture ........... picture(t) -> the clean frame (no captions, no Hook Text: finish.py adds those)
  main .............. stills

    python3 source/brexit_is_done.py stills OUT_DIR T [T ...]
    python3 source/brexit_is_done.py final OUT.mp4 [--small] [--span T0 T1]     a clip, the animatic, the final
"""
import math
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import people as PK                  # noqa: E402
import people_parts as PPt           # noqa: E402
import places as PL                  # noqa: E402
import sitting as S                  # noqa: E402
import brexit_is_done_action as ACT  # noqa: E402  the background action (shots 2 and 3)
from satire_style import install_circle_hands   # noqa: E402

B = PPt.B
V = PPt.V
install_circle_hands(B)
W, H = 1080, 1920

# ================================================================================================= setup
NAME = 'brexit-is-done'
FILM = 'brexit-is-done'
NOTES = os.path.join(os.path.dirname(HERE), 'notes', 'brexit-is-done.md')
HAS = {'people', 'rooms', 'props'}
FPS = 12
LINES = [   # stand-in timing (Sam's pace, 3.3 words a second) until his recordings set the clock
    dict(who='may', text='The Prime Minister would do well to remember that we had a referendum, and in that '
                         'referendum, the British Public chose wolves.', start=0.6, end=7.0),
    dict(who='kemi', text='Andy Burnham needs to spend less time trying to take us backwards and more time doing his '
                          'job: reducing the number of British people with their faces chewed off.', start=8.1, end=16.9),
    dict(who='blair', text="Well, in my opinion, you shouldn't listen to anything I say, I'm Tony Blair, I invaded "
                           "Iraq, I belong in The Hague.", start=18.0, end=24.6),
]
SHOTS = [('1', 0.0, 7.5), ('2', 7.5, 17.5), ('3', 17.5, 26.9)]
DUR = SHOTS[-1][2]
T = {'chose_wolves': 6.0, 'grin': 25.0, 'lunge': 26.5}
SHOT_CAST = {'1': ['may'], '2': ['kemi'], '3': ['blair']}
SHOT_MARKS = SHOT_CAST                 # rule 38: who the front-on check looks at, per shot
# rule 38: all three are turned to the unseen interviewer off-frame left (item 14), the interview look Sam locked on
# 24 Nov (the camera and framing are his; a fix may never move them: CLAUDE.md "Fix the drawing, never the shot")
THREE_QUARTER_OK = [('1', 'may', 'locked by Sam: the interview look, turned to the interviewer off-frame left (item 14)'),
                    ('2', 'kemi', 'locked by Sam: the interview look, turned to the interviewer off-frame left (item 14)'),
                    ('3', 'blair', 'locked by Sam: the interview look, turned to the interviewer off-frame left (item 14)')]
# rule 78: Blair's forearms rest on the wing chair's arms between gestures (the acting list: 'hands on its arms')
RESTS = [('*Blair*.forearmL', 'armrest', 17.5, 26.9, "Blair's left forearm on the wing chair's arm between gestures"),
         ('*Blair*.forearmR', 'armrest', 17.5, 26.9, "Blair's right forearm on the wing chair's arm between gestures")]
# rule 41 exceptions (reasons in the notes' Exceptions): a side-on runner's far hand passes behind his body for one
# drawing at the back of each swing (chat 19: seen full size, the arm reads swinging; the figure is 40 px tall)
HANDS_OK = [("*workers 2", 'R', 'no hand', 7.5, 17.5, "the side-on runner's far hand passes behind his body at the "
             "back of each swing, as a real runner's does (40 px tall; chat 25: the far arm no longer opens out of his back)"),
            ("*fleeing staff and guests*", '*', 'no hand', 17.5, 26.9, "the guests run side on and three-quarter across "
             "the room: each far hand passes behind the body at the back of each swing, as a real runner's does (chat 25: "
             "the far arm no longer opens out of the back, so its hand is hidden on more drawings)")]
ALLOWED_POPS = [('guest', 17.55, 17.95, 'the butler bursts in through the double doors as they open (seen full size)'),
                ('guest', 19.85, 20.25, 'the woman in red runs off the frame\'s right edge at 4.4 m/s, half out the '
                 'frame the drawing before (seen full size, chat 19)'),
                ('guest', 22.4, 22.75, "a guest comes in at the frame's right edge behind Blair's shoulder (seen full size)"),
                ('guest', 25.2, 25.55, 'the last guest runs off the left edge ahead of the wolves (seen full size)')]
# rule 3: what makes each place recognisable, ours beside the references (chat 19; python3 source/benchmark.py)
BENCHMARK = [
    dict(place='may room', refs=['may-interview-1.jpg', 'may-interview-2.jpg'], at=3.0,
         items=[('a dark, near-black backdrop behind her', 'done: the slatted wall, dark brown'),
                ('soft vertical light streaks on the backdrop', 'done: six lamp streaks, two tones'),
                ('the backdrop out of focus, no detail to read', 'done: flat streaks, no line work'),
                ('her chest-up, turned off-frame left to an unseen interviewer', 'done: locked by Sam (item 14)'),
                ('warm key light on her face, the room dark', 'done: the house look; the wall darker than her'),
                ('nothing else in the room: no props, no desk', 'done: only the chair back shows'),
                ('the chair she sits on, barely seen', 'done: the chair back, dark grey'),
                ('the TV caption and logos', 'left out: our film carries its own Hook Text; no broadcaster marks')]),
    dict(place='building site', refs=['site-geograph-6863924.jpg', 'site-geograph-6921180.jpg'], at=12.0,
         items=[('a grey overcast British sky', 'done: the overcast and cloud banks'),
                ('tower cranes, red and blue', 'done: the red crane and the blue crane'),
                ('a concrete frame several floors high', 'done: the frame, slabs and columns'),
                ('scaffolding with lifts across the face', 'done: inner and outer scaffold, the 6.4 and 9.6 m lifts'),
                ('red-and-white barrier boards on the lifts', 'done: the barrier boards'),
                ('pipes and risers (Sam: "all holes and pipes")', 'done: orange risers, pipe ends, the big pipes'),
                ('blue site hoarding', 'done: the blue hoarding'),
                ('dusty open ground with clutter: cones, a skip, a sand heap', 'done: all four'),
                ('Heras fencing', 'done: the fence')]),
    dict(place='blair room', refs=['oakroom-geograph-4684411.jpg', 'oakroom-geograph-7898479.jpg'], at=22.0,
         items=[('oak panelling, square panels', 'done: the oak panelling'),
                ('a heavy cornice and a coffered or beamed ceiling line', 'done: the cornice'),
                ('a brass chandelier with candle lights', 'done: the chandelier'),
                ('tall doors in the panelling', 'done: the double doors (the guests burst through them)'),
                ('warm polished floor', 'done: the floor and a rug'),
                ('book-lined walls (the brief: "book-lined")', 'done: the bookcases, left and right'),
                ('leaded windows', 'left out: the locked camera faces the doors and bookcases, no window wall in view'),
                ('a grand, quiet, old London room', 'done: oxblood wing chair, oak, books')])]
# rule 1: the three places in metres, top down (x across, z away from the lens; each set laid 100 m apart). Each is
# one locked camera; every piece's own size and depth is in story/brexit-is-done-places.txt (chat 19)
PLAN = dict(
    CEIL=4.0,                                        # the oak room's cornice at 3.9-4.1 m
    ROOMS={'may room': (-6.0, -1.0, 6.0, 3.0), 'building site': (88.0, -1.0, 112.0, 35.0),
           'blair room': (195.0, -1.0, 205.0, 7.0), 'corridor': (198.1, 7.0, 199.9, 11.0)},
    OPENINGS={'double doors': dict(wall=('z', 7.0), span=(198.1, 199.9), sill=0.0, head=3.0, to='corridor')},
    THINGS={'may chair': dict(at=(0.3, 1.75), size=(0.6, 0.6, 1.0), facing=225),
            'slatted wall': dict(at=(0.0, 2.95), size=(12.0, 0.1, 3.8), facing=180),
            'site frame': dict(at=(100.0, 26.0), size=(24.0, 1.0, 14.0), facing=180),
            'big pipes': dict(at=(96.0, 20.9), size=(2.0, 1.0, 1.8), facing=0),
            'blue hoarding': dict(at=(92.0, 22.9), size=(6.0, 0.1, 2.0), facing=180),
            'wing chair': dict(at=(200.3, 2.25), size=(0.85, 0.85, 1.0), facing=225),
            'bookcases, left': dict(at=(196.8, 6.8), size=(2.0, 0.3, 3.0), facing=180,
                                    why='built-in wall units, not free-standing cases'),
            'bookcases, right': dict(at=(202.0, 6.8), size=(4.0, 0.3, 3.0), facing=180,
                                     why='built-in wall units, not free-standing cases')},
    PEOPLE={'may': dict(at=(0.3, 1.6), facing=225, who='may', on='may chair'),
            'kemi': dict(at=(100.3, 1.21), facing=225, who='kemi'),
            'blair': dict(at=(200.3, 2.06), facing=225, who='blair', on='wing chair')},
    CAMS={1: dict(pos=(0.0, 1.2, 0.0), look=(0.0, 1.2, 3.0)), 2: dict(pos=(100.0, 1.6, 0.0), look=(100.0, 1.6, 3.0)),
          3: dict(pos=(200.0, 1.2, 0.0), look=(200.0, 1.2, 3.0))})
HOOK = ('Andy is opening old wounds... \U0001F1EC\U0001F1E7', {'y': 300, 'until': 3.0})   # item 15: above her hair (top at about 465)


def scene_of(t):
    for n, t0, t1 in SHOTS:
        if t < t1:
            return n, t - t0
    n, t0, _ = SHOTS[-1]
    return n, t - t0


def shot_of(t):
    return scene_of(t)[0]


# ================================================================================================= framing
# The interview look, set on May (shot 1) and matched by Kemi and Blair (Sam, 24 Nov): face centre about 62% across,
# the eyes on one row, one head size; May about waist up (note 9) with clear space above her head and on both sides.
FACE_X = 670
EYE_Y = 700
KEEP_CLEAR = [("the lead's face", lambda t: (FACE_X - 150, EYE_Y - 200, FACE_X + 150, EYE_Y + 220))]   # rule 75

# ================================================================================================= people
CAST = PK.install(PK.load(FILM))
FEET = 928.0                         # neck base to sole, person units


def scale_at(pxm, sp):
    """The kit's scale for someone drawn at pxm pixels per metre (their neck base sits at 0.84 of their height)."""
    return pxm * sp['height'] * 0.84 / FEET


def seated(img, who, L, X, d, t, yaw, pose='upright', look=None, chair=False, joints=None):
    """`who` seated at depth d (m) through level camera L, their body centre at screen X; the sitting kit's pose
    (or `joints`: the moves kit's acted pose on the same seat). Seated neck height scales with them (Milburn's 1.06 m
    at 1.75 m)."""
    sp = dict(look or CAST[who])
    pxm = L.ppm(d)
    s = scale_at(pxm, sp)
    neck_y = L.p(0.0, d, 1.06 * sp['height'] / 1.75)[1]
    j = joints if joints is not None else S.pose(sp, pose)
    if not chair:
        j['chair_draw'] = lambda *a, **k: None       # the photos hide her chair behind her
    neck_y -= j.get('bob', 0.0) * s                   # the sitting kit drops the body by bob: the neck stays put
    B.SS = 1
    cam = B.Cam(1.0, 540, 960)
    V.person(img, cam, X, neck_y, s, sp, t, yaw, j)
    return s


# ================================================================================================= faces and moves
# Stand-in timing until Sam records (LINES): each word's time from its syllables spread over its line, the lips on the
# same spread (mouths.track), blinks (F.blinks), head life on a stand-in loudness made from the lip track (open
# shapes speak); every number here is re-timed on Sam's takes. The moves are story/brexit-is-done-moves.txt
# (source/acting.py), each block one acting-list row (rule 74).
import mouths                        # noqa: E402
import figure as FG                  # noqa: E402

TRACK = {ln['who']: [(a + ln['start'], b + ln['start'], sh) for a, b, sh in
                     mouths.track(ln['text'], [(0.0, ln['end'] - ln['start'])])] for ln in LINES}
BLINKS = {w: FG.blinks(17 + 5 * i, 0.0, DUR, talking=True) for i, w in enumerate(('may', 'kemi', 'blair'))}
# The house face's channels: smile (-1 .. +1), lid4 (upper lid), brow_up, frown, squint, look (eyes sideways), mouth.
MOODS = {
    'neutral': dict(),
    'composed': dict(smile=0.05, lid4=0.1, brow_up=0.006),          # May: calm, reasonable, firm
    'pointed': dict(smile=0.18, lid4=0.15, brow_up=0.014),           # ... the faint knowing look on "wolves"
    'stare': dict(smile=-0.25, lid4=0.1, frown=0.03),                # Kemi: hard, level, unbothered by the carnage
    'curt': dict(smile=-0.35, lid4=0.14, frown=0.04),                # ... the curt nod on "job"
    'genial': dict(smile=0.4, lid4=0.12, brow_up=0.01),               # Blair: warm, reasonable, talking
    'grin': dict(smile=1.0, squint=0.35, lid4=0.14, brow_up=0.02, mouth='v:grin'),   # the big grin held from 25.0
    # chat 15, Sam's acting plan (25 Nov): a mood for each beat; the face leads the hand by a drawing or two
    'patient': dict(smile=0.16, lid4=0.2, brow_up=0.03),             # May: the thin patient smile, talking down
    'stern': dict(smile=0.0, lid4=0.12, brow_up=0.035),              # ... the schoolmistress's raised finger
    'brows up': dict(smile=0.06, lid4=0.06, brow_up=0.05),           # ... "remember"; "chose" (a tiny pause)
    'reasonable': dict(smile=0.1, lid4=0.12, brow_up=0.02),
    'firm': dict(smile=-0.12, lid4=0.16, frown=0.025),               # ... the chops (it was decided)
    'satisfied': dict(smile=0.45, lid4=0.2, brow_up=0.012),  # (critique hunt 2: 0.32 read as a plain closed mouth)          # ... the tight satisfied smile on "wolves"
    'satisfied brows': dict(smile=0.45, lid4=0.16, brow_up=0.04),    # ... and the small brow raise to the cut
    'disdain': dict(smile=-0.38, lid4=0.24, frown=0.02, brow_up=0.012),   # Kemi: "Andy", lips tight
    'flat': dict(smile=-0.3, lid4=0.14, frown=0.02),                 # ... the manager giving targets
    'sincere': dict(smile=0.3, lid4=0.14, brow_up=0.03, frown=0.01), # Blair: hand on his chest
    'chuckle': dict(smile=0.7, squint=0.2, lid4=0.16, brow_up=0.015),
    'breezy': dict(smile=0.55, lid4=0.12, brow_up=0.03),
}


import subtitles as SUB          # noqa: E402  rule 62: captions from LINES (finish.py burns them in)
PIECE_FIX = {}


def caption_at(t):
    return SUB.caption_at(LINES, t, PIECE_FIX)      # 3-5 words a piece, each on its syllable


def word_at(n, words):
    """When line n reaches `words`: its syllables spread over the line (stand-in timing, as TRACK)."""
    ln = LINES[n - 1]
    k = len(ln['text'][:ln['text'].index(words)].split())
    syl = [mouths._syllables(w) for w in ln['text'].split()]
    return ln['start'] + (ln['end'] - ln['start']) * sum(syl[:k]) / max(1, sum(syl))


HEAD_LIFE = {}


def head_life(who):
    """Rule 74: the head tilts and nods on the voice (headlife): a stand-in loudness from the lip track until Sam's
    takes (1 while the mouth is open, 0 at rest), each on their own line only."""
    if who not in HEAD_LIFE:
        import numpy as np
        import headlife
        n = int(DUR * FPS) + 2
        env = np.array([0.0 if mouths.at(TRACK[who], i / FPS) in ('rest', 'M') else 1.0 for i in range(n)])
        HEAD_LIFE[who] = headlife.HeadLife(env, 0.0, fps=FPS, seed=41 + ('may', 'kemi', 'blair').index(who))
    return HEAD_LIFE[who]


for _w in ('may', 'kemi', 'blair'):
    head_life(_w)


def face_sp(shot, who, t, mood, shades=None):
    """The moves kit's seam: who's build with the face for a mood, lips on their own line, blinks, head life."""
    d = dict(CAST[who], **MOODS[mood])
    shape = mouths.at(TRACK[who], t)
    if shape != 'rest':
        d['mouth'] = 'v:' + shape
    d['blink'] = FG.blinking(t, BLINKS[who])
    d['head_life'] = head_life(who)
    return d


_MOVES = {}


def acted(shot, who, t):
    """(face sp, joints) for who's block in shot at film time t (story/brexit-is-done-moves.txt)."""
    if not _MOVES:
        import acting as AC
        _MOVES.update(AC=AC, desc=AC.load(FILM), film=AC.film_side(FILM))
    m = _MOVES
    sp, _, _, j, hy = m['AC'].person(m['desc'], m['film'], shot, t)
    if hy is not None:
        j['_head_yaw'] = hy
    return sp, j


# ================================================================================================= shot 1: May
_DESC = PL.load(FILM)
_PAINT = {v: {layer: PL.painter(_DESC, v, layer) for layer in ('back', 'mid', 'front', 'over')}
          for v in ('may', 'site', 'blair')}
MAY = dict(yaw=-45.0,                # turned to screen-left, as her photos
           d=1.6,                    # m from the lens (story/brexit-is-done-places.txt, view may)
           x=690)                    # her body centre on screen: her face lands at FACE_X


def _cam(view):
    return PL.LevelCam.of(_DESC, view)


def _paint(img, view, layer, t):
    if _PAINT[view][layer]:
        _PAINT[view][layer](img, B.Cam(1.0, 540, 960), t)


def may_shot(t):
    img = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    B.SS = 1                                           # before the room paints (the first frame drew it at SS 2)
    L = _cam('may')
    for layer in ('back', 'mid'):
        _paint(img, 'may', layer, t)
    sp, j = acted('1', 'may', t)
    seated(img, 'may', L, MAY['x'], MAY['d'], t, MAY['yaw'], chair=True, look=sp, joints=j)
    for layer in ('front', 'over'):
        _paint(img, 'may', layer, t)
    return img.convert('RGB')


# ================================================================================================= shot 2: Kemi
def standing(img, who, L, X, d, t, yaw, look=None, joints=None):
    """`who` standing on the ground at depth d (m) through level camera L, body centre at screen X."""
    sp = dict(look or CAST[who])
    pxm = L.ppm(d)
    s = scale_at(pxm, sp)
    sole_y = L.p(0.0, d, 0.0)[1]
    B.SS = 1
    V.person(img, B.Cam(1.0, 540, 960), X, sole_y - FEET * s, s, sp, t, yaw, joints)
    return s


KEMI = dict(yaw=-45.0, d=1.21, x=700)   # May's place and size: face centre about 64% across, eyes on row 700


def kemi_shot(t):
    img = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    B.SS = 1
    L = _cam('site')
    u = scene_of(t)[1]
    PL.paint_with(img, _DESC, 'site', B.Cam(1.0, 540, 960), u, ACT.site_actors(u, L))   # the background action
    B.SS = 1
    sp, j = acted('2', 'kemi', t)
    standing(img, 'kemi', L, KEMI['x'], KEMI['d'], t, KEMI['yaw'], look=sp, joints=j)
    for layer in ('front', 'over'):
        _paint(img, 'site', layer, t)
    return img.convert('RGB')


# ================================================================================================= shot 3: Blair
BLAIR = dict(yaw=-45.0, d=2.06, x=537)  # May's place and size, in the oxblood wing chair (the sitting kit's armchair)


def blair_shot(t):
    img = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    B.SS = 1
    L = _cam('blair')
    u = scene_of(t)[1]                                 # the room's pieces run on shot time (the doors open at 0.3 s)
    room, beyond = ACT.room_actors(u, L)               # the chase: guests and wolves among the room's pieces
    PL.paint_with(img, _DESC, 'blair', B.Cam(1.0, 540, 960), u, room, beyond=beyond)
    ACT.lunger(img, L, u)                              # Wp, at his depth just behind his shoulder, 9.0 s (cut 9.4)
    B.SS = 1
    sp, j = acted('3', 'blair', t)
    seated(img, 'blair', L, BLAIR['x'], BLAIR['d'], t, BLAIR['yaw'], pose='armchair', chair=True, look=sp, joints=j)
    for layer in ('front', 'over'):
        _paint(img, 'blair', layer, u)
    return img.convert('RGB')


# ================================================================================================= the general audit
def _alone(shot, who, view, P, kind):
    """`who` alone on a clear layer at t (the shared general audit: kitinputs.alone_audit, through ALONE)."""
    def draw(t):
        B.SS = 1
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        L = _cam(view)
        sp, j = acted(shot, who, t)
        if kind == 'stand':
            standing(lay, who, L, P['x'], P['d'], t, P['yaw'], look=sp, joints=j)
        else:
            seated(lay, who, L, P['x'], P['d'], t, P['yaw'], pose=kind, chair=False, look=sp, joints=j)
        return lay
    return draw


ALONE = {'may [1]': (0.0, 7.5, _alone('1', 'may', 'may', MAY, 'upright')),
         'kemi [2]': (7.5, 17.5, _alone('2', 'kemi', 'site', KEMI, 'stand')),
         'blair [3]': (17.5, 26.9, _alone('3', 'blair', 'blair', BLAIR, 'armchair'))}


# ================================================================================================= picture
def picture(t):
    n = shot_of(t)
    if n == '1':
        return may_shot(t)
    if n == '2':
        return kemi_shot(t)
    return blair_shot(t)


def frame_image(t):
    return picture(t)


def main(argv):
    if len(argv) >= 3 and argv[1] == 'stills':
        os.makedirs(argv[2], exist_ok=True)
        for v in argv[3:]:
            p = os.path.join(argv[2], f'brexit-is-done-{float(v):05.2f}.jpg')
            picture(float(v)).save(p, quality=88)
            print(p)
    elif len(argv) >= 3 and argv[1] == 'final':          # chat 15: clips and renders (silent until Sam records)
        import wave
        import numpy as np
        import film_engine as E
        SR = 44100

        def write_wav(path, x):                         # silent until Sam records (no finished film's file loaded)
            with wave.open(path, 'wb') as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(SR)
                w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
        a = argv[1:]
        small = '--small' in a
        E.render(NAME, a[1], size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
                 picture=picture, overlay=lambda img, t: img, shot_of=shot_of,
                 sound=lambda: np.zeros(int(DUR * SR) + 1), write_wav=write_wav,
                 set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, reuse='--reuse' in a,
                 redo=tuple(a[a.index('--redo') + 1].split(',')) if '--redo' in a else (),
                 span=(float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2])) if '--span' in a else None,
                 stamp=False if '--nostamp' in a else None)
    else:
        print(__doc__)


if __name__ == '__main__':
    main(sys.argv)
