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

from PIL import Image, ImageDraw

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
    dict(who='milburn', text='The essence of my report is quite simple.', start=0.4, end=2.9),
    dict(who='milburn', text='Those not in education, employment or training will be presented with a unique '
                             'opportunity to serve their country.', start=3.5, end=9.0),
    dict(who='milburn', text='Each NEET will have to arm themselves before heading further into the Zone.', start=10.1,
         end=13.8),
    dict(who='andy', text="God damnit, Milburn. You're pulling a Hunger Games slash Battle Royale on us, aren't you?",
         start=14.1, end=18.8),
    dict(who='milburn', text='This report has been long in the making. Would you care to hear the findings or would '
                             'you prefer to interrupt?', start=19.3, end=25.5),
    dict(who='pat', text="I'd like to hear where this one goes, Prime Minister.", start=26.1, end=28.9),
    dict(who='andy', text='Fine! Continue.', start=29.5, end=30.7),
    dict(who='milburn', text='The NEETs will form a unit.', start=31.8, end=33.7),
    dict(who='milburn', text='And will encounter teams of their erstwhile colleagues.', start=36.2, end=38.8),
    dict(who='andy', text="You fucker! You're pulling a Maze Runner, Squid Games, Fortnite on me!", start=39.1,
         end=42.8),
    dict(who='milburn', text='I am sorry that you feel that way.', start=43.5, end=46.0),
    dict(who='andy', text='Are you or are you not sending NEETs to kill each other on live TV?', start=46.8, end=51.3),
    dict(who='milburn', text='My report is nuanced and multifaceted. I also recommend taking away PIP after they receive '
                             'their life-changing injuries in the Blood Dome.', start=52.9, end=60.3),
    dict(who='pat', text='I think the backbenchers will like this one, sir.', start=61.5, end=64.3),
]
import milburn_voice as V_       # noqa: E402  Sam's recordings (18 Nov): the lines' real times, every cut and beat
for _i, _ln in enumerate(LINES):    # the stand-in times above are only the old film's; the takes set the clock now
    _ln.update(start=V_.START[_i + 1], end=V_.END[_i + 1], audio='milburn-' + '+'.join(V_.TAKES[_i + 1]))
    _ln.update(_voice=V_.VOICES[_i + 1], _stretches=V_.LINES_TIMED[_i + 1]['stretches'], n=_i + 1)   # the checks measure the cleaned take the film plays, not the raw file
LINES[9]['bleep'] = V_.LINES_TIMED[10]['bleep']             # "fucker": Sam says it, a tone goes over "fuck" (rule 26)
SHOTS, T, _FOREST, DUR = V_.shots_and_beats({_i + 1: _ln['text'] for _i, _ln in enumerate(LINES)})
#   T: 'simple' shot 1 lands on "simple"; 'light_on_them' 2a: the light reaches their heads ("training"); 'locks' 2b:
#   the deck locks level with the grass; 'gunfire' / 'flame' / 'stars' scene 6 beats; 'glance' 7d: Milburn's eyes
#   slide aside; 'gape' 7e: Andy's mouth falls open
_FOUR = ['goth', 'rangy', 'swindon', 'waif']
REVERSE = ('4a', '4c', '7a', '7c', '7e')            # the reverse: Andy and Pat across the table
ACROSS = ('1', '4b', '7b', '7d')                     # shot 1's camera: Milburn
SHOT_CAST = dict({'2a': _FOUR, '2b': _FOUR, '3': _FOUR, '6': _FOUR}, **{n: ['milburn'] for n in ACROSS},
                 **{n: ['andy', 'pat'] for n in REVERSE})
KEEP_CLEAR = [("Milburn's face", lambda t: (420, 580, 680, 960) if t < SHOTS[0][2] else None)]   # rule 75: the Hook Text sits above it
HOOK = ('The Milburn Report is released 😬', {'y': 420, 'until': 3.0, 'tilt': -7})   # rule 75: the band above his head
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
    THINGS={'table': dict(at=(0.0, 1.12), size=(5.2, 1.65, 0.76)), 'window': dict(at=(0.88, 3.42), size=(1.2, 0.1, 2.0), outside=True),
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
    hy = joints.pop('_head_yaw', None) if joints else None
    return V.person(img, cam, X, sole_y - FEET * s, s, dict(look or sp), t, yaw, joints, head_yaw=hy)


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
    'rage': dict(smile=-0.9, frown=0.14, lid4=0.08, squint=0.4),            # ... angrier still (scene 7); Sam note 1
    #       (18 Nov): brows at furious's 0.14 (0.16 tipped them into steep slashes through the glasses)
    'exasperated': dict(smile=-0.5, brow_up=0.03, frown=-0.01, lid4=0.05),   # "Fine!"
    'sulky': dict(smile=-0.6, lid4=0.34, frown=0.012),                      # arms folded, leaning back
    'despair': dict(smile=-0.7, brow_up=0.035, frown=-0.02, lid4=0.04),     # brows up in the middle
    'gape': dict(smile=-1.0, frown=0.14, squint=0.6, lid4=0.04),   # Sam note 1: brows as furious (frown 0.22 = a cartoon V)   # note 8: cross, not
    #       surprised: brows hard down and knitted, eyes narrowed, mouth open in outrage (was brows up: read as shock)
    'patient': dict(smile=0.12, lid4=0.3),                                  # Pat: calm, a little heavy-lidded
    'approving': dict(smile=0.4, lid4=0.3),                                 # ... the backbenchers will like it
    'attentive': dict(smile=0.15, lid4=0.2, brow_up=0.006),                 # Milburn: nonplussed, soft
    'sorry': dict(smile=0.2, lid4=0.24, brow_up=0.02, frown=-0.012),        # sorry-not-sorry
    'stoked': dict(smile=0.85, squint=0.45, lid4=0.14, brow_up=0.015, mouth='v:grin'),   # the goth, crossbow up: "sick, this one's mine"
    'focused': dict(smile=-0.1, squint=0.7, lid4=0.12, frown=0.1),          # the goth in combat: jaw set, eyes narrowed on the target
    'grim': dict(smile=0.25, lid4=0.3, frown=0.02),                         # the goth, pleased and dangerous
    'thrilled': dict(smile=0.8, squint=0.6, lid4=0.1),                      # Swindon, firing back
    'aghast': dict(smile=-0.6, brow_up=0.05, lid4=0.0, mouth='v:O'),        # the rangy lad
    'terrified': dict(smile=-0.7, brow_up=0.05, frown=-0.02, lid4=0.0),     # the waif
    'eyes shut': dict(smile=-0.7, frown=0.02, blink_hold=True),             # the waif, curled up
}


def word_at(n, words):
    """When line n reaches `words`: its syllables spread over where the recording really speaks."""
    ln = LINES[n - 1]
    k = len(ln['text'][:ln['text'].index(words)].split())
    return V_.word_times(n, ln['text'])[k][1]


import mouths                        # noqa: E402  (the house lip sync: shapes from the words, on the stand-in timing)
import figure as F                   # noqa: E402
TRACK = {}
for _ln in LINES:
    _lt = V_.LINES_TIMED[LINES.index(_ln) + 1]
    TRACK.setdefault(_ln['who'], []).extend((a + _ln['start'], b + _ln['start'], sh) for a, b, sh in
                                            mouths.track(_ln['text'], _lt['stretches'], _lt['env']))
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
        for k, who in enumerate(('milburn', 'andy', 'pat')):    # each on their own lines' loudness only
            mask = np.zeros(len(env))                           # (chat 10: Andy and Pat too, rule 74)
            for ln in LINES:
                if ln['who'] == who:
                    mask[int(ln['start'] * FPS):int(ln['end'] * FPS) + 1] = 1.0
            HEAD_LIFE[who] = headlife.HeadLife(env * mask, 0.0, fps=FPS, seed=21 + k)
    return HEAD_LIFE['milburn']


def face_sp(shot, who, t, mood, shades=None):
    """The moves kit's seam: who's build with the face for a mood, lips on their own lines, blinks."""
    d = dict(CAST[who], **MOODS[mood])
    if who in TRACK:
        shape = mouths.at(TRACK[who], t)
        if shape != 'rest':
            d['mouth'] = 'v:' + shape
    d['blink'] = F.blinking(t, BLINKS[who])
    if who in ('milburn', 'andy', 'pat'):
        head_life()
        d['head_life'] = HEAD_LIFE[who]
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
    sp, _, _, j, hy = m['AC'].person(m['desc'], m['film'], key, t)
    if hy is not None:
        j['_head_yaw'] = hy                       # note 7: `keys head_yaw` turns the head (person() passes it on)
    return sp, j


# ================================================================================================= shot 1
_DESC = PL.load(FILM)
_PAINT = {layer: PL.painter(_DESC, 'cabinet', layer) for layer in ('back', 'mid', 'front', 'over')}
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
    if _PAINT['over']:                                 # the name card, nearest of all: no sleeve or hand over it
        _PAINT['over'](img, cam, t)
    return img.convert('RGB')


# ================================================================================================= scenes 4 and 7: the reverse
_RPAINT = {layer: PL.painter(_DESC, 'reverse', layer) for layer in ('back', 'mid', 'front', 'over')}
SEATS = {'andy': (-0.35, 2.2), 'pat': (0.35, 2.2)}       # (x, depth) from the reverse's lens: equal and centred (Sam, chat 11)
SPLIT = 540                                              # screen x between them: each one's table strip


def reverse(t):
    """Andy and Pat across the table from Milburn's seat (places view `reverse`), seated as Milburn is in shot 1: the
    table's front layer between each one's body and arms (cropped to their own side, so one never covers the other's
    hands), then the table's near part over both."""
    img = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    cam = B.Cam(1.0, 540, 960)
    B.SS = 1
    v = _DESC['views']['reverse']['camera']
    L = MS.LevelCam(v['up'], v['horizon'], v['lens'], v.get('centre', 540.0))
    _RPAINT['back'](img, cam, t)
    if _RPAINT['mid']:
        _RPAINT['mid'](img, cam, t)
    front = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    _RPAINT['front'](front, cam, t)
    shot = shot_of(t)
    for who in ('pat', 'andy'):                    # Sam's note (chat 11): Andy, the nearer, drawn last, so Pat's
        x, d = SEATS[who]                         # table strip never covers the half of Andy's arm that crosses it
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
    if _RPAINT['over']:                               # note 10: the drinks on their coasters, nearest of all
        _RPAINT['over'](img, cam, t)
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
FIELD3 = [('goth', -0.55, 3.0), ('rangy', 0.05, 5.6), ('swindon', 1.05, 7.4), ('waif', -0.46, 6.6)]   # Sam (chat 11):
# a clear diagonal: the goth front left, the rangy lad dead centre, Swindon back right, the waif in the gap at back left
PLINTHS3 = [(-0.12, 3.3, 'goth'), (0.55, 5.9, 'rangy'), (1.5, 7.7, 'swindon'), (-0.95, 6.9, None)]   # each one's own, just
#   in front of them on the side they face (the weapon taken off it); the stapler and mace plinths gone (Sam, chat 11)


def _hoist(t):
    """0 -> 1: the goth's crossbow from across her hips up onto her shoulder (lands on "arm themselves")."""
    a = word_at(3, 'arm themselves')
    return MS.ease(min(1.0, max(0.0, (t - (a - 0.45)) / 0.65)))


def _mix(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


def _picked(who, t):
    """0 -> 1: how far `who` has lifted their weapon off the plinth (0: it still lies there, their hands on it)."""
    if who == 'goth':
        return _hoist(t)
    if who == 'rangy':
        a = word_at(3, 'arm themselves')
        return MS.ease(min(1.0, max(0.0, (t - (a - 0.3)) / 0.7)))
    if who == 'swindon':
        return MS.ease(min(1.0, max(0.0, (t - (word_at(3, 'Each') + 0.1)) / 0.6)))
    return 1.0


ON_PLINTH = {'goth': 'crossbow', 'rangy': 'katana', 'swindon': 'uzi'}


def arming(who, t):
    """(face sp, joints) for scene 3 (acting list row 3): the weapons in their hands, the moves on line 3."""
    sp = CAST[who]
    j = V.standing(sp)
    sw = sp.get('shoulders', 150) / 2.0
    if who == 'goth':                                   # raises the heavy crossbow to her shoulder, aiming off
        u = _hoist(t)                                   # the right of the frame, pleased
        V.arm_to(j, 'R', _mix((sw * 0.35, 150, 170), (sw * 0.35, 50, 150), u), 'down', 'fist')   # Sam (chat 11): lifts it
        V.arm_to(j, 'L', _mix((-sw * 0.1, 170, 450), (-sw * 0.1, 70, 430), u), 'down', 'fist')  # off the plinth beside her,
        if u > 0.04:                                    # it to her shoulder, and (till then it lies on the plinth)
            MP.in_hands(j, sp, 'crossbow', 'R', 'L', along=-0.06)
        j['lean'] = 8.0 * (1 - u) + 3.0 * u                                             # is satisfied with it
        j['nod'] = 6.0 * u * (1 - _ramp(t, word_at(3, 'arm themselves') + 0.5, word_at(3, 'arm themselves') + 0.9) * 0.5)
        mood = 'stoked' if u > 0.3 else 'pleased'       # Sam (18 Nov): "yeah, sick, this is the weapon for me"
    elif who == 'rangy':                                # holds the katana out flat in front and stares at it, unsure
        a = word_at(3, 'arm themselves')
        u = MS.ease(min(1.0, max(0.0, (t - (a - 0.3)) / 0.7)))
        V.arm_to(j, 'R', _mix((90, 300, 330), (70, 220, 190), u), 'down', 'fist')   # Sam (chat 11): off the plinth,
        V.arm_to(j, 'L', _mix((110, 300, 560), (10, 215, 430), u), 'down', 'palm')  # then held up and stared at
        if u > 0.04:
            MP.in_hands(j, sp, 'katana', 'R', 'L', along=0.0)
        j['nod'] = 5.0 * u
        j['lean'] = 7.0 * (1 - u)
        mood = 'nervous'
    elif who == 'swindon':                              # twin uzis out in front, spraying at invisible targets
        a0 = word_at(3, 'Each')
        kick = [0.0, 0.0]
        for i, tt in enumerate(np.arange(a0 + 0.9, SHOTS[3][1] - 0.3, 0.42)):
            k = i % 2
            kick[k] = max(kick[k], max(0.0, 1 - abs(t - tt) / 0.12))
        sway = math.sin((t - a0) * 2.6)
        up = MS.ease(min(1.0, max(0.0, (t - (a0 + 0.1)) / 0.6)))   # Sam (chat 11): both uzis off the plinth, then aimed
        for side, sg, kk in (('R', 1, kick[0]), ('L', -1, kick[1])):
            V.arm_to(j, side, _mix((sg * sw * 0.45, 400, 280), (sg * (sw * 0.55), 130 - 40 * sway * sg - 30 * kk,
                                                                   330 - 50 * kk), up), 'down', 'fist')
            if up > 0.04:
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
    if who == 'swindon' and word_at(3, 'Each') + 1.2 < t < SHOTS[3][1] - 0.7:   # mouths "pow" silently (Sam Q4 N)
        d['mouth'] = 'v:O' if int((t - 10.7) / 0.21) % 2 == 0 else 'v:grin'   # note 6: was 'v:M' (no such shape)
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
            prop = ON_PLINTH.get(a[2]) if a[2] and _picked(a[2], t) <= 0.04 else None   # still lying there
            MP.plinth(ImageDraw.Draw(lay), L, a[0], a[1], prop, ss=2)   # Sam (chat 6): no "DLC" sign
            img.alpha_composite(lay.resize((W, H), Image.LANCZOS))
        else:
            who, x, dd = a
            X, Y = L.p(x, dd, 0.0)
            look, j = arming(who, t)
            X += j.pop('shake_x', 0.0) * scale_at(L.ppm(dd), CAST[who])
            person(img, who, X, Y, L.ppm(dd), YAW3, t, j, look)
    return img.convert('RGB')


# ================================================================================================= scene 6: the forest
import milburn_forest as MF          # noqa: E402
import moves as MO                   # noqa: E402
FOREST6 = [('goth', 0.5, 3.8), ('swindon', -0.25, 4.3), ('rangy', -1.0, 4.8), ('waif', -1.75, 5.3)]   # single
# file walking right, leader first; staggered back in depth so all four read in the tall frame (0.75 m apart, not
# the plan's 1.4: the plan's spacing puts the last one off the left edge)
CLOSE6 = {'rangy': 0.12, 'waif': 0.25}   # m: the back two close up on "unit"
GOTH_SHOTS = (MF.T_FLAME + 1.0, MF.T_FLAME + 2.6)   # note 9: the goth looses a bolt, cocks, looses another
SKY_SHOT = MF.T_GUN + 0.1                           # Sam (chat 11): the first gunfire makes her jerk and loose a bolt
#                                                     straight up into the air in surprise


def _sky(t):
    """0 -> 1 -> 0: the goth's crossbow jerked up skyward on the first gunfire, then lowered again."""
    return _ramp(t, MF.T_GUN, SKY_SHOT) * (1 - _ramp(t, SKY_SHOT + 0.35, SKY_SHOT + 0.8))
RETREAT = 0.5                           # m the goth backs off (leftwards on screen), from the flame's first lick to the end of the shot
RET0, RET1 = MF.T_FLAME + 0.4, MF.T1 - 0.2
HALT = 0.25                              # s: they stop dead on the gunfire (the camera takes MF.STOP)


def _ramp(t, a, b):
    return MS.ease(min(1.0, max(0.0, (t - a) / (b - a))))


def walked(who, t):
    """How far `who` has walked (m, across the screen) since the shot began: the camera's pace, stopping dead on
    the gunfire, plus the back two closing up on "unit"."""
    v = MF.V_EFF
    if t <= MF.T_GUN:
        d = v * (t - MF.T0)
    else:
        u = min(1.0, (t - MF.T_GUN) / HALT)
        d = v * (MF.T_GUN - MF.T0) + v * HALT * (u - u * u / 2)
    a = word_at(8, 'unit')
    d += CLOSE6.get(who, 0.0) * _ramp(t, a - 0.3, a + 0.4)
    if who == 'goth':                                # Sam (18 Nov): under fire she backs off along the line, loosing bolts
        d -= RETREAT * _ramp(t, RET0, RET1)          # as she goes (the others are staggered in depth, so none is walked through)
    return d


def _crouch(j, amt, lean):
    """Lower the body `amt` person units with the feet kept on the floor (knees bend), leaning forward."""
    j['bob'] = j.get('bob', 0.0) + amt
    for side in 'LR':
        if 'foot' + side in j:
            fx, fy, fz = j['foot' + side]
            j['foot' + side] = (fx, fy - amt, fz)
    j['lean'] = j.get('lean', 0.0) + lean


def forest_pose(who, t):
    """(face sp, joints, firing) for scene 6 (acting rows 8 and 9): walking with their weapons, the jolt on the
    gunfire, everyone ducking the flame, then each one's own answer; `firing`: Swindon's guns going off."""
    sp = CAST[who]
    k = MP.units_per_m(sp)
    tau = walked(who, t) / MF.V_EFF
    j = MO.gait(sp, tau, 'walk', stride=0.45 * k)
    stop = _ramp(t, MF.T_GUN, MF.T_GUN + HALT)
    if stop > 0:
        if who == 'goth':                              # she keeps walking, backwards, once the flame comes
            stop *= 1 - _ramp(t, RET0 - 0.2, RET0 + 0.1)
        j = MO.mix_poses(j, V.standing(sp), stop)
    sw = sp.get('shoulders', 150) / 2.0
    unit = word_at(8, 'unit')
    jolt = max(0.0, 1 - abs(t - (MF.T_GUN + 0.08)) / 0.12)
    duck = _ramp(t, MF.T_FLAME - 0.05, MF.T_FLAME + 0.2) * (1 - 0.4 * _ramp(t, MF.T_FLAME + 1.45, MF.T_FLAME + 2.0))   # held till the flame dies (critique r2)
    after = _ramp(t, MF.T_FLAME + 0.3, MF.T_FLAME + 0.7)        # each one's own answer to the ambush
    shock = MF.T_GUN < t < MF.T_FLAME + 0.4
    firing = []
    flail = _ramp(t, MF.T_GUN + 0.05, MF.T_GUN + 0.3)           # note 9: the waif flails from the first shots
    if who == 'goth':                                   # crossbow shouldered, pleased; a cool sway aside from the flame,
        kick = max([max(0.0, 1 - abs(t - tt) / 0.12) for tt in GOTH_SHOTS])      # then aims and looses bolts (note 9)
        V.arm_to(j, 'R', _mix((sw * 0.35, 50, 150), (sw * 0.3 - 20 * kick, -10 + 25 * kick, 170 - 40 * kick), after),
                 'down', 'fist')
        V.arm_to(j, 'L', _mix((-sw * 0.1, 70, 430), (-sw * 0.05, -150 + 20 * kick, 430 - 40 * kick), after),
                 'down', 'fist')
        sky = _sky(t)                                   # Sam (chat 11): jerked skyward, a bolt straight up
        if sky > 0:
            V.arm_to(j, 'R', _mix((sw * 0.35, 50, 150), (sw * 0.3, -30, 210), sky), 'down', 'fist')
            V.arm_to(j, 'L', _mix((-sw * 0.1, 70, 430), (-sw * 0.05, -290, 440), sky), 'down', 'fist')
        shots = (SKY_SHOT,) + tuple(GOTH_SHOTS)          # Sam (chat 11): the bolt leaves the crossbow; she reloads
        empty = any(tt <= t < (nxt - 0.6 if nxt else 99) for tt, nxt in zip(shots, shots[1:] + (None,)))   # before the next
        MP.in_hands(j, sp, 'crossbow_empty' if empty else 'crossbow', 'R', 'L', along=-0.06)
        j['head_roll'] = j.get('head_roll', 0.0) - 9 * duck     # she leans aside, barely bothered
        if RET0 < t < RET1:                             # Sam (18 Nov): backing off, ducking and weaving as she fires
            wv = math.sin((t - RET0) * 2 * math.pi * 1.5)
            j['bob'] = j.get('bob', 0.0) + 22 * max(0.0, -wv)         # dips under the fire
            j['lean'] = j.get('lean', 0.0) - 5 - 5 * wv                # leaning back and weaving
            j['head_roll'] = j.get('head_roll', 0.0) + 5 * wv
        mood = ('aghast' if (MF.T_GUN < t < MF.T_FLAME + 0.4) else          # Sam (18 Nov): in combat she concentrates,
                'focused' if t > MF.T_GUN else 'pleased')                   # no grin, once the flame is on
    elif who == 'rangy':                                # the katana out in front like a torch; ducks too deep, then
        sw_t = t - MF.T_STARS                           # hacks wildly at the morning stars over his head (note 9)
        hack = math.sin(sw_t * 2 * math.pi * 1.6) if 0.0 < sw_t < 2.2 else 0.0
        if after < 0.5:                                 # the torch hold (both hands, blade up)
            V.arm_to(j, 'R', _mix((60, 150, 210), (40, -120, 200), after * 2), 'down', 'fist')
            V.arm_to(j, 'L', _mix((40, -30, 300), (40, -170, 200), after * 2), 'down', 'palm')
            MP.in_hands(j, sp, 'katana', 'R', 'L', along=0.0)
        else:                                           # one-handed hacks: up-back to chopping forward
            V.arm_to(j, 'R', (-20 - 50 * hack, -260 + 50 * hack, 180), 'down', 'fist')   # (figures drawn mirrored: -x is ahead)
            V.arm_to(j, 'L', (-120, -60, 160), 'down', 'palm')
            MP.in_hands(j, sp, 'katana', 'R', None, ang=-125 - 35 * hack, along=0.0)   # critique r2: never across his face
        j['head_roll'] = j.get('head_roll', 0.0) + 6 * hack
        mood = 'aghast' if t > MF.T_GUN else 'nervous'
    elif who == 'swindon':                              # uzis up at his chest swinging side to side; forward on "unit";
        sway = math.sin((t - MF.T0) * 3.0)              # sprays back wildly once the flame has passed
        fwd = _ramp(t, unit - 0.25, unit + 0.1) * (1 - _ramp(t, unit + 0.5, unit + 0.9))
        kick = [0.0, 0.0]
        spray = MF.T_FLAME + 0.45 < t < MF.T1 - 1.0
        if spray:
            for i, tt in enumerate(np.arange(MF.T_FLAME + 0.45, MF.T1 - 1.0, 0.14)):
                kick[i % 2] = max(kick[i % 2], max(0.0, 1 - abs(t - tt) / 0.07))
            sway = math.sin(t * 7.0)
        for side, sg, kk in (('R', 1, kick[0]), ('L', -1, kick[1])):
            V.arm_to(j, side, (sg * sw * 0.55, 130 - 40 * sway * sg - 30 * kk - 40 * fwd,
                               330 + 120 * fwd - 50 * kk), 'down', 'fist')
            ang = -12 * sway * sg - 25 * kk - 10 * fwd - (38 if spray else 0)
            MP.in_hands(j, sp, 'uzi', side, None, ang=ang, along=-0.02)
            if kk > 0.5:
                firing.append((side, ang))
        mood = 'aghast' if shock else 'thrilled'
    else:                                               # hugs the grenade, terrified, eyes darting; from the gunfire
        w1 = math.sin((t - MF.T_GUN) * 2 * math.pi * 2.3)          # she waves it over her head, freaking out
        w2 = math.sin((t - MF.T_GUN) * 2 * math.pi * 3.1 + 1.0)    # (note 9: no curling round it)
        Rh = _mix((55, 200, 150), (280 + 80 * w1, -330 + 40 * abs(w1), 40), flail)   # up to her side: face clear
        Lh = _mix((-55, 200, 150), (-190 - 50 * w2, -230 + 70 * w2, -10), flail)
        V.arm_to(j, 'R', Rh, 'down', 'palm')
        V.arm_to(j, 'L', Lh, 'down', 'palm')
        MP.in_hands(j, sp, 'grenade', 'R', None, ang=-90 + 50 * w1 * flail, along=-0.0)
        mood = 'terrified'
    _crouch(j, -40 * jolt, 0.0)
    deep, lean = {'waif': (0.7, 10), 'rangy': (1.25, 26), 'goth': (1.3, -10), 'swindon': (0.95, 30)}[who]   # note 9:
    _crouch(j, 190 * duck * deep, lean * duck)          # goth sinks and leans back, cool; Swindon dives forward; rangy
                                                        # ducks deepest; all clear of the flame (critique r2)
    if who == 'swindon':                                # a cocky bob under the morning star, still firing (note 9)
        _bob = max(0.0, 1 - abs(t - (MF.T_STARS + 0.25)) / 0.3)        # on the morning star's pass (was a fixed 36.85 s from the old
        _crouch(j, 150 * _bob, 10 * _bob)                               # clock: it fired while they were still walking; Sam 18 Nov)
    d = face_sp('6', who, t, mood)
    if who == 'rangy' and t < MF.T_GUN:
        d['gaze_dy'] = 0.5 * (math.sin(t * 2.3) > 0)        # glancing down at the blade
    if who == 'swindon' and not shock:                  # note 6: his grin must read (closed lips read as no mouth)
        d['mouth'] = ('v:O' if int(t / 0.21) % 2 == 0 else 'v:grin') if spray else 'v:grin'
    if who == 'waif':
        if t < MF.T_GUN:
            d['look'] = 0.5 * math.sin(t * 5.0)             # eyes darting
        else:                                               # screaming, eyes everywhere (note 9)
            d['look'] = 0.7 * math.sin(t * 7.0)
            d['mouth'] = 'v:O'
        j['shake_x'] = (4.0 + 6.0 * flail) * math.sin(t * 2 * math.pi * 9)
    return d, j, firing


def forest_shot(t):
    img = MF.behind(t)
    MF.gunfire(img, t)
    cx = MF.cam_x(t)
    for who, x0, dd in sorted(FOREST6, key=lambda q: -q[2]):
        look, j, firing = forest_pose(who, t)
        pxm = MF.CAM.ppm(dd)
        s = scale_at(pxm, CAST[who])
        X, Y = MF.CAM.p(x0 + walked(who, t) - cx, dd, 0.0)
        X += j.pop('shake_x', 0.0) * s
        pts = person(img, who, X, Y, pxm, YAW3, t, j, look)
        for side, ang in firing:                        # Swindon's muzzles: the hand plus the gun's length
            hx, hy = pts['wr' + side]
            a = math.radians(ang)
            gx = X + hx * s + math.cos(a) * 0.4 * pxm
            gy = Y - FEET * s + (hy + j.get('bob', 0.0)) * s + math.sin(a) * 0.4 * pxm - 0.05 * pxm
            MF.muzzle(img, gx, gy, pxm, int(t * 97) + (side == 'L'), 0.16)
        if who == 'goth' and 0.0 <= t - SKY_SHOT < 0.5:   # Sam (chat 11): the surprised bolt, straight up
            u = t - SKY_SHOT
            hx, hy = pts['wrL']
            bx = X + hx * s + (0.15 + 1.2 * u) * pxm
            by = Y - FEET * s + (hy + j.get('bob', 0.0)) * s - (0.55 + 9.0 * u) * pxm
            dx, dy = 0.13 * pxm, -0.39 * pxm                # the bolt's length, pointing up the crossbow's line
            dr = ImageDraw.Draw(img)
            dr.line([(bx - dx, by - dy), (bx, by)], fill=(70, 50, 34), width=max(3, int(0.02 * pxm)))
            nx, ny = dx / 0.41 / pxm, dy / 0.41 / pxm         # unit along the bolt, then its tip
            px_, py_ = -ny, nx
            dr.polygon([(bx + 0.06 * pxm * nx, by + 0.06 * pxm * ny),
                        (bx + 0.025 * pxm * px_, by + 0.025 * pxm * py_),
                        (bx - 0.025 * pxm * px_, by - 0.025 * pxm * py_)], fill=(170, 176, 186), outline=(20, 20, 24))
        if who == 'goth':                               # note 9: her bolts streak off ahead, into the trees
            for tt in GOTH_SHOTS:
                u = t - tt
                if 0.0 <= u < 0.4:
                    hx, hy = pts['wrR']
                    bx = X + hx * s + (0.45 + 6.0 * u) * pxm
                    by = Y - FEET * s + (hy + j.get('bob', 0.0)) * s - 0.06 * pxm - 0.3 * u * pxm
                    dr = ImageDraw.Draw(img)
                    dr.line([(bx - 0.4 * pxm, by + 0.02 * pxm), (bx, by)], fill=(70, 50, 34),
                            width=max(3, int(0.02 * pxm)))
                    dr.polygon([(bx + 0.06 * pxm, by), (bx - 0.02 * pxm, by - 0.025 * pxm),
                                (bx - 0.01 * pxm, by + 0.03 * pxm)], fill=(170, 176, 186), outline=(20, 20, 24))
    MF.flame(img, t)
    MF.stars(img, t)
    img.alpha_composite(MF.in_front(t))
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
DUCK_TO = 0.3                       # ... and 30% of that (about -10 dB) while anyone speaks (Sam, 18 Nov: Y)
SFX_GAIN = 0.6                      # Sam (18 Nov): the effects at 60% so they don't overwhelm the dialogue
_SFX = {}


def _sfx(name):
    """One of Sam's sound effects (source/audio/milburn-sfx-NAME.mp3), as supplied."""
    if name not in _SFX:
        from burnham_film import load
        _SFX[name] = load(os.path.join(HERE, 'audio', f'milburn-sfx-{name}.mp3'))
    return _SFX[name]


def sfx_cues():
    """[(effect, film second it starts, seconds it may run or None, fade out)]: where each effect lands (Sam, 18 Nov:
    the lift as the deck rises, Swindon's uzis in the forest only (scene 3 he mimes 'pow pow': no sound, Sam 18 Nov), the gunfire, the flamethrower, the
    morning stars' blades, the goth's crossbow bolts)."""
    cues = [('lift', SHOTS[1][1], T['locks'] + 0.3 - SHOTS[1][1], 0.6),
            ('crossbow', SKY_SHOT, None, 0.1)]
    cues += [('ak47', MF.T_GUN, None, 0.2), ('ak47', MF.T_GUN + 2.1, MF.T1 - 2.0 - (MF.T_GUN + 2.1), 0.3),
             ('flamethrower', MF.T_FLAME - 0.3, 2.4, 0.5), ('uzi', MF.T_FLAME + 0.45, MF.T1 - 1.0 - MF.T_FLAME - 0.45, 0.4),
             ('dagger', MF.T_STARS - 0.2, None, 0.1), ('dagger', MF.T_STARS + 0.1, None, 0.1)]
    cues += [('crossbow', tt, None, 0.1) for tt in GOTH_SHOTS]
    return cues


def soundtrack():
    """Sam's recordings, cleaned and matched, each where its line starts (the swear bleeped), then the effects at 60%."""
    import numpy as np
    n = int((DUR + 0.3) * 48000)
    mix = np.zeros(n)
    for i, ln in enumerate(LINES):
        x = V_.bleeped(i + 1)
        st = int(ln['start'] * 48000)
        mix[st:st + len(x)] += x[:max(0, n - st)]
    fx = np.zeros(n)                                                   # the effects on their own, then ducked
    for name, t, span, fade in sfx_cues():
        x = _sfx(name)
        x = x[:int(span * 48000)].copy() if span is not None else x.copy()
        k = min(len(x), int(fade * 48000))
        if k:
            x[-k:] *= np.linspace(1, 0, k)
        st = int(t * 48000)
        fx[st:st + len(x)] += SFX_GAIN * x[:max(0, n - st)]
    duck = np.ones(n)                                                  # Sam (18 Nov, Y): under a speaking voice the
    for ln in LINES:                                                   # effects drop to DUCK_TO, and come back after
        duck[max(0, int((ln['start'] - 0.1) * 48000)):int((ln['end'] + 0.15) * 48000)] = DUCK_TO
    w = int(0.15 * 48000)                                              # eased over 150 ms so it never pumps or clicks
    duck = np.convolve(np.pad(duck, (w, w), mode='edge'), np.ones(w) / w, 'same')[w:-w]
    mix += fx * duck
    hot = np.abs(mix) > 0.9                                            # never clip: bend only what goes over 0.9
    mix[hot] = np.sign(mix[hot]) * (0.9 + 0.1 * np.tanh((np.abs(mix[hot]) - 0.9) / 0.1))
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


def caption_at(t):
    """The subtitle on screen at t (finish.py burns them in; rule 62), from LINES."""
    import subtitles as SUB
    return SUB.caption_at(LINES, t)
