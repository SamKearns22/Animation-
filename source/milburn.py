#!/usr/bin/env python3
"""Milburn: the film (chat 2, 17 Nov; this is the screenplay's first quarter: shots 1, 2a, 2b).
Milburn, across the Cabinet table, says the essence of his proposal is simple; four NEETs rise up a lift shaft into
the light while he goes on; from above, the platform comes up into the middle of a wide field ringed by forest.

MAP (rule 61)
  setup ............. NAME, FILM, HAS, FPS, LINES (stand-in timing until Sam records), SHOTS, DUR, T (beats),
                      SHOT_CAST, KEEP_CLEAR (the Hook Text's band), scene_of(t)
  plan .............. PLAN (rule 1, metres: the three places, where everyone is, every camera), BENCHMARK (rule 3)
  people ............ CAST from story/milburn-people.txt (people kit); scale_at(pxm, sp): the kit's scale for a level
                      camera's pixels per metre; person(img, who, X, sole_y, pxm, yaw)
  shot 1 ............ cabinet(t): the places kit's Cabinet Room (story/milburn-places.txt, view `cabinet`), Milburn
                      seated across the table (neck at seated height; the table's front layer hides his legs)
  shot 2a ........... shaft_shot(t): milburn_sets.shaft (wall slides down, the light sweeps down), the four at four
                      depths (NEETS: who, x, depth), the light reaching them
  shot 2b ........... field_shot(t): milburn_sets.field; the deck rises from 9 m down and locks level with the grass;
                      the four as tiny figures on it (F8)
  picture ........... picture(t) -> the clean frame (no captions, no Hook Text: finish.py adds those)
  main .............. stills, cast

    python3 source/milburn.py stills OUT_DIR T [T ...]
    python3 source/milburn.py cast OUT.jpg
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
import milburn_sets as MS            # noqa: E402
from satire_style import install_circle_hands   # noqa: E402

B = PPt.B
V = PPt.AV.MC.V
install_circle_hands(B)
W, H = 1080, 1920

# ================================================================================================= setup
NAME = 'milburn'
FILM = 'milburn'
NOTES = os.path.join(os.path.dirname(HERE), 'notes', 'milburn.md')
HAS = {'people', 'rooms', 'voices', 'props'}
FPS = 12
LINES = [   # stand-in timing (about 3 words a second) until Sam's recordings: then 'audio': 'milburn-1' ...
    dict(who='milburn', text='The essence of my proposal is quite simple.', start=0.4, end=2.9),
    dict(who='milburn', text='Those not in education, employment or training will be presented with a unique '
                             'opportunity to serve their country.', start=3.5, end=9.0),
]
SHOTS = [('1', 0.0, 3.3), ('2a', 3.3, 6.5), ('2b', 6.5, 11.0)]    # cut to the aerial on "unique opportunity"
DUR = 11.0
T = {'simple': 2.5,          # shot 1 lands on "simple"
     'light_on_them': 5.6,   # 2a: the light reaches their heads; all four look up ("training")
     'locks': 9.4}           # 2b: the deck locks level with the grass ("country")
SHOT_CAST = {'1': ['milburn'], '2a': ['goth', 'rangy', 'swindon', 'waif'], '2b': ['goth', 'rangy', 'swindon', 'waif']}
KEEP_CLEAR = {'1': [(60, 330, 1020, 560)]}    # the Hook Text's band above Milburn's head (never over his face)


def scene_of(t):
    for n, t0, t1 in SHOTS:
        if t < t1:
            return n, t - t0
    n, t0, _ = SHOTS[-1]
    return n, t - t0


def shot_of(t):
    return scene_of(t)[0]


# ================================================================================================= plan (rule 1)
PLAN = dict(
    ROOMS={'cabinet room': (-2.6, 0.0, 2.6, 3.4),          # x0, depth0, x1, depth1 from the shot-1 lens (m)
           'shaft': (-8.5, -2.5, 8.5, 14.5),               # 17 m across; the lens 6 m from its middle
           'field': (-300.0, -300.0, 300.0, 300.0)},       # the meadow inside the forest ring, the shaft at (0, 0)
    THINGS={'table': dict(at=(0.0, 1.12), size=(5.2, 1.65, 0.76)), 'window': dict(at=(0.88, 3.42)),
            'platform': dict(at=(0.0, 6.0), size=(17.0, 17.0, 0.0))},
    PEOPLE={'milburn': dict(at=(0.0, 2.2), facing=180, seated=True),
            'goth': dict(at=(-0.44, 2.6)), 'rangy': dict(at=(0.58, 3.6)), 'swindon': dict(at=(0.26, 4.8)),
            'waif': dict(at=(-0.26, 6.2))},
    CAMS={'1': dict(up=1.2, look='level', lens=1700, why='seated eye height, straight across the table: he talks to us'),
          '2a': dict(up=1.6, look='level', lens=2000, why='standing head height: every head on one line (F2), we are '
                                                          'among them; room above for the light'),
          '2b': dict(up=70.0, back=79.0, pitch=28.0, lens=1000, why='high and tilted: the size of the arena is the '
                                                                    'joke; peaks kept in the tall frame (F1 bands)')},
)
BENCHMARK = [dict(place='cabinet room', refs=['references/milburn/cabinet-room-burnham.jpg'], at=1.0, items=[
    ('cream panelled walls', 'panels, picture rail, dado rail'),
    ('green damask curtains at a tall bright window', 'curtain (damask pattern, gold tie-back) beside the window'),
    ('the green-baize table', 'table top: baize with a polished rim'),
    ('red leather folders', 'folder at each place, gold crest'),
    ('cut-glass water tumblers', 'tumbler at each place'),
    ('white name cards', 'name card: "Alan Milburn"'),
    ('dark wood chairs with leather backs', 'chair back x3 (his and the two empty ones)'),
    ('papers on the table', 'papers')])]

# ================================================================================================= people
CAST = PK.install(PK.load(FILM))
FEET = 928.0                         # neck base to sole, person units


def scale_at(pxm, sp):
    """The kit's scale for someone drawn at pxm pixels per metre (their neck base sits at 0.84 of their height)."""
    return pxm * sp['height'] * 0.84 / FEET


def person(img, who, X, sole_y, pxm, yaw=0.0, t=0.0, joints=None):
    sp = CAST[who]
    s = scale_at(pxm, sp)
    B.SS = 1
    cam = B.Cam(1.0, 540, 960)
    return V.person(img, cam, X, sole_y - FEET * s, s, dict(sp), t, yaw, joints)


# ================================================================================================= shot 1
_DESC = PL.load(FILM)
_PAINT = {layer: PL.painter(_DESC, 'cabinet', layer) for layer in ('back', 'mid', 'front')}
SEATED_NECK = 1.06                   # m above the floor: seat 0.46, hips 0.5, hips to neck 0.56


def cabinet(t):
    img = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    cam = B.Cam(1.0, 540, 960)
    B.SS = 1
    v = _DESC['views']['cabinet']['camera']
    L = MS.LevelCam(v['up'], v['horizon'], v['lens'])
    if _PAINT['back']:
        _PAINT['back'](img, cam, t)
    d = PLAN['PEOPLE']['milburn']['at'][1]
    pxm = L.ppm(d)
    sp = CAST['milburn']
    neck_y = L.p(0.0, d, SEATED_NECK)[1]
    person(img, 'milburn', 540, neck_y + FEET * scale_at(pxm, sp), pxm, 0.0, t)
    for layer in ('mid', 'front'):
        if _PAINT[layer]:
            _PAINT[layer](img, cam, t)
    return img.convert('RGB')


# ================================================================================================= shot 2a
NEETS = [('waif', -0.26, 6.2), ('swindon', 0.26, 4.8), ('rangy', 0.58, 3.6), ('goth', -0.44, 2.6)]   # far to near


def shaft_shot(t):
    _, lt = scene_of(t)
    t0, t1 = 0.0, T['light_on_them'] - SHOTS[1][1]
    lit = MS.light_line(lt, t0, t1)
    img = MS.shaft(lt, lit).convert('RGBA')
    L = MS.SHAFT_CAM
    for who, x, d in NEETS:
        X, Y = L.p(x, d, 0.0)
        person(img, who, X, Y, L.ppm(d), 0.0, t)
    u = max(0.0, min(1.0, (2.2 - lit) / 1.2))       # the light reaching them: a warm wash over everyone
    out = img.convert('RGB')
    if u > 0:
        out = Image.blend(out, Image.new('RGB', out.size, (255, 238, 196)), 0.16 * u)
    return out


# ================================================================================================= shot 2b
TINY = [(-1.6, 0.6, 'goth'), (1.4, -0.2, 'rangy'), (0.2, 1.8, 'swindon'), (-0.3, -1.4, 'waif')]   # on the deck (m)


def _tiny():
    out = []
    for x, y, who in TINY:
        sp = CAST[who]
        top = sp.get('dress') if sp.get('outfit') == 'dress' else sp.get('jacket')
        out.append((x, y, sp['height'], tuple(top or (90, 90, 90)), tuple(sp['hair_c']), tuple(sp['skin'])))
    return out


def field_shot(t):
    _, lt = scene_of(t)
    u = lt / (T['locks'] - SHOTS[2][1])
    return MS.field(lt, MS.deck_z(u), _tiny())


# ================================================================================================= picture
def picture(t):
    n = shot_of(t)
    if n == '1':
        return cabinet(t)
    if n == '2a':
        return shaft_shot(t)
    return field_shot(t)


def cast(out):
    return PK.sheet(FILM, out)


def main(argv):
    if len(argv) >= 3 and argv[1] == 'stills':
        os.makedirs(argv[2], exist_ok=True)
        for v in argv[3:]:
            p = os.path.join(argv[2], f'milburn-{float(v):05.2f}.jpg')
            picture(float(v)).save(p, quality=88)
            print(p)
    elif len(argv) == 3 and argv[1] == 'cast':
        print(cast(argv[2]))
    else:
        print(__doc__)


if __name__ == '__main__':
    main(sys.argv)
