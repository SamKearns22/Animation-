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
  shot 2 ............ (next: kemi_shot, the site and its background action)
  shot 3 ............ (then: blair_shot, the oak room, the chase, the lunge)
  picture ........... picture(t) -> the clean frame (no captions, no Hook Text: finish.py adds those)
  main .............. stills

    python3 source/brexit_is_done.py stills OUT_DIR T [T ...]
"""
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import people as PK                  # noqa: E402
import people_parts as PPt           # noqa: E402
import places as PL                  # noqa: E402
import sitting as S                  # noqa: E402
from milburn_sets import LevelCam    # noqa: E402
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


def seated(img, who, L, X, d, t, yaw, pose='upright', look=None, chair=False):
    """`who` seated at depth d (m) through level camera L, their body centre at screen X; the sitting kit's pose.
    Seated neck height scales with them (Milburn's 1.06 m at 1.75 m)."""
    sp = dict(look or CAST[who])
    pxm = L.ppm(d)
    s = scale_at(pxm, sp)
    neck_y = L.p(0.0, d, 1.06 * sp['height'] / 1.75)[1]
    j = S.pose(sp, pose)
    if not chair:
        j['chair_draw'] = lambda *a, **k: None       # the photos hide her chair behind her
    neck_y -= j.get('bob', 0.0) * s                   # the sitting kit drops the body by bob: the neck stays put
    B.SS = 1
    cam = B.Cam(1.0, 540, 960)
    V.person(img, cam, X, neck_y, s, sp, t, yaw, j)
    return s


# ================================================================================================= shot 1: May
_DESC = PL.load(FILM)
_PAINT = {v: {layer: PL.painter(_DESC, v, layer) for layer in ('back', 'mid', 'front', 'over')}
          for v in ('may', 'site', 'blair')}
MAY = dict(yaw=-45.0,                # turned to screen-left, as her photos
           d=1.6,                    # m from the lens (story/brexit-is-done-places.txt, view may)
           x=690)                    # her body centre on screen: her face lands at FACE_X


def _cam(view):
    v = _DESC['views'][view]['camera']
    return LevelCam(v['up'], v['horizon'], v['lens'])


def _paint(img, view, layer, t):
    if _PAINT[view][layer]:
        _PAINT[view][layer](img, B.Cam(1.0, 540, 960), t)


def may_shot(t):
    img = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    B.SS = 1                                           # before the room paints (the first frame drew it at SS 2)
    L = _cam('may')
    for layer in ('back', 'mid'):
        _paint(img, 'may', layer, t)
    seated(img, 'may', L, MAY['x'], MAY['d'], t, MAY['yaw'], chair=True)
    for layer in ('front', 'over'):
        _paint(img, 'may', layer, t)
    return img.convert('RGB')


# ================================================================================================= picture
def picture(t):
    n = shot_of(t)
    if n == '1':
        return may_shot(t)
    raise NotImplementedError(f'shot {n} is next (film order: May first)')


def frame_image(t):
    return picture(t)


def main(argv):
    if len(argv) >= 3 and argv[1] == 'stills':
        os.makedirs(argv[2], exist_ok=True)
        for v in argv[3:]:
            p = os.path.join(argv[2], f'brexit-is-done-{float(v):05.2f}.jpg')
            picture(float(v)).save(p, quality=88)
            print(p)
    else:
        print(__doc__)


if __name__ == '__main__':
    main(sys.argv)
