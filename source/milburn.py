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
  sound, render ..... soundtrack() (espeak stand-ins until Sam records), final(out, small, span)
  main .............. stills, cast, final

    python3 source/milburn.py stills OUT_DIR T [T ...]
    python3 source/milburn.py cast OUT.jpg
    python3 source/milburn.py final OUT.mp4 [--small] [--span T0 T1]    (a clip: --small --span; stand-in voice)
"""
import math
import os
import sys

import numpy as np

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
    dict(who='milburn', text='Each NEET must arm themselves before heading further into the Zone.', start=11.4,
         end=15.1),
    dict(who='andy', text="God damnit, Milburn. You're pulling a Battle Royale slash Hunger Games on us, aren't you?",
         start=15.4, end=20.1),
    dict(who='milburn', text='This report has been long in the making. Would you care to hear the findings or would '
                             'you prefer to interrupt?', start=21.0, end=27.2),
    dict(who='pat', text="I'd like to hear where this goes, Prime Minister.", start=27.8, end=30.6),
    dict(who='andy', text='Fine! Continue.', start=31.2, end=32.4),
    dict(who='milburn', text='The NEETs will form a unit.', start=34.5, end=36.4),
    dict(who='milburn', text='And will encounter teams of their erstwhile colleagues.', start=38.9, end=41.5),
    dict(who='andy', text="You fucker! You're pulling a Maze Runner, Squid Games, Fortnite on me!", start=41.8,
         end=45.5),
    dict(who='milburn', text='I am sorry that you feel that way.', start=46.2, end=48.7),
    dict(who='andy', text='Are you or are you not sending NEETs to kill each other on live TV?', start=49.5, end=54.0),
    dict(who='milburn', text='My report is nuanced and multifaceted. I also suggest taking away PIP after they obtain '
                             'their life-changing injuries in the Blood Dome.', start=55.6, end=63.0),
    dict(who='pat', text='I think the backbenchers will like this one, sir.', start=64.8, end=67.6),
]
SHOTS = [('1', 0.0, 3.3), ('2a', 3.3, 6.5), ('2b', 6.5, 11.0),     # cut to the aerial on "unique opportunity"
         ('3', 11.0, 15.3),                                          # cut on Milburn's dash
         ('4a', 15.3, 20.6), ('4b', 20.6, 27.6), ('4c', 27.6, 34.0),   # scene 4: the table (Sam's Q1)
         ('6', 34.0, 41.6),                                          # the forest; cut on the dash
         ('7a', 41.6, 45.9), ('7b', 45.9, 49.2), ('7c', 49.2, 54.4), ('7d', 54.4, 63.4), ('7e', 63.4, 68.4)]
DUR = 68.4
T = {'simple': 2.5,          # shot 1 lands on "simple"
     'light_on_them': 5.6,   # 2a: the light reaches their heads; all four look up ("training")
     'locks': 9.4,           # 2b: the deck locks level with the grass ("country")
     'gunfire': 36.7,        # 6: gunfire rips from the greenery ahead; the camera stops
     'flame': 37.5,          # 6: the flamethrower's blast whips out
     'stars': 38.2,          # 6: morning stars swing down out of the trees
     'glance': 54.6,         # 7d: Milburn's eyes slide aside (back by 55.3)
     'gape': 63.5}           # 7e: Andy's mouth falls open
_FOUR = ['goth', 'rangy', 'swindon', 'waif']
REVERSE = ('4a', '4c', '7a', '7c', '7e')            # the reverse: Andy and Pat across the table
ACROSS = ('1', '4b', '7b', '7d')                     # shot 1's camera: Milburn
SHOT_CAST = dict({'2a': _FOUR, '2b': _FOUR, '3': _FOUR, '6': _FOUR}, **{n: ['milburn'] for n in ACROSS},
                 **{n: ['andy', 'pat'] for n in REVERSE})
KEEP_CLEAR = {'1': [(60, 330, 1020, 560)]}    # the Hook Text's band above Milburn's head (never over his face)
HOOK = ('The Milburn Report is released 😬', {'y': 420, 'until': 3.0})   # rule 75: the band above his head
SHOT_MARKS = dict(SHOT_CAST, **{'2b': []})          # rule 38: front on (2b: tiny, from above)


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


def person(img, who, X, sole_y, pxm, yaw=0.0, t=0.0, joints=None, look=None):
    """Draw `who` standing on sole_y; their face and pose come from story/milburn-moves.txt (the moves kit) when the
    shot has a block for them (`look`: the kit's face sp), else the plain standing pose."""
    sp = CAST[who]
    s = scale_at(pxm, sp)
    B.SS = 1
    cam = B.Cam(1.0, 540, 960)
    return V.person(img, cam, X, sole_y - FEET * s, s, dict(look or sp), t, yaw, joints)


# ================================================================================================= faces and moves
# The house face's channels (people_parts.front_head): smile (-1 down .. +1 up), lid4 (upper lid, 0 open), brow_up
# (raised), frown (inner ends down), squint, look (eyes sideways), gaze_dy (- up), mouth ('v:SHAPE' while talking).
MOODS = {
    'neutral': dict(),
    'pleased': dict(smile=0.35, lid4=0.26, brow_up=0.004),         # Milburn: calm, reasonable, faintly pleased
    'smug': dict(smile=0.6, lid4=0.3, brow_up=0.01),               # ... a touch more on "simple"
    'unimpressed': dict(smile=-0.7, lid4=0.24),                    # the goth: heavy lids, mouth down
    'unimpressed up': dict(smile=-0.7, lid4=0.06),                 # ... looking up (lids lifted, or the pupils hide)
    'gormless': dict(smile=-0.5, lid4=0.2, brow_up=0.0, mouth='v:O'),   # the rangy lad: mouth hanging open
    'proud': dict(smile=0.3, squint=0.75, lid4=0.3, frown=0.01),              # the Swindon lad: chest out, squinting
    'nervous': dict(smile=-0.55, brow_up=0.03, frown=-0.012, lid4=0.04, look=0.35),   # the waif: worried, glancing
    'proud up': dict(smile=0.2, squint=0.9, lid4=0.18, frown=0.012),   # squinting up into the light
    'awe': dict(brow_up=0.04, lid4=0.0, smile=-0.3, mouth='v:U'),               # looking up into the light
    'awe open': dict(brow_up=0.04, lid4=0.0, mouth='v:O'),         # ... mouth falling open
    # chat 6: the table (scenes 4 and 7)
    'furious': dict(smile=-0.7, frown=0.14, lid4=0.12, squint=0.4),          # Andy: brows hard down
    'rage': dict(smile=-0.9, frown=0.16, lid4=0.0, squint=0.3),             # ... angrier still (scene 7)
    'exasperated': dict(smile=-0.5, brow_up=0.03, frown=-0.01, lid4=0.05),   # "Fine!"
    'sulky': dict(smile=-0.6, lid4=0.34, frown=0.012),                      # arms folded, leaning back
    'despair': dict(smile=-0.7, brow_up=0.035, frown=-0.02, lid4=0.04),     # brows up in the middle
    'gape': dict(smile=-0.4, brow_up=0.03, lid4=0.0, mouth='v:O'),          # mouth hanging open in outrage
    'patient': dict(smile=0.12, lid4=0.3),                                  # Pat: calm, a little heavy-lidded
    'approving': dict(smile=0.4, lid4=0.3),                                 # ... the backbenchers will like it
    'attentive': dict(smile=0.15, lid4=0.2, brow_up=0.006),                 # Milburn: nonplussed, soft
    'sorry': dict(smile=0.2, lid4=0.24, brow_up=0.02, frown=-0.012),        # sorry-not-sorry
    'grim': dict(smile=0.25, lid4=0.3, frown=0.02),                         # the goth, pleased and dangerous
    'thrilled': dict(smile=0.8, squint=0.6, lid4=0.1),                      # Swindon, firing back
    'aghast': dict(smile=-0.6, brow_up=0.05, lid4=0.0, mouth='v:O'),        # the rangy lad
    'terrified': dict(smile=-0.7, brow_up=0.05, frown=-0.02, lid4=0.0),     # the waif
    'eyes shut': dict(smile=-0.7, frown=0.02, blink_hold=True),             # the waif, curled up
}


def word_at(n, words):
    """When line n reaches `words` (stand-in timing: the text spread evenly by letters over the line's span)."""
    ln = LINES[n - 1]
    return ln['start'] + ln['text'].index(words) / len(ln['text']) * (ln['end'] - ln['start'])


import mouths                        # noqa: E402  (the house lip sync: shapes from the words, on the stand-in timing)
import figure as F                   # noqa: E402
TRACK = {}
for _ln in LINES:
    TRACK.setdefault(_ln['who'], []).extend((a + _ln['start'], b + _ln['start'], sh) for a, b, sh in
                                            mouths.track(_ln['text'], [(0.0, _ln['end'] - _ln['start'])]))
BLINKS = {w: F.blinks(11 + 4 * i, 0.0, DUR, talking=(w == 'milburn')) for i, w in enumerate(CAST)}


HEAD_LIFE = {}


def head_life():
    """Rule 74: Milburn's head tilts and nods on his voice (headlife, from the stand-in's loudness per drawing)."""
    if not HEAD_LIFE:
        import numpy as np
        import headlife
        x = soundtrack()
        n = 48000 // FPS
        env = np.array([np.sqrt(np.mean(x[i * n:(i + 1) * n] ** 2)) for i in range(len(x) // n)])
        HEAD_LIFE['milburn'] = headlife.HeadLife(env, 0.0, fps=FPS, seed=21)
    return HEAD_LIFE['milburn']


def face_sp(shot, who, t, mood, shades=None):
    """The moves kit's seam: who's build with the face for a mood, lips on their own lines, blinks."""
    d = dict(CAST[who], **MOODS[mood])
    if who in TRACK:
        shape = mouths.at(TRACK[who], t)
        if shape != 'rest':
            d['mouth'] = 'v:' + shape
    d['blink'] = F.blinking(t, BLINKS[who])
    if who == 'milburn':
        d['head_life'] = head_life()
    return d


_MOVES = {}


def moves():
    """(the moves file, the film's side) for the kit, read once."""
    if not _MOVES:
        import acting as AC
        _MOVES.update(AC=AC, desc=AC.load(FILM), film=AC.film_side(FILM))
    return _MOVES


def acted(shot, who, t):
    """(face sp, joints) for who's block in shot at film time t (story/milburn-moves.txt)."""
    m = moves()
    key = m['AC'].block_key(shot, who, m['desc']['shots']) if m['desc']['shots'].get(shot, {}).get('who') != who \
        else shot
    sp, _, _, j, _ = m['AC'].person(m['desc'], m['film'], key, t)
    return sp, j


# ================================================================================================= shot 1
_DESC = PL.load(FILM)
_PAINT = {layer: PL.painter(_DESC, 'cabinet', layer) for layer in ('back', 'mid', 'front')}
_seated_neck = 1.06                   # m above the floor: seat 0.46, hips 0.5, hips to neck 0.56


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
    neck_y = L.p(0.0, d, _seated_neck)[1]
    if _PAINT['mid']:
        _PAINT['mid'](img, cam, t)
    look, j = acted(shot_of(t), 'milburn', t)
    j['chair_draw'] = lambda *a, **k: None            # the room paints his chair
    j['pre'] = []
    j['mid'] = [lambda p, j2, view: p.img.alpha_composite(_table_layer(t))]   # the table between body and arms,
    neck_y -= j.get('bob', 0.0) * scale_at(pxm, sp)      # so his hands lie on the folder (study_pose's way);
    # seated drops the body by bob: his neck stays put
    person(img, 'milburn', 540, neck_y + FEET * scale_at(pxm, sp), pxm, 0.0, t, j, look)
    cut = int(L.p(0.0, 1.62, 0.76)[1]) + 60            # below the folder's near edge only the table shows: his
    img.alpha_composite(_table_layer(t).crop((0, cut, W, H)), (0, cut))   # shins drawn after it are covered again
    return img.convert('RGB')


# ================================================================================================= scenes 4 and 7: the reverse
_RPAINT = {layer: PL.painter(_DESC, 'reverse', layer) for layer in ('back', 'mid', 'front')}
SEATS = {'andy': (-0.3, 2.15), 'pat': (0.36, 2.15)}     # (x, depth) from the reverse's lens (its chairs' middles)
SPLIT = 560                                              # screen x between them: each one's table strip


def reverse(t):
    """Andy and Pat across the table from Milburn's seat (places view `reverse`), seated as Milburn is in shot 1: the
    table's front layer between each one's body and arms (cropped to their own side, so one never covers the other's
    hands), then the table's near part over both."""
    img = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    cam = B.Cam(1.0, 540, 960)
    B.SS = 1
    v = _DESC['views']['reverse']['camera']
    L = MS.LevelCam(v['up'], v['horizon'], v['lens'])
    _RPAINT['back'](img, cam, t)
    if _RPAINT['mid']:
        _RPAINT['mid'](img, cam, t)
    front = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    _RPAINT['front'](front, cam, t)
    shot = shot_of(t)
    for who in ('andy', 'pat'):
        x, d = SEATS[who]
        pxm = L.ppm(d)
        sp = CAST[who]
        X, neck_y = L.p(x, d, _seated_neck)
        look, j = acted(shot, who, t)
        j['chair_draw'] = lambda *a, **k: None
        j['pre'] = []
        side = front.crop((0, 0, SPLIT, H)) if who == 'andy' else front.crop((SPLIT, 0, W, H))
        ox = 0 if who == 'andy' else SPLIT
        j['mid'] = [lambda p, j2, view, side=side, ox=ox: p.img.alpha_composite(side, (ox, 0))]
        neck_y -= j.get('bob', 0.0) * scale_at(pxm, sp)
        person(img, who, X, neck_y + FEET * scale_at(pxm, sp), pxm, 0.0, t, j, look)
    cut = int(L.p(0.0, 1.62, 0.76)[1]) + 60
    img.alpha_composite(front.crop((0, cut, W, H)), (0, cut))
    return img.convert('RGB')


def _table_layer(t):
    """The front layer (table, folders, glasses, name card) on its own, to lay between Milburn's body and arms."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if _PAINT['front']:
        _PAINT['front'](im, B.Cam(1.0, 540, 960), t)
    return im


# ================================================================================================= shot 2a
NEETS = [('waif', -0.26, 6.2), ('swindon', 0.26, 4.8), ('rangy', 0.58, 3.6), ('goth', -0.44, 2.6)]   # far to near


def shaft_shot(t):
    _, lt = scene_of(t)
    t0, t1 = 0.0, T['light_on_them'] - SHOTS[1][1]
    lit = MS.light_line(lt, t0, t1)
    img = MS.shaft(lt, lit).convert('RGBA')
    L = MS.SHAFT_CAM
    ppl = Image.new('RGBA', img.size, (0, 0, 0, 0))
    for who, x, d in NEETS:
        X, Y = L.p(x, d, 0.0)
        look, j = acted('2a', who, t)
        person(ppl, who, X, Y, L.ppm(d), 0.0, t, j, look)
    u = max(0.0, min(1.0, (2.4 - lit) / 1.0))       # the light reaching them (critique r1: they must change):
    rgb = ppl.convert('RGB')                         # in the shaft's shade, cool and dim; then lit warm
    dim = Image.blend(rgb, Image.new('RGB', rgb.size, (34, 40, 66)), 0.45 * (1 - u))
    lit_im = Image.blend(dim, Image.new('RGB', rgb.size, (255, 230, 170)), 0.24 * u)
    ppl = Image.merge('RGBA', (*lit_im.split(), ppl.split()[3]))
    img.alpha_composite(ppl)
    return img.convert('RGB')


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


# ================================================================================================= scene 3: arming
import milburn_props as MP           # noqa: E402
FIELD3 = [('rangy', -0.86, 5.0), ('waif', -0.32, 5.4), ('swindon', 0.22, 4.7), ('goth', 0.74, 4.4)]   # Sam (chat
# 6): seen side by side, a loose row across the frame (each a little nearer or further), still turned to us; the goth
# at the right end aims out of the frame, the rangy lad's blade points out at the left
PLINTHS3 = [(-0.55, 6.7, None), (0.02, 7.5, None), (0.58, 6.5, None), (1.22, 7.1, None),   # the four emptied, behind
            (-0.62, 3.9, 'stapler'), (0.72, 4.1, 'mace')]  # near corners: the stapler ("DLC") and the mace still on theirs


def _hoist(t):
    """0 -> 1: the goth's crossbow from across her hips up onto her shoulder (lands on "arm themselves")."""
    a = word_at(3, 'arm themselves')
    return MS.ease(min(1.0, max(0.0, (t - (a - 0.45)) / 0.65)))


def _mix(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


def arming(who, t):
    """(face sp, joints) for scene 3 (acting list row 3): the weapons in their hands, the moves on line 3."""
    sp = CAST[who]
    j = V.standing(sp)
    sw = sp.get('shoulders', 150) / 2.0
    if who == 'goth':                                   # raises the heavy crossbow to her shoulder, aiming off
        u = _hoist(t)                                   # the right of the frame, pleased
        V.arm_to(j, 'R', _mix((70, 330, 120), (sw * 0.35, 50, 150), u), 'down', 'fist')
        V.arm_to(j, 'L', _mix((-130, 330, 160), (-sw * 0.1, 70, 430), u), 'down', 'fist')
        MP.in_hands(j, sp, 'crossbow', 'R', 'L', along=-0.06)
        j['lean'] = 3.0 * u
        mood = 'pleased' if u < 0.9 else 'grim'
    elif who == 'rangy':                                # holds the katana out flat in front and stares at it, unsure
        a = word_at(3, 'arm themselves')
        u = MS.ease(min(1.0, max(0.0, (t - (a - 0.3)) / 0.7)))
        V.arm_to(j, 'R', _mix((90, 360, 80), (70, 220, 190), u), 'down', 'fist')
        V.arm_to(j, 'L', _mix((-60, 380, 90), (10, 215, 430), u), 'down', 'palm')
        MP.in_hands(j, sp, 'katana', 'R', 'L', along=0.0)
        j['nod'] = 5.0 * u
        mood = 'nervous'
    elif who == 'swindon':                              # twin uzis out in front, spraying at invisible targets
        a0 = word_at(3, 'Each')
        kick = [0.0, 0.0]
        for i, tt in enumerate(np.arange(a0 + 0.9, 15.0, 0.42)):
            k = i % 2
            kick[k] = max(kick[k], max(0.0, 1 - abs(t - tt) / 0.12))
        sway = math.sin((t - a0) * 2.6)
        for side, sg, kk in (('R', 1, kick[0]), ('L', -1, kick[1])):
            V.arm_to(j, side, (sg * (sw * 0.55), 130 - 40 * sway * sg - 30 * kk, 330 - 50 * kk), 'down', 'fist')
            MP.in_hands(j, sp, 'uzi', side, None, ang=-12 * sway * sg - 25 * kk, along=-0.02)
        mood = 'thrilled'
    else:                                               # the waif clutches the grenade to her chest, shaking
        for side, sg in (('R', 1), ('L', -1)):
            V.arm_to(j, side, (sg * 55, 200, 150), 'down', 'palm')
        MP.in_hands(j, sp, 'grenade', 'R', None, ang=-90, along=-0.0)
        j['lean'] = 2.0
        mood = 'terrified'
    d = face_sp('3', who, t, mood)
    if who == 'rangy':
        d['gaze_dy'] = 0.6
    if who == 'swindon' and word_at(3, 'Each') + 1.2 < t < 14.6:   # mouths "pow" silently (Sam Q4 N)
        d['mouth'] = 'v:O' if int((t - 12.0) / 0.21) % 2 == 0 else 'v:M'
    if who == 'waif':
        d['head_roll'] = 2.0 * math.sin(t * 2 * math.pi * 7)
        j['shake_x'] = 4.0 * math.sin(t * 2 * math.pi * 9)
    return d, j


YAW3 = 40.0                          # Sam (chat 6, the BoJack frames): turned three-quarter to screen right, the
#                                     camera at their side; faces still read, their focus off the right edge


def field_level_shot(t):
    from PIL import ImageDraw
    img = MS.field_level(t).convert('RGBA')
    L = MS.LEVEL_CAM
    things = [(d, 'plinth', (x, d, pr)) for x, d, pr in PLINTHS3] + [(d, 'who', (w, x, d)) for w, x, d in FIELD3]
    for d, kind, a in sorted(things, key=lambda q: -q[0]):
        if kind == 'plinth':
            lay = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0))
            MP.plinth(ImageDraw.Draw(lay), L, a[0], a[1], a[2], ss=2)   # Sam (chat 6): no "DLC" sign
            img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
        else:
            who, x, dd = a
            X, Y = L.p(x, dd, 0.0)
            look, j = arming(who, t)
            X += j.pop('shake_x', 0.0) * scale_at(L.ppm(dd), CAST[who])
            person(img, who, X, Y, L.ppm(dd), YAW3, t, j, look)
    return img.convert('RGB')


# ================================================================================================= picture
def picture(t):
    n = shot_of(t)
    if n in ACROSS:
        return cabinet(t)
    if n in REVERSE:
        return reverse(t)
    if n == '2a':
        return shaft_shot(t)
    if n == '3':
        return field_level_shot(t)
    if n == '6':
        return forest_shot(t)
    return field_shot(t)


def frame_image(t):
    return picture(t)


def cast(out):
    return PK.sheet(FILM, out)


# ================================================================================================= sound and render
def _standin(i, ln):
    """A robotic stand-in for line i (espeak-ng), only for timing until Sam records: spoken at the rate that fills
    the line's stand-in span, cached in source/data. Sam's take replaces it (then 'audio' on the line)."""
    import shutil
    import subprocess
    import numpy as np
    from burnham_film import load
    want = ln['end'] - ln['start']
    path = os.path.join(HERE, 'data', f'standin-milburn-{i + 1}.wav')
    if not os.path.exists(path) and shutil.which('espeak-ng'):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        rate = 150
        for _ in range(3):                          # a word rate that fills the span
            subprocess.run(['espeak-ng', '-v', 'en-gb', '-s', str(rate), '-p', '35', '-w', path, ln['text']],
                           check=True, stdout=subprocess.DEVNULL)
            got = len(load(path)) / 48000
            rate = int(rate * got / want)
    if not os.path.exists(path):
        return np.zeros(int(48000 * want))
    x = load(path)
    return x / (np.abs(x).max() + 1e-9) * 0.4


def soundtrack():
    import numpy as np
    n = int((DUR + 0.3) * 48000)
    mix = np.zeros(n)
    for i, ln in enumerate(LINES):
        x = _standin(i, ln)
        s = int(ln['start'] * 48000)
        mix[s:s + len(x)] += x[:max(0, n - s)]
    return mix


def final(out, small=False, span=None):
    import film_engine as E
    import mossad_audio as MA
    E.render(NAME, out, size=(540, 960) if small else (1080, 1920), ss=1 if small else 2, fps=FPS, dur=DUR,
             picture=picture, overlay=lambda img, t: img, shot_of=shot_of, sound=soundtrack, write_wav=MA.write_wav,
             set_ss=lambda v: setattr(B, 'SS', v), crf=26 if small else 20, span=span)


head_life()                          # rule 74: filled at load, so the checks see it


def main(argv):
    if len(argv) >= 3 and argv[1] == 'final':
        a = argv
        final(a[2], '--small' in a, (float(a[a.index('--span') + 1]), float(a[a.index('--span') + 2]))
              if '--span' in a else None)
    elif len(argv) >= 3 and argv[1] == 'stills':
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
