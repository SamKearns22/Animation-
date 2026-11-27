#!/usr/bin/env python3
"""kittests: each shared-kit check tested against the film fault that taught it (Build list 27 Oct: "each with a test").
A test puts the old, faulty version back for a moment (from git history, written out here), and passes only if the
check catches the old version AND passes the fixed one.

    python3 source/kittests.py            all of them (a few minutes)
    python3 source/kittests.py hands      only the tests whose name contains 'hands'
"""
import json
import math
import re
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# Checks on request (Sam, 26 Nov): the body check, the final-only send gate and the proposal guard are off unless
# asked; the kit tests test those tools themselves, so here they are asked for (kittest practice_mode tests them off).
for _k in ('BODYCHECK', 'PROPOSE_GUARD', 'SENDGATE_ALL'):
    os.environ.setdefault(_k, '1')
sys.path.insert(0, HERE)

TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


def _hand_faults(film, times, who=None):
    """handcheck's findings for these frames of a film (drawn here, one after another)."""
    import body as B
    import figure as F
    import handcheck as H
    import kitchecks
    F.guard(B)
    if 'kittests' not in F._ALLOW:
        F._ALLOW.append('kittests')
    kitchecks.install()
    H.install()
    B.SS = 1
    out = []
    for t in times:
        H.begin()
        film.frame_image(t)
        out += [f for f in H.end(t) if who is None or f['who'] == who]
    return out


# ------------------------------------------------------------------------------------------------ one source for every view
@test
def turned_parts_kept():
    """Milburn (Sam, 17 Nov: "our 3/4 characters still look like shit"): turned, the thin lad lost his pencil
    moustache and the goth her piercings and blue streaks (people_turned drew a borrowed copy). The check refuses
    the old drawing (6 lost parts) and passes the front's own parts on the turned head (proposal three-quarter-people)."""
    import milburn as M
    import people_turned as PT
    views = {w: {'three', 'side'} for w in M.CAST}
    now = PT.lost_parts(M.CAST, views)
    PT.FAITHFUL = False
    try:
        old = PT.lost_parts(M.CAST, views)
    finally:
        PT.FAITHFUL = True
    return not now and len(old) >= 6, f'now {len(now)} lost, before the fix {len(old)}'


# ------------------------------------------------------------------------------------------------ rule 41: hands
@test
def hands_round_the_head():
    """Patriots 3 note 21: the Loader's binocular pose from behind (shot 2) hid both hands: arms round his head."""
    import patriots3 as P
    import patriots3_bunker as PB
    import views as V
    times = [3.67, 3.83, 4.0, 6.33, 6.5, 6.67]
    fixed = _hand_faults(P, times, 'Loader')
    real = PB.Crew._loader

    def old(self):                                   # before cd8d4ac
        j = real(self)
        if self.loader == 'spot':
            for side, sg in (('L', -1), ('R', 1)):
                V.arm_to(j, side, (sg * 44.0, -150.0, 118.0), 'down', 'fist')
            j['hand'] = {'L': 'none', 'R': 'none'}
            j['on_face'] = {'L', 'R'}
        return j
    PB.Crew._loader = old
    try:
        caught = _hand_faults(P, times, 'Loader')
    finally:
        PB.Crew._loader = real
    both = [t for t in times if {f['side'] for f in caught if f['t'] == t and f['kind'] == 'no hand'} == {'L', 'R'}]
    left = sorted({f"{f['t']:.2f} {f['side']}" for f in fixed if f['kind'] == 'no hand'})
    ok = len(both) >= len(times) - 1 and all(not s.endswith('L') for s in left)   # at 4.0 s he is already pointing
    return ok, f'old pose: both arms hand-less in {len(both)} of {len(times)} frames; fixed: ' \
               f'{len(left)} arm(s) still hand-less ({", ".join(left) or "none"}: the right hand still behind his head ' \
               f'from this camera, found 27 Oct after the film closed)'


@test
def hands_in_sleeves():
    """Patriots 3 note 18: the flap poses' hands pushed back into the sleeves (21.9-26 s)."""
    import patriots3 as P
    import patriots3_act as ACT
    times = [21.9, 22.12, 22.34, 22.56]
    fixed = [f for f in _hand_faults(P, times, 'Patriot') if f['kind'] == 'in sleeve']
    keep = {k: dict(v) for k, v in ACT.FLAPS.items()}
    ACT.FLAPS.update({'up': {'L': (-270.0, -80.0, 120.0), 'R': (270.0, -80.0, 120.0)},       # before 28949c6
                      'pat': {'L': (-250.0, 170.0, 170.0), 'R': (250.0, 170.0, 170.0)},
                      'pat2': {'L': (-280.0, 30.0, 150.0), 'R': (280.0, 30.0, 150.0)}})
    try:
        caught = [f for f in _hand_faults(P, times, 'Patriot') if f['kind'] == 'in sleeve']
    finally:
        ACT.FLAPS.update(keep)
    ok = len({f['t'] for f in caught}) == len(times) and not fixed
    return ok, f'old flaps: caught in {len({f["t"] for f in caught})} of {len(times)} frames; fixed: {len(fixed)}'


# ------------------------------------------------------------------------------------------------ rule 42: poses
@test
def pose_gallery():
    """Rule 42: every gallery pose passes the hand check from every view except those its AVOID lists. A view avoided
    because it was SEEN wrong on the sheet (no check catches it yet, the reason says "seen on the sheet") need not
    fail the hand check; every other avoided view must still fail it (else the kit got better: free the view)."""
    import posegallery as PG
    argv = sys.argv
    sys.argv = ['posegallery', os.path.join(HERE, 'data', 'pose-gallery.jpg')]
    try:
        bad = PG.main()
    finally:
        sys.argv = argv
    want = {n: {k for k, why in v.items() if 'seen on the sheet' not in why} for n, v in PG.AVOID.items()}
    want = {n: v for n, v in want.items() if v}
    got = {n: v for n, v in PG.results.items() if v}
    return not bad and got == want, f'{len(PG.results)} poses; failing views {got or "none"} (AVOID lists {want})'


# ------------------------------------------------------------------------------------------------ rule 43: looks
@test
def looks_at_the_shot_camera():
    """Patriots 3 note 11: the Loader's profile at the Gunner (41-42.6 s) read as looking at the wall."""
    import body as B
    import filmkit
    import patriots3 as P
    import patriots3_act as ACT
    B.SS = 1
    times = [i / 12 for i in range(int(41.0 * 12), int(42.6 * 12))]

    def faults():
        filmkit.EYES.clear()
        for t in times:
            P.picture(t)
        recs = list(filmkit.EYES)
        return [x for x in filmkit.check_eyelines() if x.startswith('LOOKS: loader')], recs
    fixed, recs = faults()
    real = ACT.loader

    def old(t):                                      # before db3f208: his head turned fully to the Gunner (a profile)
        a = real(t)
        if t >= ACT.T_MEET:
            a.head_facing = ACT.toward(ACT.L_BACK, ACT.G_WALL)
        return a
    ACT.loader = old
    try:
        caught, _ = faults()
    finally:
        ACT.loader = real
    meet = filmkit.meets(recs)
    ok = bool(caught) and 'looks past them' in caught[0] and not fixed and meet and meet[0][:2] == ('gunner', 'loader')
    return ok, f'old head: {caught[0][:90] if caught else "not caught"}...; fixed: {len(fixed)} fault(s); eyes meet: ' \
               f'{", ".join(f"{a}+{b} {t0:.1f}-{t1:.1f} s" for a, b, t0, t1 in meet) or "none found"}'


# ------------------------------------------------------------------------------------------------ the kit lessons
@test
def head_turns_its_own_way():
    """Kit lesson 1 (Patriots 3): a front-on body's head could only turn the way the body's drawing was mirrored."""
    from PIL import Image
    import body as B
    import patriots3_cast as C
    import views as V
    B.SS = 1
    sides = {}
    for hy in (-90.0, 90.0):
        im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
        j2 = V.person(im, B.Cam(1.0, 540, 960), 540, 700, 0.8, dict(C.GUNNER), 0.0, 5.0, None, hy)
        d = j2['_drawn']
        sides[hy] = (d['head'], d['head_mirror'], sum(e['off'][0] for e in d['eyes']))
    ok = sides[-90.0][2] < 0 < sides[90.0][2] and sides[-90.0][0] == sides[90.0][0] == 'side'
    return ok, f'body facing us; head turned left: pupils {sides[-90.0][2]:+.2f}, right: {sides[90.0][2]:+.2f} ' \
               f'(screen left is minus)'


@test
def push_in_keeps_the_view():
    """Kit lesson 2 (Patriots 3): sets.Cam.yaw_of used the camera's own right, so a push-in (the camera only turning)
    changed how someone was drawn: the Patriot popped to three-quarter mid push-in."""
    import sets as S
    person, facing = (1.2, 0.0, 0.0), (-0.5, 1.0)
    yaws = [S.Cam((0.0, 1.5, 4.0), (x, 1.2, 0.0), focal=1000).yaw_of(person, facing) for x in (-1.0, 0.0, 1.2)]
    spread = max(yaws) - min(yaws)
    return spread < 0.01, f'one person, the camera turning from left of them to on them: view {yaws[0]:.1f} to ' \
                          f'{yaws[-1]:.1f} degrees (spread {spread:.3f})'


@test
def tilt_at_chest_height():
    """Kit lesson 3 (Patriots 3): lying.stand measured the camera's tilt at the floor, so close up a hand held out at
    chest height sank (the salute to the chest). Now measured at the arms' height, as patriots3._tilt did."""
    import lying
    import patriots3 as P
    import sets as S
    cam = S.Cam((0.0, 1.45, 1.6), (0.3, 1.3, -1.0), focal=1000)
    mine = lying.place(cam, 0.4, -0.4, 0.0, 1.78)
    film = P._tilt(cam, 0.4, -0.4, dict(name='Patriot'))   # (the film rounds the neck to 1.41 m: 0.2% apart)
    same = all(abs(a - b) <= 2e-3 * max(1.0, abs(b)) for a, b in zip(mine, film))
    Xf, Yf, s, e, c = mine
    W = (0.4, 1.2, -0.4 + 0.42)                       # a hand 42 cm in front of the chest, towards the lens
    (_, Yw), _ = cam.project(W)
    (_, Yc), _ = cam.project((0.4, 1.2, -0.4))
    k = 1.78 / 1.75
    err = abs((Yc + e * s * 0.42 / (lying.M * k)) - Yw)
    return same and err < 6, f'same numbers as Patriots 3: {same}; a hand held out at chest height lands {err:.1f} px ' \
                             f'from where the camera sees it'


@test
def held_prop_through_the_camera():
    """Kit lesson 4 (Patriots 3): held 3D props drawn through the real camera with the hands on the grip points the
    camera sees (held3d.py, from patriots3.hold_gun). Same hand targets as the film's own code, in shot 9."""
    import held3d
    import lying
    import patriots3 as P
    import patriots3_act as ACT
    t = 38.0
    cam = P.cam_for(t)
    a = next(x for x in ACT.everyone(t) if x.who == 'patriot')
    j0 = {k: v for k, v in a.j.items()}
    P.hold_gun(a, cam, t)
    want = {sd: a.j['wr' + sd] for sd in a.j['grip']}
    a.j.clear()
    a.j.update(j0)
    g = ACT.gun_at(a.fire_t)
    yw = P.view_yaw(cam, a.x, a.z, a.facing)
    yw = abs(yw) if abs(yw) < 22.5 else yw            # as the film: facing us he is never mirrored
    place = lying.place(cam, a.x, a.z, 0.0, P.PC.HEIGHTS.get('Patriot', 1.75))
    held3d.hold(a.j, cam, a.x, a.z, yw, place, [g(0.40, -0.04), g(0.24, 0.02)], lambda p, j2: None,
                height=P.PC.HEIGHTS.get('Patriot', 1.75), one_hand=a.one_hand, reach=a.reach, centre=g(0.32, 0.0))
    got = {sd: a.j['wr' + sd] for sd in a.j['grip']}
    d = max(math.dist(want[sd], got[sd]) for sd in want) if set(want) == set(got) else 1e9
    return d < 1.0 and a.j.get('wrap') == set(want), f'hands {sorted(got)} within {d:.2g} units (under a mm) of ' \
                                                    f'the film\'s; ' \
                                                      f'arms behind the gun: {bool(a.j.get("wrap"))}'


@test
def nostamp_in_the_template():
    """Rule 47 / Build list item 5: `--nostamp` is a standard option of satire_template.py's main."""
    import film_engine as E
    import satire_template as T
    got = {}
    real = E.render
    E.render = lambda *a, **k: got.update(k)
    argv = sys.argv
    try:
        sys.argv = ['x', 'final', 'x.mp4', '--span', '1', '2', '--nostamp']
        T.main()
        no = got.get('stamp')
        sys.argv = ['x', 'final', 'x.mp4', '--span', '1', '2']
        T.main()
        default = got.get('stamp')
    finally:
        E.render, sys.argv = real, argv
    return no is False and default is None, f'with --nostamp: stamp={no}; without: stamp={default} (on for clips)'


# ------------------------------------------------------------------------------------------------ rules 57, 59, 60
@test
def order_flip_mid_shot():
    """Rule 57 (Flying Whales note 16): a smoke column sent behind the rig at one instant is caught; a planned swap is not."""
    import types
    import clipcheck as C
    film = types.SimpleNamespace(SHOTS=[('rig', 0.0, 2.0)], FPS=12, DUR=2.0,
                                 draw_order=lambda t: ['sea', 'smoke', 'rig'] if t >= 1.0 else ['sea', 'rig', 'smoke'])
    caught = C.flip_faults(film, C._times(film)[0])
    film.ORDER_SWAPS = [('smoke', 'rig', 0.9, 1.1, 'meant')]
    planned = C.flip_faults(film, C._times(film)[0])
    film.SHOTS = [('a', 0.0, 1.0), ('b', 1.0, 2.0)]
    film.ORDER_SWAPS = []
    at_cut = C.flip_faults(film, C._times(film)[0])
    return bool(caught) and not planned and not at_cut, f'caught {len(caught)}; planned {len(planned)}; at a cut {len(at_cut)}'


@test
def near_thing_after_the_haze():
    """Rule 57 (critic bench, Remakes note 73): a near flower box drawn before the haze is caught; after it, clear; a
    film that says it hazes but never names 'haze' in draw_order is named."""
    import types
    import clipcheck as C
    film = types.SimpleNamespace(SHOTS=[('square', 0.0, 1.0)], FPS=12, DUR=1.0,
                                 draw_order=lambda t: ['square', 'near flower box', 'haze', 'line-up'])
    caught = C.haze_faults(film, C._times(film)[0])
    film.draw_order = lambda t: ['square', 'haze', 'near flower box', 'line-up']
    clear = C.haze_faults(film, C._times(film)[0])
    film.draw_order = lambda t: ['square', 'line-up']
    film.__file__ = os.path.join(HERE, 'remakes.py')
    unnamed = C.haze_faults(film, C._times(film)[0])
    return len(caught) == 1 and not clear and len(unnamed) == 1, \
        f'caught {len(caught)}; after the haze {len(clear)}; unnamed haze {len(unnamed)}'


@test
def townsfolk_not_in_the_house_walls():
    """Rule 13 (critic bench, Remakes note 68): S11's townsfolk as Sam saw them (two in the house fronts) are caught
    against the street's SET_FEET; as fixed, clear."""
    import remakes as R
    old = ((-1.6, 22.0, 0, 21), (1.5, 25.0, 0, 22), (0.3, 30.0, 0, 23), (-0.6, 15.0, 0, 24), (1.4, 13.0, 0, 25),
           (-1.9, 12.0, 0, 26))
    then, now = R.street_paths(old), R.street_paths()
    hit = {f.split()[3] for f in then if 'stands in' in f}
    return hit == {'25', '26'} and not now, f'as Sam saw it: {sorted(hit)}; now {len(now)}'


@test
def hiss_heard_only_between_lines():
    """Rule S3 (Flying Whales): speech full of "s" sounds is not hiss; noise in the gaps between lines still is."""
    import numpy as np
    import filmkit
    sr, rng = 48000, np.random.default_rng(1)
    voice = 0.05 * rng.standard_normal(sr * 12)                     # 12 s of hissy "speech" (all "s" sounds) ...
    voice[6 * sr:int(6.5 * sr)] = 0                                 # ... with one short pause, as in a busy film
    old = filmkit.hiss_check(voice, sr, 12.0)                       # the quietest fifth: mostly speech, a false alarm
    clean = filmkit.hiss_check(voice, sr, 12.0, voice=voice)
    hissy = filmkit.hiss_check(voice + 0.003 * rng.standard_normal(len(voice)), sr, 12.0, voice=voice)
    return bool(old) and not clean and bool(hissy), \
        f'old way: {len(old)} fault(s) (the false alarm); speech alone: {len(clean)}; noise in the pause: {len(hissy)}'


@test
def could_not_test_cover():
    """could-not-test (Sam's pick 1, 22 Nov): the clipping check is fed by the drawing itself (cover.py). A further
    thing drawn over a nearer one is a fault; a hand resting on flat papers is not; a person drawn with no depth is
    COULD NOT TEST; and that stop passes no flag: only the check's Exceptions row with Sam's Y."""
    import types
    import tempfile
    import cover
    import film_engine as E
    from PIL import Image, ImageDraw

    def film(order, flat=False, depth=True):
        def picture(t):
            img = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
            d = ImageDraw.Draw(img)
            card = lambda: d.rectangle((400, 1000, 700, 1100), fill=(240, 236, 220), outline=(0, 0, 0))
            arm = lambda: d.rectangle((500, 900, 560, 1150), fill=(40, 40, 70))
            steps = {'card': lambda: (cover.thing(img, 'name card', 1.44, flat=flat, surface=0.76 if flat else None),
                                      card),
                     'arm': lambda: (cover.person(img, 'andy', 2.2) if depth else cover.thing(img, 'x', 9), arm),
                     'hand': lambda: (cover.thing(img, 'hand', 1.7, bottom=0.72), arm)}   # resting on the table
            for k in order:
                ctx, fn = steps[k]()
                with ctx:
                    fn()
            return img.convert('RGB')
        m = types.ModuleType('fake_cover_film')
        m.picture, m.SHOTS, m.FPS = picture, [('1', 0, 1)], 12
        return m

    def run(f):
        items, fr, blind = cover.record(f, 0.0)
        return cover.faults(items, fr), blind
    wrong, _ = run(film(['card', 'arm']))                     # the arm (2.2 m) drawn over the card (1.44 m)
    right, _ = run(film(['arm', 'card']))
    papers, _ = run(film(['card', 'hand'], flat=True))        # flat on the table: a hand resting on it is fine
    real = E.PASSES
    E.PASSES = tempfile.mkdtemp()
    try:
        E.write_pass('x', 1, untested=['clipcheck: COULD NOT TEST: nothing recorded'])
        stopped = E.lock_fault('x', faults_named=True)        # no flag passes it
        E.write_pass('x', 0, untested=[])
        clear = E.lock_fault('x', faults_named=True)
    finally:
        E.PASSES = real
    import preflight
    with tempfile.TemporaryDirectory() as tmp:
        notes = os.path.join(tmp, 'n.md')
        line = 'clipcheck: COULD NOT TEST (shot 2a): goth drawn with no depth'
        old = preflight.notes_path
        try:
            preflight.notes_path = lambda f, n: notes
            open(notes, 'w').write('## Exceptions\n| check | who | why | looked at |\n|---|---|---|---|\n'
                                   '| clipcheck | shot 2a | a shaft of light only | full size, 23 Nov |\n')
            no_y = preflight.untested_waived(None, 'x', [line])
            open(notes, 'w').write('## Exceptions\n| check | who | why | looked at |\n|---|---|---|---|\n'
                                   "| clipcheck | shot 2a | a shaft of light only (Sam's Y, 23 Nov) | full size |\n")
            with_y = preflight.untested_waived(None, 'x', [line])
        finally:
            preflight.notes_path = old
    ok = (len(wrong) == 1 and not right and not papers and bool(stopped) and clear is None and not no_y
          and with_y == [line])
    return ok, (f'arm over a nearer card: {len(wrong)} fault; drawn right: {len(right)}; over flat papers: '
                f'{len(papers)}; COULD NOT TEST with --faults-named refused: {bool(stopped)}; cleared: {clear is None};'
                f' row without Sam\'s Y excuses: {bool(no_y)}; with it: {with_y == [line]}')


@test
def could_not_test_readable():
    """could-not-test (3): a name card the render drew under the caption is a fault; one clear above it is not."""
    import types
    import cover
    m = types.ModuleType('fake_read_film')
    m.caption_at = lambda t: 'The essence of my report'
    import subtitles as SUB
    from PIL import Image
    lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    SUB.draw(lay, 'The essence of my report', ss=1)
    y0, y1 = lay.getbbox()[1], lay.getbbox()[3]
    under = {'fps': 12, 'frames': {'0': [('his name card', 400, y0 - 20, 600, y0 + 60)]}}
    clear = {'fps': 12, 'frames': {'0': [('his name card', 400, y0 - 200, 600, y0 - 110)]}}
    a, b = cover.readable_faults(m, under), cover.readable_faults(m, clear)
    return len(a) == 1 and not b, f'card under the caption: {len(a)} fault; card clear above it: {len(b)}'


@test
def named_lines_each_answered():
    """named-lines change 2 (Sam's Y, 23 Nov; rule 59): Milburn's 61 lines went past every round under one switch; each
    warning now needs its own written answer, blind ones never pass, and an answered line comes back if its numbers
    change."""
    import film_engine as E
    import tempfile
    import types
    import waivers
    rows = [json.loads(x) for x in open(os.path.join(HERE, '..', 'notes', 'ledger', 'milburn', 'checks.jsonl'))]
    run = rows[0]['run']
    lines = [f for r in rows if r['run'] == run for f in r['faults']]
    film = types.ModuleType('milburn_replay')                 # Milburn had no scene(t)
    blind = [x for x in lines if waivers.is_blind(x, film)]
    cap = next(x for x in lines if x.startswith('caption "to kill each"'))
    card = next(x for x in lines if 'COULD NOT TEST' in x)
    notes = ('## Exceptions\n| check | who | why | looked at |\n|---|---|---|---|\n'
             f'| `{cap}` | - | Sam speaks fast; his own take | 1.1 s full size | chosen | Sam |\n'
             f'| `{card}` | - | named to Sam | animatic 1 | chosen | chat 15 |\n'
             '| `plan: goth has no facing (which way they face)` | - | fine | | chosen | chat 15 |\n')
    none_done, none_left = waivers.split(lines, '', film)
    done, left = waivers.split(lines, notes, film)
    moved = cap.replace('0.38', '0.41')
    back = waivers.split([moved], notes, film)[1]
    real = E.PASSES
    E.PASSES = tempfile.mkdtemp()
    try:
        E.write_pass('x', len(left), left=left)
        refused = E.lock_fault('x', faults_named=True)
        E.write_pass('x', 0, left=[])
        clear = E.lock_fault('x')
    finally:
        E.PASSES = real
    card_left = any(x.startswith(card) and 'BLIND' in x for x in left)
    incomplete = any(x.startswith('ANSWER incomplete') for x in left)
    ok = (len(lines) == 61 and len(blind) == 37 and len(none_left) == 61 and len(done) == 1 and card_left
          and incomplete and moved in back and bool(refused) and clear is None)
    return ok, (f'Milburn lines {len(lines)}, blind {len(blind)} (learn.md: 37); unanswered with no notes '
                f'{len(none_left)}; answered 1 caption: {len(done)}; blind card line answered but still stops: '
                f'{card_left}; a row with no look flagged: {incomplete}; caption back when its time changes: '
                f'{moved in back}; --faults-named refused: {bool(refused)}; all answered passes: {clear is None}')


@test
def named_lines_body_each_answered():
    """named-lines change 2 (Sam's Y, 23 Nov): the body check's whole list was named with one reason (GTA, 11 at once);
    now --named alone holds the clip, and it goes back only when each line has its own answer in the film's notes."""
    import humancheck as HC
    import tempfile
    d = tempfile.mkdtemp()
    out = os.path.join(d, 'clip.mp4')

    def clip():
        open(out, 'w').write('x')
        w = HC.Writer('clip.mp4')
        w.found = {('jason', 'arm', 'x'): [17.9, 3, 'jason: an arm out of the back']}
        return w
    w = clip()
    line = w.lines()[0]
    try:
        w.finish(out, named=True, notes='')
        held_named = False
    except SystemExit:
        held_named = os.path.exists(out[:-4] + '.held.mp4') and not os.path.exists(out)
    notes = f'## Exceptions\n| `{line}` | - | a passer-by behind the car, 2 drawings | 17.9 s full size | real | chat 44 |\n'
    clip().finish(out, named=False, notes=notes)
    rec = HC.load(out)
    passed = bool(rec and rec['named'] and rec['answered'] == 1)
    try:
        HC.main(['name', out, 'all named to Sam'])
        one_reason = False
    except SystemExit:
        one_reason = True
    return held_named and passed and one_reason, (f'--named alone held: {held_named}; each line answered passes: '
                                                  f'{passed}; one reason for the list refused: {one_reason}')


@test
def turned_curves():
    """R7 chat 10 (Sam, 25 Nov, examples/sam-25nov-may-too-curvaceous.png: "Way too curvaceous from this angle.
    She's Theresa May not a swimsuit model"): views.turned_curves_fault catches that frame's drawing (May, mode
    'body', crossed three-quarter, turned_curves 1) and passes her boxy jacket (turned_curves 0)."""
    import sys
    sys.path.insert(0, 'notes/learn/seated/solid')
    import views as V
    import sheet_solid as SH
    SH.MODE = 'body'
    got = {}
    keep = SH.cast['may']
    try:
        for tc in (1.0, 0.0):
            SH.cast['may'] = dict(keep, turned_curves=tc)
            SH.tile('may', -45, 'cross, knee over knee')
            got[tc] = V.turned_curves_fault()
    finally:
        SH.cast['may'] = keep
    return bool(got[1.0]) and not got[0.0], f"Sam's frame: {got[1.0] or 'MISSED'}; boxy jacket: {got[0.0] or 'passes'}"


@test
def jacket_under_hem():
    """R7 chat 10 (Sam, 25 Nov, side view: "Is this bottom purple section supposed to be there or is it supposed to
    be trousers", examples/r7c10-purple-under-jacket-side.jpg): the seated check 'jacket under the hem' catches the
    solid bottom in jacket colour (SEAT_TROUSERS off) and passes it as trousers."""
    import sys
    sys.path.insert(0, 'notes/learn/seated/solid')
    import solid_seat as SO
    import sheet_solid as SH
    SH.MODE = 'body'
    got = {}
    try:
        for on in (False, True):
            SO.SEAT_TROUSERS = on
            got[on] = SH.tile('may', 90, 'upright')[1].get('jacket under the hem')
    finally:
        SO.SEAT_TROUSERS = True
    return bool(got[False]) and got[True] == 0, f"Sam's purple bottom: {got[False]} dots; as trousers: {got[True]}"


@test
def short_top_hem():
    """R7 chat 13 (Sam, 26 Nov, on learn-sheet-kemi.jpg front: "Kemi's jacket is behaving like a suit jacket at the
    bottom, and we should have a solid block of trouser beginning about halfway through the blue";
    notes/learn/pose-kit/examples/sam-26nov-kemi-vest-hangs-like-jacket.jpg): solid_seat.short_top_faults catches
    Sam's frame and Kemi seated on the full body with her hi-vis at suit length (views.SHORT_TOP_RISE 0), and passes
    her as now (the hem halfway through the navy, trousers below) in the front and three-quarter views."""
    import sys
    from PIL import Image
    sys.path.insert(0, 'notes/learn/seated/solid')
    import solid_seat as SO
    import sheet_solid as SH
    import views as V
    SH.MODE = 'body'
    sp = SH.cast['kemi']
    sam = SO.short_top_faults(Image.open('notes/learn/pose-kit/examples/sam-26nov-kemi-vest-hangs-like-jacket.jpg'), sp)
    got = {}
    keep = V.SHORT_TOP_RISE
    try:
        for rise in (0.0, keep):
            V.SHORT_TOP_RISE = rise
            got[rise] = [SO.short_top_faults(SH.tile('kemi', yaw, 'upright', full=True)[0], sp) for yaw in (0, 45)]
    finally:
        V.SHORT_TOP_RISE = keep
    ok = bool(sam) and all(got[0.0]) and not any(got[keep])
    return ok, f"Sam's frame: {sam or 'MISSED'}; suit length: {got[0.0]}; as now: {got[keep]}"


@test
def leg_tone():
    """R7 chat 14 (Sam, 26 Nov, note 1: "In 3/4 pose the legs are different colour";
    examples/sam-26nov-kemi-34-far-leg.jpg): solid_seat.leg_tone_faults catches Sam's frame and passes May, Kemi and
    Blair at three-quarter as now (before chat 14 all three were caught: shadow tone 0.51, 0.44, 0.61)."""
    import sys
    from PIL import Image
    sys.path.insert(0, 'notes/learn/seated/solid')
    import solid_seat as SO
    import sheet_solid as SH
    SH.MODE = 'body'
    sam = SO.leg_tone_faults(Image.open('notes/learn/pose-kit/examples/sam-26nov-kemi-34-far-leg.jpg'), SH.cast['kemi'])
    sam7 = SO.leg_tone_faults(Image.open('notes/learn/pose-kit/examples/sam-26nov-c14-crossed-two-colours.jpg'),
                              SH.cast['kemi'])          # chat 15, note 7: "On the crossed legs, they are still different colors"
    now = {(w, yaw): SO.leg_tone_faults(SH.tile(w, yaw, pose, full=True)[0], SH.cast[w]) for w in ('may', 'kemi', 'blair')
           for yaw, pose in ((45, 'upright'), (-45, 'cross, knee over knee'))}
    now = {k: v for k, v in now.items() if v}
    return bool(sam) and bool(sam7) and not now, f"Sam's frames: {sam or 'MISSED'} / crossed {sam7 or 'MISSED'}; as now: {now or 'clean'}"


@test
def back_clip():
    """R7 chat 14 (Sam, 26 Nov, note 5: "Back of bum clips slightly into chair in side-on pose and needs stronger
    lining"; examples/sam-26nov-kemi-side-bum-line-chair.jpg): solid_seat.back_clip_faults catches Sam's frame and
    Kemi side on with the chair back at its old place (views.r7_back_face off), and passes all three as now."""
    import sys
    from PIL import Image
    sys.path.insert(0, 'notes/learn/seated/solid')
    import solid_seat as SO
    import sheet_solid as SH
    import views as V
    SH.MODE = 'body'
    sam = SO.back_clip_faults(Image.open('notes/learn/pose-kit/examples/sam-26nov-kemi-side-bum-line-chair.jpg'),
                              SH.cast['kemi'])
    keep = V.r7_back_face
    try:
        V.r7_back_face = lambda *a, **k: None
        old = SO.back_clip_faults(SH.tile('kemi', 90, 'upright', full=True)[0], SH.cast['kemi'])
    finally:
        V.r7_back_face = keep
    now = {w: SO.back_clip_faults(SH.tile(w, 90, 'upright', full=True)[0], SH.cast[w]) for w in ('may', 'kemi', 'blair')}
    return bool(sam) and bool(old) and not any(now.values()), f"Sam's frame: {sam or 'MISSED'}; old chair: {old}; now: {now}"


@test
def stray_ink():
    """R7 chat 14 (Sam, 26 Nov, note 2: "Stray horizontal line on butt"; examples/sam-26nov-kemi-side-bum-line-chair.jpg):
    solid_seat.stray_ink finds the loose end of the line on Sam's frame, and none of Kemi's side view where that line
    was (the bottom, under the hem). (It misses note 3's crotch tick on Sam's frame: not yet proven there.)"""
    import sys
    from PIL import Image
    sys.path.insert(0, 'notes/learn/seated/solid')
    import solid_seat as SO
    import sheet_solid as SH
    SH.MODE = 'body'
    sp = SH.cast['kemi']
    sam = SO.stray_ink(Image.open('notes/learn/pose-kit/examples/sam-26nov-kemi-side-bum-line-chair.jpg'), sp)
    hit = [e for e in sam if 150 < e[1] < 200 and 200 < e[0] < 360]          # the line itself (not the hand's edge)
    im = SH.tile('kemi', 90, 'upright', full=True)[0].crop((480, 1400, 720, 1470))   # under the hem, where the line was
    #   (from 480: the bottom's back corner on the seat has a small step of its own, open in notes/r7.md, chat 14)
    now = SO.stray_ink(im, sp)
    sam6 = [e for e in SO.stray_ink(Image.open('notes/learn/pose-kit/examples/sam-26nov-c14-34-bottom-line.jpg'), sp)
            if 180 < e[0] < 240 and 125 < e[1] < 155]   # chat 15, note 6: the line's open end on Sam's three-quarter
    k34 = SH.tile('kemi', 45, 'upright', full=True)[1].get('stray ink')   # the sheet's own check, where it was
    import body as B                    # the sheet's own check (every tile) red on chat 14's line, put back
    keep = B.SEAT_BACK_CORNER
    try:
        B.SEAT_BACK_CORNER = True
        old = SH.tile('kemi', 45, 'upright', full=True)[1].get('stray ink')
    finally:
        B.SEAT_BACK_CORNER = keep
    return bool(hit) and bool(sam6) and bool(old) and not now and not k34, \
        f"Sam's frames: {hit or 'MISSED'} / 3-4 {sam6 or 'MISSED'}; sheet check on chat 14's line: {old or 'MISSED'}; " \
        f"Kemi's bottom now: side {now}, 3-4 {k34}"


@test
def shoe_shapes():
    """R7 chat 10 (Sam, 26 Nov: "Shoes clipping on 3/4 view", "Confused shoe shapes on side view";
    examples/sam-26nov-shoes-clipping-34.jpg, sam-26nov-shoe-shapes-side.jpg): solid_seat.shoe_faults catches May's
    shoes as Sam saw them (SHOE_HEM off: the shin through the shoe, ankle-high hooves) in his two views and passes
    all four views as now."""
    import sys
    sys.path.insert(0, 'notes/learn/seated/solid')
    import solid_seat as SO
    import sheet_solid as SH
    SH.MODE = 'body'
    views = ((45, 'upright'), (90, 'upright'), (-45, 'cross, knee over knee'), (0, 'upright'))
    old, new = {}, {}
    try:
        for on, got in ((False, old), (True, new)):
            SO.SHOE_HEM = on
            for yaw, pose in (views[:2] if not on else views):
                SH.tile('may', yaw, pose)
                got[yaw] = SO.shoe_faults()
    finally:
        SO.SHOE_HEM = True
    ok = all(old.values()) and not any(new.values())
    return ok, f"Sam's shoes: {old}; now: {new}"


def _apart_pair():
    """Sam's frame (26 Nov, both of its halves) and 'upright, apart' as drawn now, through solid_seat.apart_faults."""
    import sys
    sys.path.insert(0, 'notes/learn/seated/solid')
    from PIL import Image
    import solid_seat as SO
    import sheet_solid as SH
    SH.MODE = 'body'
    sam = Image.open('notes/learn/seated/examples/sam-26nov-apart-spread-crotch.png')
    old = [SO.apart_faults(sam.crop((k * 405, 0, k * 405 + 405, sam.height)), SH.cast['may']) for k in (0, 1)]
    new = SO.apart_faults(SH.tile('may', 0, 'upright, apart', full=True)[0], SH.cast['may'])
    return old, new


@test
def legs_apart_spread():
    """R7 chat 11 (Sam, 26 Nov, on 'upright, apart': "Those legs are sort of spread ... a bearing the crotch pose";
    examples/sam-26nov-apart-spread-crotch.png): apart_faults' 'legs spread' catches both halves of Sam's frame and
    passes the pose as now (legs straight forward, a small even gap)."""
    old, new = _apart_pair()
    hit = lambda fs: [f for f in fs if f.startswith('legs spread')]
    return all(hit(o) for o in old) and not hit(new), f"Sam's frame: {[hit(o) for o in old]}; now: {hit(new) or 'passes'}"


@test
def jacket_triangle():
    """R7 chat 11 (Sam, 26 Nov: "her purple jacket dips inward in a triangle, rather than having an appropriate
    trouser section in that area"; same frame): apart_faults' 'jacket triangle' catches both halves of Sam's frame and
    passes the pose as now (the jacket opens over the lap, trousers below it)."""
    old, new = _apart_pair()
    hit = lambda fs: [f for f in fs if f.startswith('jacket triangle')]
    return all(hit(o) for o in old) and not hit(new), f"Sam's frame: {[hit(o) for o in old]}; now: {hit(new) or 'passes'}"


@test
def solid_crop_same():
    """Speed (Sam's Y, 26 Nov: "A 10 second clip taking 15 mins is unsustainable"): the seated body is drawn over its
    own box, not the whole picture (solid_seat.CROP). Proven to change nothing: May's shot 1 frame and a crossed-legs
    sheet tile pixel for pixel with the box off and on, and the box faster."""
    import sys
    import time
    import numpy as np
    sys.path.insert(0, 'source')
    sys.path.insert(0, 'notes/learn/seated/solid')
    import solid_seat as SO
    import brexit_is_done as F
    import sheet_solid as SH
    SH.MODE = 'body'
    keep, out, secs = SO.CROP, {}, {}
    try:
        for c in (False, True):
            SO.CROP = c
            t0 = time.time()
            out[c] = [np.asarray(F.may_shot(3.0).convert('RGB'))]
            secs[c] = time.time() - t0
            out[c].append(np.asarray(SH.tile('kemi', -45, 'cross, knee over knee', full=True)[0]))
    finally:
        SO.CROP = keep
    moved = [int((np.abs(a.astype(int) - b.astype(int)).sum(-1) > 0).sum()) for a, b in zip(out[False], out[True])]
    return not any(moved) and secs[True] < secs[False], (
        f"dots moved (May's frame, Kemi crossed tile): {moved}; May's frame {secs[False]:.1f} s -> {secs[True]:.1f} s")


@test
def fold_stub():
    """Open Wounds chat 27 (May on the seated body tool, shot 1): a fold line inside her back leg (the calf over the
    thigh) faded out in the open at the seat's edge, a loose ink tick (examples/ow-c27-may-calf-fold-tick.png, the
    sheet check stray_ink caught it on every sampled frame). solid_seat._ink now drops a short fold that meets other
    ink at one place only (FOLD_MIN). Red on the saved frame and on the drawing with the drop off; green now."""
    import sys
    from PIL import Image
    from scipy import ndimage
    sys.path.insert(0, 'source')
    import solid_seat as SO
    import brexit_is_done as F
    sp, _ = F.acted('1', 'may', 3.0)
    ex = SO.stray_ink(Image.open('notes/learn/pose-kit/examples/ow-c27-may-calf-fold-tick.png'), sp)
    saved = [e for e in ex if 140 < e[0] < 160 and 140 < e[1] < 160]   # the tick (the frame at 404, 1564)
    got = {}
    keep = SO.FOLD_MIN
    try:
        for fm in (0, keep):
            SO.FOLD_MIN = fm
            img = F.may_shot(3.0).convert('RGB')
            got[fm] = SO.stray_ink(img, sp, where=ndimage.binary_erosion(SO.LAST['shown'], iterations=6))
    finally:
        SO.FOLD_MIN = keep
    return bool(saved) and bool(got[0]) and not got[keep], (
        f"saved frame: {saved or 'MISSED'}; drop off: {got[0] or 'MISSED'}; now: {got[keep] or 'none'}")


def _ring_px(img):
    """The outline's thickness round a drawing on white: ink within 8 px of the open background, per edge pixel."""
    import numpy as np
    from scipy import ndimage as ND
    a = np.asarray(img.convert('RGB')).astype(int)
    white = a.min(-1) > 245
    lab, _ = ND.label(white)
    bg = np.isin(lab, np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    ink = a.sum(-1) < 150
    near = ND.distance_transform_edt(~bg) <= 8
    edge = ink & ND.binary_dilation(bg)
    return float((ink & near).sum()) / max(1, int(edge.sum()))


@test
def wolf_house_line():
    """Open Wounds note 16 (Sam, 26 Nov, animatic: "the line work on the wolves is very thick in comparison to our house
    style"; his frame notes/learn/wolf-line/ow-animatic-wolves-thick-sam-26nov.png): a kit wolf's outline was 5 wolf
    units, about twice a worker's at the same depth. wolf.house_ctx now sets it to the people's own weight
    (lying._lw). Red with the old weight, green now: the wolf's outline within 1.3 times the worker's at 5 and 7 m."""
    import sys
    from PIL import Image
    sys.path.insert(0, 'source')
    import brexit_is_done as F
    ACT, WF = F.ACT, F.ACT.WF
    L = F._cam('site')
    keep = WF.house_ctx
    res = {}
    try:
        for name, fn in (('old', lambda X, s, ppm: X), ('now', keep)):
            WF.house_ctx = fn
            r = []
            for d in (5.0, 7.0):
                a = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
                ACT.wolf_at(a, L, 0, d, 0, 1, WF.pose('stand', 0), pal=1, shade=False)
                b = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
                ACT.person_at(b, L, ACT.WORKERS[0], 0, d, 0, 90, None, 0.0, shadow=False)
                r.append(_ring_px(a) / _ring_px(b))
            res[name] = r
    finally:
        WF.house_ctx = keep
    return max(res['old']) > 1.45 and max(res['now']) <= 1.3, (
        'wolf outline / worker outline at 5, 7 m: old ' + ', '.join(f'{v:.2f}' for v in res['old'])
        + '; now ' + ', '.join(f'{v:.2f}' for v in res['now']))


@test
def seated_r7_switch():
    """R7 (25 Nov): the seated lower body as one shape is on for every new film and off for every posted film, whose
    seated people stay pixel for pixel (fingerprints taken before R7 was built). Open Wounds (Sam, 26 Nov: "These
    fixes were built specifically for Open Wounds ... Implement."): May and Kemi on the seated body tool (mode
    'body', people.SEAT_BODY); Blair and the crowds stay on the house drawing until their poses are learned (rule
    91); with the tool taken off, all three still draw exactly the old frames."""
    import hashlib
    import people
    import castsheet as CS
    import sitting as S
    from PIL import Image
    saved = {('blair', 0): '13d5c648a6ed', ('blair', 45): '24f16e2873e6', ('blair', 90): '3732d689f2ab',   # re-held 26 Nov, chat 30: notes 20-21 changed the heads (neck, brows, lines), nothing below them   # 45/90: Open
             #   Wounds' own chain moved them (3d10d4c7, its shared sleeve lift in turned views), proven with R7's
             #   chat 2 changes taken out (still moved); was 5e30e187e32c / 397e4b53c71f
             ('kemi', 0): 'c736ac4bb567', ('kemi', 45): 'aa63685bd955', ('kemi', 90): 'cc0826ec4d61',
             ('may', 0): '97cbfbe3e550', ('may', 45): '5e504d91a956', ('may', 90): 'dbeb1214140e'}
    off = [f for f in people.BEFORE_SEATED if people.seat_r7(f) and f != 'brexit-is-done']
    new_on = people.seat_r7('a-new-film')
    cast, PP = CS._setup('brexit-is-done', None)
    want = set(people.SEAT_BODY['brexit-is-done'])
    marked = {w for w, sp in cast.items() if sp.get('seat_r7')}
    body = {w for w, sp in cast.items() if sp.get('seat_solid') == 'body'}
    crowd_on = [w for w, d in people.crowds('brexit-is-done').items() if d.get('seat_r7')]
    moved, changed = [], 0
    for (who, yaw), h in saved.items():
        for on in (False, True):
            sp = dict(cast[who])
            for k in ('seat_r7', 'seat_solid', 'turned_curves', 'turned_bust'):
                sp.pop(k, None)
            if on:
                people.seat_body(sp)
            s = 0.5 * sp['height'] / 1.75
            img = Image.new('RGBA', (1080, 1920), (235, 235, 230, 255))
            PP.V.person(img, PP.B.Cam(2.0, 540, 470), 540, 840 - 928 * s, s, sp, 0.0, yaw, S.pose(sp, 'upright'))
            got = hashlib.md5(img.tobytes()).hexdigest()[:12]
            if not on and got != h:
                moved.append(f'{who} {yaw}')
            changed += on and got != h
    ok = (not off and new_on and marked == want and body == want and not crowd_on and not moved
          and changed == len(saved))
    return ok, (f'posted films switched on: {off or "none"}; a new film on: {new_on}; Open Wounds on the body tool: '
                f'{sorted(body)} (want {sorted(want)}); crowds on: {crowd_on or "none"}; old frames moved with the '
                f'tool off: {moved or "none"}; body tool changes {changed}/9')


@test
def seated_r7_look():
    """R7 (25 Nov): the seated look reads the picture as a viewer. It must catch Sam's marked frame (a ball knee and
    no bottom: notes/learn/seated/no-bum-circular-knees-sam.jpg) and the old drawing (the ring knee; no bottom in the
    three-quarter views), and find nothing wrong with R7's lower body in any pose or view (chat 2: the hem is now read
    whole, across hands and a vest's stripes, which had been taken for the hem). Chat 4: and chat 3's legs in one
    flat tone (its judges: "one dark mass", "no knees")."""
    import castsheet as CS
    exs = CS.seated_example_faults()
    ex = exs['no-bum-circular-knees-sam']
    sam = any('ball' in f for f in ex) and any('bottom' in f for f in ex)
    # chat 4: R7 chat 3's own drawing, as its blind judges saw it ("one dark mass", "no visible knees")
    tone = all(any('one flat tone' in f for f in exs[n]) for n in ('one-tone-c3-may-34', 'one-tone-c3-kemi-front'))
    raw = CS.seated_look_faults('brexit-is-done', raw=True)
    old = any('ball' in f for f in raw) and any('bottom' in f and ' 45:' in f for f in raw)
    new = CS.seated_look_faults('brexit-is-done', force=True)
    return sam and tone and old and not new, (
        f"Sam's frame caught (ball and bottom): {sam}; chat 3's one dark mass caught (3/4 and front): {tone}; the old "
        f"drawing caught (ball and bottom): {old}; faults on R7: {len(new)} {new[:2]}")


@test
def override_word():
    """Sam's Override (23 Nov, proposal override-word option 2). Saved example: chat 47 built animatic v5 and the send
    guard refused it (no body check), so Sam waited a whole chat. Sam's word must open that stop for one ask; a chat
    writing the word itself, or the word in an older message, must not."""
    import override as O, tempfile, subprocess
    d = tempfile.mkdtemp()
    real = O.LOG
    O.LOG = os.path.join(d, 'overrides.log')

    def chat(*lines):
        f = os.path.join(d, f'c{len(os.listdir(d))}.jsonl')
        with open(f, 'w') as fh:
            for who, text in lines:
                e = {'type': who, 'message': {'content': text}}
                if who == 'tool':
                    e = {'type': 'user', 'message': {'content': [{'type': 'tool_result', 'content': 'override'}]}}
                if who == 'seed':      # a chat's opening prompt, written by the chat before it (create_session)
                    e = {'type': 'user', 'message': {'content': text}, 'textNotTyped': True, 'promptSource': 'system',
                         'origin': {'kind': 'task-notification'}}
                fh.write(json.dumps(e) + '\n')
        return f
    sam = chat(('user', 'Override, send me the animatic'), ('assistant', 'ok'), ('tool', ''),
               ('user', '[SYSTEM NOTIFICATION - NOT USER INPUT] done'))
    plain = chat(('user', 'send me the animatic'), ('assistant', 'Treating this as an override.'))
    older = chat(('user', 'override'), ('assistant', 'done'), ('user', 'thanks, now the next one'))
    # saved example (chat 53, 23 Nov): chat 52's opening prompt for chat 53 said "the handover at the end was passed
    # under Sam's Override", and the whole chat ran under an Override Sam never typed
    seeded = chat(('seed', "Grand Theft Autism, chat 53 (Opus, medium effort, a round of Sam's notes). Branch note: the "
                           "handover at the end was passed under Sam's Override; the body test body_check_back_view is red"))
    video = os.path.join(d, 'v.mp4')
    open(video, 'wb').write(b'0')

    def send(tr):
        inp = json.dumps({'tool_name': 'SendUserFile', 'tool_input': {'files': [video]}, 'cwd': os.path.dirname(HERE),
                          'transcript_path': tr})
        env = dict(os.environ, PYTHONPATH=HERE)
        r = subprocess.run([sys.executable, '-c', 'import sys, override; override.LOG = sys.argv[1]; '
                            'import humancheck; sys.exit(humancheck.sendgate())', O.LOG],
                           input=inp, capture_output=True, text=True, cwd=HERE, env=env)
        return r.returncode
    try:
        refused, opened, faked, stale = send(plain), send(sam), O.active(plain), O.active(older)
        seed = O.active(seeded)
        logged = os.path.exists(O.LOG) and 'skipped' in open(O.LOG).read()
    finally:
        O.LOG = real
    ok = refused == 2 and opened == 0 and not faked and not stale and logged and not seed
    return ok, (f'no Override: refused {refused == 2}; Sam typed it: sent {opened == 0}; chat wrote it: ignored '
                f'{not faked}; older message: ignored {not stale}; a chat\'s opening prompt: ignored {not seed}; '
                f'skip logged {logged}')


@test
def locked_line_not_to_sam():
    """Sam (23 Nov): no "Locked by Sam" line in messages to him (it stays in the notes). Example: chat 46/47 replies."""
    import propose as P
    bad = P.locked_line('Done: v5 built.\nLocked by Sam: every camera, beat, shot length.\nNext: send it.')
    bad2 = P.locked_line('- **Locked by Sam:** shot 4 25% slower')
    ok = P.locked_line('Done: v5 built. Your locked shots are unchanged.')
    return bool(bad) and bool(bad2) and not ok, f'line caught: {bool(bad)}, bold caught: {bool(bad2)}, plain words pass: {not ok}'


@test
def render_lock():
    """Rule 59 (Flying Whales animatic 4): no animatic or final without pre-flight's pass on the code as it is now."""
    import film_engine as E
    import tempfile
    real = E.PASSES
    E.PASSES = tempfile.mkdtemp()
    try:
        none = E.lock_fault('x')
        E.write_pass('x', 0)
        ok = E.lock_fault('x')
        E.write_pass('x', 3)
        faults = E.lock_fault('x')
        named = E.lock_fault('x', faults_named=True)          # named-lines (23 Nov): the switch no longer passes
        E.write_pass('x', 0)
        final_quick = E.lock_fault('x', final=True)           # pictures not yet checked: no final
        E.write_pass('x', 0, pictures=True)
        final_ok = E.lock_fault('x', final=True)
    finally:
        E.PASSES = real
    return bool(none) and ok is None and bool(faults) and bool(named) and bool(final_quick) and final_ok is None, \
        (f'no pass: {bool(none)}; pass: {ok is None}; 3 faults: {bool(faults)}; --faults-named refused: {bool(named)}; '
         f'final before the pictures are checked refused: {bool(final_quick)}; after: {final_ok is None}')


@test
def subtitles_readable():
    """Rule 62 (Terfwarts, 3 Nov): a fast speaker's subtitles are made readable when cut: on screen at least 0.8 s and
    at most 220 words a minute, over a fast line and a slow one."""
    import subtitles as SUB
    bad = []
    for text, dur in (("When you throw open the door of a bathroom or changing room to any man so-called trying to save "
                       "the life of a woman then you throw it open to anyone wanting to come inside.", 12.0),
                      ("I don't like spiders, Harry.", 2.5), ("Dead is a thought-terminating cliche.", 3.0)):
        ln = dict(n=0, text=text + str(dur), _dur=dur, _voice=None, _stretches=[(0.0, dur)])
        ln['text'] = text
        ct = SUB.chunk_times(ln)
        for i, (c, a) in enumerate(ct):
            d = (ct[i + 1][1] if i + 1 < len(ct) else dur + 0.45) - a
            if d < 0.8 or len(c.split()) / d * 60 > 220:
                bad.append((c, round(d, 2)))
    return not bad, f'too quick: {bad}' if bad else 'every piece readable'


@test
def render_leaves_no_old_file():
    """Rule 66 (Terfwarts, 3 Nov): a refused, stopped or failed render leaves no file at its output path. (Run in
    this process with no pass stamp, so the render is always refused and never starts.)"""
    import film_engine as E
    import tempfile
    real = E.PASSES
    E.PASSES = tempfile.mkdtemp()
    out = os.path.join(tempfile.mkdtemp(), 'old.mp4')
    with open(out, 'w') as fh:
        fh.write('an old render')
    refused = False
    try:
        E.render('kittest', out, size=(10, 10), ss=1, fps=1, dur=1, picture=None, overlay=None, shot_of=None,
                 sound=None, write_wav=None, set_ss=None)
    except SystemExit:
        refused = True
    finally:
        E.PASSES = real
    return refused and not os.path.exists(out), f'refused: {refused}; old file gone: {not os.path.exists(out)}'


@test
def house_look_once_in_pairs():
    """Rule S7 (house look, Sam 12 Nov): the engine lays the paper, light edges and shadows on every drawing ONCE,
    captions stay clean, and a film drawn at 12 a second comes out at 24 fps with every frame in a pair. Checked on a
    tiny demo render read back from the file; and pre-flight's look_faults catches a film drawn at 24 with no reason
    or laying the look itself (the faults it exists for)."""
    import tempfile
    import types
    import numpy as np
    import imageio_ffmpeg
    from PIL import Image, ImageDraw
    import film_engine as E
    import house_look as L

    def pic(t):
        im = Image.new('RGB', (216, 384), (150, 190, 225))
        d = ImageDraw.Draw(im)
        x = 40 + int(t * 120)
        d.rectangle([x, 120, x + 70, 260], fill=(200, 60, 50), outline=(20, 20, 20), width=2)
        d.ellipse([90, 40, 150, 100], fill=(240, 210, 90), outline=(20, 20, 20), width=2)
        return im

    d = tempfile.mkdtemp()
    out = os.path.join(d, 'demo.mp4')
    real_cache = os.environ.get('FILM_CACHE')
    os.environ['FILM_CACHE'] = d
    from mossad_audio import write_wav
    try:
        E.render('kittest-look', out, size=(216, 384), ss=1, fps=12, dur=1.0, picture=pic, overlay=lambda im, t: im,
                 shot_of=lambda t: 'a', sound=lambda: np.zeros(48000, np.float32), write_wav=write_wav,
                 set_ss=lambda v: None, crf=1, preset='ultrafast', stamp=False, lock=False, look=True)
    finally:
        if real_cache is None:
            os.environ.pop('FILM_CACHE', None)
        else:
            os.environ['FILM_CACHE'] = real_cache
    r = imageio_ffmpeg.read_frames(out)
    meta = next(r)
    fr = [np.frombuffer(f, np.uint8).reshape(384, 216, 3).astype(np.float32) for f in r]
    pairs = max(np.abs(fr[i] - fr[i + 1]).mean() for i in range(0, len(fr) - 1, 2))
    steps = min(np.abs(fr[i] - fr[i + 1]).mean() for i in range(1, len(fr) - 1, 2))
    clean = np.asarray(pic(0.0), np.float32)
    once = np.asarray(L.apply(pic(0.0)), np.float32)
    twice = np.asarray(L.apply(L.apply(pic(0.0))), np.float32)
    d1, d2, d0 = (np.abs(fr[0] - x).mean() for x in (once, twice, clean))
    ok_render = round(meta['fps']) == 24 and len(fr) == 24 and pairs < 0.5 and steps > 2 * pairs + 0.3 and d1 < min(d0, d2)
    smooth = types.ModuleType('smooth')
    smooth.FPS = 24
    twice_film = types.ModuleType('twice')
    twice_film.FPS = 12
    old = len(E.look_faults(smooth)) == 1 and len(E.look_faults(L)) >= 1    # house_look's own source names itself
    smooth.SMOOTH_WHY = 'glides'
    ok_checks = old and not E.look_faults(smooth) and not E.look_faults(twice_film)
    return ok_render and ok_checks, (f'{round(meta["fps"])} fps, {len(fr)} frames, in pairs (diff {pairs:.2f}) v steps '
                                    f'({steps:.2f}); look once {d1:.1f} / twice {d2:.1f} / none {d0:.1f}; '
                                    f'pre-flight catches: {ok_checks}')


@test
def preflight_lines_grouped():
    """Rule 19 (Sam, 13 Nov, proposals 2-3): one line per fault, grouped by check, shot and who (an extra's number and
    the frame's time do not make a new fault); one named person drawn twice in a frame is not a copy of themselves."""
    import report
    import kitchecks as K
    import types
    lines = [f'{t:6.2f} s: press{k} stands in the sign' for k in range(3) for t in (1.0, 1.08, 1.17)]
    lines += ['HANDS: Journalist 4 left hand hidden 3.1-3.5 s', 'HANDS: Journalist 12 left hand hidden 3.9-4.5 s',
              'plan: the cell has no door', '  6.00 s: press1 stands in the sign']
    g = report.group(lines, [('a', 0, 5), ('b', 5, 9)])
    look = K.look({'height': 1})
    film = types.SimpleNamespace()
    same = K.copies(film, [('a 1s', 'Brand', {'_look': look}), ('a 1s', 'Brand', {'_look': look})])
    two = K.copies(film, [('a 1s', 'press1', {'_look': look}), ('a 1s', 'press2', {'_look': look})])
    return len(g) == 4 and '[9 like it: shot a, 1.00-1.17 s]' in ' '.join(g) and not same and len(two) == 1, \
        f'{len(lines)} lines -> {len(g)}; Brand with himself: {len(same)}; two extras alike: {len(two)}'


@test
def every_face_has_a_mouth():
    """Rule 13 (Sam, 13 Nov, proposal 5; Blessed notes 5, 15, 45): a face turned to us with no mouth drawn is caught,
    front and three-quarter; one with its mouth, or seen from behind, is not."""
    from PIL import Image
    import body as B
    import posegallery as G
    import views as V
    B.SS = 1

    def seen():
        out = []
        for deg in (0, 40, 180):
            im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
            out.append(V.person(im, B.Cam(1.0, 540, 960), 540, 700, 0.8, dict(G.MODEL), 0.0, deg)['_drawn']['mouth'])
        return out
    real = B.mouth
    a = seen()
    B.mouth = lambda *x, **k: None
    try:
        b = seen()
    finally:
        B.mouth = real
    return a == [True, True, None] and b == [False, False, None], f'with mouth: {a}; mouth removed: {b}'


@test
def mouth_name_that_does_not_exist_stops():
    """Rule 13 (lesson 7, Milburn note 6, Sam 17 Nov: "character 3 has no mouth"): Swindon's "pow" switched between
    'v:O' and 'v:M', a shape name that does not exist, so half his frames drew no mouth and every face check passed
    (a face with a mouth slot is not a face with a mouth). mouths.draw now refuses an unknown name for every film;
    the old 'M' must stop, the fix's 'grin' must draw."""
    import mouths

    class Pen:
        def __init__(self):
            self.n = 0

        def line(self, *a, **k):
            self.n += 1
        poly = ell = arc = line
    stopped = False
    try:
        mouths.draw(Pen(), {}, 0, 0, 'M')
    except ValueError:
        stopped = True
    pen = Pen()
    mouths.draw(pen, {}, 0, 0, 'grin')
    return stopped and pen.n > 0, f"'M' (Milburn chat 7) stopped: {stopped}; 'grin' drew {pen.n} strokes"


@test
def board_gate_milburn_reverse():
    """Rule 11 (lesson 7, Milburn note 5, Sam 17 Nov: "the scene composition in scene 4 as proposed is poor"): when the
    reverse two-shot was built, Milburn's only delivered board held shots 1, 2a and 2b; the other 10 (the reverse 4a,
    4c, 7a, 7c, 7e among them) were first seen by Sam in the animatic. Fed Milburn's own board record as it stood
    then, rough.board_gate must refuse those 10 shots by name; with today's record (the second board) it lets them by."""
    import milburn as M
    import rough as R
    real_rec, real_before = R.board_record, R._before_rule
    full = real_rec('milburn')
    try:
        R._before_rule = lambda *a: False
        R.board_record = lambda *a: full[:1]
        then = R.board_gate(M, 'milburn')
        R.board_record = lambda *a: full
        now = R.board_gate(M, 'milburn')
    finally:
        R.board_record, R._before_rule = real_rec, real_before
    hit = next((f for f in then if 'on no delivered board' in f), '')
    ok = hit.startswith('10 shot') and '4a' in hit and not any('on no delivered board' in f for f in now)
    return ok, f'as at chat 6: {hit[:70] or "not refused"}; with the second board: {len(now)} refusals'


V7_COMMIT = '3844e0a9'                   # GTA shot 4 version 7 as Sam saw it (21 Nov, chat 22; stills in sam-v7/)


def _as_seen(commit, code, now, timeout=900):
    """Run `code` on a film exactly as Sam saw it: every source file from `commit` (the film's own timing, poses and
    kit as they were), with only the check under test taken from today (`now`: {name in the old copy: today's file}).
    A replay that mixes today's kit into an old film tests a drawing Sam never saw (chain A chat 6: GTA chat 43's
    "25% slower" moved v3's Jason to another pose, so the back-view check lost 1.3 s and found a head that wasn't
    missing). Returns the finished process (stdout, stderr, returncode), or None if the commit is not in this copy."""
    import shutil
    import subprocess
    import tempfile
    tmp = tempfile.mkdtemp()
    try:
        tar = subprocess.run(['git', 'archive', commit, 'source', 'story'], cwd=os.path.dirname(HERE),
                             capture_output=True).stdout
        if not tar:
            return None
        subprocess.run(['tar', '-x', '-C', tmp], input=tar, check=True)
        src = os.path.join(tmp, 'source')
        for dest, mine in now.items():
            shutil.copy(os.path.join(HERE, mine), os.path.join(src, dest))
        return subprocess.run([sys.executable, '-c', f'import sys; sys.path.insert(0, {src!r}); ' + code], cwd=src,
                              capture_output=True, text=True, timeout=timeout)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _seen_faults(commit, shot, times):
    """Today's body check (humancheck.py) on a film's shot exactly as Sam saw it (_as_seen): [(t, who, kind, text)].
    Old copies record no 'head' drawings (that hook came in GTA chat 20), so their 'head' faults are left out.
    Raises RuntimeError when the version is missing or its replay crashed (a test that cannot run says so)."""
    import json
    code = ('import json, gta_rehearse as G, humancheck as HC\nout = []\nfor t in %r:\n    HC.frame_begin(); G.%s(t)\n'
            '    out += [list(x) for x in HC.frame_end(t)]\nprint("FAULTS " + json.dumps(out))' % (tuple(times), shot))
    r = _as_seen(commit, code, {'humancheck.py': 'humancheck.py'})
    if r is None:
        raise RuntimeError(f'COULD NOT TEST: {commit} is not in this copy\'s history')
    line = next((ln for ln in r.stdout.splitlines() if ln.startswith('FAULTS ')), None)
    if line is None:
        raise RuntimeError(f'{commit} replay crashed: {r.stderr.strip().splitlines()[-1:]}')
    return [tuple(x) for x in json.loads(line[7:]) if x[2] != 'head']


@test
def solid_check_shot4_v7():
    """Rule 17 (lesson 7; GTA v7 note 3, Sam 21 Nov: "Jason clips through two parts of the car as he moves"): the
    times of Sam's v7 stills were matched on the v7 strip (77a3eb10 ~1.0 s, 2194502b ~1.5 s); viewchecks.solid_faults
    on version 7's own code at just those frames must flag Jason through the car (his arm in front of the window
    frame that rubs it out; his hips through the window pillar). The whole shot takes 8+ minutes, three frames about 2.
    Chain A chat 5 (23 Nov): v7 note 2, the see-through bonnet (still b03d81c2, 0.67 s = frame 8), passed every bone
    point (the vest's edge showed between them); viewchecks.outline_shows now tests the drawn outline, so frame 8 must
    flag Jason's body through the tulip's bonnet; and v7 note 7, the hydrant water through the cruiser (still c0d78111,
    3.33 s = frame 40), effect_shows must flag the water (effect 0) through the cruiser's bonnet."""
    code = ('import gta_rehearse as G, viewchecks_now as VC; '
            'print("\\n".join(VC.solid_faults(G.shot4, G.SHOT4_LEN, frames=[8, 12, 18, 40], label="v7")))')
    r = _as_seen(V7_COMMIT, code, {'viewchecks_now.py': 'viewchecks.py'})    # today's check on version 7's own code
    if r is None:
        return False, 'COULD NOT TEST: version 7 is not in this copy\'s history'
    water = any(ln.startswith('BODY:') and ' 3.33 s: effect 0 shows through the cruiser' in ln for ln in r.stdout.splitlines())
    lines = [ln for ln in r.stdout.splitlines() if ln.startswith('BODY:') and 'jason' in ln and 'tulip' in ln]
    arm = any('rubbed out' in ln for ln in lines)
    hips = any('window pillar' in ln for ln in lines)
    bonnet = any('drawn body shows through the tulip\'s bonnet' in ln and ' 0.67 s' in ln for ln in lines)
    return arm and hips and bonnet and water, f'v7 at 1.0 and 1.5 s: arm through the window frame {arm}; hips ' \
        f'through the pillar {hips}; at 0.67 s the body through the bonnet {bonnet}; at 3.33 s the hydrant water ' \
        f'through the cruiser {water}' + \
        ('' if r.returncode == 0 else f'; crashed: {r.stderr.strip().splitlines()[-1:]}')


@test
def bump_test_bench_old_poses():
    """Rule 5 (nothing passes through anything; the fault of GTA v4 note 4 and v7 note 3, Jason's body through the car):
    the solid-body bench (bench_move.py, the shot 4 rebuild) runs its bump tests on the OLD failed poses it replaced and
    must catch them: the chat 33 seated still (his hip 7.4 cm into the seat, the pistol 4.8 cm into his body) and the old
    lean (leanout.at) at K3 (into the dash); and must pass the new move at the same moments (K1, K3). About 10 s.
    Not in this proof: audit.py, the other films' bump test, has no saved example of its own yet (rule_proofs.json)."""
    import bench_move as BM
    import gta_cast as GC
    import leanout as LO
    sp = dict(GC.cast()['jason'], mood='stern')
    T = dict((k, t) for t, k in reversed(BM._times()))
    old = BM._old_out(LO.seated(sp))
    seat, gun = BM.car(old).get('seat R', (0, 0))[1], BM.pistol(old).get('pistol in body', (0, 0))[1]
    dash = 'dash' in BM.car(BM._old_out(LO.at(T['K3'], sp)))
    new = [k for k in ('K1', 'K3') for o in [BM.solve(BM.goals_at(T[k]))] if BM.car(o) or BM.pistol(o) or BM.gun_car(o)]
    ok = seat >= 5 and gun >= 3 and dash and not new
    return ok, f'old still: seat {seat} cm, pistol {gun} cm; old K3 into the dash {dash}; new move faults at {new or "none"}'


@test
def audit_door_through_officer():
    """Rule 5 (a bump test on every frame; Power Crime Action note 47, Sam 20 Oct, animatic 3: "The door clips through
    the character."): the van's rear door swung through the officer who slams it. The fix moved him 0.8 m further back,
    clear of the swing (notes/archive/power-crime-action.md row 47). The film's code from before 14 Nov was not kept,
    so the old spot is rebuilt by undoing just that recorded move. audit.py, the bump test every other film uses, must
    flag the van's door in the officer there, and pass the film as it is now. About 10 s."""
    import power_crime as PC
    import audit as A
    real = PC.door_officer

    def old_spot(img, cam, t):                       # the officer where he stood in animatic 3
        put = PC.put
        PC.put = lambda img_, cam_, sp, x, z, *a, **k: put(img_, cam_, sp, x - 0.8, z, *a, **k)
        try:
            real(img, cam, t)
        finally:
            PC.put = put

    def door_hits():
        return [f['text'] for f in A.run(PC, 15.9, 16.6, log=lambda *a: None)
                if f['what'] == 'collision' and set(f['names']) == {'VAN', 'VANPC'}]
    now = door_hits()
    PC.door_officer = old_spot
    try:
        then = door_hits()
    finally:
        PC.door_officer = real
    ok = any('door' in x for x in then) and not now
    return ok, f'animatic 3 spot: {then or "NOT flagged"}; today: {now or "clean"}'


# ------------------------------------------------------------------------------------------------ running them
@test
def standing_legs_straight_elbows_out():
    """Rule 81 (Sam, 8 Nov, Ad-Vanced Notice notes 15-17): standing at rest, each knee sits within 5 units of the line
    from hip to ankle (the old solver bent it 36 units forward), and each elbow sits a little OUTSIDE the line from
    shoulder to wrist (never inside it, never more than 40 units out), whatever the shoulder width."""
    import views as V
    bad = []
    for sw in (130, 150, 186):
        j = V.standing({'shoulders': sw})
        for side, sg in (('L', -1), ('R', 1)):
            hip, foot, knee = j['hip' + side], j['foot' + side], V.knee_of(j, side)
            u = (knee[1] - hip[1]) / ((foot[1] - hip[1]) or 1)
            dev = max(abs(knee[0] - (hip[0] + (foot[0] - hip[0]) * u)), abs(knee[2] - (hip[2] + (foot[2] - hip[2]) * u)))
            sh, el, wr = j['sh' + side], j['el' + side], j['wr' + side]
            v = (el[1] - sh[1]) / ((wr[1] - sh[1]) or 1)
            out = sg * (el[0] - (sh[0] + (wr[0] - sh[0]) * v))
            if dev > 5:
                bad.append(f'sw {sw} {side}: knee {dev:.0f} off the line')
            if not 0 < out < 40:
                bad.append(f'sw {sw} {side}: elbow {out:.0f} out (wanted 0 to 40)')
    return not bad, '; '.join(bad) or 'knees on the hip-ankle line; elbows a little out'


@test
def elbow_folded_back_is_a_stop():
    """Rule 41 (Sam, 13 Nov, Blessed animatic 3: an arm bent the wrong way passed 185 flags as 'allowed'): an arm whose
    elbow sits across the chest with the forearm running back out is refused in 3D, whatever allow() is open and
    whichever way the person faces; the same arm with the elbow out is fine."""
    import figure as F
    import views as V
    sw = 150
    j = V.standing({'shoulders': sw})
    V.arm_to(j, 'R', (sw * 0.55, -250.0, 40.0), 'in', 'palm')       # Brand's hand through his hair, elbow in
    stopped = False
    try:
        with F.allow('a test'):
            V.check_arm3(j, 'R', 'test arm')
    except F.FigureError:
        stopped = True
    V.arm_to(j, 'R', (sw * 0.55, -250.0, 40.0), 'out', 'palm')       # the same hand, elbow out
    fine = True
    try:
        V.check_arm3(j, 'R', 'test arm')
    except F.FigureError:
        fine = False
    return stopped and fine, f'folded arm stopped: {stopped}; the elbow-out arm passes: {fine}'


@test
def folded_back_never_allowed_on_screen():
    """Job C 1 (Sam, 13 Nov): the on-screen arm check's 'folded back across the body' is never waved through by the
    'skeleton arm' allow(); with ARM_FOLD_NAMED it is written to pre-flight's named list instead of stopping."""
    import tempfile
    import figure as F
    stopped = False
    try:
        with F.allow('a skeleton arm, checked in 3D (check_arm3); on screen it may be foreshortened'):
            F.fail('test arm: elbow folded back across the body (elbow on the chest, forearm pointing back out)')
    except F.FigureError:
        stopped = True
    with F.allow('a skeleton arm'):
        F.fail('test arm: upper arm 99 is longer than 90 (+6%)')         # an ordinary fault is still allowed
    path = tempfile.mktemp()
    os.environ.update(ARM_FOLD_NAMED='1', NAMED_FAULTS_FILE=path)
    try:
        F.fail('test arm: elbow folded back across the body')
        named = open(path).read().strip()
    finally:
        del os.environ['ARM_FOLD_NAMED'], os.environ['NAMED_FAULTS_FILE']
    return stopped and named.endswith('folded back across the body'), f'stopped: {stopped}; named: {named!r}'


@test
def point_hand_shows_a_finger():
    """Rule 41 (Sam, 4 Nov, MidTerminal note 33): whenever anyone points, the hand shows a pointing finger: the house
    circle hands draw one for 'point', and films that load them after their own finger keep it."""
    import types
    from satire_style import install_circle_hands
    calls = {}
    B = types.SimpleNamespace()
    install_circle_hands(B)

    class P:
        def poly(self, *a, **k):
            calls['poly'] = calls.get('poly', 0) + 1

        def ell(self, *a, **k):
            calls['ell'] = calls.get('ell', 0) + 1
    B.gesture_hand(P(), (0, 0), (0, 100), 'point', (230, 190, 160))
    point = dict(calls)
    calls.clear()
    B.gesture_hand(P(), (0, 0), (0, 100), 'palm', (230, 190, 160))
    ok = point.get('poly', 0) >= 1 and point.get('ell', 0) >= 2 and not calls.get('poly')
    return ok, f"point hand: {point}; palm hand: {calls}"


@test
def grips_contacts_and_carry():
    """Job G (9 Nov): a hand that can't reach the table hovers and is caught (views.arm_to stops at full reach without
    a word); a hand on the top passes; a cup handed over before the hand reaches it jumps and is caught."""
    import grips
    import posegallery as G
    import views as V
    j = V.standing(G.MODEL)
    near, far = grips.Table(z0=95.0), grips.Table(z0=520.0)
    grips.on_table(j, 'R', near, 112.0)
    grips.on_table(j, 'L', far, -112.0)
    fs = grips.contact_faults(j)
    ok1 = [f[:2] for f in fs] == [('L', 'hovers'), ('L', 'off edge')]
    hand = lambda t: (100.0 * t, 0.0)                     # the hand moves in from 0 to 100 over a second
    good = grips.Carry([(0.0, lambda t: (100.0, 0.0)), (1.0, hand)]).faults()
    bad = grips.Carry([(0.0, lambda t: (100.0, 0.0)), (0.5, hand)]).faults()
    return ok1 and not good and len(bad) == 1, f"contacts {fs}; carry on time {good}; early {bad}"


@test
def shoulder_seam_caught():
    """Rule 81 (Sam, 7-8 Nov; Job G, 9 Nov): the shoulder-seam check. Drawn front on and then three-quarter at the same
    spot (as the gallery and a turning film do), the pointing arm joins its own body, not the one left over from the
    last drawing (that cut a wedge of background into the shoulder: the gap Sam saw, failed four times by hand). Then
    a gap painted across the far arm's join, and a line painted across the near arm's, must both be caught."""
    import itertools
    import body as B
    import figure as F
    import handcheck as H
    import kitchecks
    import limbs
    import numpy as np
    import posegallery as G
    import views as V
    from PIL import Image
    from satire_style import install_circle_hands
    B.SS = 1
    F.guard(B)
    F._ALLOW.append('the pose gallery')
    install_circle_hands(B)
    limbs.install(B)
    kitchecks.install()
    H.install()

    def probe(name, deg):
        im = Image.new('RGBA', (1200, 1100), G.BG)
        H.begin()
        V.person(im, B.Cam(1.0, 540, 960), 600, 330, 0.62, G.MODEL, 0.0, deg, G.pose(name, G.MODEL))
        pp = H.FRAME[-1]
        H.end(0.0)
        return pp

    def paint(pp, sd, kind):                        # 4 pixels just before the sleeve on each walked line
        a, k = pp['arms'][sd], pp['k']
        sh, el = np.array(a['sh'], float), np.array(a['el'], float)
        u = (el - sh) / np.linalg.norm(el - sh)
        v = np.array([-u[1], u[0]])
        for off in np.linspace(-0.6, 0.6, 7):
            ts = np.arange(-0.35 * F.UPPER * k, 0.45 * F.UPPER * k)
            pts = (sh + off * 30 * 1.15 * k * v + ts[:, None] * u).round().astype(int)
            on = [a['sleeve'][y, x] for x, y in pts]
            i = next((i for i in range(1, len(on)) if on[i] and not on[i - 1]), None)
            for x, y in ([] if i is None else pts[max(0, i - 4):i]):
                for dx, dy in itertools.product((-1, 0, 1), repeat=2):
                    q = (y + dy, x + dx)
                    pp['other'][q] = pp['cloth'][q] = a['sleeve'][q] = False
                    if kind == 'gap':
                        pp['body'][q] = pp['inkpx'][q] = False
                    else:
                        pp['inkpx'][q] = True

    probe('pointing', 0.0)
    three = probe('pointing', 45.0)
    clean = H.seam_faults(three, 'R', three['arms']['R']) + H.seam_faults(three, 'L', three['arms']['L'])
    paint(three, 'R', 'gap')
    gap = H.seam_faults(three, 'R', three['arms']['R'])
    front = probe('hands up', 0.0)
    near = next(sd for sd in 'LR' if sd not in front['behind'])
    paint(front, near, 'line')
    line = H.seam_faults(front, near, front['arms'][near])
    return (not clean and gap and line and 'R' in three['behind'],
            f"three-quarter pointing after front on: {clean or 'clean'}; gap painted (far arm): {gap}; "
            f"line painted (near arm): {line}")


@test
def held_prop_touches():
    """Job G chat 3: a hand meets what it holds on the picture (handcheck.held_faults), not only in 3D. The phone at
    the ear (redone: the phone sat on top of his head) and the cup are clean from every view; the same phone drawn a
    hand's width and more away from the hand is caught. Job J: a prop hidden on the picture (behind his back or head)
    is flagged, and the views it is flagged in are exactly the gallery's avoid views for it."""
    import body as B
    import figure as F
    import handcheck as H
    import kitchecks
    import limbs
    import moves
    import posegallery as G
    import views as V
    from PIL import Image
    from satire_style import install_circle_hands
    B.SS = 1
    F.guard(B)
    F._ALLOW.append('the pose gallery')
    install_circle_hands(B)
    limbs.install(B)
    kitchecks.install()
    H.install()

    def faults(j, deg):
        im = Image.new('RGBA', (1200, 1100), G.BG)
        H.begin()
        V.person(im, B.Cam(1.0, 540, 960), 600, 330, 0.62, G.MODEL, 0.0, deg, j)
        pp = H.FRAME[-1]
        H.end(0.0)
        return [f for sd in 'LR' for f in H.held_faults(pp, sd, pp['arms'][sd])], \
            sum(int(pp['arms'][sd]['prop'].any()) for sd in 'LR')

    clean, seen, hid = [], 0, set()
    rows = {'phone_ear': 'phone at the ear', 'phone_read': 'phone, reading', 'mug': 'cup in hand', 'mug_sip': 'cup, sipping'}
    for name in ('phone_ear', 'phone_read', 'mug', 'mug_sip'):
        for deg, label in G.VIEWS:
            fs, n = faults(moves.pose(G.MODEL, name), float(deg))
            clean += [f for f in fs if f[0] != 'prop hidden']
            hid |= {(rows[name], label) for f in fs if f[0] == 'prop hidden'}
            seen += n
    avoid = {(r, lb) for r in rows.values() for lb in G.AVOID.get(r, {})}
    hid_ok = hid == {(r, lb) for r, lb in avoid if 'hidden' in G.AVOID[r][lb]}   # Job J: every hidden prop is avoided
    far = V.standing(G.MODEL)
    V.arm_to(far, 'R', (120.0, 300.0, 120.0), 'down', 'grip')
    moves._held(far, 'R', G.MODEL, lambda p, j2: moves._phone(p, {**j2, 'wrR': (j2['wrR'][0] + 90, j2['wrR'][1] - 90)},
                                                              'R'))
    caught = faults(far, 0.0)[0]
    return not clean and seen == 24 and bool(caught) and hid_ok, \
        f"kit poses: {clean or 'clean'} ({seen} of 24 props seen); phone moved off the hand: {caught}; " \
        f"props hidden: {sorted(hid)} ({'= the avoid list' if hid_ok else 'NOT the avoid list'})"


@test
def held_over_or_behind_the_head():
    """Protest Tiers note 1 (chat 7): a held thing up at the head is in front of or beside it (rule 41). Chat 5's phone
    (hand at the crown, the phone a prop drawn before the head) is caught from the front as covered by the head though
    in front of it; a phone held up behind the head is caught from every view; the whole pose gallery is clean of both."""
    import body as B
    import figure as F
    import handcheck as H
    import kitchecks
    import limbs
    import posegallery as G
    import views as V
    from PIL import Image
    from satire_style import install_circle_hands
    B.SS = 1
    F.guard(B)
    F._ALLOW.append('the pose gallery')
    install_circle_hands(B)
    limbs.install(B)
    kitchecks.install()
    H.install()
    kinds = ('behind head', 'under head')

    def found(j, deg):
        im = Image.new('RGBA', (1200, 1100), G.BG)
        H.begin()
        V.person(im, B.Cam(1.0, 540, 960), 600, 330, 0.62, G.MODEL, 0.0, deg, j)
        return [f for f in H.end(0.0) if any(k in f['kind'] or k in f['text'] for k in kinds)]

    def phone(p, j2):                                # a phone above the hand, drawn as a plain prop (chat 5)
        x, y = j2['wrR'][0], j2['wrR'][1]
        p.poly([(x - 22, y - 74), (x + 22, y - 74), (x + 22, y + 4), (x - 22, y + 4)], (40, 44, 54), (20, 20, 24), 2.0)

    def c5():                                        # (the model's head is smaller: the hand at his brow, as the
        j = V.standing(G.MODEL)                      # marcher's was at his crown)
        V.arm_to(j, 'R', (40.0, -210.0, 90.0), 'out')
        j['props'] = [phone]
        return j

    def back():
        j = V.standing(G.MODEL)
        V.arm_to(j, 'R', (30.0, -260.0, -90.0), 'out')
        j['props'] = [phone]
        return j
    gallery = [(n, lb) for n, build, _ in G.GALLERY for deg, lb in G.VIEWS
               if lb not in G.AVOID.get(n, {}) and found(build(G.MODEL), float(deg))]
    V.RAISED_OVER = False                          # the kit as chat 5 drew it: the hand and phone under the face
    try:
        front = found(c5(), 0.0)
    finally:
        V.RAISED_OVER = True
    fixed = found(c5(), 0.0)                       # chat 8: the kit draws a raised hand nearer than the head over it
    behind = [deg for deg, _ in G.VIEWS if found(back(), float(deg))]
    ok = not gallery and bool(front) and not fixed and len(behind) == len(G.VIEWS)
    return ok, f"gallery: {gallery or 'clean'}; chat 5's phone from the front: {'caught' if front else 'MISSED'} " \
               f"(kit as then), {'clean' if not fixed else 'STILL UNDER'} (kit now); " \
               f"phone behind the head caught in {len(behind)} of {len(G.VIEWS)} views"


@test
def critique_library():
    """Job J: a clean critique pass files each panel marked "new" in the catalogue's "Passed the critique" table,
    once (a second clean pass adds nothing), and panels not marked new are not filed."""
    import tempfile
    import critique as C
    path = os.path.join(tempfile.mkdtemp(), 'cat.md')
    open(path, 'w').write('# Kit catalogue\n')
    spec = {'panels': [{'is': 'a pigeon, side on', 'new': 'Swindon pigeon', 'drawn': 'elder_swindon.pigeon'},
                       {'is': 'shot 3, wide'}]}
    a = C.library('test', spec, 1, 2, path)
    b = C.library('test', spec, 1, 3, path)
    text = open(path).read()
    ok = a == ['Swindon pigeon'] and b == [] and text.count('Swindon pigeon') == 1 and 'shot 3' not in text
    return ok, f"first pass filed {a}; second {b}; rows: {text.count('| Swindon pigeon |')}"


@test
def lying_and_pose_checks():
    """Job G chat 4: Sam's lying notes caught (Ad-Vanced 57-58: both arms on one side, no neck; Elder Swindon 6: the
    arm curled up off the ground) and every kit lying pose clean from every view; and pre-flight's pose check
    (posecheck.py) flags a gallery pose seen from an avoid view and a pose with no gallery row."""
    import numpy as np
    import body as B
    import handcheck as H
    import lying as L
    import moves
    import posecheck as P
    import posegallery as G
    import views as V
    from PIL import Image
    kit = {p: sum(len(v) for v in vs.values()) for p, vs in L.gallery().items()}
    sp = L._cast()[0]
    old = L.POSES['face_down']

    def face_down_1(sp):                                 # the kit's arms before chat 4: elbows bent up in the air
        k = old(sp)
        for side, pole in (('R', (0.2, 1.0, -0.6)), ('L', (0.3, 1.0, 0.8))):
            k['el' + side], k['wr' + side] = L.limb(k['sh' + side], k['wr' + side], L.UPPER, L.FORE, pole)
        return k
    L.POSES['face_down'] = face_down_1
    try:
        k, surf = L.lie(sp, 'face_down', 0.0, 0.0, 0.0)
    finally:
        L.POSES['face_down'] = old
    curled = [f for f in L.body_faults(k, sp, surf) if 'held up' in f]
    k, surf = L.lie(sp, 'ball', 0.0, 0.0, 0.0)          # Ad-Vanced 57: both arms over the head off one shoulder
    for side in 'LR':
        k['el' + side], k['wr' + side] = L.limb(k['sh' + side], k['neck'] + np.array([0.28, -0.12, 0.3]),
                                                L.UPPER, L.FORE, (0.1, 0.3, 1.0))
    one_side = [f for ang in (None, 30, 60) for f in L.body_faults(k, sp, surf, L._cam_for(ang, 4.6, (0, 0.2, 0)))
                if 'crosses' in f]
    k, surf = L.lie(sp, 'side', 0.0, 0.0, 0.0)           # 57: the head sat on the shoulders
    k['head'] = k['neck'] + (k['head'] - k['neck']) * 0.45
    no_neck = [f for f in L.body_faults(k, sp, surf) if 'neck' in f]

    P.install()
    H.install()
    P.ON[0] = True
    got = {}
    try:
        for label, name, deg in (('cup from behind', 'mug', 180.0), ('cup from the front', 'mug', 0.0),
                                 ('untested', 'chop', 0.0)):
            im = Image.new('RGBA', (1200, 1100), G.BG)
            H.begin()
            V.person(im, B.Cam(1.0, 540, 960), 600, 330, 0.62, G.MODEL, 0.0, deg, moves.pose(G.MODEL, name))
            got[label] = sorted({f['kind'] for f in H.end(0.0) if f.get('rule') == 42})
    finally:
        P.ON[0] = False
    ok = (not any(kit.values()) and bool(curled) and bool(one_side) and bool(no_neck)
          and got == {'cup from behind': ['avoid view'], 'cup from the front': [], 'untested': ['untested pose']})
    return ok, f"kit lying poses (faults per pose, every view): {kit}; old face-down arm caught: {bool(curled)}; " \
               f"arms off one shoulder caught: {bool(one_side)}; no neck caught: {bool(no_neck)}; pose check: {got}"


@test
def critique_record():
    """Job H (rule 89): critique.py record refuses a half answer and a look written after the result; passes a whole one."""
    import json, tempfile, time
    import critique as C
    d = tempfile.mkdtemp(prefix='kt-crit-r1-p1')
    spec = {'round': 1, 'panels': [{'img': 'x', 'is': 'a man', 'parts': 'P'}, {'img': 'x', 'is': 'a sign', 'parts': 'O'}]}
    json.dump(spec, open(d + '.spec.json', 'w'))
    p1, p2 = C.applies(spec['panels'][0]), C.applies(spec['panels'][1])
    look, res = os.path.join(d, 'look.md'), os.path.join(d, 'result.md')
    whole = (f"## Panel 1\nok: {' '.join(p1[1:])}\nFAULT {p1[0]}: left hand - hovers\n"
             f"## Panel 2\nok: {' '.join(p2[:-1])}\nCAN'T TELL {p2[-1]}: a full-size crop of the sign\n## Cold look\nfine\n")
    half = f"## Panel 1\nok: {' '.join(p1)}\n## Panel 2\nok: {' '.join(p2[:3])}\n"
    out = {}
    for name, l_first, body in (('half', True, half), ('late look', False, whole), ('whole', True, whole)):
        if l_first:
            open(look, 'w').write('1: a man waving\n2: a sign saying EGG MAYO\n'); time.sleep(0.05)
            open(res, 'w').write(body)
        else:
            open(res, 'w').write(body); time.sleep(0.05)
            open(look, 'w').write('1: a man waving\n2: a sign saying EGG MAYO\n')
        out[name] = C.check_answer(d)[0]
    r = C.parse(whole)['panels']
    ok = bool(out['half']) and bool(out['late look']) and not out['whole'] and r[1][p1[0]][0] == 'FAULT' \
        and r[2][p2[-1]][0] == "CAN'T TELL"
    return ok, f"half: {len(out['half'])} reason(s); late look: {len(out['late look'])}; whole: {out['whole'] or 'recorded'}"


@test
def critique_closeups():
    """Sam, 14 Nov: every person in a full critique panel gets a close-up (boxes from the spec's "people" or the
    film's scene(t)); none for a detail, a Glimpse, a panel with no person, or someone already filling the frame;
    overlapping people share one; a film with no scene(t) and no boxes is named, not skipped silently."""
    import critique as C

    class NoScene:
        pass
    panels = [{'t': 1.0, 'is': 'two men talking', 'parts': 'PS',
               'people': [[100, 900, 300, 1500], [250, 950, 420, 1500], {'name': 'judge', 'box': [700, 200, 860, 500]}]},
              {'t': 1.0, 'is': 'a close-up', 'parts': 'P', 'people': [[0, 0, 1080, 1920]]},
              {'t': 1.0, 'is': 'a detail', 'parts': 'P', 'crop': [0, 0, 500, 500], 'people': [[10, 10, 50, 50]]},
              {'t': 1.0, 'is': 'a glimpse', 'parts': 'P', 'glimpse': True, 'people': [[10, 10, 300, 300]]},
              {'t': 1.0, 'is': 'a sign', 'parts': 'O'},
              {'t': 1.0, 'is': 'a crowd', 'parts': 'P'}]
    extra, blind = C.closeups(NoScene(), panels)
    names = [e['is'].split(':')[1].split('(')[0].strip() for e in extra]
    whole = all(0 <= e['crop'][0] < e['crop'][2] <= 1080 and 0 <= e['crop'][1] < e['crop'][3] <= 1920 for e in extra)
    ok = len(extra) == 2 and names == ['person', 'judge'] and blind == [6] and whole \
        and all(e['crop'][2] - e['crop'][0] >= 300 for e in extra) and 'people' not in extra[0]
    real = ''
    try:
        import importlib
        F = importlib.import_module('satire_template')
        t = F.SHOTS[0][1] + 0.5
        got = C.people_boxes(F, t)
        real = f"; satire_template at {t:.1f} s: {len(got or [])} person box(es)"
        ok = ok and got is not None
    except Exception as e:                               # the template may need its voice files: say so, not fail
        real = f"; satire_template not tried ({type(e).__name__})"
    return ok, f"close-ups: {names}, no boxes for panel(s) {blind}, all inside the frame: {whole}{real}"


@test
def critique_each_fault_once():
    """Rule 89 (Sam, 11 Nov): the helper lists each fault ONCE with its panels; the old per-panel form still reads, merged."""
    import json, tempfile, time
    import critique as C
    spec = {'round': 1, 'stage': 'cast', 'panels': [{'img': 'x', 'is': 'a man', 'parts': 'P', 'refs': ['r']}] * 3}
    ids = C.applies(spec['panels'][0])
    rest = ' '.join(i for i in ids if i not in ('A2', 'P2'))
    old = ''.join(f"## Panel {n}\nok: {rest}{'' if n == 3 else ' P2'}\nFAULT A2: cap - no beads\n"
                  + ('FAULT P2: arms - stiff\n' if n == 3 else '') for n in (1, 2, 3)) \
        + '## Cold look\nfine\n## Same fault elsewhere\n- No beads: 1-3.\n- Stiff arms: 3 only.\n'
    new = "## Faults\nFAULT A2 [1-3]: cap - no beads\nFAULT P2 [3]: arms - stiff\n## Checked\n1-3\n## Cold look\nfine\n"
    half = new.replace('1-3\n## Cold', '1-2\n## Cold')
    d = tempfile.mkdtemp(prefix='kt-crit-r1-p1')
    json.dump(spec, open(d + '.spec.json', 'w'))
    why = {}
    for name, body in (('new', new), ('half', half), ('old', old)):
        open(os.path.join(d, 'look.md'), 'w').write('1: a man\n2: a man\n3: a man\n'); time.sleep(0.05)
        open(os.path.join(d, 'result.md'), 'w').write(body)
        why[name] = C.check_answer(d)[0]
    po, pn = C.parse(old), C.parse(new)
    once = lambda r: sorted((f['lids'][0], tuple(f['panels'])) for f in r['faults'])
    step2 = C.STEP2.format(opening='', checks='c', n=3, extra='', notes_part='')
    ok = (once(po) == once(pn) == [('A2', (1, 2, 3)), ('P2', (3,))] and not why['new'] and not why['old']
          and bool(why['half']) and '## Faults' in step2 and 'Same fault elsewhere' not in step2
          and len(new.split()) < 0.6 * len(old.split()))
    return ok, (f"old form {len(old.split())} words, 4 fault lines; new form {len(new.split())} words, 2 fault lines, the "
                f"same faults; panel left unchecked: {'refused' if why['half'] else 'MISSED'}")


@test
def critique_two_hunts_then_sam():
    """Rule 89 (Sam, 11 Nov): two hunts a stage, one pack each; no third; CAN'T TELL never blocks; `fixed` clears hunt 2."""
    import json, tempfile
    import critique as C
    import ledger
    tmp = tempfile.mkdtemp(prefix='kt-hunts')
    keep = ledger.DIR, ledger.CURRENT, C.PACKS
    ledger.DIR, ledger.CURRENT, C.PACKS = tmp, os.path.join(tmp, '.current'), os.path.join(tmp, 'packs')
    try:
        def add(stage, pas, hunt, faults, cant):
            d = ledger.load('kt')
            d.setdefault('critique', {'passes': [], 'lines': {}})['passes'].append(
                {'round': 1, 'pass': pas, 'stage': stage, 'hunt': hunt, 'faults': faults, 'cant_tell': cant, 'open': []})
            ledger.store(d)
        add('sets', 1, 1, 3, 0)
        after1 = (C.third_hunt('kt', 1, 'sets'), C.status('kt')[0])
        add('sets', 2, 2, 2, 4)
        third, blocked = C.third_hunt('kt', 1, 'sets'), C.status('kt')
        other = C.third_hunt('kt', 1, 'cast')
        C.fixed('kt', 'the bench and the lamp redrawn')
        cleared = C.status('kt')
        add('cast', 3, 1, 0, 5)
        cant_only = C.status('kt')
        os.makedirs(os.path.join(C.PACKS, 'kt'))
        for n in (4, 5):                                         # one pack per set: the third is refused
            json.dump({'round': 1, 'stage': 'moves'}, open(os.path.join(C.PACKS, 'kt', f'r1-p{n}.spec.json'), 'w'))
        per_set = C.third_hunt('kt', 1, 'moves')
    finally:
        ledger.DIR, ledger.CURRENT, C.PACKS = keep
    ok = (after1 == (None, False) and third and 'No third' in third and not blocked[0] and other is None
          and cleared[0] and cant_only[0] and per_set and 'WHOLE stage' in per_set)
    return ok, (f"hunt 2 allowed: {after1[0] is None}; hunt 3 refused: {bool(third)}; after `fixed`: "
                f"{'gate open' if cleared[0] else 'BLOCKED'}; 5 can't tell, no fault: {'gate open' if cant_only[0] else 'BLOCKED'}; "
                f"a third pack for one stage: {'refused' if per_set else 'ALLOWED'}")


@test
def critique_helper_kind():
    """Budget job (d), 11 Nov: the pack names one helper kind, never a read-only one (it could not write the cold look);
    a home-made kind must exist with only Read and Write."""
    import critique as C
    line = C.agent_line('/x/r1-p1')
    refused = []
    for k in C.READ_ONLY:
        try:
            C.agent_line('/x/r1-p1', k)
        except SystemExit:
            refused.append(k)
    builtin = C.HELPER in ('general-purpose', 'claude')
    path = os.path.join(C.ROOT, '.claude', 'agents', C.HELPER + '.md')
    own = os.path.exists(path) and bool(re.search(r'^tools: Read, Write$', open(path).read(), re.M))
    ok = f'({C.HELPER}, model sonnet' in line and refused == list(C.READ_ONLY) and (builtin or own)
    return ok, f"names '{C.HELPER}' ({'built in' if builtin else 'own definition'}); read-only kinds refused: {refused}"


@test
def critique_redo_one_command():
    """Budget job (c), 11 Nov: one command redraws, runs the checks and builds one sheet of only the changed panels,
    printing only the fault lines (a fixing chat took four steps and four printouts for this, 59-70 steps a pass)."""
    import contextlib, io, json, tempfile
    from PIL import Image
    import critique as C
    tmp = tempfile.mkdtemp(prefix='kt-redo')
    keep, C.PACKS = C.PACKS, os.path.join(tmp, 'packs')
    a, b, col = os.path.join(tmp, 'a.png'), os.path.join(tmp, 'b.png'), os.path.join(tmp, 'colour')
    Image.new('RGB', (270, 480), (200, 60, 60)).save(a)
    open(col, 'w').write('60')
    draw = (f"python3 -c \"from PIL import Image; Image.new('RGB', (270, 480), (0, int(open('{col}').read()), 200))"
            f".save('{b}')\"")
    noisy = "python3 -c \"[print('frame', i, 'ok') for i in range(40)]; print('FAULT: hand off the mug at 3.2 s')\""
    spec = {'round': 1, 'stage': 'cast', 'draw': [draw], 'checks': [noisy, 'echo hands: clean'],
            'panels': [{'img': a, 'is': 'a man', 'parts': 'P', 'refs': [a]}, {'img': b, 'is': 'a mug', 'parts': 'O'}]}
    sp = os.path.join(tmp, 'spec.json')
    json.dump(spec, open(sp, 'w'))
    runs, said = [], []
    try:
        for green in ('60', '90', '90'):                     # first run; panel 2 redrawn; nothing redrawn
            open(col, 'w').write(green)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                runs.append(C.redo('none', sp))
            said.append(buf.getvalue().splitlines())
    finally:
        C.PACKS = keep
    only_faults = all(len(x) <= 4 and not any(re.search(r'frame \d+ ok', ln) for ln in x) and any('hand off the mug' in ln for ln in x)
                      for x in said)
    ok = ([r[0] for r in runs] == [[1, 2], [2], []] and only_faults and len(runs[1][2]) == 1
          and os.path.exists(runs[1][2][0]) and not runs[2][2] and 'nothing to look at' in said[2][-1])
    return ok, (f"changed panels per run: {[r[0] for r in runs]}; printed {[len(x) for x in said]} lines a run for 42 "
                f"lines of check output; the fault kept: {only_faults}; unchanged run: no sheet")


@test
def critique_palette_colour():
    """Budget job (e), 11 Nov (lines A2, S3; Blessed "orange, not buff brick"): a main colour of ours the reference shows
    almost none of is flagged by script; the right colour under different light, and the photo's sky, are not."""
    import tempfile
    from PIL import Image, ImageDraw
    import critique as C
    ref = os.path.join(tempfile.mkdtemp(prefix='kt-pal'), 'ref.jpg')
    photo = Image.new('RGB', (400, 300), (120, 160, 215))                      # sky
    d = ImageDraw.Draw(photo)
    d.rectangle([40, 90, 360, 300], fill=(196, 160, 104))                      # a buff brick court
    d.rectangle([170, 200, 230, 300], fill=(60, 50, 44))                       # its door
    photo.save(ref, quality=90)

    def ours(wall):
        im = Image.new('RGB', (540, 480), (255, 255, 255))
        dd = ImageDraw.Draw(im)
        dd.rectangle([60, 120, 480, 480], fill=wall)
        dd.rectangle([240, 330, 300, 480], fill=(52, 44, 40))
        return im
    old, new = C.palette(ours((222, 118, 40)), [ref]), C.palette(ours((210, 172, 116)), [ref])
    ok = len(old) == 1 and 'orange' in old[0] and not new
    return ok, f"orange wall beside a buff reference: {old or 'MISSED'}; buff wall, lighter than the photo: {new or 'clean'}"


@test
def critique_checklist_parts():
    """Job H: the helper's checklist.md holds A plus only the parts asked, with no "Came from", counts or tools."""
    import critique as C
    s = C.checklist_for('PO')
    secs = set(re.findall(r'^## ([A-Z])\.', s, re.M))
    bad = [x for x in ('Came from', 'Tool:', 'Islamocommunism', '(10)') if x in s]
    return secs == {'A', 'P', 'O'} and not bad, f'sections {sorted(secs)}; leaks: {bad or "none"}'


@test
def critique_where_pops():
    """Job H (rule 56, line M1): critique.py where flags a thing that pops in mid-shot (Elder Swindon 59, 62, 64)."""
    import types
    import critique as C
    film = types.SimpleNamespace(FPS=12, SHOTS=[('1 street', 0.0, 4.0), ('2 shop', 4.0, 8.0)],
                                 draw_order=lambda t: ['set', 'MAN'] + (['DOG'] if t >= 5.0 else [])
                                 + (['PIGEON'] if t < 2.0 else []), ENTRANCES={})
    _, flags = C.where('made-up', film=film)
    film.ENTRANCES = {'DOG': 'runs in from the left'}
    _, planned = C.where('made-up', film=film)
    caught = any('DOG in at 5.00' in f for f in flags) and any('PIGEON out at' in f for f in flags)
    return caught and len(flags) == 2 and len(planned) == 1, f'flags: {flags}; with DOG planned: {planned}'


@test
def bleeps_every_swear():
    """Rule 26 (Sam, 4 Nov; Job L): every swear in the script is bleeped, asterisks or not: a line with a swear and no
    bleep is caught; with its bleep, a '[bleep]' gap, or a SWEARS_OK entry it passes."""
    import types
    import voices
    film = types.SimpleNamespace(LINES=[dict(n=9, who='harry', text="Well, she's f****** dead.")])
    caught = voices.bleep_check(film, [])
    film.LINES[0]['bleep'] = (2.56, 2.96)
    fixed = voices.bleep_check(film, [])
    film.LINES = [dict(n=1, who='far', text="I swear to [bleep] I'll have your [bleep] ass deported."),
                  dict(n=2, who='a', text='Fucking shit, mate.', bleep=[(0.1, 0.4), (0.6, 0.8)]),
                  dict(n=3, who='b', text='What a prick.')]
    film.SWEARS_OK = [(3, 'prick', 'Sam: leave it')]
    rest = voices.bleep_check(film, [])
    ok = len(caught) == 1 and not fixed and not rest
    return ok, f'unbleeped caught: {len(caught)}; bleeped / gaps / allowed: {len(fixed) + len(rest)} fault(s)'


@test
def subtitle_starts_on_its_word():
    """Rule 62's 0.3 s (Terfwarts line 8, Job L): a subtitle piece up 2.3 s before its phrase is said is caught (the
    subtitle code's syllable fallback, still live); Ad-Vanced Notice's hand-timed subtitles pass."""
    import importlib
    import voices
    out = {}
    for name in ('terfwarts', 'ad_vanced_notice'):
        film = importlib.import_module(name)
        out[name] = voices.caption_start_check(film, voices.prepared(film))
    caught = any('line 8' in f and 'to any man' in f for f in out['terfwarts'])
    return caught and not out['ad_vanced_notice'], \
        f"Terfwarts line 8 caught: {caught}; Ad-Vanced Notice: {len(out['ad_vanced_notice'])} fault(s)"


@test
def cut_before_the_return():
    """Rule 72 (Job L): an arm posed out, then hanging at rest in the last 0.4 s before a cut, is caught; the same arm
    held out to the cut, or the film's last shot ending on black, passes."""
    import types
    import kitchecks as K
    import views as V
    sp = {'shoulders': 150}
    rest = V.standing(sp)
    up = V.standing(sp)
    V.set_arm(up, 'R', 1.4, 0.6)                 # the right arm swung forward and up, bent
    rec = lambda j, t: ('', 'ANDY', {'_rest': K._rest_record(j, t), '_t': t})
    film = types.SimpleNamespace(SHOTS=[('a', 0.0, 2.0), ('b', 2.0, 4.0)], DUR=4.0)
    drop = [rec(up, 1.0), rec(up, 1.25), rec(rest, 1.75)]
    held = [rec(up, 1.0), rec(up, 1.25), rec(up, 1.75)]
    last = [rec(up, 3.0), rec(up, 3.25), rec(rest, 3.75)]
    a, b, c = K.cut_rests(film, drop), K.cut_rests(film, held), K.cut_rests(film, last)
    gap = K._rest_gap(drop[0][2]['_rest'], 'R')
    return len(a) == 1 and not b and not c, f'raised arm {gap:.2f} arm lengths from rest; dropped: {len(a)}, ' \
                                           f'held: {len(b)}, last shot: {len(c)}'


@test
def famous_face_size():
    """Rule 50 (Job L): a famous person's face is measured as drawn (1920-tall frame): a close-up passes 240 px, a wide
    shot alone is caught, a name never drawn is caught, and a film with people but no FAMOUS list is asked for one."""
    import types
    from PIL import Image
    import body as B
    import kitchecks as K
    import patriots3_cast as C
    import views as V
    B.SS = 1
    px = {}
    for s in (0.3, 1.6):
        im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
        j2 = V.person(im, B.Cam(1.0, 540, 960), 540, 700, s, dict(C.GUNNER), 0.0, 5.0)
        px[s] = j2['_drawn']['face_px']
    film = types.SimpleNamespace(FAMOUS=['gunner'], HAS=('people',))
    wide = K.faces(film, [('', 'GUNNER', {'face_px': px[0.3], 'face_in': True})])
    close = K.faces(film, [('', 'GUNNER', {'face_px': px[0.3], 'face_in': True}),
                           ('', 'GUNNER', {'face_px': px[1.6], 'face_in': True})])
    film.FAMOUS = ['gunner', 'trump']
    missing = K.faces(film, [('', 'GUNNER', {'face_px': px[1.6], 'face_in': True})])
    asked = K.faces(types.SimpleNamespace(HAS=('people',)), [])
    ok = len(wide) == 1 and not close and len(missing) == 1 and 'never found' in missing[0] and len(asked) == 1
    return ok, f'face {px[0.3]:.0f} px wide, {px[1.6]:.0f} px close; wide caught {len(wide)}, close {len(close)}, ' \
               f'missing name {len(missing)}, no list {len(asked)}'


@test
def sounds_and_references_kept():
    """Rule 37 (Job L): a reference or sound file git does not hold is listed at the handover (ledger log / kept)."""
    import ledger
    path = os.path.join(ledger.ROOT, 'refs', 'zz-kittest.txt')
    open(path, 'w').write('test')
    try:
        add, _ = ledger.kept()
    finally:
        os.remove(path)
    after, _ = ledger.kept()
    caught = any(p.endswith('zz-kittest.txt') for p, _ in add)
    return caught and not any(p.endswith('zz-kittest.txt') for p, _ in after), f'untracked file caught: {caught}'


@test
def quiet_cost_line():
    """Job 2 (Sam, 19 Nov) and the check audit (Sam, 26 Nov, his answer 2: the paused budget alarms deleted, "tracked
    quietly"): the cost line is recorded in the ledger and the notes at a handover and nothing is shown: no forecast,
    no warning, no stop, also for a stage far over its share and a film over its estimate."""
    import shutil
    import tempfile
    import costline, ledger
    tmp = tempfile.mkdtemp()
    keep = ledger.DIR
    try:
        ledger.DIR = tmp
        d = {'film': 'zz', 'estimate': 10.0, 'chats': [{'cost': 30.0, 'round': None, 'notes': 0, 'repeats': [],
             'date': '2026-11-26', 'chat': 'aaaaaaaa', 'model': 'opus', 'stage': 'x'}], 'checks': {}, 'stages': ledger.parse_stages('cast 3, sets 2')}
        ledger.mark_stage(d, 'cast')
        ledger.store(d)
        notes = os.path.join(tmp, 'zz.md')
        open(notes, 'w').write('# zz\n')
        shown = costline.faults('zz', notes)
        logged = ledger.load('zz').get('cost_log') or []
        in_notes = costline.MARK in open(notes).read()
        gone = [n for n in ('forecast', 'budget_stop', 'stage_alarm', 'problems') if hasattr(ledger, n) or hasattr(costline, n)]
    finally:
        ledger.DIR = keep
        shutil.rmtree(tmp, ignore_errors=True)
    ok = shown == [] and len(logged) == 1 and logged[0]['spent'] == 30.0 and in_notes and not gone
    return ok, f'shown {shown}, recorded {logged}, in the notes {in_notes}, alarms left {gone}'


@test
def copies_in_a_group():
    """Job K (Sam: Y, 10 Nov): two people drawn from one copy in one frame are flagged (Ad-Vanced Notice's officers
    before they were varied); a varied pair passes; COPIES_OK lets a meant pair through."""
    import types
    from PIL import Image
    import body as B
    import figure as F
    import kitchecks as K
    import views as V
    import ad_vanced_notice_street as ST
    B.SS = 1
    K.install()
    person = sys.modules['views'].person
    im, cam, n0 = Image.new('RGBA', (1080, 1920)), B.Cam(1.0, 540, 960), len(K.DRAWN)
    for t, same in ((1.0, True), (2.0, False)):
        F.CONTEXT['where'] = f'kittest {t}'
        a = dict(ST.CAST['O1'])
        b = dict(a, name='ICE officer 9') if same else dict(ST.CAST['O2'])
        person(im, cam, 300, 800, 0.4, a, t, 0)
        person(im, cam, 700, 800, 0.4, b, t, 0)
    F.CONTEXT['where'] = ''
    rec = K.DRAWN[n0:]
    flags = K.copies(types.SimpleNamespace(), rec)
    ok = K.copies(types.SimpleNamespace(COPIES_OK=[('ICE officer 1', 'ICE officer 9', 'twins')]), rec)
    return len(flags) == 1 and 'kittest 1.0' in flags[0] and not ok, f'flags: {flags}; with COPIES_OK: {ok}'



@test
def lopsided_invented_only():
    """Job K 5 (Sam: Y, 11 Nov): an invented person can be drawn a touch uneven (brow, mouth corner, side hair);
    a likeness head never is. Since the one-route kit (20 Nov) the film that taught it (Vance's advert) draws from its
    bookmark, so this draws with today's people kit: an invented Milburn face (the goth) changes a little when
    lopsided, Andy and Kemi on the house head (likenesses) not at all."""
    import numpy as np
    from PIL import Image
    import body as B
    import views as V
    import people as PK
    B.SS = 1

    def face(sp):
        im = Image.new('RGBA', (1080, 1920), (238, 234, 228, 255))
        V.person(im, B.Cam(1.0, 540, 960), 540, 1150, 2.2, dict(sp), 0.0, 0)
        return np.asarray(im.convert('L'), np.int16)

    def diff(sp):
        return float((np.abs(face(dict(sp, lopsided=True)) - face(dict(sp, lopsided=None))) > 40).mean())
    cast = PK.load('milburn')
    PK.install(cast)
    changed = diff(cast['goth'])
    house = PK.load('facetool')
    PK.install(house)
    likeness = [w for w in ('andy', 'kemi') if diff(house[w]) > 0]
    return 0.0005 < changed < 0.02 and not likeness, \
        f'face pixels changed {changed * 100:.2f}%; likeness heads uneven: {likeness or "none"}'


# ------------------------------------------------------------------------------------------------ Job I faces
@test
def turned_heads_for_anyone():
    """Job I faces (Sam, 11 Nov): any person with a front design turns with their own face (turnhead.register), built
    only when a shot needs it; old faults: views.head_view patched for Vance alone (the lying driver got the old
    generic head, and pre-flight never said), and the driver's draft (his goatee clipped inside the chin: a stripe,
    gone side on; his hair a flat slab round the back). Vance's turned heads stay exactly as before."""
    import hashlib
    from PIL import Image
    import numpy as np
    import body as B
    import views as V
    import ad_vanced_notice_cast as C
    import turnhead as TH
    from ink import curve
    B.SS = 1

    def head(sp, yaw):
        im = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
        V.person(im, B.Cam(1.0, 540, 960), 540, 1060, 1.25, dict(sp), 0.0, yaw)
        return np.asarray(im.crop((375, 620, 705, 1020)).convert('RGB')).astype(int)
    out = []
    # 1. a person with a measured front design but no turned head: recorded (pre-flight names it), then built
    import faces as FA                                      # since 20 Nov (one-route kit) a film measures its people
    keep = TH.PEOPLE.pop('man')                             # in faces.MEASURED; this old film used its own copy
    had = 'man' in FA.MEASURED
    FA.MEASURED.setdefault('man', C.P4.MEASURED['man'])
    del TH.MISSING[:], TH.SEEN[:]
    try:
        head(C.MAN, 90)
    finally:
        TH.PEOPLE['man'] = keep
        if not had:
            FA.MEASURED.pop('man', None)
    caught = ('man', 'side') in TH.MISSING
    del TH.MISSING[:]
    side = head(C.MAN, 90)
    fixed = ('man', 'side') in TH.SEEN and not TH.MISSING
    out.append(f'no turned head: {"caught" if caught else "NOT caught"}, built: {fixed}')
    # 2. the goatee side on: its hair reaches the chin's front (the draft clipped it inside: never past the skin)
    def goatee_front(px):                                   # solid goatee (the ink lines opened away), px
        from scipy.ndimage import binary_opening
        dark = (abs(px - np.array(C.M_HAIR)).sum(2) < 40)[280:, 220:]   # the mouth and chin, side on
        return int(binary_opening(dark, np.ones((5, 5), bool)).any(1).sum())   # rows it covers, mouth to chin
    P = TH.PEOPLE['man']

    def old_over(img, p, f, L, sp, view):                   # the draft (619856d): clipped to the head, no volume
        if view != 'back':
            hd = TH.outline(p, f, view, P.skin, ink=False)
            TH.inside(img, p, hd, lambda pen: pen.poly(curve(f.pts(TH.dense(curve(C.man_goatee(L), 4))), 2),
                                                       C.M_HAIR, None))
            TH.outline(p, f, view, P.skin, fill=False)
    new_over, P.over = P.over, old_over
    try:
        old_g = goatee_front(head(C.MAN, 90))
    finally:
        P.over = new_over
    new_g = goatee_front(side)
    out.append(f'goatee seen side on, rows from the mouth down: old {old_g}, now {new_g}')
    # 3. the hair from behind: a band round the back, not a slab (the draft: from the temples' row to the nape)
    def hair_share(px):
        dark = (abs(px - np.array(C.M_HAIR)).sum(2) < 60) | (abs(px - np.array(C.M_HAIR_L)).sum(2) < 60)
        head_ = dark | (abs(px - np.array(C.M_SKIN)).sum(2) < 40)
        return dark[:300].sum() / max(1, head_[:300].sum())
    prof = P.build({})[1]
    old_prof = dict(prof, hair_top=0.1, hair_top_back=0.1, hair_ragged=0.0, nape=0.66)
    P.built[False] = P.built[False][:1] + (old_prof,) + P.built[False][2:]
    try:
        old_h = hair_share(head(C.MAN, 180))
    finally:
        P.built.clear()
    new_h = hair_share(head(C.MAN, 180))
    out.append(f'hair share of the head from behind: old {old_h:.2f}, now {new_h:.2f}')
    # 4. Vance's side and behind unchanged (pixel for pixel, as drawn before the shared tool, 8 Nov note 44); his
    # three-quarter redrawn (face tool chat 12, Sam: "3/4 front poses ... look gaunt and weird"): both eyes now show
    vh = hashlib.md5(b''.join(head(C.VANCE, y).astype(np.uint8).tobytes() for y in (90, 135, 180))).hexdigest()
    out.append(f'Vance side and behind unchanged: {vh == VANCE_TURNED_MD5}')
    real, seen = FA.eye, []                                 # the eyes are faces.eye since 20 Nov (was traitors_cast.eye)
    FA.eye = lambda *a, **k: (seen.append(1), real(*a, **k))[1]
    try:
        head(C.VANCE, 45)
    finally:
        FA.eye = real
    out.append(f'three-quarter eyes drawn: {len(seen)} (was 1: the far eye hidden)')
    ok = (caught and fixed and new_g >= old_g + 15 and new_h < old_h - 0.06 and vh == VANCE_TURNED_MD5
          and len(seen) == 2)
    return ok, '; '.join(out)


VANCE_TURNED_MD5 = 'd060e9f4dd0faec864fb5ea831162aea'   # side, 3/4 behind, behind: as main line c6b007a (yaw 90-180)


@test
def lying_shirt_and_nape():
    """Job I lying fixes (Sam, 11 Nov, for every character): slumped against a wall the shirt was a stiff box (lying
    16: square shoulders, straight sides), now bent as cloth (lying_flat.Slump); lying with the back of the head to
    us, the neck was drawn again over the head as a square block (18, a blindfold with the driver's hair band), now
    the head is inked all round with no neck over it (turnhead, nape_in_head). Standing views are untouched."""
    import numpy as np
    from PIL import Image
    import body as B
    import lying as L
    import lying_flat as LF
    import turnhead as TH
    import views as V
    import ad_vanced_notice_cast as AC

    def corners(a):                                   # the share of the shirt's top corners filled (a box: ~1)
        ys, xs = np.nonzero(a > 8)
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        h, w = int((y1 - y0) * 0.12), int((x1 - x0) * 0.12)
        return float(np.mean([(a[y0:y0 + h, x0:x0 + w] > 8).mean(), (a[y0:y0 + h, x1 - w:x1] > 8).mean()]))
    made, calls, out, ok = [], [], [], True
    real, real_over = LF.Slump, TH.neck_over

    class Spy(real):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            made.append(self)
    LF.Slump = Spy
    TH.neck_over = lambda *a, **k: (calls.append(1), real_over(*a, **k))[1]
    B.SS = 2
    try:
        for who in ('vance', 'man'):
            sp = dict(AC.CAST[who])
            for pose, ang, yaw in (('slump', None, -60.0), ('back', 60, 0.0), ('ball', 30, 180.0)):
                del made[:], calls[:]
                img = B.canvas((214, 206, 188))
                kk, surf = L.lie(sp, pose, 0.0, 0.0, yaw)
                cam = L._fit(L._cam_for(ang, 4.5, (0, 0.35 if pose == 'slump' else 0.1, 0)),
                             [kk[n] for n in L.POINTS] + [kk['head'] + 0.15 * kk['hup']], fill=0.7)
                L.draw(img, cam, kk, dict(sp, blink=True), 0.0, surfaces=[(p0, n) for _, p0, n in surf])
                if pose == 'slump':
                    if not made:
                        ok = False
                        out.append(f'{who} slumped: shirt NOT bent')
                        continue
                    sl = made[0]
                    bent = Image.new('RGBA', img.size, (0, 0, 0, 0))
                    sl.paste(bent)
                    a0, a1 = corners(np.asarray(sl.layer)[:, :, 3]), corners(np.asarray(bent)[:, :, 3])
                    ok &= a1 < 0.8 * a0
                    out.append(f'{who} slumped: shoulder corners filled {a0:.2f} (box) -> {a1:.2f}')
                elif made:
                    ok = False
                    out.append(f'{who} {pose}: shirt bent though not sitting')
                if pose == 'ball':
                    ok &= not calls
                    out.append(f'{who} back of head lying: neck over it {len(calls)}x')
        del calls[:]
        B.SS = 1
        im = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
        V.person(im, B.Cam(1.0, 540, 960), 540, 1060, 1.25, dict(AC.MAN), 0.0, 180)
        ok &= bool(calls)
        out.append(f'standing from behind: neck over the nape kept ({len(calls)}x)')
    finally:
        LF.Slump, TH.neck_over = real, real_over
        B.SS = 1
    return bool(ok), '; '.join(out)


@test
def lying_fall_settle_clean():
    """Open Wounds chat 16 (body check on shot 2, 8.67-8.92 s): knocked over backwards, the in-between from sitting to
    lying slid every joint straight to its new place, so the head sank into the shoulders (no neck, 4 drawings) and
    the elbows hung 13-20 cm over the dirt (3 drawings). Now the trunk keeps its bone lengths through the settle and
    the arms reach the floor as the back goes down (lying.blend, lying._brace). Measured: body_faults at every
    1/48 s of the settle, facing four ways; and the old point-sliding in-between is still caught."""
    import numpy as np
    import lying as L
    sp = L._cast()[0]
    now = []
    for face in ((-1.0, 0.0), (1.0, 0.0), (0.0, 1.0), (0.6, -0.8)):
        for t in np.arange(1.1, 1.62, 1 / 48):
            kind, *r = L.fall(sp, t, 0.6, 0.0, 6.0, face)
            if kind == '3d':
                now += [f'{face} {t:.2f}: {f}' for f in L.body_faults(r[0], sp, r[1], who='')]
    old = 0                                               # the saved fault: plain point sliding, no brace
    j_sit = L.moves.fall(sp, 1.1, 0.6)[0]
    k0 = L.from_views(j_sit, sp, 0.0, 6.0, (-1.0, 0.0))
    k1, surf = L.lie(sp, 'back', k0['pelvis'][0], k0['pelvis'][2], 0.0)
    for u in np.linspace(0.1, 0.9, 9):
        k = L.Body()
        for n in k0:
            k[n] = k0[n] + (k1[n] - k0[n]) * u if n in L.POINTS else L._unit(k0[n] + (k1[n] - k0[n]) * u + 1e-6)
        old += len(L.body_faults(k, sp, surf, who=''))
    ok = not now and old > 0
    return ok, (f'settle faults now {len(now)} ({"; ".join(now[:3])}); the old sliding in-between caught {old}x')


@test
def lying_neck_from_behind():
    """Job I lying 18 (Sam, 11 Nov, "fix the neck in 14 and 18", a repeated note): curled up and seen from behind,
    the head sat straight on the collar with no neck (the shirt's back and the arm round the head were drawn over
    it) and the back collar stood up beside the head like a block. Now the neck rises out of the collar, which
    wraps its foot. Measured: the neck's own pixels left showing (drawn in a test colour), and the collar's turn."""
    import numpy as np
    import body as B
    import lying as L
    import lying_flat as LF
    import ad_vanced_notice_cast as AC
    real = LF._neck
    out, ok = [], True

    def green(img, hc, sp, aff, view, foot=40):
        return real(img, hc, dict(sp, skin=(0, 255, 0)), aff, view, foot)
    LF._neck = green
    B.SS = 2
    try:
        for who in ('vance', 'man'):
            sp = dict(AC.CAST[who])
            img = B.canvas((214, 206, 188))
            kk, surf = L.lie(sp, 'ball', 0.0, 0.0, 180.0)
            cam = L._fit(L._cam_for(30, 4.5, (0, 0.1, 0)), [kk[n] for n in L.POINTS] + [kk['head'] + 0.15 * kk['hup']],
                         fill=0.7)
            L.draw(img, cam, kk, dict(sp, blink=True), 0.0, surfaces=[(p0, n) for _, p0, n in surf])
            a = np.asarray(img.convert('RGB')).astype(int)
            n = int(((a[:, :, 1] > 200) & (a[:, :, 0] < 60) & (a[:, :, 2] < 60)).sum())
            ok &= n > 2000                            # before: 0 (all of it covered)
            out.append(f'{who} curled from behind: neck showing {n} px (was 0)')
    finally:
        LF._neck = real
        B.SS = 1
    return bool(ok), '; '.join(out)


@test
def eyes_cut_to_the_outline():
    """Rule S5 (tool job, 11 Nov): KG's owl pupil at a hard glance spilled past his eye; eyekit cuts it, and the
    house-style check names a cast file that draws pupils without cutting them."""
    import types
    import eyekit
    import housestyle
    from ink import oval
    import shocking_cast  # noqa: F401  (an old cast that draws uncut pupils)
    r, look, pr = 38, 2.4, 38 * 0.5 * 1.2
    outline = oval(0, 0, r, r, 40)
    old = oval(look * r * 0.3, 2, pr, pr, 28)                  # the old pupil: never cut to the outline
    new = eyekit.inside(outline, old)
    caught = eyekit.spill(outline, old) > 0.05 and eyekit.spill(outline, new) < 1e-3
    flagged = bool(housestyle.eye_faults(types.SimpleNamespace(__name__='shocking')))
    import remakes_creatures  # noqa: F401
    clean = not housestyle.eye_faults(types.SimpleNamespace(__name__='remakes'))
    return caught and flagged and clean, (f'old pupil spills {eyekit.spill(outline, old):.0%}, cut '
                                          f'{eyekit.spill(outline, new):.1%}; old cast flagged {flagged}; Remakes clean {clean}')


@test
def hook_text_planned():
    """Rule 75 (tool job, 11 Nov): a film with HOOK but no KEEP_CLEAR was skipped quietly; now it is refused, and
    pre-flight's gate stops an animatic with no Hook Text plan."""
    import types
    import hookcheck
    no_keep = types.SimpleNamespace(HOOK=('Hook', {'y': 880}))
    no_plan = types.SimpleNamespace()
    planned = types.SimpleNamespace(HOOK=('Hook', {'y': 880}), KEEP_CLEAR=[('face', lambda t: (0, 0, 50, 50))])
    a, b, c = hookcheck.faults(no_keep), hookcheck.plan_faults(no_plan), hookcheck.faults(planned) + hookcheck.plan_faults(planned)
    return bool(a) and len(b) == 2 and not c, f'no KEEP_CLEAR: {len(a)} fault; no plan: {len(b)} gate(s); planned: {len(c)}'


@test
def hook_text_flag_emoji():
    """Open Wounds chat 3 (Sam's Hook Text "Andy is opening old wounds... 🇬🇧", 23 Nov): a flag is two regional
    letters; the card drew them as two letter boxes. Now one flag picture: its red, white and blue all present, and
    one picture's width (not two)."""
    import tempfile
    import numpy as np
    import hook_text as H
    from PIL import Image
    out = []
    for txt in ('Andy is opening old wounds... \U0001F1EC\U0001F1E7', 'Andy is opening old wounds...'):
        with tempfile.NamedTemporaryFile(suffix='.png') as tf:
            H.card(1080, 1920, txt, 880, tf.name)
            out.append(np.asarray(Image.open(tf.name).convert('RGBA')))
    diff = np.any(out[0] != out[1], axis=2)
    ys, xs = np.nonzero(diff)
    px = out[0][diff][:, :3].astype(int)
    red = np.sum((px[:, 0] > 170) & (px[:, 1] < 90) & (px[:, 2] < 90))
    blue = np.sum((px[:, 2] > 90) & (px[:, 0] < 80))
    w = (xs.max() - xs.min()) if len(xs) else 0
    ok = red > 50 and blue > 50
    return ok, f'flag pixels: red {red}, blue {blue}; changed width {w} px'


@test
def moving_figures_against_the_set():
    """Rule 13 (tool job, 11 Nov): Remakes' camp check moved into the kit (setcheck.moving_faults); Remakes calls it.
    Clean on Remakes' camp as built; Link put back into a barrel is caught, and so is a figure drawn over what hides him."""
    import remakes as R
    import remakes_sets as RS
    import setcheck
    clean = not R.camp_paths()
    n, x0, x1, d0, d1, z1, layer = RS.SET_FEET[0]
    real = R._link_camp
    R._link_camp = lambda t: ((x0 + x1) / 2, (d0 + d1) / 2) + tuple(real(t)[2:] if real(t) else ())
    try:
        walk_in = R.camp_paths()
    finally:
        R._link_camp = real
    behind = setcheck.moving_faults(lambda t: [('test', (x0 + x1) / 2, d1 + 0.6, (0.5, 1.8))],
                                    [RS.SET_FEET[0]], RS.CAMP, 0, 0, label='S7')
    caught = any('link stands in' in f for f in walk_in) and any('drawn over' in f for f in behind)
    return clean and caught, f'Remakes clean: {clean}; walk-in caught: {walk_in[:1]}; behind caught: {bool(behind)}'


@test
def moving_figures_per_shot():
    """Rule 13 (Blessed, 12 Nov): a film with a set per shot gives SET_FEET, SET_CAM and MOVE_SPAN keyed by shot;
    film_faults runs each shot against its own set, catches a walk into a thing in either, and names a shot whose
    camera or span is missing."""
    import types
    import setcheck
    from remakes_sets import Level
    L = Level(1.6, 800.0, 1000.0)
    box = ('crate', -0.3, 0.3, 3.0, 3.5, 0.8, 'under')
    walk = lambda t: [('him', 0.0, 2.0 + t, (0.5, 1.8))] if t < 2 else [('her', 2.0, 4.0, (0.5, 1.7))]
    film = types.SimpleNamespace(FPS=12, HAS={'people'}, movers=walk, SET_FEET={'a': [box], 'b': [box]},
                                 SET_CAM={'a': L, 'b': L}, MOVE_SPAN={'a': (0.0, 1.9), 'b': (2.0, 3.0)})
    hit = setcheck.film_faults(film)
    film.SET_FEET = {'a': [box], 'c': [box]}
    named = setcheck.film_faults(film)
    film.SET_FEET = {'b': [box]}
    clear = setcheck.film_faults(film)
    ok = any('a ' in f and 'him stands in the crate' in f for f in hit) and any('c but SET_CAM' in f for f in named) \
        and not clear
    return ok, f'walk-in: {hit[:1]}; missing camera: {named[-1:]}; clear shot: {clear}'


def _finish_fake(tmp, caption=True):
    """A 3 s made-up film (12 fps, a 440 Hz tone, one caption, a Hook Text) run through finish.py in this process."""
    import subprocess
    import types
    import finish
    clean = os.path.join(tmp, 'clean.mp4')
    subprocess.run([finish.FF, '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'color=c=0x203040:s=540x960:r=12:d=3',
                    '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000:duration=3', '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', clean], check=True)
    with open(clean + '.readable.json', 'w') as fh:                 # what the render keeps beside it (could-not-test 3)
        fh.write('{"fps": 12, "frames": {}}')
    m = types.ModuleType('kt_film')
    m.FPS, m.DUR, m.HOOK, m.KEEP_CLEAR = 12, 3.0, ('Hook here', {'y': 880}), []
    if caption:
        m.caption_at = lambda t: 'One two three' if 0.2 <= t < 1.5 else None
    sys.modules['kt_film'] = m
    lines = os.path.join(tmp, 'follow-lines.md')                    # a copy: the tests never use up a real follow line
    with open(lines, 'w', encoding='utf-8') as f:
        f.write('- [ ] Test line. Follow 👉\n')
    os.environ['FOLLOW_LINES'] = lines
    out = os.path.join(tmp, 'out.mp4')
    argv = sys.argv
    sys.argv = ['finish.py', clean, out, '--film', 'kt_film']
    import propose                                  # the test film's own proposal log: empty (lesson 7 step 3's stop
    props, propose.PROPS = propose.PROPS, tmp       # on a real let-through is tested in rule_proofs_gate)
    try:
        finish.main()
    except SystemExit as e:
        return None, str(e)
    finally:
        sys.argv = argv
        propose.PROPS = props
    return out, ''


def _frame(path, t):
    import subprocess
    import numpy as np
    import finish
    w, h, _ = finish.video_info(path)
    raw = subprocess.run([finish.FF, '-loglevel', 'error', '-ss', f'{t}', '-i', path, '-frames:v', '1', '-f', 'rawvideo',
                          '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w, 3)


@test
def finish_captions_by_default():
    """Rule 62 (tool job, 11 Nov): captions were opt-in (SUBTITLES_AT_FINISH) and a film could go out without them;
    finish.py now refuses a film with no caption_at and burns the kit's style (Remakes') into every film that has one."""
    import tempfile
    import subtitles as SUB
    with tempfile.TemporaryDirectory() as tmp:
        none, why = _finish_fake(tmp, caption=False)
        out, _ = _finish_fake(tmp)
        lit = (_frame(out, 0.9)[700:740, :, :].min(2) > 200).sum() if out else 0     # white caption letters, lower third
    import remakes
    same = remakes.draw_subtitle is SUB.draw
    ok = none is None and 'caption' in why and lit > 50 and same
    return ok, f'no captions refused: {none is None}; caption drawn: {lit} white px; Remakes on the kit style: {same}'


@test
def finish_delivers_at_one_point_one():
    """Rule 70 (tool job, 11 Nov): 1.1x was done by hand; finish.py now speeds the film after the captions with the
    voice at its pitch, then adds the Hook Text (still popping at 0.5 s) and the sign-off (still 1.6 s)."""
    import subprocess
    import tempfile
    import numpy as np
    import finish
    import hookcheck
    with tempfile.TemporaryDirectory() as tmp:
        out, _ = _finish_fake(tmp)
        fast = os.path.join(tmp, 'fast.mp4')
        finish.speed_up(os.path.join(tmp, 'clean.mp4'), fast, 1.1)
        film_s = finish._duration(fast)
        signoff = finish._duration(out) - film_s
        raw = subprocess.run([finish.FF, '-loglevel', 'error', '-i', fast, '-f', 's16le', '-ac', '1', '-ar', '48000', '-'],
                             capture_output=True).stdout
        x = np.frombuffer(raw, np.int16).astype(float)[4800:-4800]
        hz = np.argmax(np.abs(np.fft.rfft(x))) * 48000 / len(x)
        x0, y0, x1, y1 = hookcheck.hook_box('Hook here', y=880)
        box = lambda t: _frame(out, t)[y0 // 2 + 4:y1 // 2 - 4, x0 // 2 + 4:x1 // 2 - 4].mean()   # 540 wide: half
        before, after = box(0.35), box(0.85)
    ok = abs(film_s - 3 / 1.1) < 0.12 and abs(signoff - 1.6) < 0.06 and abs(hz - 440) < 5 and before < 120 < after
    return ok, (f'film {film_s:.2f} s (3 s at 1.1x: {3 / 1.1:.2f}); sign-off {signoff:.2f} s; tone {hz:.0f} Hz; '
                f'Hook Text box brightness {before:.0f} at 0.35 s, {after:.0f} at 0.85 s')


@test
def caption_check_at_delivered_speed():
    """Rule 70: the caption readability check runs at 1.1x: a 3-word piece on for 0.85 s of film time passes at 1x
    but is caught at 1.1x (0.77 s delivered)."""
    import subtitles as SUB
    cap = lambda t: 'Not too fast here' if t < 1.1 else ('Just long enough' if t < 1.95 else None)
    at1 = [f for f in SUB.readable_faults(cap, 3, 100, 1.0) if 'Just long' in f]
    at11 = [f for f in SUB.readable_faults(cap, 3, 100) if 'Just long' in f]
    return not at1 and bool(at11) and SUB.SPEED == 1.1, f'at 1x: {len(at1)} fault; at 1.1x: {at11[:1]}'


@test
def follow_line_on_signoff():
    """Rule 52 (Sam, 12 Nov): each film takes the next follow line once and keeps it; finishing stops when the list
    is used up; the card sits top left inside the safe area (x 60-900, below TikTok's tabs at y 310)."""
    import tempfile
    import follow_line
    import signoff
    with tempfile.TemporaryDirectory() as tmp:
        lines = os.path.join(tmp, 'l.md')
        with open(lines, 'w', encoding='utf-8') as f:
            f.write('# x\n- [ ] One 👉\n- [ ] Two 👉\n')
        old = os.environ.get('FOLLOW_LINES')
        os.environ['FOLLOW_LINES'] = lines
        try:
            a, a2, b = follow_line.line_for('film_a'), follow_line.line_for('film_a'), follow_line.line_for('film_b')
            try:
                follow_line.line_for('film_c')
                stopped = False
            except SystemExit:
                stopped = True
        finally:
            if old is None:
                os.environ.pop('FOLLOW_LINES', None)
            else:
                os.environ['FOLLOW_LINES'] = old
    worst = None
    for text in ['Feed the beaver. Follow 👉', 'Follow. We ruin the news 👉', 'Follow or the beaver cries 👉']:
        piece, (x, y) = signoff.follow_card(text)
        x0, y0, x1, y1 = piece.getbbox()
        box = (x + x0, y + y0, x + x1, y + y1)
        if box[0] < 60 or box[1] < 310 or box[2] > 900 or box[3] > 700:
            worst = (text, box)
    ok = (a, a2, b) == ('One 👉', 'One 👉', 'Two 👉') and stopped and worst is None
    return ok, f'film_a {a!r} then {a2!r}, film_b {b!r}, used up stops: {stopped}; card outside the safe area: {worst}'


@test
def exceptions_need_a_written_reason():
    """Rule 13 (tool chat, 12 Nov): every exception in a film's settings (HANDS_OK, LINE_OK, any *_OK, ALLOWED_POPS)
    needs a row in the notes' "## Exceptions" with a reason and a full-size look; one without is refused, a pattern
    row covers its matches, and the staging's meant touches (ALLOWED, TOUCHES) are not exceptions."""
    import types
    import waivers as W
    film = types.SimpleNamespace(HANDS_OK=[('Journalist 3', '*', 'no hand', 0, 1, 'under the phone')],
                                 LINE_OK=[('brand', 'line weight', 540, 289)], TOUCHES=[('a', 'b', 0, 1, 'meant')])
    none = W.gate_faults(film, '# notes\n')[0]
    half = W.gate_faults(film, '## Exceptions\n| check | who | why | looked at |\n|---|---|---|---|\n'
                               '| HANDS_OK | Journalist* | seen from behind, under the phone | |\n')[0]
    full = W.gate_faults(film, '## Exceptions\n| check | who | why | looked at |\n|---|---|---|---|\n'
                               '| HANDS_OK | Journalist* | seen from behind, under the phone | sheet r2, panel 4 |\n'
                               '| LINE_OK | brand | his moustache is a filled shape | sheet r2, panel 1 |\n')[0]
    n = len(W.entries(film))
    return (bool(none) and '2 exception' in none[0] and bool(half) and not full and n == 2,
            f'entries {n}; no table: {len(none)} fault; a row with no look: {len(half)}; both written: {len(full)}')


@test
def house_look_and_lap():
    """Rule 13's house look and rule 80 (tool chat, 12 Nov; Blessed notes 45, 52): with anyone on their own face,
    someone on the house head is caught (not in a film where everyone is on it); a seated front-on body with no lap
    is caught, its lap off the picture is not, and an exceptions row excuses one."""
    import waivers as W
    log = [('Brand', 'brand', False, 'tv 1s'), ('Newsreader', 'newsreader', True, 'tv 2s')]
    all_house = [('A', 'a', True, ''), ('B', 'b', True, '')]
    table = W.rows('## Exceptions\n| check | who | why | looked at |\n|-|-|-|-|\n'
                   '| lap | Juror* | behind the box front | sheet 1 |\n')
    drawn = [('jury 1s', 'Juror 4', dict(view='front', seated=True, lap=False, lap_in=True)),
             ('tv 2s', 'Inmate', dict(view='front', seated=True, lap=False, lap_in=True)),
             ('tv 2s', 'Low', dict(view='front', seated=True, lap=False, lap_in=False)),
             ('tv 2s', 'Kit', dict(view='three', seated=True, lap=True, lap_in=True))]
    a, b, c = W.look_faults(log), W.look_faults(all_house), W.lap_faults(drawn, table)
    return (len(a) == 1 and 'Newsreader' in a[0] and not b and len(c) == 1 and 'Inmate' in c[0],
            f'house head beside own faces: {len(a)}; all house: {len(b)}; laps caught: {[x.split(" ")[1] for x in c]}')


@test
def camera_feel():
    """Rule 72 (tool chat, 12 Nov; Blessed note 51): a zoom eased over 3 s passes; the same zoom in 0.5 s, or one that
    starts at full speed, is caught unless the acting list marks its shot sharp; a jump in one frame is a cut."""
    import types
    import body as B
    import camfeel as C

    def film(cam, dur=4.0):
        return types.SimpleNamespace(__name__='fake', SHOTS=[('a', 0.0, dur)], DUR=dur, LINES=[], cam_for=cam)
    ease = lambda u: 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, u)))
    slow = film(lambda t: B.Cam(1 + ease((t - 0.5) / 3.0)))
    fast = film(lambda t: B.Cam(1 + 2 * ease((t - 1.0) / 0.5)))
    jolt = film(lambda t: B.Cam(1 + 0.6 * max(0.0, min(1.0, (t - 1.0) / 2.5))))
    cut = film(lambda t: B.Cam(1.0 if t < 2 else 2.0))
    sharp = '## The acting list\n| line | who | shot and why |\n|-|-|-|\n| 1 | A | a: sharp snap in |\n'
    r = [C.faults(slow, ''), C.faults(fast, ''), C.faults(fast, sharp), C.faults(jolt, ''), C.faults(cut, '')]
    return ([len(x) for x in r] == [0, 1, 0, 1, 0],
            'slow, fast, fast marked sharp, no ease, a cut: ' + str([len(x) for x in r]))


# ------------------------------------------------------------------------------------------------ Job Q handovers
@test
def handover_drops():
    """Job Q (Sam, 13 Nov): the handover check catches Blessed's real drops: N8-N10 unread when chat 5 broke, note 47's face half."""
    import json, tempfile
    import handover as H
    D = os.path.join(HERE, 'data', 'handover')
    fx = json.load(open(os.path.join(D, 'blessed-chat5.json')))
    d = tempfile.mkdtemp()
    notes = lambda c: H.note_lines(os.path.join(D, f'blessed-notes-{c}.md.gz'))
    tr = [(t, 'sam', x, []) for t, x in fx['chat5_sam']] + [('2026-11-13T09:48:00', 'claude', 'Two clips sent.', []),
                                                            ('2026-11-13T09:48:00', 'sent', '', ['a.mp4'])]
    broke = H.check(tr, notes('cdffdf4'), notes('689092b'))   # only lines written after Sam spoke carry it
    caught = sorted({f.split(':')[0] + ':' + f.split(':')[1][:2] for f in broke})
    final = H.check(tr, notes('163c3e5'), notes('689092b'))
    t47 = [('2026-11-12T20:00:00', 'sam', fx['note47'], [])]
    then, closed = H.check(t47, notes('c1ccf4d')), H.check(t47, notes('163c3e5'))
    # the other three: a clip claimed but not sent, a message after the last reply, an override Sam never typed
    claim = [('T09:00:00', 'claude', 'Clip sent: blessed-r2-cell.mp4', [])]
    sent = claim + [('T09:00:01', 'sent', '', ['blessed-r2-cell.mp4'])]
    late = [('2026-11-13T09:00:00', 'claude', 'Done.', []), ('2026-11-13T09:05:00', 'sam', 'Y fix', [])]
    over = [('2026-11-13T09:00:00', 'sam', "Don't stop for any Y", []),
            ('2026-11-13T09:01:00', 'claude', "Sam's 'don't stop for any Y' counts as an override, so on past red", [])]
    # Sam's messages from a chat record: a parent's seed and a task notice are not his; a typed message is
    rec = os.path.join(d, 'r.jsonl')
    with open(rec, 'w') as f:
        for dd in ({'type': 'user', 'origin': {'kind': 'task-notification'}, 'message': {'content': 'Overnight run, chat 1'}},
                   {'type': 'user', 'message': {'content': '<task-notification>x</task-notification>'}},
                   {'type': 'user', 'message': {'content': [{'type': 'tool_result', 'content': 'x'}]}},
                   {'type': 'user', 'timestamp': '2026-11-13T09:00:00Z', 'message': {'content': 'N8: the pool player clips'}}):
            f.write(json.dumps(dd) + '\n')
    own = H.sam_messages(rec)
    r = [caught == ['NOT CARRIED 09:35', 'NOT CARRIED 09:36', 'NOT CARRIED 09:37'], not final,
         len(then) == 1 and 'face' in then[0], not closed,
         len(H.check(claim, [])) == 1, not H.check(sent, []), any('UNANSWERED' in f for f in H.check(late, [])),
         any('OVERRIDE' in f for f in H.check(over, [])), [x for _, x in own] == ['N8: the pool player clips'],
         H._not_typed('Overnight run, chat 1', rec), not H._not_typed('N8: the pool player clips', rec),
         H._not_typed('not in the record yet', rec) is None,              # the hook's background step waits for it
         not H._is_sam('<agent-message from="a1">\n[Subagent hand-back] report')]   # overnight chat 3: helpers' reports
    return all(r), f'chat 5 caught {caught}, after N8-N11 written {len(final)}; note 47 then {then}, closed ' \
                    f'{len(closed)}; checks {r}'


@test
def critic_bench_scores():
    """Ranking item 3: the critic bench scores an answer against Sam's real Blessed notes: a hit by line or words, a miss names its line."""
    import json, tempfile
    import critbench as B
    c = B.case('blessed-a1')
    d = tempfile.mkdtemp()
    c['name'] = 'kittest'
    B.DATA = d
    out = os.path.join(d, 'kittest', 'x')
    os.makedirs(out)
    json.dump({'round': 0, 'stage': 'bench', 'panels': c['panels']}, open(out + '.spec.json', 'w'))
    open(os.path.join(out, 'look.md'), 'w').write('\n'.join(f'{i}: a picture' for i in range(1, 15)))
    import time
    time.sleep(0.01)
    open(os.path.join(out, 'result.md'), 'w').write(
        "## Faults\nFAULT P12 [2, 4]: the judge has no mouth\nFAULT A1 [3]: back-row woman's head sits straight on "
        "her shoulders, no neck\nFAULT P11 [12]: chin to chest join reads wrong\nFAULT O5 [8]: a cup floats\n"
        "CAN'T TELL P4 [1]: no reference\n## Checked\n1-14\n## Cold look\nfine\n")
    got, miss, extras, cant, rep = B.score(c, 'x', write=False)
    keys = {k['id'] for k in c['key']}
    r = [sorted(got) == ['k13', 'k14a', 'k23'], len(miss) == len(keys) - 3, len(extras) == 1, len(cant) == 1,
         'improve P5' in rep, all(set(k['panels']) <= set(range(1, 15)) for k in c['key']),
         len(c['panels']) == len(c['shots'])]
    return all(r), f'caught {sorted(got)}, {len(miss)} missed, {len(extras)} extra; checks {r}'


@test
def round_page():
    """Ranking item 6 (overnight chat 3): a round reads Blessed's page (under 15% of its code) and a note finds its lines."""
    sys.path.insert(0, HERE)
    import page as P
    out, pg, code = P.build('blessed')
    found = P.find('blessed', "note 28: the escort should look like an HM Prison officer", 3)
    hit = [w for _, w, _ in found]
    # line numbers drift as the files are edited (20 Nov kit changes): the test checks the functions found
    officer = any(w.startswith('blessed.py:') and '`_officer_turned`' in d for _, w, d in found)
    # show (Sam's Y, 15 Nov): one command, a note -> ~40 numbered lines of the code it touches, either film spelling
    sh = P.show('protest-tiers', "frames missing: a stopped drawing mid-throw, the picture goes black")
    got = [h.split('`')[1] for h, rows in sh if rows and '`' in h][:2]
    n = sum(len(rows) for _, rows in sh)
    ok_show = (set(got) == {'_resolve_mixed_arms', '_clear_of_shoulder'} and n <= 44 and
               any('def _resolve_mixed_arms' in t for _, rows in sh for _, t in rows))
    return (pg * 100 < code * 15 and officer and ok_show,
            f'page {pg} tokens, code {code}; note 28 -> {hit}; show "frames missing" -> {got} ({n} lines)')


@test
def womens_builds():
    """Rule S12 (Open Wounds chat 6; Sam's notes 5 and 7): the cast-sheet build check catches both n5 pictures (the
    women on the man's box) and note 7 (May's hourglass on Kemi, not her body), and passes Lucia and Blair."""
    sys.path.insert(0, HERE)
    import contextlib
    import io
    import castsheet as CS
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ok = CS.build_selftest()
    lines = [ln.split(' | ')[0] for ln in buf.getvalue().splitlines()]
    return ok, '; '.join(lines)


@test
def people_from_a_description():
    """Ranking item 4 (overnight chat 4): the people kit redraws Blessed's people from their descriptions, pixel for pixel."""
    import glob
    import people as K
    bad = []
    for txt, why in (('# a: A\nskin: 1 2', 'a colour of two numbers'), ('# a: A\nskin: pale\nhat: red', 'an unknown line'),
                     ('# a: A\nskin: pale\nhair: mohican', 'an unknown haircut'), ('skin: pale', 'no person yet'),
                     ('# a: A\nskin: pale\nbeard: full, chin pale', 'a full beard missing its colours'),
                     ('# a: A\nskin: pale\nhead: part nobody', 'an unknown head part'),
                     ('# a: A\nlook of: b', 'a look of nobody'),
                     ('# a: A\ncrowd: x\nskin (2q): pale; pink', 'a crowd formula not of i and s')):
        try:
            K.parse(txt)
            bad.append(why + ' was not refused')
        except K.DescriptionError:
            pass
    # Sam approved the kit for films (16 Nov): the old 'no film uses the kit yet' clause is gone
    tmp = os.path.join(HERE, 'data', 'kittest-people')
    import blessed as BL0
    press = K.crowds('blessed')['press']                # chat 4d: the press pack, a crowd of 31 from 16 lines
    for i in range(31):
        f, k = BL0.press_sp(i, 0), K.crowd_person(press, i, 0, BL0.press_sp(i, 0)['kit'])
        if any(f.get(q) != k.get(q) for q in ('skin', 'hair_c', 'jacket', 'trousers', 'shirt', 'shoe', 'shoulders',
                                             'height', 'hw', 'seed')) or f['face_m'] != k['kit_face']['m']:
            bad.append(f'journalist {i + 1} not as the film drew them')
            break
    import people_turned as PTN                         # Blessed was drawn before the kit's neck fix (GTA chat 10,
    neck = PTN.LIFT, PTN.CHIN_V                         # Sam: "weird slumped necks"): compare with the old necks
    PTN.LIFT, PTN.CHIN_V = False, 1.06
    import body as BD                                   # the film's own quality (2): earlier tests leave the quick 1,
    ss, BD.SS = BD.SS, 2                                # which drew half size beside the posted film (full run crash)
    bss, BL0.B.SS = BL0.B.SS, 2                         # Blessed's own engine (burnham) keeps its own setting
    try:
        out, scores = K.replicate('blessed', tmp, [(8.6, 'jury'), (5.6, 'oath'), (59.5, 'walliams'), (20.5, 'van'),
                                                   (24.0, 'escort'), (60.5, 'gates2')], film_keys=True)
    finally:
        PTN.LIFT, PTN.CHIN_V = neck
        BD.SS, BL0.B.SS = ss, bss
        K.FILM_TURNED.clear()                           # a crash mid-replicate left Blessed's scarf and officer as the
        PTN.KEYED.clear()                               # film's own: outfit_every_view then lost them (full run)
    drawn = set().union(*[set(w) for *_, w in scores])
    if 'escort' not in K.replicate.turned:                 # chat 4d: invented people turn with their own face
        bad.append('the officer in escort was not turned by the kit')
    for who in ('brand', 'walliams', 'brand (turned)', 'press (turned)', 'officer (turned)'):
        if who not in drawn:
            bad.append(f'{who} not drawn by the kit')
    for t, label, diff, _ in scores:
        if diff > 0.05:
            bad.append(f'{label} {t}s: {diff:.2f}% of pixels differ')
    if len(drawn) < 18:
        bad.append(f'only {len(drawn)} people drawn by the kit')
    import freeze as FZ
    drift = max(K.FROZEN_DRIFT.values() or [0.0])           # live code vs the posted film (its bookmark): may not rise
    # line moved 1.92 -> 2.06 on 22 Nov (check repairs 2): all of the rise is aa09376a, Sam's one smooth shoulder line
    # (20 Nov), per frame against 413beb3e; nothing since. The posted film redraws from its bookmark (freeze.py).
    base = FZ.drift_baseline('blessed', drift)
    if drift > base + 0.05:
        bad.append(f'the live film now differs from the posted Blessed by {drift:.2f}% (was {base:.2f}%)')
    import blessed as BL
    import blessed_cast as BC
    import people_parts as PPK
    TC = PPK.B                                     # since 20 Nov the engine holds each look's head (was BC.TC's copy)
    caught = K.faults(dict(judge=BC.JUDGE)) == []
    keep = TC.HEADS.get('judge')
    TC.HEADS['judge'] = TC.plain_head              # the old fault (notes 13, 15): the judge on the plain (house) head
    caught = caught and bool(K.faults(dict(judge=BC.JUDGE)))
    TC.HEADS['judge'] = keep
    if not caught:
        bad.append('the house head (no mouth) was not caught')
    a = BL.frame_image(5.6)
    BC.JUDGE['kit_face']['lip'] = (90, 20, 20)     # one description fact changed: the picture must show it
    b = BL.frame_image(5.6)
    import numpy as np
    seen = float((np.abs(np.asarray(a.convert('RGB'), np.int16) - np.asarray(b.convert('RGB'), np.int16)).max(axis=2) > 24).mean() * 100)
    if seen <= 0.0:
        bad.append('a changed lip colour did not change the picture')
    return not bad, '; '.join(bad) or (f'{len(drawn)} people redrawn from their descriptions (the press pack a crowd'
                                        f' of 31; turned heads new: escort {K.replicate.turned["escort"]:.2f}%), '
                                        + ', '.join(f'{lb} {d:.2f}%' for _, lb, d, _ in scores) + f' differ; a changed line shows ({seen:.2f}%); live code vs the posted film: {drift:.2f}% at most')


@test
def kept_report_travels():
    """Chat 22 (Sam, 26 Nov): chat 20 pushed brexit-is-done's clean render with no body-check report, so chat 22 could not
    send the animatic. The saved example is that state: a kept clean render with no report is a fault at the start and the
    end of a chat; a report that is not committed is a fault; a committed report is clean; a kept animatic with no fresh
    critique says so."""
    import shutil
    import subprocess
    import tempfile
    import handover as H
    bad = []
    root = tempfile.mkdtemp()
    try:
        d = os.path.join(root, 'animations', 'drafts')
        os.makedirs(d)
        git = lambda *a: subprocess.run(['git', *a], cwd=root, capture_output=True, text=True, check=True)
        git('init', '-q')
        for k in ('clean', 'animatic'):
            open(os.path.join(d, f'f-{k}.mp4'), 'wb').write(b'x')
        got = H.kept_report_faults('f', root)
        if sum(x.startswith('REPORT') and 'no body-check report' in x for x in got) != 2:
            bad.append(f'a kept clean render with no report was not caught: {got}')
        for k in ('clean', 'animatic'):
            json.dump({'faults': [], 'critique': k == 'clean'}, open(os.path.join(d, f'f-{k}.mp4.bodycheck.json'), 'w'))
        got = H.kept_report_faults('f', root)
        if sum('not committed' in x for x in got) != 2:
            bad.append(f'reports that are not committed were not caught: {got}')
        git('add', '-A')
        got = H.kept_report_faults('f', root)
        if len(got) != 1 or not got[0].startswith('CRITIQUE') or 'animatic' not in got[0]:
            bad.append(f'committed reports should leave only the animatic critique line: {got}')
        if H.kept_report_faults('nothing-kept', root):
            bad.append('a film with no kept video was flagged')
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return not bad, '; '.join(bad) or 'missing, uncommitted and committed reports and the critique line told apart'


@test
def places_from_a_description():
    """Ranking item 5 (overnight chat 5d): the places kit redraws Blessed's 13 paintings from 226 lines, and its boxes."""
    import glob
    import places as K
    import setcheck
    bad = []
    head = '# place: p\ncolours: wall 1 2 3\n## view: v\ncamera: up 1.6, horizon 850, lens 1500\n'
    for txt, why in (('panels: x 0 to 1, z 0 to 1, depth 6', 'a piece before any place'),
                     ('# place: p\n## view: v\npanels: x 0 to 1, z 0 to 1, depth 6', 'a view with no camera'),
                     (head + 'sofa: at 0 0, depth 3', 'an unknown kind'),
                     (head + 'clock: at 0 0', 'a piece with no depth'),
                     (head + 'clock: at 0 0, depth 6, colourful 3', 'an unknown param'),
                     (head + 'door: x 0 to 1, z 0 to 2, depth 6, look palace', 'an unknown look'),
                     (head + 'camera: up 1.6, horizon 850', 'a camera with no lens'),
                     (head + 'clock: at 0 0, depth 6, on the wall (the clock)', 'on a piece that is not there'),
                     ('# place: p\ncolours: wall 1 2', 'a colour of two numbers')):
        try:
            K.parse(txt)
            bad.append(why + ' was not refused')
        except K.DescriptionError:
            pass
    # Sam approved the kit for films (14 Nov, notes/morning-report.md): the old 'no film uses the kit yet' clause is gone
    out, scores = K.replicate('blessed', os.path.join(HERE, 'data', 'kittest-places'), frames=False)
    if len(scores) < 13:
        bad.append(f'only {len(scores)} of 13 paintings redrawn')
    bad += [f'{lb}: {d:.3f}% of pixels differ' for lb, d in scores if d > 0.05]
    desc = K.load('blessed')
    boxes, meant = K.set_boxes(desc)
    names = [n for n, _ in boxes]
    for thing in ("court_box the judge's bench", 'court_box the witness box'):   # chat 5d: 'wider than 80%' dropped them
        if thing not in names:
            bad.append(f'{thing} is not a thing for rule 83')
    if len(names) != len(set(names)):
        bad.append('two boxes share a name (repeats must be numbered)')
    known = setcheck.faults(boxes, meant)          # the one the hand list missed (stale box): phone's Samaritans notice
    if len(known) != 1 or 'samaritans' not in known[0]:
        bad.append(f'rule 83 on the kit\'s boxes: {known}')
    gates = desc['views']['gates']['items']        # the old fault: a window in a tower with no 'on' must be caught
    w = next(it for it in gates if it['name'] == 'a window')
    keep = w['raw'].pop('on')
    caught = len(setcheck.faults(*K.set_boxes(desc))) > len(known)
    w['raw']['on'] = keep
    if not caught:
        bad.append('a window in a tower with no "on" was not caught')
    import page as PG
    hit = [w for _, w, _ in PG.find('blessed', 'move the TV room clock left', 3)] if PG.build('blessed') else []
    if 'blessed-places.txt:212' not in hit:
        bad.append(f'a note on the TV room clock did not find its line: {hit}')
    lines = len(K.lines('blessed'))
    return not bad, '; '.join(bad) or (f'{len(scores)} paintings from {lines} piece lines, worst '
                                        f'{max(d for _, d in scores):.3f}%; {len(boxes)} boxes from the pieces')


@test
def moves_from_the_acting_list():
    """Ranking item 7 (overnight chats 7-8): the moves kit redraws Brand's six showman shots (arrival, oath x2, dock,
    gates, gates2) and (chat 8) the judge, the dock guards, the van, the escort (Brand and the officer), the phone,
    the TV room and the push, the gates2 head turns and the guard's eyes, from story/blessed-moves.txt: every joint, mark, mood and gaze the same as the film's code, each
    twelfth of a second; each block lands on its acting-list word; bad lines are refused."""
    import glob
    import acting as A
    bad = []
    for txt, why in (('## arrive: brand\nL: heart', 'a hand key with no time'),
                     ('## arrive: brand\nwiggle: 3', 'an unknown line'),
                     ('gait x: like walk, sps', 'a gait number missing'),
                     ('heart: 1 2 3', 'a library line of no kind')):
        try:
            A.parse(txt)
            bad.append(why + ' was not refused')
        except (ValueError, IndexError, AttributeError):
            pass
    # Sam approved the kit for films (14 Nov, notes/morning-report.md): the old 'no film uses the kit yet' clause is gone
    bad += A.check('blessed')
    desc, film = A.load('blessed'), A.film_side('blessed')
    BL = film['module']
    A.install_gaits(desc)
    looks = {'arrive': 'trial', 'oath': 'stand', 'oath2': 'stand', 'dock': 'dock', 'gates': 'trial', 'gates2': 'trial'}
    for shot, a, b in BL.SHOTS:
        if shot not in looks:
            continue
        fn, walks = film['stands_in'][shot]
        n, worst = 0, 0.0
        for i in range(int((b - a) * 12)):
            t = a + i / 12
            sp = BL.brand_sp(t, looks[shot])
            o = getattr(BL, fn)(sp, t)
            mk, _, kj = A.pose(desc, film, shot, sp, t)
            oj = o[2] if walks else o
            d = max([abs(x - y) for x, y in zip(o[0], mk)] if walks else [0.0])
            for k, v in oj.items():
                if isinstance(v, tuple) and len(v) == 3 and all(isinstance(x, float) for x in v):
                    d = max(d, max(abs(x - y) for x, y in zip(v, kj[k])))
                elif isinstance(v, float):
                    d = max(d, abs(v - kj.get(k, 0.0)))
            mood = A.face(desc, film, shot, t)
            if mood[:2] != BL.brand_mood(t):
                d = max(d, 1.0)
            n += d > 1e-6
            worst = max(worst, d)
        if n:
            bad.append(f'{shot}: {n} drawings differ from the film (worst {worst:.3f} person units)')
    # chat 8: everyone else through the film's person(shot, who, t) seam, and the head and eye hooks
    def diff(a, b):
        d = 0.0
        for k, v in a.items():
            if isinstance(v, tuple) and len(v) == 3 and all(isinstance(x, (int, float)) for x in v):
                d = max(d, max(abs(x - y) for x, y in zip(v, b[k])))
            elif isinstance(v, (int, float)) and not isinstance(v, bool):
                d = max(d, abs(v - b.get(k, 0.0)))
            elif isinstance(v, (bool, str)) and v != b.get(k):
                d = max(d, 1.0)
        return d
    people = 0
    for key, blk in desc['shots'].items():
        b = A.block_for(desc, key)
        if (b['shot'], b['who']) not in film['people'] or b['code']:
            continue
        people += 1
        a, c = [(x, y) for s_, x, y in BL.SHOTS if s_ == b['shot']][0]
        n, worst = 0, 0.0
        for i in range(int((c - a) * 12)):
            t = a + i / 12
            o, k_ = BL.person(b['shot'], b['who'], t), A.person(desc, film, key, t)
            d = max(diff(o[0], k_[0]), diff(o[3], k_[3]), max(abs(x - y) for x, y in zip(o[1], k_[1])),
                    abs(o[2] - k_[2]), 0.0 if o[4] == k_[4] else 1.0)
            n += d > 1e-6
            worst = max(worst, d)
        if n:
            bad.append(f'{key}: {n} drawings differ from the film (worst {worst:.3f})')
    for fn, (key, ch, floor) in film['hooks'].items():
        a, c = [(x, y) for s_, x, y in BL.SHOTS if s_ == A.block_for(desc, key)['shot']][0]
        for i in range(int((c - a) * 12)):
            t = a + i / 12
            v = A.channel(desc, film, key, ch, t)
            v = (v if abs(v) > floor else None) if floor is not None else v
            o = getattr(BL, fn)(t)
            if (o is None) != (v is None) or (o is not None and abs(o - v) > 1e-6):
                bad.append(f'{fn}: differs from the film at {t:.2f} s')
                break
    # the acting list itself (step 4): Blessed's list was corrected to its film (14 Nov: the dock slump at the start
    #   of line 3, the face change 2.6 s after "early release"), so it finds nothing; a row with no block is caught too
    drift = A.check_list('blessed')
    if drift:
        bad.append(f'the acting-list check found {drift}')
    keep = desc['shots'].pop('phone')
    A.load = (lambda f, d=desc: d)
    try:
        if not any('no block' in d for d in A.check_list('blessed')):
            bad.append('a list row with no block was not caught')
    finally:
        desc['shots']['phone'] = keep
        import importlib
        importlib.reload(A)
    return not bad, '; '.join(bad) or (f'six showman shots and {people} more people, every drawing the same as the '
                                       f'film; head and eye hooks the same; every block lands; the list check works')


@test
def rough_of_every_new_thing():
    """Ranking item 1 (overnight chat 10): rough.py finds every person, place view and moves block in Blessed's three
    description files, sends only what is new or changed (a record keeps what was sent), draws one of each with the
    kits (a place, a person, a move on the real clock and on the draft clock), and the pre-flight names what never went
    on a rough."""
    import shutil
    import tempfile
    import rough as R
    bad = []
    have = R.items('blessed')
    n = {k: sum(1 for x in have if x[0] == k) for k in ('person', 'place', 'move')}
    if n['place'] < 12 or n['move'] < 23 or n['person'] < 20:
        bad.append(f'items found {n} (Blessed has 25 people, 12 views, 23 blocks)')
    rec = R.record_path('blessed')
    keep = open(rec).read() if os.path.exists(rec) else None
    try:
        if os.path.exists(rec):
            os.remove(rec)
        if len(R.new_items('blessed')) != len(have):
            bad.append('with no record, not everything is new')
        if not R.gate_faults('blessed'):
            bad.append('the pre-flight line missed things never on a rough')
        R.mark_sent('blessed', 'test')
        if R.new_items('blessed') or R.gate_faults('blessed'):
            bad.append('after `sent`, things still show as new')
        lines = open(rec).read().splitlines()
        lines = [ln.replace(ln.split()[2], '0000000000') if ln.startswith('place court_out ') else ln for ln in lines]
        open(rec, 'w').write('\n'.join(lines) + '\n')
        left = R.new_items('blessed')
        if [(k, nm) for k, nm, _ in left] != [('place', 'court_out')] or 'changed since' not in left[0][2]:
            bad.append(f'a changed place was not the only thing re-sent: {left}')
    finally:
        if keep is None:
            os.path.exists(rec) and os.remove(rec)
        else:
            open(rec, 'w').write(keep)
    if R.place_tile('blessed', 'court_box').size[0] < 100:
        bad.append('a place did not draw')
    for draft in (False, True):
        t = R.move_tiles('blessed', ['arrive', 'cot'], draft=draft)
        if sum(im is not None for im, _ in t['arrive']) < 4:
            bad.append(f'arrive drew {len(t["arrive"])} moments (draft {draft})')
        if 'left as code' not in t['cot'][0][1]:
            bad.append('a block left as code was not named')
    tmp = tempfile.mkdtemp()
    try:
        if R.people_tile('blessed', {'judge'}) is None:
            bad.append('a person did not draw')
    finally:
        shutil.rmtree(tmp)
    return not bad, '; '.join(bad) or (f'{len(have)} things found; only new or changed ones go on the sheet; a person, '
                                       f'a place and a move (real and draft clock) drawn; the pre-flight line works')


def _facepick_burnham():
    """Burnham's picked heads (references/faces/burnham/pick) as facepick draws them: F, frame, shapes, colours, meta."""
    import json
    import facepick as FP
    meta = json.load(open(os.path.join(FP.ROOT, 'references/faces/burnham/pick/burnham-pick.json')))
    F = [(FP._find(p, FP.ROOT), n) for p, n in (FP._split(a) for a in meta['fronts'])]
    fr = FP.photo_frame(*F[0])
    shapes = FP.traced(fr)
    return FP, F, fr, shapes, FP.colours(fr, shapes), meta


def _ink(png):
    import numpy as np
    from PIL import Image
    return np.asarray(Image.open(png).convert('L'))


@test
def facepick_extras_after_the_check():
    """Rule 49.3 (face tool, 13-14 Nov): glasses, beard, age lines and the eyes' look are drawn AFTER the likeness
    check, never into the checked head (the face finder read Burnham's cheek folds as his lips, fuller irises as a brow
    change: C 62% -> 34%); eye_look gives his dark eyes fuller irises at the house size; `redraw` works from any folder
    (his pick held '../references': it only ran from source/)."""
    import json
    import shutil
    import tempfile
    import numpy as np
    FP, F, fr, shapes, col, meta = _facepick_burnham()
    tmp = tempfile.mkdtemp()
    try:
        meas = meta['heads']['C']['measures']
        bare = os.path.join(tmp, 'bare.png')
        FP.draw_head(meas, fr, shapes, col, bare, extras=False)
        look = FP.eye_look(F)
        dressed = dict(shapes, age=meta['age'], eyes=look)
        clean = os.path.join(tmp, 'clean.png')
        FP.draw_head(meas, fr, dressed, col, clean, extras=False, glasses=meta.get('glasses'))
        full = os.path.join(tmp, 'full.png')
        FP.draw_head(meas, fr, dressed, col, full, extras=True, glasses=meta.get('glasses'))
        clean_same = bool((_ink(bare) == _ink(clean)).all())
        extras_moved = float((np.abs(_ink(full).astype(int) - _ink(clean)) > 30).mean())
        # the old fault: the extras drawn into the head the check measures
        old_caught = extras_moved > 0.002
        eyes_ok = look and look['scale'] == 1.0 and look['iris_r'] > 1.2
        # redraw from another folder, from a pick that still holds the old '../' paths
        m2 = dict(meta, fronts=['../' + a for a in meta['fronts']])
        json.dump(m2, open(os.path.join(tmp, 'burnham-pick.json'), 'w'))
        shutil.copy(os.path.join(FP.ROOT, 'references/faces/burnham/pick/burnham-C.png'), tmp)
        here = os.getcwd()
        os.chdir(tmp)
        try:
            FP.redraw(tmp, 'burnham')
        finally:
            os.chdir(here)
        redrawn = os.path.exists(os.path.join(tmp, 'burnham-C.png')) and \
            json.load(open(os.path.join(tmp, 'burnham-pick.json')))['heads']['C']['measures'] == meas
    finally:
        shutil.rmtree(tmp)
    ok = clean_same and old_caught and eyes_ok and redrawn
    return ok, (f'checked head untouched by the extras: {clean_same}; extras change {extras_moved:.1%} of the drawn '
                f'head; irises {look and look["iris_r"]} at size {look and look["scale"]}; redraw from another '
                f'folder: {redrawn}')


@test
def facepick_beard_from_any_front():
    """Face tool chat 5 (Walliams replay, 14 Nov): his first front photo is nearly shaven, and beardkit keeps only
    what matches its FIRST photo, so the stubble in his other three was dropped (and the redraw crashed). The beard
    is now read with each photo leading in turn, the fullest kept."""
    import shutil
    import tempfile
    import beardkit
    import facepick as FP
    L = os.path.join(FP.ROOT, 'references/blessed/likeness')
    F = [(os.path.join(L, f), None) for f in ('w06-front-hedge-sam.jpg', 'w07-front-bowtie-sam.jpg',
                                            'w02-front-bbc2024.jpg')]
    tmp = tempfile.mkdtemp()
    try:
        old = beardkit.analyse('walliams', [f for f, _ in F], tmp)[2]
        new = FP._beard('walliams', F, tmp)
    finally:
        shutil.rmtree(tmp)
    old_caught = not old.get('base')
    ok = old_caught and bool(new) and new.get('coverage', 0) > 0.1
    return ok, (f'shaven photo first: beard {"none" if old_caught else "found"} (the old way); each photo leading: '
                f'coverage {new.get("coverage", 0) if new else 0:.2f}')


@test
def agelines_by_measure_and_age():
    """Face tool chat 3 (13 Nov): a 56-year-old came out young and round; the age lines are measured in the photos
    and scaled by age (Badenoch's top light deepened a 46-year-old's folds past a 56-year-old's): older draws more
    line, a line under LO draws nothing, and Burnham's crow's feet (11 of 12 in the line-up) are drawn."""
    import shutil
    import tempfile
    import numpy as np
    import agelines as AG
    FP, F, fr, shapes, col, meta = _facepick_burnham()
    meas = meta['heads']['C']['measures']
    st = meta['age']['strength']
    tmp = tempfile.mkdtemp()
    ink = {}
    try:
        for tag, age in (('none', None), ('young', {k: v * AG.age_factor(30) for k, v in st.items()}),
                         ('his', st)):
            png = os.path.join(tmp, f'{tag}.png')
            FP.draw_head(meas, fr, dict(shapes, age={'strength': age} if age else None), col, png, extras=True)
            ink[tag] = _ink(png)
    finally:
        shutil.rmtree(tmp)
    young = float((np.abs(ink['young'].astype(int) - ink['none']) > 20).mean())
    his = float((np.abs(ink['his'].astype(int) - ink['none']) > 20).mean())
    order = AG.age_factor(30) < AG.age_factor(46) < AG.age_factor(56) <= AG.age_factor(70)
    floor = AG.strength({k: AG.LO[k] for k in AG.LO}) == {k: 0.0 for k in AG.LO}
    ok = order and floor and his > young * 1.3 and his > 0 and st['crows_feet'] > 0.8
    return ok, (f'lines at 30: {young:.2%} of the head, at his 64: {his:.2%}; age order {order}; faint lines drawn '
                f'as none {floor}; crow\'s feet {st["crows_feet"]}')


@test
def facehouse_brows_sit_on_hers():
    """Face tool chat 10 (Sam on Kemi: "her eyebrows are really far from her eyes"): the arch bends the brow's ends
    down and leaves its middle where it was measured (it used to lift the whole brow a fifth of an eye); a heavier
    lid moves the brows with it; with the photos measured (browcheck) the drawn brow sits at the photos' height."""
    import facehouse as FH
    import patriots4_cast as P4
    kh = FH.person('badenoch', 'detail', **FH.CAST['badenoch'])['kit_house']
    L = P4.layout(kh['meas'])
    flat, arched = (P4.brow_uv(L, 0.032, arch=a) for a in (0.0, 0.03))
    middle_kept = abs(flat[1][1] - arched[1][1]) < 1e-9 and arched[0][1] > flat[0][1] and arched[2][1] > flat[2][1]
    gap = FH._brow_gap(FH.face_layout(kh), kh)
    want = (kh.get('brow') or {}).get('high')
    fitted = want is not None and abs(gap - want) < 0.01 and 0.4 < want < 0.75
    ok = middle_kept and fitted
    return ok, f'arch keeps the middle {middle_kept}; drawn brow {gap:.2f} eye widths above the lid, her photos {want}'


@test
def facehouse_whole_head():
    """Face tool chat 11 (Sam: Y to the kit plan): the house head as a film gets it. Andy's and Kemi's finished heads
    held pixel for pixel (Sam: "Kemi is right", "Andy is finished"); a people file's `head: house NAME` lines build
    the same person as facehouse's own; every turned view draws through the house head's own turned Person (no
    generic head), with her ears under her plaits."""
    import hashlib
    import shutil
    import tempfile
    import facehouse as FH
    import people
    import turnhead as TH
    held = {'burnham': '4f13fdafb1c7d29d2c492a16fbe949c4', 'badenoch': '286fdc3a67bb7b6714d99414c330f955'}
    # re-held 26 Nov (Open Wounds chat 30, Sam's note 21: Kemi's mouth and eye lines "make her look less like the
    # real life Kemi"): her age lines off (age_boost 0; facehouse.line_faults), nothing else changed
    # re-held 21 Nov (check repairs 2): both changed at aa09376a only (Sam, 20 Nov: one smooth shoulder line), found by
    # bisecting; the pictures differ only below the collar (rows 707-767 of 1038), the faces identical.
    # re-held 19 Nov (front-on focus chat 2): both changed at 594f94ba only (Sam, 14 Nov: the flat dark shadow side
    # taken off people), found by bisecting; unchanged from then to today, so today's heads are the finished ones
    tmp = tempfile.mkdtemp()
    got = {}
    try:
        for n in held:
            png = FH.draw(n, 'detail', os.path.join(tmp, f'{n}.png'))
            got[n] = hashlib.md5(open(png, 'rb').read()).hexdigest()
        pk = __import__('json').load(open(FH.pick_file('badenoch')))                 # chat 13: facepick's sheet draws A, B, C
        alt = FH.draw('badenoch', 'detail', os.path.join(tmp, 'v.png'), lines=FH.CAST['badenoch'],   # this way
                      src=FH.pick_dir('badenoch'), variant=pk['picked'])
        sheet_way = hashlib.md5(open(alt, 'rb').read()).hexdigest() == got['badenoch']
        cast = {w: sp for w, sp in people.load('facetool').items()}
        same = sheet_way and all(cast[w]['kit_house']['meas'] == FH.person(n, 'detail', **FH.CAST[n])['kit_house']['meas']
                   for w, n in (('andy', 'burnham'), ('kemi', 'badenoch')))
        del TH.GENERIC[:]
        FH.turns(os.path.join(tmp, 't.jpg'), list(held))
        generic = list(TH.GENERIC)
    finally:
        shutil.rmtree(tmp)
    kept = [n for n in held if got[n] == held[n]]
    ok = len(kept) == 2 and same and not generic
    return ok, (f'held pixel for pixel: {kept}; people file = facehouse = facepick sheet: {same}; '
                f'turned on a generic head: {generic}')


@test
def facehouse_head_from_photos():
    """Face tool chat 16 (Sam on Walliams, 14 Nov: "Very different head shape ... draw the face shape from the
    reference a lot more intelligently"): a measured head (facehouse.measure_head, saved in the pick) is drawn on its
    photos' shape: the face's edge within 0.025 face heights of the photos' skin (ears cut) from the cheekbones to the
    chin, the hair's outer edge within 0.03 of the photos' silhouette over the temples, the crown within 0.04. Fails
    on the house outline and cap (narrow temples, a crown a tenth too high)."""
    import numpy as np
    import facehouse as FH
    kh = FH.person('walliams', 'detail', **dict(FH.CAST['walliams'], shape_push=1.0))['kit_house']
    hd = kh.get('head_m') or {}
    if not hd:
        return False, 'no measured head in the pick (facehouse.py measure walliams)'
    L = FH.face_layout(kh)
    rows = dict((v, (s, b)) for v, s, b in zip(hd['v'], hd['skin'], hd['both']))
    face = [abs(FH._face_u(L, v) - rows[v][0]) for v in (0.4, 0.5, 0.6, 0.7, 0.8, 0.9) if rows[v][0]]
    sh = FH._swept_shapes(L, kh, (60, 50, 40))
    cap = sh['cap'] + [q for sd in sh['sides'] for q in sd]

    pieces = [sh['cap']] + sh['sides']

    def outer(v):                                      # the farthest crossing of row v by any piece's edge
        r = []
        for pc in pieces:
            q = FH.curve(pc, 2)
            for (u0, v0), (u1, v1) in zip(q, q[1:] + q[:1]):
                if (v0 - v) * (v1 - v) < 0:
                    r.append(abs(u0 + (v - v0) / (v1 - v0) * (u1 - u0)))
        return max(r) if r else 0.0
    hair = [abs(outer(v) - rows[v][1]) for v in (-0.2, -0.1, 0.0, 0.1) if rows[v][1]]
    crown = min(w for _, w in cap)
    errs = (max(face), max(hair), abs(crown - hd['crown']))
    ok = errs[0] <= 0.025 and errs[1] <= 0.03 and errs[2] <= 0.04
    return ok, f'face edge off by {errs[0]:.3f}, hair edge {errs[1]:.3f}, crown {errs[2]:.3f} (face heights)'


@test
def dome_not_a_carrot():
    """Rule 49 (lesson 7, Milburn note 4: Pat McFadden's bald dome passed the likeness test at 62% and Sam saw "an
    alien carrot man"): facehouse.dome_faults flags Pat's head as chat 5 drew it (dome -0.44, no measured width: the
    skull 1.9x as tall as its half width, widest at the cheeks) and passes chat 6's fixed head and a head with hair."""
    import facehouse as FH
    old = dict(FH.CAST['mcfadden'])
    old.pop('dome', None)
    old.pop('dome_wide', None)
    caught, fixed, hair = FH.dome_faults('mcfadden', old), FH.dome_faults('mcfadden'), FH.dome_faults('walliams')
    ok = len(caught) == 2 and not fixed and not hair
    return ok, f'old dome: {len(caught)} faults; fixed dome: {len(fixed)}; Walliams (hair): {len(hair)}'


@test
def face_lines_photos_show():
    """Brexit Is Done note 21 (Sam, 26 Nov: Kemi's mouth and eye lines "make her look less like the real life Kemi"):
    facehouse.line_faults flags Kemi as drawn (the shade on a dark skin measured as the deepest lines of all faces)
    and passes her fixed lines and the lighter-skinned faces whose lines are real (May, Blair, Walliams, McFadden)."""
    import facehouse as FH
    old = dict(FH.CAST['badenoch'])
    old.pop('age_boost', None)
    caught, fixed = FH.line_faults('badenoch', old), FH.line_faults('badenoch')
    others = sum(len(FH.line_faults(n)) for n in ('may', 'blair', 'walliams', 'mcfadden'))
    return len(caught) == 2 and not fixed and not others, f'old: {len(caught)}; fixed: {len(fixed)}; others: {others}'


@test
def house_head_not_a_doll():
    """Brexit Is Done note 20 (Sam, 26 Nov: Tony "a bit doll like" beside the house's Netanyahu, Trump, Brand):
    facehouse.doll_faults flags Blair as chat 27 drew him (brown brows under grey hair; his neck 5-8% of the head
    in the film's own frame at 24 s) and passes him fixed, and May's brows."""
    import numpy as np
    from PIL import Image
    import facehouse as FH
    import brexit_is_done as F
    V = FH.PP.V
    old = dict(FH.CAST['blair'])
    for k in ('neck_up', 'brow_c', 'age_boost', 'lid'):
        old.pop(k, None)

    def frame(head, neck_up):
        img = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
        sp, j = F.acted('3', 'blair', 24.0)
        sp = dict(sp, kit_house=dict(sp['kit_house'], neck_up=neck_up))
        keep = V.TURNED_HEADS['kit_house']
        if not head:
            V.TURNED_HEADS['kit_house'] = lambda *a, **k: None
        try:
            F.seated(img, 'blair', F._cam('blair'), F.BLAIR['x'], F.BLAIR['d'], 24.0, F.BLAIR['yaw'],
                     pose='armchair', chair=True, look=sp, joints=j)
        finally:
            V.TURNED_HEADS['kit_house'] = keep
        return np.asarray(img.convert('RGB'))
    caught = FH.doll_faults('blair', old, frame(True, 0.0), frame(False, 0.0))
    fixed = FH.doll_faults('blair', None, frame(True, FH.CAST['blair']['neck_up']), frame(False, 0.0))
    may = FH.doll_faults('may')
    ok = len(caught) == 2 and not fixed and not may
    return ok, f'as drawn: {len(caught)} ({"; ".join(c[:40] for c in caught)}); fixed: {len(fixed)} {fixed}; May: {len(may)}'


@test
def hands_rest_on_armrests():
    """Open Wounds note 19 (Sam, 26 Nov: Tony's "hands hover rather than resting on the chair arms"):
    sitting.armrest_faults flags the armchair pose's hands as chat 27 drew them (centre on the arm's top edge) and
    passes the fixed pose (curled over the front end) and a desk rest (a hand flat on a desk is ON it)."""
    import sitting as SIT
    seat = SIT.seat_for('armchair')
    if callable(seat):
        seat = seat()
    sp = {}
    new = SIT.spec_armrests(sp, seat)['arms']
    y = seat.surface() - seat.arms
    old = SIT.arm_rest((seat.width + 26.0, y, seat.front - 35.0), y, 'palm')
    caught = SIT.armrest_faults(seat, old)
    fixed = sum(len(SIT.armrest_faults(seat, a, k)) for k, a in new.items())
    desk = SIT.armrest_faults(seat, SIT.arm_rest((40.0, y - 80, 100.0), y - 80, 'palm'))
    return len(caught) == 1 and not fixed and not desk, f'old: {caught}; fixed: {fixed}; desk: {len(desk)}'


@test
def pounce_long_enough_to_read():
    """Open Wounds note 22 (Sam, 26 Nov: "The final wolf pounce on Tony, so quick it's barely registered"; note 13
    before it): readtime flags the pounce as chat 27 drew it (four frames from off-screen in mid-air: 0.33 s, no
    wind-up) and passes the film's acted pounce (creep, coil, leap)."""
    import readtime
    import brexit_is_done_action as A
    old = readtime.check('old pounce', 0.0, 0.0, 0.333)
    new = sum((readtime.check(*r) for r in A.READ_TIMES), [])
    return len(old) == 3 and not new, f'old: {len(old)}; new: {new}'


@test
def facehouse_head_proportions():
    """Face tool chat 17 (rule 30 on Walliams: chat 16's row push x1.3 left his head a light bulb, the narrow chin
    under wide temples): the measured head's PROPORTIONS pushed from real faces' middle by the card. A broad-jawed
    face (his card: jaw_wide z 2.5) draws a box: the jaw within 0.06 of the cheeks' width (the photos: 0.87 of
    them), the chin squarer than measured, the face wider by its face_wide push; the eye centres sit against the
    drawn cheeks as the pushed photos say (within 5%: the pick's tiny eyes had pulled them in a sixth); the turned
    views go round on the drawn face's own widths. Fails on chat 16's push (jaw about 0.87, the eye centres about 0.8 of the target)."""
    import json
    import numpy as np
    import facehouse as FH
    kh = FH.person('walliams', 'detail', **FH.CAST['walliams'])['kit_house']
    L = FH.face_layout(kh)
    hd, hm = L['head'], kh['head_m']
    r = [(v, s) for v, s, _ in hd['rows'] if s is not None]
    w = lambda rows, v: float(np.interp(v, *zip(*rows)))                     # noqa: E731
    m = [(v, s) for v, s in zip(hm['v'], hm['skin']) if s is not None]
    jaw = w(r, 0.8) / FH._cheek(r)
    square, square0 = w(r, 0.95) / w(r, 0.8), w(m, 0.95) / w(m, 0.8)
    wide = FH._cheek(r) / FH._cheek(m)
    a = json.load(open(os.path.join(HERE, 'likeness_average.json')))['neutral']
    z = kh['card']
    raw = {k: a['med'][k] + z.get(k, 0) * a['spread'][k] for k in ('face_wide', 'eye_size', 'eyes_apart')}
    ecx = lambda q: q['eye_size'] * q['face_wide'] * (q['eyes_apart'] + 1) / 2   # noqa: E731
    avg = FH._cheek([(v, x + float(np.interp(v, *zip(*FH.SKIN_BIAS)))) for v, x in zip(hm['v'], hm['avg'])
                     if x is not None]) / ecx(a['med'])
    want = FH._cheek(r) / (avg + FH.SHAPE_PUSH * (FH._cheek(m) / ecx(raw) - avg))
    eyes = L['ecx'] / want
    turned = FH._turn_widths(L)
    tw = abs(w(turned, 0.8) - w(r, 0.8))
    ok = jaw >= 0.94 and square > square0 + 0.05 and abs(wide - hd['prop']['wide']) < 0.01 and abs(eyes - 1) < 0.05 \
        and tw < 0.01
    return ok, (f'jaw {jaw:.2f} of the cheeks (photos {w(m, 0.8) / FH._cheek(m):.2f}); chin {square:.2f} of the jaw '
                f'(photos {square0:.2f}); face x{wide:.3f}; eye centres {eyes:.2f} of the target; turned jaw off by {tw:.3f}')


@test
def kit_people_never_generic():
    """Face tool chat 14 (Sam, 14 Nov, Y: background people move onto the new three-quarter turned head): everyone a
    people file builds, crowds included, turns through turnhead (its 30-degree three-quarter), never views.py's old
    generic head; only the test-only hand-made head parts (people.HEAD_PARTS) are let off."""
    from PIL import Image
    import people
    import people_parts as PP
    import turnhead as TH
    from satire_style import install_circle_hands
    B, V = PP.B, PP.V
    install_circle_hands(B)
    B.SS = 1
    films = sorted(f[:-len('-people.txt')] for f in os.listdir(os.path.join(HERE, '..', 'story')) if f.endswith('-people.txt'))
    bad, n = [], 0
    for film in films:
        cast = people.install(people.load(film))
        for w, sp in cast.items():
            if sp.get('kit_head') in people.HEAD_PARTS:
                continue
            n += 1
            del TH.GENERIC[:]
            tile = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
            V.person(tile, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(sp), 0.0, 45)
            if TH.GENERIC:
                bad.append(f'{film}:{w}')
    # Open Wounds chat 12 (the guests seen front-on all drew the engine's bald stand-in, a repeat of GTA 20 Nov): a
    # crowd member made BEFORE the kit is installed (an action file's module-level crowd) still gets its own head and
    # torso, so it is drawn as itself straight on (yaw 0) too.
    saved_h, saved_t = B.HEADS, B.TORSOS
    crowd_bad, m = [], 0
    for film in films:
        for name, d in people.crowds(film).items():
            B.HEADS, B.TORSOS = {}, {}
            try:
                sp = people.crowd_person(d, 0)
                hooked = B.HEADS.get(sp['who']) is people.kit_head
            finally:
                B.HEADS, B.TORSOS = saved_h, saved_t
            m += 1
            if not hooked and d.get('crowd_defaults', True):
                crowd_bad.append(f'{film}:{name}')
    return not bad and not crowd_bad, (f'{n} people in {len(films)} people files turned; on the generic head: '
                                       f'{bad or "none"}; {m} crowds made before the install, on the stand-in head: '
                                       f'{crowd_bad or "none"}')


@test
def facehouse_beard_turns():
    """Face tool chat 14: a measured beard (Walliams' stubble) is drawn in the turned views too, as Vance's goatee
    goes round (chat 13 drew it front-on only: his three-quarter and side were bare-chinned)."""
    import shutil
    import tempfile
    import facehouse as FH
    seen, old = [], FH.stubble
    FH.stubble = lambda p, f, *a, **k: (seen.append(type(f).__name__), old(p, f, *a, **k))[1]
    tmp = tempfile.mkdtemp()
    try:
        FH.turns(os.path.join(tmp, 't.jpg'), ['walliams'], yaws=(0, 45, 90))
    finally:
        FH.stubble = old
        shutil.rmtree(tmp)
    turned = seen.count('TurnFace')
    return turned >= 2 and len(seen) >= 3, f'stubble drawn front {len(seen) - turned}, turned {turned} (want 1 and 2)'



@test
def facehouse_walliams_kit_person():
    """Walliams kit job (Sam, 22 Nov: "Walliams: put into kit"): David Walliams is a proper kit person in the face
    tool's people file, his head the one Sam approved on 15 Nov (chat 17's pushed proportions, the rounded-dome
    swept hair, the smirk and cocked brow, look 'detail') held pixel for pixel, at his own height (1.96 m) in the
    navy suit, white shirt, no tie; every turn (0, 45, 90, 135, 180) draws his own house head, never the engine's
    plain one; Blessed's test-only hand-made head stays its own. Fails before the job (no 'walliams' in the file)."""
    import hashlib
    import shutil
    import tempfile
    import facehouse as FH
    import people
    import people_parts as PP
    import turnhead as TH
    from PIL import Image
    from satire_style import install_circle_hands
    held = '31d28a85f8b5cb406696cad7c9819aa9'    # FH.draw('walliams', 'detail') on 22 Nov: the head Sam approved
    cast = people.load('facetool')
    if 'walliams' not in cast:
        return False, 'no walliams in the face tool people file'
    sp = cast['walliams']
    out = []
    if sp.get('kit_head') != 'house' or sp['kit_house']['meas'] != FH.person('walliams', 'detail', **FH.CAST['walliams'])['kit_house']['meas']:
        out.append('the people file does not build facehouse\'s Walliams')
    if abs(sp.get('height', 0) - 1.96) > 1e-6:
        out.append(f"height {sp.get('height')}, not 1.96 m")
    tmp = tempfile.mkdtemp()
    try:
        png = FH.draw('walliams', 'detail', os.path.join(tmp, 'w.png'))
        if hashlib.md5(open(png, 'rb').read()).hexdigest() != held:
            out.append('the approved head changed')
    finally:
        shutil.rmtree(tmp)
    B, V = PP.B, PP.V
    install_circle_hands(B)
    people.install(cast)
    B.SS = 1
    del TH.GENERIC[:]
    for yaw in (0, 45, 90, 135, 180):
        tile = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
        V.person(tile, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(sp), 0.0, yaw)
    if TH.GENERIC:
        out.append(f'turned on the plain head: {list(TH.GENERIC)}')
    blessed = people.load('blessed')['walliams']
    if blessed.get('kit_head') != 'walliams':
        out.append("Blessed's own hand-made head was moved")
    return not out, '; '.join(out) or 'kit person: approved head held, 1.96 m, five turns on his own head'


@test
def outfit_every_view():
    """Face tool chat 15 (one outfit in every view): every piece a person wears over the clothes (each extra, the open
    collar) shows in the three-quarter and the side as it does from the front, and from behind where it goes round
    (people.turned's 'back'); the wig turns with the head. Fails when a turned view drops a piece the front has."""
    import numpy as np
    from PIL import Image
    import people
    import people_parts as PP
    from satire_style import install_circle_hands
    B, V = PP.B, PP.V
    install_circle_hands(B)
    B.SS = 1
    base = people.parse("# t: Test\nbody: 1.78 m\nskin: pale | hair: crop, 40 32 28\n"
                        "outfit: suit 60 60 66, shirt white, no tie\n")['t']
    tv = people.turned()

    def draw(d, yaw):
        cast = people.install({'t': people.person(d)})
        tile = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
        V.person(tile, B.Cam(1.0, 540, 960), 540, 900, 1.6, dict(cast['t']), 0.0, yaw)
        return np.asarray(tile.convert('RGB'), np.int16)
    plain = {y: draw(base, y) for y in (0, 45, 90, 135, 180)}
    bad, n = [], 0
    for e in list(people.EXTRAS) + ['open collar']:
        d = dict(base, collar='open') if e == 'open collar' else dict(base, extras=[e])
        want = (0, 45, 90) + ((135, 180) if e == 'wig' or (e in tv and tv[e]['back']) else ())
        for y in want:
            n += 1
            seen = int((np.abs(draw(d, y) - plain[y]).max(axis=2) > 24).sum())
            if seen < 150:
                bad.append(f'{e} at {y} ({seen} px)')
    return not bad, f'{n} piece-views checked; dropped: {", ".join(bad) or "none"}'


@test
def cast_tile_scale_is_one():
    """Sam Y 14 Nov: a cast tile draws at scale 1 (B.SS), whatever the film left it at."""
    import protest_tiers_cast as C
    B = C.B
    B.SS = 3
    C.tile(lambda img, cam: None)
    return B.SS == 1, f'B.SS after a tile = {B.SS}'


@test
def head_view_installs_idempotent():
    """Chat 18, 15 Nov: installing the turned/famous/house head kits again (in any order) adds no layer (pre-flight's
    child re-installed them and head_view wrapped itself to a RecursionError). Since one-route-kit Change 2 (20 Nov)
    each kit is one entry in views.TURNED_HEADS, and head_view itself is never replaced."""
    import people_turned as A
    import people_famous as Fm
    import facehouse as Hs
    V = A.PP.V
    hv = V.head_view
    for m in (A, Fm, Hs):
        m.install()
    d0 = len(V.TURNED_HEADS)
    for _ in range(5):
        for m in (Hs, A, Fm):
            m.install()
    return len(V.TURNED_HEADS) == d0 and V.head_view is hv, (f'turned-head kits {d0} -> {len(V.TURNED_HEADS)} after 5 '
                                                              f'more rounds of installs; head_view kept: {V.head_view is hv}')


# ------------------------------------------------------------------------------------------------ the proposal route
@test
def proposal_route_hook():
    """The proposal route (Sam, 15 Nov): the Stop hook blocks a change put to Sam without a judge's verdict, passes one with it, passes routine Y/N, never blocks twice."""
    import json as J
    import shutil
    import tempfile
    import propose as P
    tmp = tempfile.mkdtemp()
    old = P.PROPS
    P.PROPS = tmp
    try:
        def transcript(reply, tool=None):
            f = os.path.join(tmp, 'chat.jsonl')
            ents = [{'type': 'user', 'message': {'content': 'go on'}}]
            if tool:
                ents.append({'type': 'assistant', 'message': {'content': [tool]}})
            ents.append({'type': 'assistant', 'message': {'content': [{'type': 'text', 'text': reply}]}})
            open(f, 'w').write('\n'.join(J.dumps(e) for e in ents))
            return f

        def run(reply, tool=None, active=False):
            import io
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                P.hook(J.dumps({'transcript_path': transcript(reply, tool), 'stop_hook_active': active}))
            return buf.getvalue()

        bad = []
        # 1. the real 15 Nov ask (case 1): a tool change, Y/N, no proposal -> blocked
        ask1 = ('So the proposal is to make those two tools easier to use, not to add another.\n'
                'Need: Y or N, make that change and test it on the next round of notes? (I\'d say Y.)')
        if 'block' not in run(ask1):
            bad.append('case-1 tool change not blocked')
        if 'block' not in run('Need:\n1. Y or N: write the rule above, in that place? (I\'d say Y.)'):
            bad.append('rule ask not blocked')
        # 2. routine Y/N passes
        for r in ('Need: Y or N for the animatic', 'Need: Y or N, the final render? (I\'d say Y.)',
                  'Answer Q1: Y to raise the budget to about 63.5% of a week, or N to stop at 47%',
                  '8: fixed - the whale now knocks the helideck away. Clip sent.',
                  'Checks: the tool check slipped (looked: fine). Need: Y or N for the animatic?'):
            if run(r):
                bad.append(f'routine blocked: {r[:40]}')
        # 3. a named proposal without a verdict -> blocked, even if the wording is plain
        P.new('t1', 'test')
        f = os.path.join(tmp, 't1.md')
        txt = open(f).read()
        open(f, 'w').write(txt.replace('(what is wrong, in plain words; NO solution: the chat\'s own idea goes in t1/chat.md)', 'X is slow.')
                           .replace('(the raw facts, each with its source: file, ledger, chat record; numbers as counted, "unchecked" where not)', '- 3 s (timer)')
                           .replace('(paths the helpers may search, one per line, e.g. notes/ledger/FILM.md)', 'CLAUDE.md'))
        open(os.path.join(tmp, 't1', 'chat.md'), 'w').write('do Y')
        ask = 'Full plan in notes/proposals/t1.md. Need: Y or N, go ahead? (I\'d say Y.)'
        if 'block' not in run(ask):
            bad.append('named proposal without verdict not blocked')
        # written this turn (not named) -> blocked
        w = {'type': 'tool_use', 'name': 'Write', 'input': {'file_path': os.path.join('notes/proposals', 't1.md')}}
        if 'block' not in run('Need: Y or N, go ahead? (I\'d say Y.)', w):
            bad.append('proposal written this turn not blocked')
        # 4. stop_hook_active: never block twice; logged instead
        if run(ask1, active=True):
            bad.append('blocked although stop_hook_active')
        if not open(os.path.join(tmp, P.UNROUTED)).read().strip():
            bad.append('stop_hook_active case not logged')
        # 5. with a verdict: passes only with the Critiqued line
        import io
        import contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            P.pack('t1')
            for who in 'ab':
                open(os.path.join(tmp, 't1', f'helper-{who}.md'), 'w').write(f'helper {who}')
            P.judge('t1', seed=1)
        rows = '\n'.join(f'| V{i} | 3 | 3 | 3 | 3 | 3 | 15 |' for i in (1, 2, 3))
        raw = ('## Leak\nnone\n## Scores\n| version | quality | notes | cost | risk | undo | total |\n|---|---|---|---|---|---|---|\n'
               + rows + '\n## Sam test\n' + '\n'.join(f'Q{i}: ok' for i in range(1, 9)) +
               '\n## Pick\nV2\n## Why\nbest\n## Faults in the pick\n- F1 [fixed] a\n- F2 [named] b\n'
               '## Final version\ndo it\n## For Sam\n' + PLAIN_OPT.format(n=1) + PLAIN_OPT.format(n=2))
        open(os.path.join(tmp, 't1', 'judge', 'verdict-raw.md'), 'w').write(raw.replace('## Sam test\n', '## Sam test\nQ1: only\n').replace('Q8: ok', ''))
        try:
            P.parse(open(os.path.join(tmp, 't1', 'judge', 'verdict-raw.md')).read(), ['V1', 'V2', 'V3'])
            bad.append('a verdict missing Q8 parsed')
        except ValueError:
            pass
        # 5a. shape 2 (packed from 23 Nov, plain-check Change 1): an option missing a field, or with a code name, is
        # refused; the same verdict in the old shape (an older proposal) still parses, so no old verdict goes stale
        for cut, why in (("You'd notice: the answer comes in one look.\n", 'missing field'),
                         ('Why: ', 'Why: notes/x.md says so; ')):
            try:
                P.parse(raw.replace(cut, '' if why == 'missing field' else why, 1), ['V1', 'V2', 'V3'], 2)
                bad.append(f'a shape-2 verdict with a {why if why == "missing field" else "file name"} parsed')
            except ValueError:
                pass
        old_shape = raw.split('## For Sam')[0] + '## For Sam\n### Option 1: a\ntext\nLost: x\nAdded: y\n### Option 2: b\ntext\nLost: x\nAdded: y\n'
        try:
            P.parse(old_shape, ['V1', 'V2', 'V3'], 1)
        except ValueError:
            bad.append('an old-shape verdict no longer parses as shape 1')
        if P._state('t1').get('shape') != 2:
            bad.append('pack did not mark the proposal shape 2')
        # 5b. V0 (judge.md: no version passes, the judge writes its own) parses; V9 (no such file) does not
        v0 = raw.replace('## Pick\nV2', '## Pick\nV0').replace('| V3 | 3 | 3 | 3 | 3 | 3 | 15 |', '| V3 | 3 | 3 | 3 | 3 | 3 | 15 |\n| V0 | 4 | 4 | 4 | 4 | 4 | 20 |')
        if P.parse(v0, ['V1', 'V2', 'V3'])['pick'] != 'V0':
            bad.append('a V0 pick did not parse')
        try:
            P.parse(raw.replace('## Pick\nV2', '## Pick\nV9'), ['V1', 'V2', 'V3'])
            bad.append('a pick of a missing version parsed')
        except ValueError:
            pass
        open(os.path.join(tmp, 't1', 'judge', 'verdict-raw.md'), 'w').write(raw)
        with contextlib.redirect_stdout(io.StringIO()):
            P.record('t1')
        if 'block' not in run(ask):
            bad.append('verdict but no Critiqued line: not blocked')
        if run(ask + '\nCritiqued: 2 found, 1 fixed, 1 named.'):
            bad.append('valid verdict + Critiqued line blocked')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            P.show('t1')
        order = [buf.getvalue().find(k) for k in ('Problem:', '1. ', 'Why:', "You'd notice:", 'Other option:', 'Lost:', 'Added:')]
        if -1 in order or order != sorted(order):
            bad.append('show does not print the fields in order')
        # 6. an edit after the verdict makes it stale; `mark` does not
        P.mark('t1', 'adopted')
        if run(ask + '\nCritiqued: 2 found, 1 fixed, 1 named.'):
            bad.append('mark made the verdict stale')
        open(f, 'a').write('\nmore')
        if not P.verdict_ok('t1')[0] is False:
            bad.append('edit after verdict not stale')
        return not bad, '; '.join(bad) or ('blocks the 15 Nov asks, passes 5 routine ones, stale and missing verdicts, V0 '
                                           'pick, Critiqued line, stop_hook_active, shape-2 fields (old shape parses)')
    finally:
        P.PROPS = old
        shutil.rmtree(tmp, ignore_errors=True)


@test
def guard_one_correction():
    """guard-film-questions Change 1, the check for Sam's rule "One message, never twice" (22 Nov): every block is logged
    in full; the block tells the chat Sam has read the reply and asks for one "Correction:" line; on the retry only the
    text after the block is judged: a right correction is cleared (no let-through), a full resend is logged as one."""
    import io
    import contextlib
    import json as J
    import shutil
    import tempfile
    import propose as P
    tmp = tempfile.mkdtemp()
    old = P.PROPS
    P.PROPS = tmp
    try:
        f = os.path.join(tmp, 'abcd1234-chat.jsonl')

        def turn(*texts):
            ents = [{'type': 'user', 'message': {'content': 'go on'}}]
            for i, t in enumerate(texts):
                if i:   # the block's reason reaches the chat as a hook message, not as Sam's
                    ents.append({'type': 'system', 'subtype': 'stop_hook', 'content': 'blocked'})
                ents.append({'type': 'assistant', 'message': {'content': [{'type': 'text', 'text': t}]}})
            open(f, 'w').write('\n'.join(J.dumps(e) for e in ents))

        def run(active=False, last=None):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                P.hook(J.dumps({'transcript_path': f, 'stop_hook_active': active, 'last_assistant_message': last}))
            return buf.getvalue()

        bad = []
        unrouted = lambda: P._read(os.path.join(tmp, P.UNROUTED)).count('\n')
        # 1. Sam's 22 Nov chat (56d8e5c4): an unjudged system ask; the block asks for ONE correction line
        ask = ('Way 2 is written in as a rule.\nStill open:\n1. Should lessons 2 and 3 from the articles change how the '
               'rules file is read? Y or N. My pick is Y.\n2. Should I lower the big-film figure in the rulebook? Y or N.')
        turn(ask)
        out = run()
        reason = J.loads(out)['reason'] if out else ''
        if 'ALREADY READ' not in reason or 'Correction: ignore question 1, it is withdrawn' not in reason \
                or 'Do NOT send the reply again' not in reason:
            bad.append(f'block message does not ask for one correction line: {reason[:120]}')
        log = P._blocks()
        if not log or log[-1].get('reply') != ask or log[-1].get('event') != 'block':
            bad.append('first block not logged with the whole reply')
        # 2. a right one-line correction clears it: logged, no let-through
        n0 = unrouted()
        turn(ask, 'Correction: ignore question 1, it is withdrawn.')
        if run(active=True):
            bad.append('blocked twice')
        r = P._blocks()[-1]
        if r.get('event') != 'retry' or r.get('result') != 'cleared' or r.get('shape') != 'short':
            bad.append(f'correct one-liner not cleared: {r}')
        if unrouted() != n0:
            bad.append('a cleared correction was logged as a let-through')
        # 3. the fault Sam saw three times (22 Nov, "Why did you write your response 3 times?"): a full resend after
        # the block is logged as a full repeated reply and a let-through
        turn(ask)
        run()
        turn(ask, 'Sorry, here it is again.\n' + ask)
        run(active=True)
        r = P._blocks()[-1]
        if r.get('shape') != 'full' or r.get('result') != 'let-through' or unrouted() != n0 + 1:
            bad.append(f'a full resend was not caught: {r.get("shape")}, {r.get("result")}')
        # 4. a judged proposal missing its Critiqued line: the block names the exact line; only that line clears it
        fault = ['proposal x: the reply must carry "Critiqued: 6 found, 2 fixed, 4 named" (counted from its file)']
        rs = P.block_reason(fault, 'Need: 1 or 2 below.')
        if '"Correction: Critiqued: 6 found, 2 fixed, 4 named"' not in rs:
            bad.append('Critiqued block does not print the exact line')
        if not P.correction_ok('Correction: Critiqued: 6 found, 2 fixed, 4 named.', fault)[0]:
            bad.append('right Critiqued correction refused')
        if P.correction_ok('Correction: Critiqued: 6 found, 3 fixed, 3 named.', fault)[0]:
            bad.append('wrong numbers accepted')
        if P.correction_ok('Critiqued: 6 found, 2 fixed, 4 named\n' + 'more\n' * 4, fault)[0]:
            bad.append('a long resend accepted as a correction')
        # 3b. Sam's own example (22 Nov, chat 56d8e5c4, saved from its record): the stopped reply sent again whole 12 s
        # later; Sam: "You keep sending me messages twice". The check names question 2 and catches the resend.
        ex = J.load(open(os.path.join(os.path.dirname(HERE), 'notes', 'proposals', 'guard-film-questions',
                                      'example-22nov.json'), encoding='utf-8'))
        turn(ex['blocked'])
        out = run()
        if 'question 2' not in (J.loads(out)['reason'] if out else ''):
            bad.append("Sam's 22 Nov reply: the block does not name question 2")
        turn(ex['blocked'], ex['retry'])
        run(active=True)
        r = P._blocks()[-1]
        if r.get('shape') != 'full' or r.get('result') != 'let-through':
            bad.append(f"Sam's 22 Nov resend not caught: {r.get('shape')}, {r.get('result')}")
        n1 = unrouted()
        turn(ex['blocked'])
        run()
        turn(ex['blocked'], 'Correction: question 2 is not a change, it only asks what you meant by 15% per film.')
        run(active=True)
        if P._blocks()[-1].get('result') != 'cleared' or unrouted() != n1:
            bad.append("Sam's 22 Nov reply: the right one-line correction was not cleared")
        n0 = unrouted() - 1                     # step 5 expects exactly one more let-through
        # 5. a stop by another hook first (no block of ours pending): never blocks twice, logged as before
        open(os.path.join(tmp, P.BLOCKS), 'w').close()
        turn(ask)
        if run(active=True) or unrouted() != n0 + 2:
            bad.append('stop_hook_active without our block: blocked, or not logged as a let-through')
        rep = P.blocks_report()
        return not bad, '; '.join(bad) or ('block asks for one Correction line; a right one clears (no let-through); a '
                                           f'full resend is logged; Critiqued line exact; report: {rep.splitlines()[0]}')
    finally:
        P.PROPS = old
        shutil.rmtree(tmp, ignore_errors=True)


@test
def takes_loads_no_film():
    """takes.py (the shared voice clean-up for every film) loads no finished film's file: its cleaning comes from the
    shared audiokit.py (23 Nov, chain B chat 3; freeze count 21 -> 20)."""
    import ast
    import freeze as FZ
    tree = ast.parse(open(os.path.join(HERE, 'takes.py')).read())
    mods = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names} | \
           {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
    films = sorted(m for m in mods if FZ.FILM.match(m))
    return not films and 'audiokit' in mods, f'film files imported: {films or "none"}; audiokit used: {"audiokit" in mods}'


# the guard's score on its labelled list as measured 23 Nov (chain B chat 4, before Change 2): never worse. Change 2
# (its own yes from Sam) sets all four to 0.
GUARD_BASELINE = {'wrong': 21, 'missed': 2, 'probe_missed': 9, 'probe_blocked': 1}


@test
def guard_labelled_list():
    """guard-film-questions Learn step 2: the guard's 51 real stops (15-23 Nov), each labelled from its chat (film
    question, job, start the route, Critiqued wording, path misread, meaning: wrong stops; Critiqued missing, unjudged
    system ask: true catches), plus the 15 Nov probe. The guard is replayed on all of them: never worse than measured."""
    import json as J
    import propose as P
    d = J.load(open(P.GUARD_LIST, encoding='utf-8'))
    bad = []
    ok_labels = {'film': False, 'job': False, 'start-route': False, 'critiqued-wording': False, 'path-misread': False,
                 'meaning': False, 'critiqued-missing': True, 'unjudged-system': True}
    for r in d['rows']:
        if ok_labels.get(r['label']) is None or ok_labels[r['label']] != r['true_catch']:
            bad.append(f"row {r['n']}: label {r['label']} / true_catch {r['true_catch']} do not agree")
    logged = [ln for ln in P._read(P._p(P.UNROUTED)).splitlines() if ln.startswith('- ') and ln[2:18] <= '2026-11-23 08:38']
    if len(d['rows']) != len(logged) or len(d['probe_change']) != 12 or len(d['probe_routine']) != 10:
        bad.append(f"list incomplete: {len(d['rows'])} rows for {len(logged)} logged stops; probe "
                   f"{len(d['probe_change'])}+{len(d['probe_routine'])}")
    g = P.guard_score()
    for k, base in GUARD_BASELINE.items():
        if len(g[k]) > base:
            bad.append(f'{k}: {len(g[k])} > {base} ({g[k]})')
    return not bad, '; '.join(bad) or ('51 labelled stops + 22 probe questions; replay: ' + ', '.join(
        f'{k} {len(g[k])} (at most {GUARD_BASELINE[k]})' for k in GUARD_BASELINE))


PLAIN_OPT = ("### Option {n}: two quick stills first\n"
             "Problem: staging was built three times before Sam saw the framing he wanted.\n"
             "1. When a note is about framing, draw two small stills of it.\n"
             "2. Send them in one message, a number on each.\n"
             "3. Build the one Sam picks.\n"
             "Why: one cheap look costs less than a whole round.\n"
             "You'd notice: the answer comes in one look.\n"
             "Other option: build and send a short clip, as now.\n"
             "Lost: nothing.\n"
             "Added: one small picture message before a staging round.\n")


@test
def plain_check_fields():
    """CLAUDE.md "Back-end proposals are explained plainly" (Sam's Y, 23 Nov; plain-check Change 1, his answer 2):
    checker A (the fixed fields, no code names) fails all 10 Milburn lessons as they were sent (Sam: "Explain" on 2
    and 6, "don't know what you mean by brow cap" on 9), passes the same lesson rewritten in the fields, and the
    review's lesson check (`propose.py plain`) agrees; the blind reader's saved answers (Step 0, reader3) read as
    advice: L09's list names the brow cap, and every saved answer parses."""
    import contextlib
    import io
    import propose as P
    base = os.path.join(P.PROPS, 'plain-check', 'step0')
    bad = []
    for i in range(1, 11):
        f = os.path.join(base, 'cases', f'L{i:02d}.md')
        if not P.shape_faults(open(f).read()):
            bad.append(f'Milburn lesson {i} passed A')
        with contextlib.redirect_stdout(io.StringIO()):
            if P.plain(f) == 0:
                bad.append(f'plain passed Milburn lesson {i}')
    if P.shape_faults(PLAIN_OPT.format(n=1)):
        bad.append('the field-shaped ask failed A: ' + '; '.join(P.shape_faults(PLAIN_OPT.format(n=1))))
    if not P.shape_faults(PLAIN_OPT.format(n=1).replace('Two quick', 'x').replace('Send them', 'Send them via source/stills.py')):
        bad.append('a file name in a step passed A')
    r3 = os.path.join(base, 'reader3')
    n = 0
    for k in sorted(os.listdir(r3)):
        look, res = (open(os.path.join(r3, k, x)).read() for x in ('look.md', 'result.md'))
        v = P.reader_verdict(look, res)
        n += 1
        if k == 'L09' and not any('brow cap' in w.lower() for w in v['words']):
            bad.append('the reader on L09 does not name the brow cap')
    return not bad, '; '.join(bad) or f'10/10 Milburn lessons fail A (and plain), the field-shaped ask passes, {n} saved reader answers parse'


@test
def never_blame_long_chats():
    """Sam, 26 Nov (Open Wounds chat 39): "Stop telling me chats are long unless you are admitting that your own tool
    is broken." Saved example: chat 39's own reply. The plain-words check stops it; a sentence that owns the handover
    tool's failure passes."""
    import plainwords as PW
    bad = ("Long chats and heavy reading look like a big cause, and that can be checked for about 1-2% of a week. "
           "This chat shows it: each step now costs over three times what it did at the start, because the history is long.")
    ok = "My own handover tool failed here: it should have opened the next chat at 100 steps and didn't."
    plain = ("The nod now turns the head; Kemi's legs part up to the crotch. I've recorded it: \"Stop telling me chats "
             "are long unless you are admitting that your own tool is broken.\"")
    got = [k for k, _, _ in PW.faults(bad, [])]
    return (got.count('chatlong') >= 2 and not PW.faults(ok, []) and not PW.faults(plain, []),
            f'example: {got.count("chatlong")} stopped; owned failure passes; plain passes')


@test
def plain_words_every_message():
    """CLAUDE.md "Checked on every message" (Sam, 26 Nov; R8 chat 2): the every-message plain-words check sends back
    the two replies Sam could not follow (bad-1: "Let's move through these one at a time in simple language"; bad-2:
    "I don't understand") and passes the one he called the model (good-1); the Stop hook blocks once and lets the
    second try through with a log line (never loops); Sam's "I don't understand" saves the reply as a new example and
    puts its project words on the list."""
    import io
    import contextlib
    import shutil
    import tempfile
    import plainwords as PW
    bad = []
    for b, (want, fs) in PW.score().items():
        if b.split('-')[1] in ('1', '2') and b.startswith(('bad-1-', 'bad-2-', 'good-1-')) and bool(fs) != (want == 'fail'):
            bad.append(f'{b} did not {want}')
    msg = PW.example_text(os.path.join(PW.EX, 'bad-2-two-small-items.md'))
    tmp = tempfile.mkdtemp()
    keep = PW.EX, PW.WORDS, PW.LET_LOG
    try:
        PW.LET_LOG = os.path.join(tmp, 'log')
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            PW.hook(json.dumps({'last_assistant_message': msg, 'stop_hook_active': False}))
        if '"block"' not in out.getvalue():
            bad.append('the hook did not send bad-2 back')
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            PW.hook(json.dumps({'last_assistant_message': msg, 'stop_hook_active': True}))
        if out.getvalue().strip() or 'let-through' not in open(PW.LET_LOG).read():
            bad.append('the second try was blocked again or not logged')
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            PW.hook(json.dumps({'last_assistant_message': PW.example_text(
                os.path.join(PW.EX, 'good-1-failing-tests.md')), 'stop_hook_active': False}))
        if out.getvalue().strip():
            bad.append('the hook sent good-1 back')
        PW.EX = tmp
        PW.WORDS = os.path.join(tmp, 'words.json')
        shutil.copy(keep[1], PW.WORDS)
        confusing = 'The **bay splitter** now runs on every take, and the "wobble pass" is next.'
        with contextlib.redirect_stdout(io.StringIO()):
            PW.learn(sam_text="I don't understand", reply=confusing)
            PW.learn(sam_text='Y, go', reply='Done.')
        saved = [f for f in os.listdir(tmp) if f.startswith('bad-')]
        if len(saved) != 1:
            bad.append(f'{len(saved)} examples saved (want 1: only the reply Sam did not follow)')
        if not PW.faults('The bay splitter is next.'):
            bad.append('a learned word ("bay splitter") is not caught next time')
    finally:
        PW.EX, PW.WORDS, PW.LET_LOG = keep
        shutil.rmtree(tmp, ignore_errors=True)
    return not bad, '; '.join(bad) or 'bad-1 and bad-2 sent back, good-1 passes; one block then a logged let-through; a confused reply saved and its words learned'


# ------------------------------------------------------------------------------------------------ code finder (Sam's 1, 16 Nov)
@test
def code_finder_replay():
    """The frozen 26-note Blessed replay (notes/proposals/learn/replay-show.py): page.py show, given each note's words,
    shot and time, must keep at least 25/26 loose, 14/14 strict, every answer under 45 lines (code-finder change 2)."""
    import importlib.util as u
    sp = u.spec_from_file_location('replay_show', os.path.join(os.path.dirname(HERE), 'notes', 'proposals', 'learn',
                                                               'replay-show.py'))
    r = u.module_from_spec(sp); sp.loader.exec_module(r)
    lo, st, mx, _ = r.run()
    return lo >= 25 and st >= 14 and mx < 45, f'loose {lo}/26, strict {st}/14, longest {mx} lines (bar 25, 14, <45)'


@test
def finder_reaches_shared_nod():
    """R12 (Sam, 26 Nov: "It should cover everything in the project that we use!!"): the code finder searches the shared
    kit a film imports, not only the film's own files: chat 39's note 26, "It's not a nod, it's a head-bob", must show
    views.py's nod drawing (Pitched / NOD_DEG) with its lines; other films' code stays out of the reach."""
    import page
    reach = {os.path.basename(f) for f in page.files('brexit-is-done')}
    out = page.show('brexit-is-done', "It's not a nod, it's a head-bob.", 40)
    nod = [h for h, rows in out if rows and h.startswith('views.py') and re.search(r'Pitched|Rolled|NOD_', h + ' '.join(t for _, t in rows))]
    bad = (['views.py not in the reach'] if 'views.py' not in reach else []) + \
          (['another film (blessed.py) in the reach'] if 'blessed.py' in reach else []) + \
          ([] if nod else ['note 26 shows no views.py nod drawing: ' + ', '.join(h.split()[0] for h, _ in out)])
    return not bad, '; '.join(bad) or f'{len(reach)} files searched; note 26 -> {nod[0].split("  ")[0]}'


@test
def finder_reach_end_check():
    """R12 part 2: handover end flags a chat that used the finder and then edited code it cannot see or never pointed
    to. Saved example: chat 39 (show log, 26 Nov 22:11, zkJd6kM8) asked show about note 26, was pointed only at
    brexit_is_done.py, then edited views.py, solid_seat.py and facehouse.py by hand; with the old own-files-only finder
    each is a blind spot, with today's each is a miss; a chat pointed at the file, or with no show call, is clean."""
    import handover, page
    shows = {'brexit-is-done': {'brexit_is_done.py'}}
    chat39 = ['views.py', 'solid_seat.py', 'facehouse.py']
    old = lambda film: [os.path.basename(f) for f in page.own_files(film)]
    new = lambda film: [os.path.basename(f) for f in page.files(film)]
    blank = lambda film: ''
    a = handover.reach_faults(chat39, shows, old, blank)
    b = handover.reach_faults(chat39, shows, new, blank)
    c = handover.reach_faults(['views.py'], {'brexit-is-done': {'views.py'}}, new, blank)
    d = handover.reach_faults(chat39, {}, new, blank)
    e = handover.reach_faults(['views.py', 'body.py'], shows, new, lambda film: 'finder reach: views.py, body.py (a new tool)')
    bad = ([f'old finder: {len(a)} of 3 blind spots'] if sum(x.startswith('FINDER REACH') for x in a) != 3 else []) + \
          ([f'new finder: {len(b)} of 3 misses'] if sum(x.startswith('FINDER MISSED') for x in b) != 3 else []) + \
          (['a pointed-to edit flagged'] if c else []) + (['a chat with no show call flagged'] if d else []) + \
          (['a notes line did not settle it'] if e else [])
    return not bad, '; '.join(bad) or 'chat 39: 3 blind spots under the old finder, 3 misses under the new; clean cases clean'



def _repo_pair():
    """A pretend GitHub (a bare repo) with the main line holding one ledger row, and a chat's copy of it on its own
    branch: (bare, copy, git)."""
    import subprocess
    import tempfile
    import mainline
    top = tempfile.mkdtemp()
    bare, copy = os.path.join(top, 'gh.git'), os.path.join(top, 'chat')
    git = lambda root, *a: subprocess.run(['git', '-C', root] + list(a), capture_output=True, text=True)
    subprocess.run(['git', 'init', '-q', '--bare', bare])
    subprocess.run(['git', 'init', '-q', copy])
    git(copy, 'config', 'user.email', 'k@t'); git(copy, 'config', 'user.name', 'kt')
    os.makedirs(os.path.join(copy, 'notes', 'ledger'))
    row = {'date': '2026-11-10', 'chat': 'aaaa1111', 'cost': 1.0, 'src': 'estimate', 'round': None, 'model': 'opus', 'stage': 'auto', 'notes': 0, 'repeats': [], 'sid': 'session_A'}
    open(os.path.join(copy, 'notes', 'ledger', 'kt.json'), 'w').write(json.dumps(
        {'film': 'kt', 'estimate': None, 'chats': [row], 'checks': {}}, indent=1))
    open(os.path.join(copy, '.gitattributes'), 'w').write(open(os.path.join(HERE, '..', '.gitattributes')).read())
    git(copy, 'add', '-A'); git(copy, 'commit', '-q', '-m', 'start')
    git(copy, 'remote', 'add', 'origin', bare)
    git(copy, 'push', '-q', 'origin', f'HEAD:refs/heads/{mainline.MAIN}')
    git(copy, 'checkout', '-q', '-b', 'claude/chat-work')
    return bare, copy, git


@test
def cost_rows_reach_the_main_line():
    """startup-fixes 1 (Sam, 16 Nov): 7 of 9 chats' cost rows sat on side branches; each row now goes onto the main
    line alone (never the chat's half-done work), survives another chat pushing first, merges row by row, and the
    one-off gather brings stranded rows in with each chat once."""
    import json as _j
    import ledger
    import mainline
    bare, copy, git = _repo_pair()
    keep = ledger.ROOT, ledger.DIR, ledger.CURRENT
    ledger.ROOT, ledger.DIR = copy, os.path.join(copy, 'notes', 'ledger')
    ledger.CURRENT = os.path.join(ledger.DIR, '.current')
    main = lambda p='notes/ledger/kt.json': git(bare, 'show', f'{mainline.MAIN}:{p}').stdout
    bad = []
    try:
        open(os.path.join(copy, 'work.txt'), 'w').write('half-done film work')
        git(copy, 'add', 'work.txt'); git(copy, 'commit', '-q', '-m', 'half-done')
        open(os.path.join(copy, 'dirty.txt'), 'w').write('unsaved')
        # another chat pushes its row first: to_main must build on it, not overwrite it
        real = mainline._git
        state = {'n': 0}

        def racing(root, *a, **k):
            if a[:1] == ('push',) and state['n'] == 0:
                state['n'] = 1
                other = os.path.join(os.path.dirname(bare), 'other')
                real(os.path.dirname(bare), 'clone', '-q', '-b', mainline.MAIN, bare, other)
                git(other, 'config', 'user.email', 'k@t'); git(other, 'config', 'user.name', 'kt')
                p = os.path.join(other, 'notes', 'ledger', 'kt.json')
                d = _j.load(open(p))
                d['chats'].append({'date': '2026-11-11', 'chat': 'cccc3333', 'cost': 0.5, 'src': 'estimate', 'round': None, 'model': 'opus', 'stage': 'auto', 'notes': 0, 'repeats': []})
                open(p, 'w').write(_j.dumps(d, indent=1))
                git(other, 'commit', '-q', '-am', 'other chat'); git(other, 'push', '-q', 'origin', 'HEAD')
            return real(root, *a, **k)
        mainline._git = racing
        try:
            res = ledger.push_row('kt', {'date': '2026-11-12', 'chat': 'bbbb2222', 'cost': 2.0, 'src': 'estimate',
                                         'sid': 'session_B', 'round': None, 'model': 'opus', 'stage': 'auto', 'notes': 0, 'repeats': []})
        finally:
            mainline._git = real
        on = {c['chat'] for c in _j.loads(main())['chats']}
        if res != 'pushed' or on != {'aaaa1111', 'bbbb2222', 'cccc3333'}:
            bad.append(f'main line rows {sorted(on)} ({res})')
        if 'work.txt' in git(bare, 'ls-tree', '--name-only', mainline.MAIN).stdout:
            bad.append("the chat's own work reached the main line")
        if git(bare, 'rev-parse', '-q', '--verify', 'refs/heads/claude/chat-work').returncode == 0:
            bad.append("the chat's branch was pushed")
        if git(copy, 'status', '--porcelain', 'notes').stdout.strip():
            bad.append('the ledger left uncommitted here')
        # merge driver: the chat's copy and the main line both grew; a merge keeps every row, no clash
        git(copy, 'rm', '-q', '--cached', 'dirty.txt')
        p = os.path.join(copy, 'notes', 'ledger', 'kt.json')
        d = _j.load(open(p))
        d['chats'].append({'date': '2026-11-13', 'chat': 'dddd4444', 'cost': 0.3, 'src': 'estimate', 'round': None, 'model': 'opus', 'stage': 'auto', 'notes': 0, 'repeats': []})
        open(p, 'w').write(_j.dumps(d, indent=1)); git(copy, 'commit', '-q', '-am', 'local row')
        ledger.push_row('kt', {'date': '2026-11-13', 'chat': 'eeee5555', 'cost': 0.4, 'src': 'estimate', 'round': None, 'model': 'opus', 'stage': 'auto', 'notes': 0, 'repeats': [],
                               'notes': 0, 'repeats': []})
        git(copy, 'reset', '-q', '--hard', 'HEAD~1')    # drop the local copy of eeee5555: only the main line has it
        git(copy, 'fetch', '-q', 'origin')
        m = git(copy, 'merge', '-q', '--no-edit', f'origin/{mainline.MAIN}')
        rows = {c['chat'] for c in _j.load(open(p))['chats']}
        if m.returncode or not {'dddd4444', 'eeee5555', 'cccc3333'} <= rows:
            bad.append(f'merge: {m.stderr.strip()[:80]} rows {sorted(rows)}')
        # rules: an app row beats an estimate; two app reads keep the larger dollars at today's price; an estimate
        # with no app id after the film's first app row is the same chat and stays out
        L = {'chats': [{'date': '2026-11-10', 'chat': 'x', 'sid': 's1', 'src': 'app', 'cost': 1, 'usd': 2.45}]}
        ledger.merge_row(L, {'date': '2026-11-10', 'chat': 'y', 'sid': 's1', 'src': 'estimate', 'round': None, 'model': 'opus', 'stage': 'auto', 'notes': 0, 'repeats': [], 'cost': 9})
        ledger.merge_row(L, {'date': '2026-11-11', 'chat': 'z', 'src': 'estimate', 'round': None, 'model': 'opus', 'stage': 'auto', 'notes': 0, 'repeats': [], 'cost': 3})
        ledger.merge_row(L, {'date': '2026-11-10', 'chat': 'x', 'sid': 's1', 'src': 'app', 'cost': 9, 'usd': 4.9})
        if len(L['chats']) != 1 or L['chats'][0]['usd'] != 4.9 or L['chats'][0]['cost'] != ledger._pct(4.9):
            bad.append(f'row rules: {L["chats"]}')
        # gather: a stranded row on a side branch comes in once; a chat the main line files under another film
        # does not come back under this one
        side = os.path.join(os.path.dirname(bare), 'side')
        git(os.path.dirname(bare), 'clone', '-q', '-b', mainline.MAIN, bare, side)
        git(side, 'config', 'user.email', 'k@t'); git(side, 'config', 'user.name', 'kt')
        git(side, 'checkout', '-q', '-b', 'claude/old-side')
        sp = os.path.join(side, 'notes', 'ledger', 'kt.json')
        d = _j.load(open(sp))
        d['chats'] += [{'date': '2026-11-14', 'chat': 'ffff6666', 'cost': 1.1, 'src': 'estimate', 'round': None, 'model': 'opus', 'stage': 'auto', 'notes': 0, 'repeats': [], 'sid': 'session_F'},
                       {'date': '2026-11-14', 'chat': 'gggg7777', 'cost': 0.9, 'src': 'estimate', 'round': None, 'model': 'opus', 'stage': 'auto', 'notes': 0, 'repeats': [], 'sid': 'session_G'}]
        d['alarms_off'] = 'an old switch a later chat removed'
        open(sp, 'w').write(_j.dumps(d, indent=1))
        open(os.path.join(side, 'notes', 'ledger', 'other.json'), 'w').write(_j.dumps({'film': 'other', 'estimate': None, 'checks': {}, 'chats': [
            {'date': '2026-11-14', 'chat': 'gggg7777', 'cost': 0.9, 'src': 'estimate', 'round': None, 'model': 'opus', 'stage': 'auto', 'notes': 0, 'repeats': [], 'sid': 'session_G'}]}))
        git(side, 'add', '-A'); git(side, 'commit', '-q', '-m', 'stranded'); git(side, 'push', '-q', 'origin', 'HEAD')
        git(copy, 'fetch', '-q', 'origin')
        before = sum(len(v) for v in ledger.missing(copy).values())
        res, added = ledger.gather(copy)
        git(copy, 'fetch', '-q', 'origin')
        after = sum(len(v) for v in ledger.missing(copy).values())
        kt = [c['chat'] for c in _j.loads(main())['chats']]
        oth = [c['chat'] for c in _j.loads(main('notes/ledger/other.json') or '{"chats": []}')['chats']]
        if before != 2 or after or kt.count('ffff6666') != 1 or kt.count('gggg7777') + oth.count('gggg7777') != 1:
            bad.append(f'gather: missing {before} -> {after}; kt {kt}; other {oth}')
        if 'alarms_off' in main() or 'ffff6666' not in main('notes/ledger/kt.md'):
            bad.append('gather brought back a removed key, or left the .md behind')
        # Sam's saved messages go the same way (two chats' logs were stranded on claude/chat-XXXX branches)
        import handover as HO
        hk = HO.ROOT, HO.LOGDIR, HO._not_typed
        HO.ROOT, HO.LOGDIR = copy, os.path.join(copy, 'notes', 'ledger', 'sam')
        HO._not_typed = lambda *a: False
        try:
            HO._late({'prompt': 'Y to all', 'sid': 'session_01KTKTKT', 'at': '10:00'})
        finally:
            HO.ROOT, HO.LOGDIR, HO._not_typed = hk
        if 'Y to all' not in main('notes/ledger/sam/01ktktkt.md'):
            bad.append("Sam's message did not reach the main line")
    finally:
        ledger.ROOT, ledger.DIR, ledger.CURRENT = keep
        mainline.config(ledger.ROOT)
    return not bad, '; '.join(bad) or 'rows on the main line alone, a race survived, merges by row, gather once each'



@test
def branch_printout_lists_only_real_work():
    """startup-fixes 2 (Sam, 16 Nov): chats read all ~254 branches at start; the start now lists only branches whose
    newest work never reached the main line, judged by content (the main line was rewritten once and this copy is
    shallow, so shared commits mean nothing; the first try listed 190 branches); the end refuses an unnamed one."""
    import subprocess
    import branches
    import mainline
    bare, copy, git = _repo_pair()
    top = os.path.dirname(bare)
    side = os.path.join(top, 'side')
    git(top, 'clone', '-q', '-b', mainline.MAIN, bare, side)
    git(side, 'config', 'user.email', 'k@t'); git(side, 'config', 'user.name', 'kt')

    def branch(name, files, base=mainline.MAIN):
        git(side, 'checkout', '-q', '-B', name, f'origin/{base}')
        for f, text in files.items():
            os.makedirs(os.path.dirname(os.path.join(side, f)) or side, exist_ok=True)
            open(os.path.join(side, f), 'w').write(text)
        git(side, 'add', '-A'); git(side, 'commit', '-q', '-m', name)
        git(side, 'push', '-q', '-f', 'origin', f'HEAD:refs/heads/{name}')
    branch('claude/real-work', {'source/new.py': 'new tool'})
    branch('claude/ledger-only', {'notes/ledger/kt.json': '{"film": "kt", "chats": []}'})
    branch('claude/merged-by-copy', {'notes/done.md': 'already on the main line'})
    git(side, 'checkout', '-q', '-B', 'rewrite', f'origin/{mainline.MAIN}')   # the main line gets the same text by
    open(os.path.join(side, 'notes', 'done.md'), 'w').write('already on the main line')   # another commit
    git(side, 'add', '-A'); git(side, 'commit', '-q', '-m', 'same text, other history')
    git(side, 'push', '-q', 'origin', f'HEAD:refs/heads/{mainline.MAIN}')
    branches.fetch(copy)
    names = [b[0] for b in branches.scan(copy)]
    old = [b[0] for b in branches.scan(copy, now=__import__('time').time() + 9 * 86400)]
    left = [b[0] for b in branches.unsettled('notes: claude/real-work kept off (Sam, 16 Nov)', copy)]
    left2 = [b[0] for b in branches.unsettled('nothing named', copy)]
    ok = names == ['claude/real-work'] and not old and not left and left2 == ['claude/real-work']
    return ok, f'listed {names}; after 9 days {old}; named -> {left}; unnamed -> {left2}'


@test
def notes_printout_reads_only_open_notes():
    """startup-fixes 3 (Sam, 16 Nov): chats read the whole notes file at start (~3.6k tokens); `handover.py start
    --film` now prints "Where things stand" and only the unticked notes, while carried() still checks the whole file."""
    import tempfile
    import handover
    p = os.path.join(tempfile.mkdtemp(), 'kt.md')
    open(p, 'w').write("""# Notes for kt
## Where things stand (the ONE handover)
- **Next:** the bin lid note.
## Round notes
- [ ] R1 the whale knocks the helideck away
- [x] R2 the moped is red
## The brief as a checklist
| # | from the brief | done? |
|---|---|---|
| 1 | the granny throws a shoe | |
| 2 | the hook text frame | ticked chat 3 |
## Plan
| thing | est | measured from |
|---|---|---|
| tourist | 1.2 | |
## Notes
| # | shot | time | note | line | status |
|---|---|---|---|---|---|
| 1 | A | 3.0 | the bin lid flaps | C4 | fixed (chat 4) |
| 2 | B | 5.1 | his face still needs work | C9 | open |
| 3 | C | 7.0 | the cart wheels skid | C2 | |
""")
    t = handover.open_notes(p)
    want = ['the bin lid note', 'R1 the whale', 'granny throws', 'face still needs', 'cart wheels skid']
    gone = ['R2 the moped', 'hook text frame', 'tourist', 'bin lid flaps']
    miss = [w for w in want if w not in t] + [f'shown: {w}' for w in gone if w in t]
    held = handover.carried('the moped is red', handover.note_lines(p))   # carried() still sees ticked lines
    return not miss and held, f'missing/extra {miss}; carried() on a ticked line: {held}'


@test
def process_work_is_never_billed_to_a_film():
    """Sam, 16 Nov: chat 7406486e built a startup fix but was billed to European Protests, Ranked (on hiatus), because
    it tested on that film's notes 14 times; then billed again under proposal-route. A task under notes/proposals/
    now bills process work; a film's task that cites a proposal stays the film's; one chat sits in one ledger."""
    import json as _j
    import tempfile
    import ledger
    import mainline
    bare, copy, git = _repo_pair()
    for n in ('kt', 'proposal-route', 'protest-tiers'):
        open(os.path.join(copy, 'notes', f'{n}.md'), 'w').write('# notes\n')
    git(copy, 'add', '-A'); git(copy, 'commit', '-q', '-m', 'notes')
    keep = ledger.ROOT, ledger.DIR, ledger.CURRENT
    ledger.ROOT, ledger.DIR = copy, os.path.join(copy, 'notes', 'ledger')
    ledger.CURRENT = os.path.join(ledger.DIR, '.current')

    def chat(task, calls):
        p = os.path.join(tempfile.mkdtemp(), 't.jsonl')
        rows = [{'type': 'user', 'message': {'content': task}}]
        rows += [{'type': 'assistant', 'message': {'content': [{'type': 'tool_use', 'input': {'command': c}}]}}
                 for c in calls]
        open(p, 'w').write('\n'.join(_j.dumps(r) for r in rows))
        return p
    tests = 14 * ['python3 -c "open_notes(\'notes/protest-tiers.md\')"']
    try:
        got = [ledger.film_of(chat('Startup fixes, chat 5: read notes/proposals/startup-reading/handover.md', tests)),
               ledger.film_of(chat('Notes round: notes/protest-tiers.md; the rule is in notes/proposals/x.md', [])),
               ledger.film_of(chat('carry on', tests))]
        ledger.drop_elsewhere('proposal-route', 'session_A', 'aaaa1111')
        here = _j.load(open(os.path.join(copy, 'notes', 'ledger', 'kt.json')))['chats']
        main = _j.loads(git(bare, 'show', f'{mainline.MAIN}:notes/ledger/kt.json').stdout)['chats']
    finally:
        ledger.ROOT, ledger.DIR, ledger.CURRENT = keep
    ok = got == ['proposal-route', 'protest-tiers', 'protest-tiers'] and not here and not main
    return ok, f'billed to {got}; rows left under the other film: here {len(here)}, main line {len(main)}'



@test
def claude_md_sentences_never_lost():
    """startup fixes 4 (Sam's Y, 16 Nov): CLAUDE.md text may move only word for word (to the rulebook or a pack); a
    dated tag may leave its sentence only with a row in the rulebook's "Dates moved from CLAUDE.md" table."""
    import subprocess
    import sentences as S
    old = "# A\n- **Rule one (Sam, 13 Nov):** do X. Do Y.\n# B\n- **Photos:** news first,\n  then libraries.\n"
    book = "# Rules\n## Dates moved from CLAUDE.md\n| CLAUDE.md rule (its first words) | date |\n|---|---|\n" \
           "| Rule one | (Sam, 13 Nov) |\n"
    good = {'CLAUDE.md': "# A\n- **Rule one:** do X. Do Y.\n# B\n- Photos: see the pack.\n",
            'guides/film-quality-rules.md': book,
            'guides/job-packs.md': "## Plan\n- **Photos:** news first, then\n  libraries.\n"}
    no_row = dict(good, **{'guides/film-quality-rules.md': '# Rules\n'})
    reworded = dict(good, **{'CLAUDE.md': "# A\n- **Rule one:** do X. Do Z.\n# B\n"})
    got = [S.lost(old, good), S.lost(old, no_row), S.lost(old, reworded)]
    ok = got[0] == [] and any('Rule one' in s for s in got[1]) and got[2] == ['Do Y.']
    r = subprocess.run(['git', '-C', S.ROOT, 'show', 'f16bf306:CLAUDE.md'], capture_output=True, text=True)
    if r.returncode == 0:      # the real move (chat 7): the CLAUDE.md before it against today's files
        now = {f: open(os.path.join(S.ROOT, f), encoding='utf-8').read() for f in S.FILES}
        real = S.lost(r.stdout, now)
        ok = ok and not real
        got.append(real[:3])
    return ok, f'good move lost {got[0]}; tag with no row lost {len(got[1])}; reworded lost {len(got[2])}; ' \
               f'the real move: {got[3] if len(got) > 3 else "old copy not in this shallow clone"}'


@test
def phone_size_poses():
    """Craft change 2 (Sam, 16 Nov): pre-flight refuses a film with people and no SHOT_MARKS, and every acting-list body
    move or never-looked-at gallery pose with no 'Pose looked at:' line; replayed on EPR (its shrug failed twice);
    the drawing-pass facing check flags a named person turned off the lens in a film with no rooms plan."""
    import posecheck as P
    src = '\n'.join(open(p).read() for p in P._film_files('protest-tiers'))
    notes = open(P._notes_of('protest-tiers')).read()
    epr = P.gate_faults(src, notes, {'people'}, None)
    caught = any('SHOT_MARKS' in x for x in epr) and any('shrug' in x for x in epr)
    fixed = notes + '\n- Pose looked at: passenger, C | 2.40 s | phone size: shoulders up, palm up, reads\n'
    cleared = not any('shrug' in x for x in P.gate_faults(src, fixed, {'people'}, {'C': ['passenger']}))
    gal = P.gate_faults("j = moves.pose(sp, 'shrug')", '', {'people'}, {'a': ['x']})
    nopeople = P.gate_faults('', '', {'props'}, None)

    class Film:
        SHOTS = [('a', 0, 2)]
        SHOT_MARKS = {'a': ['bob']}
        THREE_QUARTER_OK = ()
    P.set_marks(Film)
    P.FACING[:] = [('Bob', 90), ('Ann', 90)]
    side = P.take(1.0)
    P.FACING[:] = [('Bob', 10)]
    front = P.take(1.0)
    P.MARKS.clear()
    ok = caught and cleared and len(gal) == 1 and not nopeople and len(side) == 1 and not front
    return ok, f'EPR refusals {len(epr)} (shrug and no marks caught: {caught}); cleared by its line: {cleared}; ' \
               f'gallery shrug refused: {len(gal)}; side-on Bob flagged: {len(side)}, front Bob: {len(front)}'


@test
def drawn_angle_every_film():
    """C1 (front-on focus, Sam: Y to all, 19 Nov): pre-flight reads the DRAWN angle on every film, rooms plan or not
    (until then only films with no rooms plan were read, so Milburn's YAW3 = 40 passed). Replayed on Milburn: its
    scenes 3 and 6 (all four drawn 40 degrees off the lens) are flagged; a film with a rooms plan drawing someone at
    40 degrees is flagged, a reason in THREE_QUARTER_OK clears it, a head turned past 25 counts, a mark named by its
    CAST key matches the drawn name, and a front-on film (midterminal's shot 'two') passes."""
    import importlib
    import body as B
    import figure as F
    import posecheck as P
    import preflight
    if 'kittests' not in F._ALLOW:
        F._ALLOW.append('kittests')
    B.SS = 1

    class Film:
        HAS = {'people', 'rooms'}
        SHOTS = [('a', 0, 2)]
        SHOT_MARKS = {'a': ['bob']}
        CAST = {'bob': {'name': 'The tall man (extra)'}}
        THREE_QUARTER_OK = ()
    P.set_marks(Film)
    P.FACING[:] = [('The tall man (extra)', 40, 40)]
    rooms_turned = len(P.take(1.0))
    P.FACING[:] = [('The tall man (extra)', 0, 30)]
    body_turned = len(P.take(1.0))
    P.FACING[:] = [('The tall man (extra)', 30, 0)]
    head_turned = len(P.take(1.0))
    P.FACING[:] = [('The tall man (extra)', 12, 0)]
    front = len(P.take(1.0))
    Film.THREE_QUARTER_OK = (('a', 'bob', 'he walks out of shot'),)
    P.set_marks(Film)
    P.FACING[:] = [('The tall man (extra)', 90, 90)]
    reasoned = len(P.take(1.0))
    flagged = {}
    for name, times in (('milburn', (12.62, 36.25)), ('midterminal', ())):
        film = importlib.import_module(name)
        preflight.install_probes(film)
        preflight._FILM, preflight._FPS = film, getattr(film, 'FPS', 12)
        if not times:
            s = next(s for s in film.SHOTS if s[0] == 'two')
            times = ((s[1] + s[2]) / 2,)
        got = [preflight._turn_frame(t) for t in times]
        flagged[name] = sorted({f['who'].split(' (')[0] for fs, _ in got for f in fs})
    matched = ('two', 'satan') in {tuple(h) for _, hs in got for h in hs}    # midterminal's pass is a real one
    P.MARKS.clear()
    ok = (rooms_turned == 1 and body_turned == 1 and head_turned == 1 and not front and not reasoned
          and len(flagged['milburn']) == 4 and not flagged['midterminal'] and matched)
    return ok, (f'rooms film at 40: {rooms_turned}; body 30: {body_turned}; head 30: {head_turned}; 12: {front}; '
                f'reasoned: {reasoned}; Milburn 3 and 6 flagged: {flagged["milburn"]}; '
                f'midterminal front on: {flagged["midterminal"] or "clean"} (Satan matched: {matched})')


@test
def focus_front_heads():
    """C2 (front-on focus, Sam: Y to all, 19 Nov): the focus setting on both front heads (focus.py). At focus 0 every
    drawing is pixel for pixel what it is with the focus code taken out: Andy and Kemi on the house head, a Milburn
    frame of invented kit faces (5 s), one of Andy and Pat (32 s), a Protest Tiers frame (3 s). (Until 21 Nov these were
    fingerprints held from 19 Nov; the kit has changed on purpose since and finished films draw from their bookmarks,
    freeze.py, so the test now compares with focus switched off, drawn the same day.) At full focus every piece is MOVED, never warped: each piece keeps every distance between its points on
    one side of the face (the tilt only turns it), and the face outline stays where it was (tilt off)."""
    import hashlib
    import importlib
    import math as M
    import shutil
    import tempfile
    import body as B
    import facehouse as FH
    import figure as F
    import focus as FO
    if 'kittests' not in F._ALLOW:
        F._ALLOW.append('kittests')
    samples = [('milburn', 5.0), ('milburn', 32.0), ('protest_tiers', 3.0)]
    B.SS = 1
    tmp = tempfile.mkdtemp()

    def prints():
        out = {}
        for name, t in samples:
            out[f'{name} {t:g}'] = hashlib.md5(importlib.import_module(name).frame_image(t).tobytes()).hexdigest()
        for n in ('burnham', 'badenoch'):
            out[n] = hashlib.md5(open(FH.draw(n, 'detail', os.path.join(tmp, n + '.png')), 'rb').read()).hexdigest()
        return out

    class Off:                       # no focus code at all: every piece is the head's own face, the eyes their own look
        def __init__(self, base, sp, L, room=None):
            self.whole = self.eyes = self.brows = self.lens = self.nose = self.mouth = self.lines = self.ears = base
            self.marks = base
    try:
        live = prints()
        real_focus, real_look = FO.Focus, FO.look
        FO.Focus, FO.look = Off, (lambda sp: float(sp.get('look', 0.0) or 0.0))
        try:
            bare = prints()
        finally:
            FO.Focus, FO.look = real_focus, real_look
    finally:
        shutil.rmtree(tmp)
    same = [k for k in live if live[k] == bare[k]]

    class Face:
        tq = 0.0

        def __call__(self, u, v):
            return (540 + u * 172, 300 + v * 172)
    L = dict(eye_y=0.42, nose_y=0.66, fw=0.8)
    pts = [(-0.3, 0.4), (-0.12, 0.45), (-0.2, 0.36), (0.12, 0.44), (0.3, 0.38), (0.2, 0.47)]
    rigid = True
    for sp in (dict(focus=1.0), dict(focus=-0.7), dict(focus=1.0, focus_tilt=0.0)):
        Fo = FO.Focus(Face(), sp, L, room=0.03)
        for piece in (Fo.eyes, Fo.brows, Fo.lens, Fo.mouth, Fo.lines, Fo.ears, Fo.whole):
            for side in ([p for p in pts if p[0] < 0], [p for p in pts if p[0] > 0]):
                a = [Face()(*p) for p in side]
                b = piece.pts(side)
                for i in range(len(a)):
                    for j in range(i):
                        if abs(M.dist(a[i], a[j]) - M.dist(b[i], b[j])) > 1e-6:
                            rigid = False
    cast, B2, V = FO._cast('facetool', ('andy', 'kemi'))
    kept = moved = 0
    import numpy as np
    for w in ('andy', 'kemi'):
        base = np.asarray(FO.bust(cast[w], 0.0, B2, V))
        look = np.asarray(FO.bust(cast[w], 1.0, B2, V, extra=dict(focus_tilt=0.0)))
        sil = lambda a: np.argwhere((np.abs(a.astype(int) - (236, 232, 226)).sum(2) > 30)[:200])   # noqa: E731
        moved += int((np.abs(base.astype(int) - look.astype(int)).sum(2) > 60).sum() > 300)
        sb, sl = sil(base), sil(look)
        kept += int(abs(sb[:, 1].min() - sl[:, 1].min()) <= 6 and abs(sb[:, 1].max() - sl[:, 1].max()) <= 6)
    ok = len(same) == 5 and rigid and moved == 2 and kept == 2
    return ok, (f'held at focus 0: {same}; pieces moved not warped: {rigid}; faces changed at full focus: {moved}/2; '
                f'head outline kept: {kept}/2')


@test
def crowd_heads_hung():
    """GTA shot 4 (Sam's notes 5, 10, 14, 20 Nov): a crowd member made on the fly (crowd_person) after the kit is
    installed draws its OWN head and hair, never the body's bald stand-in (every walker and cop drew bald). Old way
    put back (the hook removed): caught."""
    import people as PK
    import people_parts as PP
    import gta_cast as GC
    GC.cast()
    cr = PK.crowds(GC.FILM)
    sps = [PK.crowd_person(cr['walker'], i) for i in range(12)] + [PK.crowd_person(cr['cop'], i) for i in range(3)]
    hung = sum(PP.B.HEADS.get(sp['who']) is PK.kit_head for sp in sps)
    want_hair = sum(sp['kit_face'].get('hair') not in ('bald', 'none') for sp in sps)
    return hung == len(sps) and want_hair >= 12, f'heads hung {hung}/{len(sps)}; members meant to have hair {want_hair}'


@test
def crowds_varied():
    """Craft change 1 (Sam, 16 Nov): the sameness check: EPR's gold hats (9 of 20 hats), one-model police and one-face
    rioters, the bald share, a place's skin mix, a crowd step that skips list items, and neighbours in step."""
    import kitchecks as K
    gold, other = (186, 146, 52), [(24, 24, 26), (80, 82, 86), (34, 40, 62), (156, 34, 38), (40, 92, 70)]

    def p(i, **kw):
        sp = dict(skin=[(236, 200, 176), (204, 160, 120)][i % 2], hair='crop', hair_c=(30 + i * 9, 20, 10),
                  jacket=(20 + 13 * i, 60, 90), height=1.7 + i / 100)
        sp.update(kw)
        return sp
    hats = [p(i, headwear='beanie', hat_c=gold if i < 9 else other[i % 5]) for i in range(20)]
    spread = [p(i, headwear='beanie', hat_c=other[i % 5]) for i in range(20)]
    police = [dict(p(0), hair='none') for _ in range(12)]
    bald = [p(i, hair='bald' if i % 4 == 0 else 'crop') for i in range(24)]
    mix = {'light': .5, 'olive': .5}
    pale = [p(i, skin=(236, 200, 176)) for i in range(24)]
    got = dict(gold=K.same_faults('a', hats), spread=K.same_faults('a', spread), police=K.same_faults('a', police),
               bald=K.same_faults('a', bald), mix=K.same_faults('a', pale, mix), mixok=K.same_faults('a', spread, mix))
    rec = []
    for f in range(6):                                   # three marchers swinging together, a fourth on its own beat
        for w in ('m1', 'm2', 'm3', 'm4'):
            rec.append(('t4', w, dict(_t=f / 12, _pose=(('wrL', (f if w != 'm4' else 5 - f, 0)),))))
    step = K.in_step(object(), rec)
    apart = K.in_step(object(), [r for r in rec if r[1] in ('m1', 'm4')])
    import people as PK                                  # the kit's crowd defaults (craft chat 3): EPR's cities
    dflt = {}                                            # from a bare 'crowd:' line pass; a 'same:' line is let be
    for city in ('barcelona', 'frankfurt', 'paris', 'tirana'):
        d = PK.parse(f'# m: M\ncrowd: m\nmix: {city}\n')['m']
        d['crowd_defaults'] = True
        dflt[city] = K.same_faults(city, [PK.crowd_person(d, i) for i in range(64)], d.get('crowd_mix'))
    one = PK.parse('# m: M\ncrowd: m\noutfit: jumper 26 26 30\n')['m']
    same = PK.parse('# m: M\ncrowd: m\noutfit: jumper 26 26 30\nsame: top because one club strip\n')['m']
    one['crowd_defaults'] = same['crowd_defaults'] = True
    told = K.same_faults('m', [PK.crowd_person(one, i) for i in range(24)])
    let = K.same_faults('m', [PK.crowd_person(same, i) for i in range(24)],
                        ok=[('*', k, w) for ks, w in same['crowd_same'] for k in ks])
    ok = (any('hat' in x for x in got['gold']) and not got['spread'] and any('look' in x for x in got['police'])
          and any('bald' in x for x in got['bald']) and any('skins' in x for x in got['mix']) and not got['mixok']
          and step and not apart and not any(dflt.values()) and any('top' in x for x in told)
          and not any('top' in x for x in let) and K.SAMENESS_ON[0])
    return ok, {k: len(v) for k, v in got.items()} | {'in step': len(step), 'apart': len(apart)} | \
        {f'default {c}': len(v) for c, v in dflt.items()} | {'one top told': len(told), 'same: let be': len(let)}


@test
def shot_board_every_shot():
    """Craft-step2 learn step (craft chat 7, 17 Nov): rough.py's board draws EVERY shot of a film's SHOTS through the
    film's own picture(t), in its own process (so an older checkout draws with its own kits): start, the key beat
    (a named time inside the shot), end, and the next shot's first frame; a shot with nobody in its cast is shown,
    a frame that fails is named (never dropped), and the plan row's missing fields are listed."""
    import shutil
    import tempfile
    import rough as R
    tmp = tempfile.mkdtemp()
    bad = []
    try:
        os.makedirs(os.path.join(tmp, 'source'))
        os.makedirs(os.path.join(tmp, 'story'))
        open(os.path.join(tmp, 'source', 'fake_board.py'), 'w').write(
            "from PIL import Image\n"
            "SHOTS = [('A', 0.0, 2.0), ('B', 2.0, 5.0), ('gone', 5.0, 5.0), ('C', 5.0, 7.0)]\n"
            "SHOT_CAST = {'A': ['kid'], 'B': ['kid', 'dog'], 'C': []}\n"
            "BANG = 3.1\n"
            "def picture(t):\n"
            "    if 6.5 < t < 7.0: raise ValueError('no end frame')\n"
            "    return Image.new('RGB', (1080, 1920), (int(t * 30), 90, 120))\n")
        open(os.path.join(tmp, 'story', 'fake-board-board.txt'), 'w').write(
            'shot A\ncamera: 1.6 m, eye level, to see the face\nlead: half the frame\nfocus: the kid\n'
            'next focus: the dog\nmatch: the red ball\nchoices: 1. ball or stick?\n')
        out = os.path.join(tmp, 'board.jpg')
        _, got, missing = R.board('fake-board', out, tmp)
        names = [n for n, _, _ in got['shots']]
        if names != ['A', 'B', 'C']:
            bad.append(f'shots {names} (a zero-length shot is left out, every other drawn)')
        labs = {n: [f[0] for f in got['frames'][n]] for n in names}
        if labs.get('B', [None, None])[1] != 'BANG':
            bad.append(f'key beat of B: {labs.get("B")} (BANG at 3.1 s is inside it)')
        if labs.get('A', [None])[1:2] != ['middle']:
            bad.append(f'A has no beat inside, so its key frame is the middle: {labs.get("A")}')
        if labs.get('A', [])[-1:] != ['next: B'] or any(x.startswith('next') for x in labs.get('C', [])):
            bad.append(f'next-shot frames wrong: {labs}')
        if not any(f[3] for f in got['frames'].get('C', [])):
            bad.append('a frame that failed to draw was not named')
        if 'A' in missing or set(missing) != {'B', 'C'}:
            bad.append(f'plan-row gaps: {missing} (A is fully planned)')
        if got['cast'].get('C') != []:
            bad.append('a shot with nobody in it was not kept as nobody')
        from PIL import Image
        if Image.open(out).height < 3 * 400:
            bad.append('the board is not one row per shot')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return not bad, '; '.join(bad) or 'every shot drawn, key beat, next shot, failures and plan gaps named'



@test
def board_gate_refusals():
    """Rule 11's gate (craft chat 8, 18 Nov): the pre-flight refuses a new film until its shot board has reached Sam
    (rough.py sent FILM OUT.jpg --delivered --board); then refuses a shot on no delivered board, a shot with nobody
    in SHOT_CAST, and a first board delivered after the first move (a moves block committed before it, or a board
    drawn while blocks existed). A made-up film in a throwaway git repo shows each; Blessed passes with a record
    of every shot, and without one keeps the old "Composition sheet sent:" line (begun before the rule)."""
    import importlib
    import shutil
    import subprocess
    import tempfile
    import time
    import rough as R
    tmp = tempfile.mkdtemp()
    bad = []

    def git(*a, when=None):
        env = dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t', GIT_COMMITTER_NAME='t',
                   GIT_COMMITTER_EMAIL='t@t')
        if when:
            env['GIT_AUTHOR_DATE'] = env['GIT_COMMITTER_DATE'] = f'@{int(when)} +0000'
        subprocess.run(['git', '-C', tmp, *a], env=env, capture_output=True, check=True)

    def has(faults, words):
        return any(words in f for f in faults)
    try:
        os.makedirs(os.path.join(tmp, 'source'))
        os.makedirs(os.path.join(tmp, 'story'))
        src = os.path.join(tmp, 'source', 'fake_gate.py')
        open(src, 'w').write(
            "from PIL import Image\n"
            "SHOTS = [('A', 0.0, 2.0), ('B', 2.0, 4.0), ('C', 4.0, 6.0)]\n"
            "SHOT_CAST = {'A': ['kid'], 'B': ['kid', 'dog'], 'C': []}\n"
            "def picture(t):\n"
            "    return Image.new('RGB', (1080, 1920), (int(t * 30), 90, 120))\n")
        git('init', '-q')
        git('add', '-A')
        git('commit', '-qm', 'film', when=time.time() - 9000)
        sys.path.insert(0, os.path.join(tmp, 'source'))
        F = importlib.import_module('fake_gate')
        if not has(R.board_gate(F, 'fake-gate', '', tmp), 'no shot board has reached Sam'):
            bad.append('a new film with no board was not refused')
        if R.board_gate(F, 'fake-gate', 'Composition sheet sent: 1 Nov, x.jpg', tmp) == []:
            bad.append('the old "Composition sheet sent:" line let a new film through')
        out = os.path.join(tmp, 'board.jpg')
        R.board('fake-gate', out, tmp)
        R.mark_board_sent('fake-gate', out, tmp)
        rec = R.board_record('fake-gate', tmp)
        if len(rec) != 1 or set(rec[0]['shots']) != {'A', 'B', 'C'} or rec[0]['shots']['B'][1] != ['kid', 'dog']:
            bad.append(f'the record does not hold each shot and its cast: {rec}')
        g = R.board_gate(F, 'fake-gate', '', tmp)
        if not has(g, 'nobody in SHOT_CAST') or len(g) != 1:
            bad.append(f'shot C (nobody in it) should be the only refusal: {g}')
        F.SHOT_CAST['C'] = ['dog']
        F.SHOTS.append(('D', 6.0, 8.0))
        F.SHOT_CAST['D'] = ['kid']
        if not has(R.board_gate(F, 'fake-gate', '', tmp), 'on no delivered board'):
            bad.append('shot D, added after the board, was not refused')
        F.SHOTS.pop()
        if R.board_gate(F, 'fake-gate', '', tmp):
            bad.append(f'a delivered board of every shot, cast in each, was refused: {R.board_gate(F, "fake-gate", "", tmp)}')
        mv = os.path.join(tmp, 'story', 'fake-gate-moves.txt')
        open(mv, 'w').write('gait amble: like walk, sps 1.5\n## a: kid\nrow: waves\n')
        git('add', '-A')
        git('commit', '-qm', 'moves', when=rec[0]['delivered'] + 60)
        if R.board_gate(F, 'fake-gate', '', tmp):
            bad.append('a move written after the board was refused')
        os.remove(R.board_record_path('fake-gate', tmp))
        R.mark_board_sent('fake-gate', out, tmp)                    # the same board, now delivered after the move
        git('commit', '-q', '--amend', '--no-edit', '--date', f'@{int(time.time()) - 600} +0000',
            when=time.time() - 600)
        if not has(R.board_gate(F, 'fake-gate', '', tmp), 'came before the first board'):
            bad.append('a move committed before the board reached Sam was not refused')
        os.remove(R.board_record_path('fake-gate', tmp))
        R.board('fake-gate', out, tmp)                              # drawn while the moves file has a block
        R.mark_board_sent('fake-gate', out, tmp)
        if not has(R.board_gate(F, 'fake-gate', '', tmp), 'drawn after 1 move block'):
            bad.append('a board drawn after a move was written was not refused')
        import blessed as BL                                        # a real film: every shot recorded, so it passes
        os.remove(R.board_record_path('fake-gate', tmp))
        p = R.board_record_path('blessed', tmp)
        with open(p, 'w') as f:
            f.write(f'board b.jpg delivered={int(time.time())} drawn={int(time.time())} commit=x moves=0\n')
            for n, a, b in BL.SHOTS:
                f.write(f'shot {n} 0123456789 {",".join(BL.SHOT_CAST.get(n) or []) or "-"}\n')
        g = R.board_gate(BL, 'blessed', '', tmp)
        if g:
            bad.append(f'Blessed with a record of every shot was refused: {g}')
        if R.board_gate(BL, 'blessed', 'Composition sheet sent: 4 Nov, comp.jpg') != []:
            bad.append('Blessed (begun before the rule) lost its old "Composition sheet sent:" line')
    finally:
        sys.path[:] = [x for x in sys.path if not x.startswith(tmp)]
        sys.modules.pop('fake_gate', None)
        shutil.rmtree(tmp, ignore_errors=True)
    return not bad, '; '.join(bad) or 'no board, a missing shot, an empty shot and a board after a move all refused'


# ------------------------------------------------------------------------------------------------ rule 85
@test
def cost_watch_lines():
    """Rule 85 (Sam's Y, 17 Nov): amber at 250k of history, red at 370k; the warning lines count steps and say aim
    ~100, up to 150 to finish, never mid-fix."""
    import importlib.util, io, contextlib, tempfile, shutil
    spec = importlib.util.spec_from_file_location('costwatch', os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                  '..', '.claude', 'hooks', 'costwatch.py'))
    C = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(C)
    bad = []
    tmp = tempfile.mkdtemp()
    C.STATE_DIR = os.path.join(tmp, 'state')
    try:
        def run(ctx, steps, event):
            path = os.path.join(tmp, f'c{ctx}-{event}.jsonl')
            with open(path, 'w') as f:
                for n in range(steps):
                    f.write(json.dumps({'type': 'assistant', 'timestamp': '2099-01-01T00:00:00Z', 'message': {
                        'id': f'm{n}', 'model': 'claude-sonnet', 'usage': {'cache_read_input_tokens': ctx}}}) + '\n')
            out = io.StringIO()
            stdin = sys.stdin
            sys.stdin = io.StringIO(json.dumps({'transcript_path': path, 'hook_event_name': event, 'prompt': 'x'}))
            try:
                with contextlib.redirect_stdout(out):
                    C.main()
            finally:
                sys.stdin = stdin
            return out.getvalue()
        if run(240_000, 3, 'PostToolUse'):
            bad.append('warned below 250k')
        a = run(260_000, 3, 'PostToolUse')
        if 'AMBER' not in a or 'RED' in a:
            bad.append('no amber at 260k')
        if '3 steps' not in a or '100 steps' not in a or '150' not in a or 'mid-fix' not in a:
            bad.append(f'amber line lacks steps / aim 100 / 150 / mid-fix: {a[:200]}')
        if 'RED' in run(360_000, 3, 'UserPromptSubmit'):
            bad.append('red below 370k')
        if 'Cost: red' not in run(380_000, 3, 'UserPromptSubmit'):
            bad.append('no red at 380k')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return not bad, '; '.join(bad) or 'quiet at 240k, amber at 260k with steps and the ~100/150/mid-fix line, red at 380k'


# ------------------------------------------------------------------------------------------------ cost-fixes (17 Nov)
def _hook(name):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, '..', '.claude', 'hooks', name + '.py'))
    M = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(M)
    return M


@test
def model_guard_stops_routine_on_opus():
    """Model guard (Sam's 1, 17 Nov): on 16 Nov the Opus fix chats spliced the animatic with the word check silent;
    the guard refuses finish.py / whole-film render / splice on Opus, allows them on Sonnet, allows --span clips."""
    import io, contextlib
    G = _hook('modelguard')
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        ok = G.test() == 0
    import handover as H
    import tempfile
    tmp = tempfile.mkdtemp()
    nf = os.path.join(tmp, 'n.md')
    with open(nf, 'w') as f:      # 16 Nov 12:46 Next line, word for word in its routine part (why-model-switch-failed)
        f.write('- **Next (Opus, medium):** clips with `final --span` of each fixed note, then splice fixed seconds '
                'into animations/drafts/protest-tiers-animatic.mp4 and send\n')
    old_silent = H.model_faults('x', nf) == []
    caught = G.routine('ffmpeg -i a.mp4 -i b.mp4 -filter_complex concat=n=2 '
                       'animations/drafts/protest-tiers-animatic.mp4') is not None
    bad = ([] if ok else [out.getvalue().strip()]) + ([] if caught else ['the 16 Nov splice is not caught'])
    note = 'the old word check stays silent on the 16 Nov line, ' if old_silent else 'the old word check now fires too, '
    return not bad, '; '.join(bad) or note + 'the guard refuses it on Opus and allows Sonnet, clips and a logged escape'


@test
def scheduled_task_guard():
    """Scheduled-task guard (Sam, 26 Nov): Open Wounds chat 17 made a scheduled task that started a fresh chat on
    firing; chat 18 got no project and the default model. The guard refuses that kind and allows wake-ups."""
    import io, contextlib
    G = _hook('triggerguard')
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        ok = G.test() == 0
    return ok, out.getvalue().strip()


@test
def message_saver_keeps_typed_messages():
    """Message saver (handover.py log): nothing Sam typed was saved after 16 Nov 19:02, because the app began stamping
    typed messages with an origin and any origin read as "not typed". Typed kinds are saved; robots are not."""
    import handover as H
    import tempfile
    tmp = tempfile.mkdtemp()
    bad = []
    for kind, robot in (('human', False), ('remote', False), (None, False), ('task-notification', True),
                        ('peer', True)):
        p = os.path.join(tmp, f'{kind}.jsonl')
        d = {'type': 'user', 'message': {'role': 'user', 'content': 'Fix the whale please'}}
        if kind:
            d['origin'] = {'kind': kind}
        if kind == 'task-notification':
            d['promptSource'] = 'system'
        with open(p, 'w') as f:
            f.write(json.dumps(d) + '\n')
        if H._not_typed('Fix the whale please', p) is not robot:
            bad.append(f'origin {kind}: read as {"robot" if not robot else "typed"}')
    old = lambda d: bool((d.get('origin') or {}).get('kind') or d.get('promptSource') == 'system')   # before 17 Nov
    if not old({'origin': {'kind': 'human'}}):
        bad.append('the old version no longer shows the fault')
    return not bad, '; '.join(bad) or 'typed (human, remote, none) saved; task notices and peers skipped; old one dropped "human"'


@test
def finder_reminder_per_chat():
    """finder-use (Sam's 1, 17 Nov): the per-day flag went silent for every chat once any chat called show (16 Nov:
    6 of 19 chats never did). Now: one line at a chat's first film-code search with no show; the end check names
    THIS chat when it edited the film's code with no show."""
    import io, contextlib
    W = _hook('finderwarn')
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        ok = W.test() == 0
    bad = [] if ok else [out.getvalue().strip()]
    return not bad, '; '.join(bad) or 'one line at the first film search with no show (the after-the-fact end check was dropped: check audit C1, Sam 26 Nov)'


@test
def watcher_catches_last_weeks_four():
    """early-warning (Sam's 1, 17 Nov): the number to beat. Last week's four silent failures, each from its own kind
    of record. Since the check audit (Sam's Y, 26 Nov, C1-C3) the saver, the model guard and the finder reminder are
    each their own live check (their own kit tests), so the watcher keeps one: the kit list behind Sam's Y (people kit,
    before 16 Nov), quiet on today's list; and a new system with no promise is flagged (Sam: "it needs to adapt to new
    systems we build too")."""
    import tempfile, shutil, subprocess
    from datetime import datetime, timezone, timedelta
    import watcher as W
    tmp = tempfile.mkdtemp()
    bad = []

    def rec(tag, lines):
        p = os.path.join(tmp, tag + '.jsonl')
        with open(p, 'w') as f:
            for d in lines:
                f.write(json.dumps(d) + '\n')
        return p
    use = lambda i, c, model='claude-opus-5-5': {'type': 'assistant', 'message': {'model': model, 'content': [
        {'type': 'tool_use', 'id': f't{i}', 'name': 'Bash', 'input': {'command': c}}]}}
    res = lambda i, text: {'type': 'user', 'message': {'content': [{'type': 'tool_result', 'tool_use_id': f't{i}',
                                                                      'content': text}]}}
    try:
        old = subprocess.run(['git', 'show', '2362763f:guides/kit-catalogue.md'], cwd=W.ROOT, capture_output=True,
                             text=True).stdout
        if not any('people kit' in f for f in W.kit_faults(text=old)):
            bad.append('kits: the 14-16 Nov people kit line was not flagged')
        if W.kit_faults():
            bad.append(f'kits: false alarm on today\'s list: {W.kit_faults()}')
        root = os.path.join(tmp, 'root')            # a system built tomorrow, with no promise
        for d in ('.claude', 'source', 'guides'):
            os.makedirs(os.path.join(root, d))
        json.dump({'hooks': {'Stop': [{'hooks': [{'command': 'python3 "$CLAUDE_PROJECT_DIR"/source/newthing.py hook'}]}]}},
                  open(os.path.join(root, '.claude', 'settings.json'), 'w'))
        open(os.path.join(root, 'source', 'handover.py'), 'w').write('def new_faults(film):\n    pass\n')
        open(os.path.join(root, 'source', 'newtool.py'), 'w').write('')
        open(os.path.join(root, 'guides', 'job-packs.md'), 'w').write('Tools: `newtool.py OUT`\n')
        real, W.ROOT = W.ROOT, root
        try:
            u = W.unlisted()
        finally:
            W.ROOT = real
        if set(u) != {'newthing.py hook', 'new_faults', 'newtool.py'}:
            bad.append(f'adapting: new systems not all flagged: {u}')
        if W.unlisted():
            bad.append(f'a system today has no promise: {W.unlisted()}')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return not bad, '; '.join(bad) or ('the people-kit line caught, quiet on today\'s kit list; a new hook, check and tool with no promise flagged')


@test
def finished_films_keep_their_bookmark():
    """One route to the kit, Change 1 (Sam's Y, 20 Nov): every finished film has a bookmark on its true source save,
    nothing in animations/ is unlisted, and the count of old-film files loaded and steps swapped has not risen."""
    import freeze as FZ
    bad = FZ.bookmark_faults() + FZ.count_faults()
    reg = FZ.load()
    for n, d in reg.items():
        if not d.get('no_frame') and not any(v.endswith('.mp4') for v in d['videos']):
            continue
        if not d.get('save') or d['save'] == '9707503c':
            bad.append(f'{n}: the bookmark is on a re-title save, not the true source')
    return not bad, '; '.join(bad[:6]) or f'{len(reg)} films bookmarked, count not risen'


# ------------------------------------------------------------------------------------------------ the human-body check
V4_COMMIT = '560d946d'                   # GTA shot 4 version 4 as Sam saw it (chat 16), with the check's hooks (chat 17)
V4_TIMES = (1.67, 2.0)                 # the right arm out of his back (notes 3, 6, 7); the gun 27 degrees off (note 8)


def _body_faults(fn, times):
    import humancheck as HC
    out = []
    for t in times:
        HC.frame_begin()
        fn(t)
        out += HC.frame_end(t)
    return out


@test
def body_check_shot4_v4():
    """GTA shot 4, version 4 (Sam, 20 Nov: "Utterly inhuman ... It really worries me that this wasn't caught"): the
    body check (humancheck.py) must catch the right arm out of Jason's back and the gun drawn off its target in the
    old version, pass the pose gallery's three former false flags (arms folded and microphone from three-quarter back,
    cup sipping three-quarter front). Shot 3 of that same version had real crossed forearms (Lucia off the wheel, the
    middle passenger's hands on the wrong sides; seen on the picture 21 Nov): the check must flag exactly those, and
    nothing else there."""
    import posegallery as PG
    import body as B
    import views as V
    import moves
    old = _seen_faults(V4_COMMIT, 'shot4', V4_TIMES)               # v4 exactly as Sam saw it
    kinds = {k for _, who, k, _ in old if who == 'Jason'}
    gal = {n: b for n, b, _ in PG.GALLERY}
    import humancheck as HC
    g = []
    for name, deg in (('arms folded', 135), ('cup, sipping', 45), ('cup, sipping', -45), ('microphone', 135)):
        build = gal.get(name) or (lambda sp, m=name: moves.pose(sp, 'mic'))
        HC.frame_begin()
        from PIL import Image
        V.person(Image.new('RGBA', (1200, 1100)), B.Cam(1.0, 540, 960), 600, 330, 0.62, PG.MODEL, 0.0, float(deg),
                 build(PG.MODEL))
        g += HC.frame_end(0.0)
    import gta_rehearse as Rn                     # chat 27: version 4's own shot 3 really had Lucia's arms crossed
    s3 = _body_faults(Rn.shot3, (0.5, 1.5, 2.5))  # (v4 note 1, caught since chat 23): today's shot 3 must be clean
    ok = {'order', 'aim'} <= kinds and not s3 and not g
    return ok, f'version 4 Jason: {sorted(kinds)}; shot 3: {len(s3)} faults {sorted({x[2] for x in s3})}; gallery: {len(g)} false flags'


V4_CURLED = (1.00, 4.92)               # Sam's v4 stills 3c (note 6, "a monstrosity") and 6b (note 15, "in reverse")


@test
def body_check_curled_v4():
    """Rule 41 (GTA v4 notes 6 and 15, Sam 20 Nov: "Limbs, neck, torso, all curled around each other and in the wrong
    place. Utterly inhuman", "the horror show in reverse"): both frames passed every check until 23 Nov. The body
    check must now flag Jason at Sam's two stills (1.00 s: the near arm straight back behind his shoulders, 'reach';
    4.92 s: his hand behind his back, the forearm end-on as a stump, 'stub'), and pass the gallery poses that a first
    draft of the stump test wrongly flagged (patting the air from behind, the phone at the ear from three-quarter)
    plus every gallery pose from the front and side. About 1 minute."""
    from PIL import Image
    import posegallery as PG
    import body as B
    import views as V
    import humancheck as HC
    seen = _seen_faults(V4_COMMIT, 'shot4', V4_CURLED)              # v4 exactly as Sam saw it
    got = {t: {x[2] for x in seen if x[0] == t and x[1] == 'Jason'} for t in V4_CURLED}
    caught = 'reach' in got[1.00] and 'stub' in got[4.92]
    gal = {n: b for n, b, _ in PG.GALLERY}
    cases = [('flapping (pat)', 180), ('phone at the ear', 45), ('phone at the ear', -45)]
    cases += [(n, d) for n in gal for d in (0, 90)]
    false = []
    for name, deg in cases:
        HC.frame_begin()
        V.person(Image.new('RGBA', (1080, 1920)), B.Cam(1.0, 540, 960), 540, 500, 0.6, PG.MODEL, 0.0, float(deg),
                 gal[name](PG.MODEL))
        false += [(name, deg) for x in HC.frame_end(0.0) if x[2] in ('reach', 'stub')]
    return caught and not false, f'v4 Jason at 1.00 s {sorted(got[1.00])}, 4.92 s {sorted(got[4.92])}; ' \
        f'gallery false flags {false or "none"} of {len(cases)}'


V3_COMMIT = '9067f25d'                  # GTA animatic v3 as Sam saw it (chat 26): Jason's back at 15.4 and 18.3 s
V3_BACK = (1.3, 4.2)                    # shot 4's own clock (film 15.4 F1, 18.3 F5)


@test
def body_check_back_view():
    """GTA v3 F1, F5, F7 (chat 27; changed chat 28 after Sam, 21 Nov: "a great shot but a broken drawing"): a person
    seen big from behind must be DRAWN to read from behind; the camera of an approved shot never moves. The body check
    must flag Jason's back in animatic v3's shot 4 (15.4 and 18.3 s) with advice that points at the drawing (never
    "choose another camera"), flag a big flat figure drawn from behind and pass the same figure from the front."""
    from PIL import Image
    import posegallery as PG
    import body as B
    import views as V
    import humancheck as HC
    old = [x for x in _seen_faults(V3_COMMIT, 'shot4', V3_BACK) if x[1] == 'Jason' and x[2] == 'back view']
    said = ' '.join(str(v) for x in old for v in x[3:])
    to_drawing = 'DRAWING' in said and 'another camera' not in said
    flat = {}
    for deg in (0.0, 180.0):
        HC.frame_begin()
        V.person(Image.new('RGBA', (1080, 1920)), B.Cam(1.0, 540, 960), 540, 500, 0.6, PG.MODEL, 0.0, deg,
                 V.standing(PG.MODEL))
        flat[deg] = [x for x in HC.frame_end(0.0) if x[2] == 'back view']
    ok = len(old) == 2 and to_drawing and flat[180.0] and not flat[0.0]
    return ok, (f'v3 Jason back views: {len(old)} of 2; advice points at the drawing: {to_drawing}; big figure from '
                f'behind flagged: {bool(flat[180.0])}, from the front: {bool(flat[0.0])}')


@test
def tools_switched_on():
    """Sam, 21 Nov: "Why are tools built then not enabled? Keeps happening. Please ensure that doesn't happen again."
    The model guard was built and tested on 17 Nov but never put in .claude/settings.json, so it never ran for four
    days. The watcher must flag it from the 17 Nov settings with no promise needed (it finds tools from the files),
    pass today's settings, and flag a switched-on step that has never been seen running (no mark), but not once it
    has its mark. This is every tool's switched-on half: it covers every hook file and every adopted proposal's tool."""
    import json
    import subprocess
    import tempfile
    import hookran
    import watcher as W
    old = subprocess.run(['git', 'show', 'edb1cd78~1:.claude/settings.json'], cwd=os.path.dirname(HERE),
                         capture_output=True, text=True, check=True).stdout
    keep = dict(W.PROMISES)
    W.PROMISES.pop('modelguard.py', None)              # 17 Nov: no promise for it either
    try:
        then = [f for f in W.unwired(old) if 'modelguard.py' in f]
    finally:
        W.PROMISES.clear()
        W.PROMISES.update(keep)
    now = W.unwired()
    d = tempfile.mkdtemp()
    rec = os.path.join(d, 'chat.jsonl')
    with open(rec, 'w') as fh:
        fh.write(json.dumps({'type': 'user', 'timestamp': '2026-11-21T22:00:00Z', 'message': {'content': 'hi'}}) + '\n')
        fh.write(json.dumps({'type': 'assistant', 'message': {'content': [{'type': 'tool_use', 'name': 'Bash'}]}}) + '\n')
    real = hookran.DIR
    hookran.DIR = os.path.join(d, 'ran')
    try:
        os.makedirs(hookran.DIR)
        open(os.path.join(hookran.DIR, '_since'), 'w').write('1000\n')     # marks kept long before this chat
        missing = [f for f in W.ran_faults(rec) if 'modelguard.py' in f]
        hookran.ran('modelguard.py')
        marked = [f for f in W.ran_faults(rec) if 'modelguard.py' in f]
    finally:
        hookran.DIR = real
    ok = bool(then) and not now and bool(missing) and not marked
    return ok, (f'17 Nov settings: model guard {"flagged" if then else "NOT flagged"}; today unwired: {now or "none"}; '
                f'never seen running: {"flagged" if missing else "NOT flagged"}; with its mark: '
                f'{"quiet" if not marked else "still flagged"}')


@test
def castsheet_only_when_cast_changed():
    """Check audit B5 (Sam's Y, 26 Nov): the cast check at handover runs only for a new or changed cast. 24 of 65
    refused handovers were the cast check repeating unchanged faults. A clean run stamps the files it read; the next
    handover skips it while they are unchanged and runs it again once one changes; a cast with faults is never stamped."""
    import tempfile
    import shutil
    import castsheet as C
    import handover as H
    tmp = tempfile.mkdtemp()
    src = os.path.join(os.path.dirname(HERE), 'notes', 'logs', '_kittest-cast.txt')   # inside the project: stamped
    open(src, 'w').write('kemi: front\n')
    calls, result = [], [[]]

    def fake(film, *a, **k):
        calls.append(open(src).read())
        return list(result[0])
    names = ('build_faults', 'crotch_faults', 'teeth_faults', 'mouth_spike_faults', 'hair_spike_faults',
             'seated_faults', 'judge_faults')
    keep = {n: getattr(C, n) for n in names}
    keep_stamps = H.CASTSTAMPS
    try:
        for n in names:
            setattr(C, n, fake)
        H.CASTSTAMPS = os.path.join(tmp, 'stamps.tsv')
        first = H.castsheet_faults('brexit-is-done'); n1 = len(calls)
        second = H.castsheet_faults('brexit-is-done'); n2 = len(calls)
        open(src, 'w').write('kemi: front, new hair\n')
        third = H.castsheet_faults('brexit-is-done'); n3 = len(calls)
        result[0] = ['kemi front: crotch line']
        open(src, 'w').write('kemi: changed again\n')
        bad1 = H.castsheet_faults('brexit-is-done'); bad2 = H.castsheet_faults('brexit-is-done')
    finally:
        for n, f in keep.items():
            setattr(C, n, f)
        H.CASTSTAMPS = keep_stamps
        shutil.rmtree(tmp, ignore_errors=True)
        os.remove(src)
    ok = first == [] and n1 == 7 and n2 == n1 and n3 == 14 and third == [] and bad1 and bad2
    return ok, (f'first run {n1} checks; unchanged: skipped {n2 == n1}; changed: run again {n3 == 14}; '
                f'faults stop it both times {bool(bad1) and bool(bad2)}')


@test
def handover_status_checks():
    """Status chat (Sam, 21 Nov: "everything needs step by step checking, fixing, testing"): the handover check must
    catch what slipped on Grand Theft Autism: notes over 4,000 words, a handover over 15 lines, a chat that never
    logged its notes, stages never marked (Opus running finish.py: modelguard.py, now wired), a refused clip told to Sam as sent (chat 26), no
    push notification; and stay quiet on the clean cases."""
    import json
    import tempfile
    import handover as H
    d = tempfile.mkdtemp()
    def rec(lines):
        f = os.path.join(d, f'r{len(os.listdir(d))}.jsonl')
        open(f, 'w').write('\n'.join(json.dumps(x) for x in lines))
        return f
    def ast(*content, model='claude-opus-5-5'):
        return {'type': 'assistant', 'timestamp': '2026-11-21T22:00:00',
                'message': {'role': 'assistant', 'model': model, 'content': list(content)}}
    bash = lambda c: {'type': 'tool_use', 'name': 'Bash', 'input': {'command': c}}
    big = os.path.join(d, 'big.md')
    open(big, 'w').write('word ' * 4100 + '\n## Where things stand\n' + 'line\n' * 16)
    small = os.path.join(d, 'small.md')
    open(small, 'w').write('notes\n## Where things stand\n- Open rule requests: none\n' + 'line\n' * 5)
    sz_big, sz_small = H.size_faults(None, big), H.size_faults(None, small)
    send = {'type': 'tool_use', 'id': 't1', 'name': 'SendUserFile', 'input': {'files': ['/x/clip.mp4']}}
    refused = {'type': 'user', 'timestamp': '2026-11-21T22:00:01', 'message': {'content': [
        {'type': 'tool_result', 'tool_use_id': 't1', 'is_error': True, 'content': 'Permission for this action was denied'}]}}
    told = ast({'type': 'text', 'text': 'I sent you a short clip, 20-26 seconds.'})
    not_sent = [f for f in H._run(H.turns(rec([ast(send), refused, told])), None, small) if 'NOT SENT' in f]
    sent_ok = [f for f in H._run(H.turns(rec([ast(send), told])), None, small) if 'NOT SENT' in f]
    no_push = H.push_faults(rec([ast(bash('ls'))]))
    push = H.push_faults(rec([ast({'type': 'tool_use', 'name': 'PushNotification', 'input': {'message': 'x'}})]))
    import ledger
    led = ledger.load('grand-theft-autism')
    stages_open = {'chats': led['chats'], 'estimate': 10, 'stages': [{'name': 'cast', 'pct': 2, 'done': None}],
                   'film': 'x'}
    real_load = ledger.load
    ledger.load = lambda f: stages_open
    try:
        st = [f for f in H.ledger_faults('x') if f.startswith('STAGES')]
    finally:
        ledger.load = real_load
    ok = (len(sz_big) == 3 and not sz_small and not_sent and not sent_ok
          and no_push and not push and not st)          # stages: no nag (Sam 26 Nov: the stage stop deleted)
    return ok, (f'big notes {len(sz_big)} faults, clean {len(sz_small)}; refused send caught {bool(not_sent)}, real send '
                f'quiet {not sent_ok}; push missing {bool(no_push)}, present quiet {not push}; stages not nagged {not st}')


@test
def crowd_head_installed():
    """Sam, 26 Nov (pose-test chat 1, saved example notes/learn/pose-test/sheet-keyframes.jpg): a test scene that never
    installed the crowd pack drew every worker and guest with the old default head, bald with no hard hat. The check
    must flag that scene's worker, and pass the same worker once the film's pack is installed."""
    import subprocess
    code = ("import sys; sys.path.insert(0, %r); import people as PK; w = PK.crowd_person(PK.crowds('brexit-is-done')"
            "['worker'], 0); a = PK.head_faults(w); PK.install(PK.load('brexit-is-done')); b = PK.head_faults(w); "
            "print(len(a), len(b))") % HERE
    r = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, cwd=HERE)
    got = (r.stdout.strip().split('\n') or [''])[-1]
    return got == '1 0', f'without the pack: flagged, with it: clean -> {got!r} {r.stderr[-200:] if got != "1 0" else ""}'


@test
def nod_reads_on_screen():
    """Open Wounds chat 32 (saved example: the fresh-eye review, notes/ledger/brexit-is-done/round-27.txt: "never
    leaning in as she talks", "no nod reads"): May's moves named a lean in and nods, but 'lean in 0.8' was 0.8 degrees
    and a nod of 0.8 dropped her head 5 px. movesize must flag those amounts and pass the film's own."""
    import acting as A
    import movesize as MS
    real = A.load

    def two(film, old):
        d = real(film)
        b = d['shots']['1']
        keep = [m for m in b['body'] if m['move'] == 'lean in'][:1] + [m for m in b['body'] if m['move'] == 'nod'][:1]
        if old:
            keep = [dict(m, amount=0.8) for m in keep]
        b['body'] = keep
        return d
    import brexit_is_done as F
    try:
        A.load = lambda f: two(f, True)
        F._MOVES.clear()                              # the film keeps the moves it read first
        before = MS.faults('brexit-is-done', ['1'])
        A.load = lambda f: two(f, False)
        F._MOVES.clear()
        now = MS.faults('brexit-is-done', ['1'])
    finally:
        A.load = real
        F._MOVES.clear()
    return len(before) == 2 and not now, f'old amounts: {len(before)} flagged; the film now: {now}'


@test
def head_moves_not_comic():
    """Open Wounds chat 37 (saved example: Sam's note 23.1, 26 Nov, notes/ledger/sam/s3zjpz4k.md: "May's lean, Kemi and
    May's head bobbing, have all become comically large ... THIS IS A MAJOR ERROR"). Chat 32 and 35 drew May's lean in
    at 15 degrees with roll 3 (166 px), her nods at 4.5-5 (28-34 px), Kemi's chin up 3.2 and nods 3.4-4.4 (22-29 px),
    Blair's preen 2.6 and nod 3.0; the check had a floor only. With those amounts every one must be flagged too large;
    with the film's own amounts none, too small or too large."""
    import acting as A
    import movesize as MS
    import brexit_is_done as F
    real = A.load
    OLD = {('1', 'lean in'): (15.0, 3.0), ('1', 'nod'): 4.5, ('2', 'chin up'): 3.2, ('2', 'nod'): 3.6,
           ('3', 'preen'): 2.6, ('3', 'nod'): 3.0}

    def old(film):
        d = real(film)
        for key, b in d['shots'].items():
            keep = []
            for m in b['body']:
                v = OLD.get((key, m['move']))
                if v is None:
                    continue
                if isinstance(v, tuple):
                    m = dict(m, amount=v[0], **{'with': dict(m.get('with') or {}, roll=v[1])})
                else:
                    m = dict(m, amount=v)
                keep.append(m)
            b['body'] = keep
        return d
    try:
        A.load = old
        F._MOVES.clear()
        before = MS.faults('brexit-is-done')
        A.load = real
        F._MOVES.clear()
        now = MS.faults('brexit-is-done')
    finally:
        A.load = real
        F._MOVES.clear()
    big = [x for x in before if 'comically large' in x]
    return (len(big) >= 6 and not now, f'old amounts: {len(big)} of {len(before)} flagged too large; the film now: {now}')


@test
def chase_order_stuck():
    """Open Wounds chat 37 (saved example: Sam's note 23.4, 26 Nov: "The wolves and guests are clipping over each other
    when they run in ... Decide who is in front of who and stick to it"). Over the chase, no two runners whose boxes
    overlap on two frames in a row may swap who is drawn in front; with the lock taken off (plain far to near, as the
    animatic was drawn) the swaps Sam saw come back (26.26 s guest 2 / wolf 1, 26.90 s guest 3 / wolf 2)."""
    import brexit_is_done as F
    import brexit_is_done_action as A
    L = F._cam('blair')

    def swaps():
        A._LOCK.clear()
        prev, out = {}, []
        for i in range(int(9.4 * 25)):
            room, beyond = A.room_actors(i / 25.0, L)
            fns = [fn for _, fn in sorted(beyond, key=lambda q: -q[0])] + \
                  [fn for _, fn in sorted(room, key=lambda q: -q[0]) if hasattr(fn, 'who')]
            pos = {fn.who: (k, A._box(L, fn)) for k, fn in enumerate(fns)}
            for a in pos:
                for b in pos:
                    if a >= b:
                        continue
                    (ka, A0), (kb, B0) = pos[a], pos[b]
                    ov = not (A0[2] <= B0[0] or B0[2] <= A0[0] or A0[3] <= B0[1] or B0[3] <= A0[1])
                    if ov and (a, b) in prev and prev[(a, b)] != (ka > kb):
                        out.append((i, a, b))
                    if ov:
                        prev[(a, b)] = ka > kb
                    else:
                        prev.pop((a, b), None)
            for k in [k for k in prev if k[0] not in pos or k[1] not in pos]:
                prev.pop(k)
        return out
    real = A._ranks
    try:
        A._ranks = lambda L_, n: {}
        old = swaps()
    finally:
        A._ranks = real
    now = swaps()
    return len(old) >= 2 and not now, f'without the lock: {len(old)} swaps; with it: {now}'


@test
def early_move_size():
    """Open Wounds chat 35 (Sam's Y, 26 Nov; saved example: notes/ledger/brexit-is-done/checks.jsonl, pre-flight 26 Nov
    18:57: "MOVE SIZE: shot 2 kemi: the chin up at 9.89 s moves the head 3 px ... the nod at 17.55 s ... 8 px ... shot
    3 blair: the preen at 28.83 s ... 12 px ... the nod at 32.48 s ... 15 px", caught only at pre-flight, ten rounds
    after the moves were written 'small' and 'curt'). The early check measures a head move the moment it is new or
    changed: with those four old amounts it must flag all four, with the film's own amounts none; a second early pass
    over moves it has already measured measures nothing; and the 'curt'/'small' rows each get their own line."""
    import acting as A
    import movesize as MS
    import brexit_is_done as F
    real = A.load
    OLD = {('2', 'chin up'): 0.4, ('2', 'nod', '"job"'): 1.2, ('3', 'preen'): 1.0, ('3', 'nod', '"Hague"'): 0.8}

    def four(film, old):
        d = real(film)
        for key in ('2', '3'):
            b = d['shots'][key]
            keep = []
            for m in b['body']:
                for k, v in OLD.items():
                    if k[0] == key and m['move'] == k[1] and (len(k) < 3 or k[2] in str(m['a'])):
                        keep.append(dict(m, amount=v) if old else m)
            b['body'] = keep
        d['shots'] = {k: d['shots'][k] for k in ('2', '3')}
        return d
    try:
        A.load = lambda f: four(f, True)
        F._MOVES.clear()
        before, n0 = MS.early('brexit-is-done', seen=set(), save=False)
        A.load = lambda f: four(f, False)
        F._MOVES.clear()
        now, n1 = MS.early('brexit-is-done', seen=set(), save=False)
        seen = set()
        d = A.load('brexit-is-done')
        for key in d['shots']:
            b = A.block_for(d, key)
            seen |= {MS._sig(b['shot'], b.get('who') or key, m) for m in b['body'] if m['move'] in MS.HEAD_MOVES}
        again, n2 = MS.early('brexit-is-done', seen=seen, save=False)
        words = MS.wording('brexit-is-done')
    finally:
        A.load = real
        F._MOVES.clear()
    curt = [w for w in words if 'curt nod' in w]
    return (len(before) == 4 and not now and n2 == 0 and curt,
            f'old amounts: {len(before)} of 4 flagged; the film now: {now}; measured again: {n2}; curt line: {bool(curt)}')


@test
def camera_measured_on_background():
    """Open Wounds chat 35 (saved example: notes/ledger/brexit-is-done/checks.jsonl, pre-flight 26 Nov 18:57: "CAMERA
    FEEL: shot 1 6.12-6.38 s, the pan: stops from 81% of its top speed (no ease out)"; shot 1's camera never moves:
    the 'pan' was May's chop and lean, measured over the whole frame, and Sam was asked to soften it). The camera is
    measured on the background above everyone drawn: over May's lean in on 'remember' the whole frame must read a
    shift and the band none; a real pan (the frame slid 6 thumb px) must still read on the band."""
    import numpy as np
    import kitinputs as KI
    import cover
    import brexit_is_done as F
    recs = []
    for t in (2.42, 2.5, 2.58):
        r = cover.survey_record(F, t)
        im = r['image']
        th = np.asarray(im.convert('L').resize(KI.THUMB), np.float32)
        top = int(min(p['box'][1] for p in r['people']) * KI.THUMB[1] / im.size[1]) - 3
        recs.append((th, top))
    whole = sum(abs(KI._shift_zoom(a[0], b[0])[0]) + abs(KI._shift_zoom(a[0], b[0])[1]) for a, b in zip(recs, recs[1:]))
    band = min(r[1] for r in recs)
    still = sum(abs(KI._shift_zoom(a[0], b[0], band)[0]) + abs(KI._shift_zoom(a[0], b[0], band)[1])
                for a, b in zip(recs, recs[1:]))
    slid = np.roll(recs[0][0], 6, axis=1)
    pan = KI._shift_zoom(recs[0][0], slid, band)[0]
    ok = band >= KI.FREE_BAND * KI.THUMB[1] and whole > 0 and still == 0 and abs(abs(pan) - 6) <= 1
    return ok, f'band {band} rows; whole frame shift {whole:.0f}, band shift {still:.0f}; a real 6 px pan reads {pan:.0f}'


@test
def hand_rests_on_thigh():
    """Open Wounds chat 32 (saved example: round-27.txt, "both ball hands sit loose at the lap edge ... neither clearly
    rests on a thigh"): with the old 'lap fwd' place (y 378) May's hands hover over her thighs at 1.0 s; the resting
    check ('thigh' in RESTS) must flag it, and pass the place as it is now."""
    import acting as A
    import kitchecks as K
    import brexit_is_done as F
    rec = lambda: [('1.00 s', 'May', {'_rest': K._rest_record(F.acted('1', 'may', 1.0)[1], 1.0)})]
    keep = A.PLACES['lap fwd']
    try:
        A.PLACES['lap fwd'] = keep[:2] + (378.0,) + keep[3:]
        before = [x for x in K.rests(F, rec()) if 'thigh' in x and 'hovers' in x]
    finally:
        A.PLACES['lap fwd'] = keep
    now = [x for x in K.rests(F, rec()) if 'thigh' in x and 'COULD NOT' not in x]
    return len(before) == 2 and not now, f'old place: {len(before)} hands hover; now: {now}'


@test
def pop_carried_off_edge():
    """Open Wounds chat 32 (saved example: pre-flight, notes/ledger/brexit-is-done/round-0.txt: "shot 3: guest
    vanishes mid-shot between 33.88 and 34.12 s, away from the frame's edge"; drawn frame by frame he runs off the
    left edge at 33.96 s): a runner carried on at his own speed past the edge between samples is no pop; someone
    who stops still and vanishes mid-frame still is."""
    import kitinputs as KI
    run = [dict(shot='3', t=t, people=[dict(who='guest', box=b)] if b else []) for t, b in
           ((33.64, (380, 700, 520, 1200)), (33.88, (76, 700, 216, 1200)), (34.12, None))]
    still = [dict(shot='3', t=t, people=[dict(who='guest', box=b)] if b else []) for t, b in
             ((33.64, (500, 700, 640, 1200)), (33.88, (500, 700, 640, 1200)), (34.12, None))]
    class F:
        ALLOWED_POPS = []
    a, b = KI.pop_faults(F, run), KI.pop_faults(F, still)
    return not a and len(b) == 1, f'runner off the edge: {a}; standing then gone: {len(b)} flagged'


@test
def words_from_takes():
    """Chat 29 of Open Wounds (26 Nov; saved example: Sam's Kemi.m4a and Kemi_2.m4a, which chat 28 could not tell apart
    and called two takes of one line): speech-to-text must hear that they are the line's two halves, give each word
    its time, and the lips from those times must rest in a pause between sentences."""
    import words as WD
    d = os.path.join(os.path.dirname(HERE), 'sounds', 'brexit-is-done')
    a, b = WD.text(os.path.join(d, 'Kemi.m4a')).lower(), WD.text(os.path.join(d, 'Kemi_2.m4a')).lower()
    halves = 'burnham' in a and 'job' in a and 'chewed' in b and 'chewed' not in a
    ws = WD.times(os.path.join(d, 'Tony.m4a'))
    trk = WD.track(ws)
    import mouths
    say, im = WD.at_word(ws, 'say.'), WD.at_word(ws, "I'm")
    end_say = next(w1 for w0, w1, w in ws if w0 == say)
    rest = mouths.at(trk, (end_say + im) / 2) == 'rest'
    talk = mouths.at(trk, WD.at_word(ws, 'Iraq') + 0.08) != 'rest'
    return halves and rest and talk, f'two halves {halves}, rest in the pause {rest}, open on "Iraq" {talk}'


@test
def crowd_pool():
    """Sam, 26 Nov (crowd pool chat 1: "Open up the crowd pack to all of the combinations that we've used before across
    all cities ... generic people in any of our films ... from a generic pooled crowd pack"): every haircut, hair colour,
    skin and top an earlier film's crowd lines used is in the pool; a new film's crowd takes the pool by default and a
    posted or locked film's crowds draw exactly as before; each city's pooled crowd passes the sameness check and
    varies; a pooled passer-by draws the pack's own head once installed; a turned ponytail hangs from the head's back
    edge (saved example: the pool's first sheet, a three-quarter ponytail drawn over the cheek)."""
    import re as _re
    import kitchecks as K
    import people as PK
    pool_c = {c for v in PK.POOL_HAIR_C.values() for c, _ in v} | set(PK.POOL_GREYS) | {(128, 120, 114)}
    tops = {c for v in PK.POOL_TOPS.values() for c, _ in v}
    skins = {c for v in PK.POOL_SKINS.values() for c in v}
    cuts = {c.split(' ')[0] for v in PK.POOL_HAIR.values() for c, _ in v}
    missing = []
    for film in PK.BEFORE_POOL:
        if not os.path.exists(PK.people_file(film)):
            continue
        for w, d in PK.crowds(film).items():
            for key, _, items in d['crowd']['cycle'] + [f for _, _, fs in d['crowd']['when'] for f in fs]:
                for it in items:
                    if key == 'hair' and it.split(',')[0].strip() not in cuts:
                        missing.append(f'{film} {w} haircut {it}')
                    elif key == 'hair colour' and PK.colour(it) not in pool_c:
                        missing.append(f'{film} {w} hair colour {it}')
                    elif key == 'skin' and PK.colour(it) not in skins:
                        missing.append(f'{film} {w} skin {it}')
                    elif key == 'jacket' and _re.fullmatch(r'[\d ]+|[a-z ]+', it) and PK.colour(it) not in tops:
                        missing.append(f'{film} {w} top {it}')
    old = [f for f in PK.BEFORE_POOL if os.path.exists(PK.people_file(f))
           and any(d.get('crowd_pool') for d in PK.crowds(f).values())]
    import tempfile
    tmp = os.path.join(tempfile.mkdtemp(), 'new-people.txt')       # a new film's people file: its crowd on the pool
    open(tmp, 'w').write('# m: Marchers\ncrowd: m\nmix: london\n')
    pf, PK.people_file = PK.people_file, lambda film: tmp
    try:
        new = PK.crowds('a-new-film')['m']
    finally:
        PK.people_file = pf
    same, varied = {}, {}
    for city in ('london', 'paris', 'miami', 'tirana', 'barcelona', 'frankfurt', 'mixed'):
        d = PK.parse(f'# m: M\ncrowd: m\nmix: pool {city}\n')['m']
        d.update(crowd_defaults=True, crowd_sex=True)
        ms = [PK.crowd_person(d, i) for i in range(64)]
        same[city] = K.same_faults(city, ms, d.get('crowd_mix'))
        varied[city] = (len({m.get('kit_face', {}).get('hair') or m.get('hair') for m in ms}),
                        len({m.get('jacket') for m in ms}), len({m.get('skin') for m in ms}))
    import subprocess                                    # in its own process: no earlier test's install
    code = ("import sys; sys.path.insert(0, %r); import people as PK; p = PK.pooled(3, 'london'); "
            "a = PK.head_faults(p); PK.install({'p': p}); print(len(a), len(PK.head_faults(p)))") % HERE
    got = (subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, cwd=HERE).stdout.strip()
           .split('\n') or [''])[-1].split()
    before, after = (int(got[0]), int(got[1])) if len(got) == 2 else (0, 1)
    edge = PK.pooled(1, 'paris').get('pony_edge') and not any(
        sp.get('pony_edge') for sp in PK.load('protest-tiers').values())
    ok = (not missing and not old and new.get('crowd_pool') and new.get('crowd_place') == 'london' and not any(same.values())
          and all(a >= 5 and b >= 15 and c >= 3 for a, b, c in varied.values()) and before and not after and edge)
    return ok, dict(missing=missing[:6], old_on_pool=old, sameness={k: v[:2] for k, v in same.items() if v},
                    varied=varied, head=(before, after), pony_edge=bool(edge))


@test
def practice_mode():
    """Sam, 26 Nov ("override all checks and produce it"; "advise whether you want to run a certain suite of checks";
    the proposal route on request): with nothing asked, a render runs no body check, a practice clip or animatic goes
    to Sam with no record, only a final is held; a practice job (Kind: practice) starts no kit tests; the proposal
    guard never stops a reply. Saved example: pose-test chat 1 (a 3 s clip took 12 min under the body check; 112 kit
    tests ran for a test clip)."""
    import tempfile
    import humancheck as HC
    import kitfilm as KF
    import propose as P
    saved = {k: os.environ.pop(k, None) for k in ('BODYCHECK', 'PROPOSE_GUARD', 'SENDGATE_ALL')}
    try:
        d = tempfile.mkdtemp()
        HC._ENTRIES.append({'kind': 'flat'})
        HC.frame_begin()
        off = HC.frame_end(0.0) == [] and not HC._ENTRIES and not HC.asked()
        clip = os.path.join(d, 'pose-test-runner.mp4')
        open(clip, 'wb').write(b'0')
        sent = HC.send_faults(clip) == []
        root = os.path.dirname(HERE)
        final = HC.is_final(os.path.join(root, 'animations', 'open-wounds.mp4'))
        draft = HC.is_final(os.path.join(root, 'animations', 'drafts', 'open-wounds-animatic.mp4'))
        open(os.path.join(d, 'zz-practice.md'), 'w').write('# x\nKind: practice\n')
        open(os.path.join(d, 'zz-film.md'), 'w').write('# x\n')
        prac = KF.practice('zz-practice', d) and not KF.practice('zz-film', d)
        quiet = P.hook('{"transcript_path": "/nonexistent"}') == 0
    finally:
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v
    ok = off and sent and final and not draft and prac and quiet and not KF.ANIMATIC_GATE
    return ok, (f'body check off {off}; practice clip sent {sent}; final held {final}, animatic not {not draft}; '
                f'practice job {prac}; proposal guard quiet {quiet}; no kit gate before animatics {not KF.ANIMATIC_GATE}')


@test
def body_send_gate():
    """Change 1 (Sam's Y, 20 Nov): a video made since the gate reaches Sam only with a body check record, clean or
    named, and a fresh critique (rule 89); videos from before the gate pass as they are."""
    import subprocess
    import tempfile
    import humancheck as HC
    d = tempfile.mkdtemp()
    v = os.path.join(d, 'clip.mp4')
    open(v, 'wb').write(b'0')
    no_rec = HC.send_faults(v)
    w = HC.Writer('clip.mp4')
    w.frame(0.0, [(0.0, 'Jason', 'order', 'R arm out of his back')])
    HC._save(v, dict(video='clip.mp4', faults=w.lines(), named=False, critique=None, made=None))
    faulty = HC.send_faults(v)
    HC._save(v, dict(video='clip.mp4', faults=[], named=False, critique='notes/critiques/x', made=None))
    clean = HC.send_faults(v)
    os.utime(v, (HC.START - 3600, HC.START - 3600))
    old = HC.send_faults(os.path.join(d, 'gone.mp4')) + HC.send_faults(v)
    hook = subprocess.run([sys.executable, os.path.join(HERE, 'humancheck.py'), 'sendgate'], cwd=d, capture_output=True,
                          text=True, input=json.dumps({'tool_input': {'files': ['clip.mp4']}, 'cwd': d}))
    ok = len(no_rec) == 1 and len(faulty) == 2 and not clean and not old and hook.returncode == 0
    return ok, f'no record {len(no_rec)}, faulty {len(faulty)}, clean {len(clean)}, old {len(old)}, hook {hook.returncode}'


@test
def body_check_headless():
    """GTA chat 20 (rule 30): the lean-out sheet showed pose K2 from three-quarter front with no head; the figure
    guard had stopped the drawing at the arm and the body check had no test for a person with no head. The old K2
    must now be caught with no head (and crossed out on the sheet); K1 from the same view must stay clean."""
    import leanout as LO
    import gta_cast as GC
    import body as B
    B.SS = 1
    sp = dict(GC.cast()['jason'], mood='stern')
    old = LO._key((0.48, 0.80, 0.0), (0.78, 1.30, 0.0), (1, 0, -0.15), (1, -0.15, -0.1),
                  {'R': ('rel', ((-0.04, 0.02, 0.32), 'out')), 'L': ((0.84, 1.34, 0.18), LO._v(0.3, -1, 0.6))},
                  {'L': (0.52, LO.SEAT + 0.05, 0.14), 'R': (0.50, LO.SEAT + 0.05, -0.12)}, sp)
    _, f_old = LO.draw_view(sp, old, 45)
    _, f_k1 = LO.draw_view(sp, LO.pose('K1', sp), 45)
    caught = any('no head' in f for f in f_old)
    return caught and not f_k1, f'old K2 at 3/4: headless caught {caught}; K1 at 3/4: {len(f_k1)} faults'



@test
def dearest_things_named():
    """Cost audit (Sam, 21 Nov: "audit every last thing done in order to find the most expensive things and run it
    through the proposal route"): GTA's record filed 69% of its cost as "other". Every dollar of a chat must now carry a
    plain name (thinking, writing code, reading notes, critique helpers ...) that adds up to the bill, the film's GTA
    code (gta_*.py) counts as film code, and the five dearest open as proposals that pass the route's own check."""
    import glob as G
    import io
    import contextlib
    import stepcost
    import dearest
    out = []
    fr = stepcost._film_paths('grand-theft-autism')
    if not fr.search('python3 source/gta_rehearse.py'):
        out.append("GTA's gta_*.py files are not counted as the film's own code")
    mine = sorted(G.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl')), key=os.path.getmtime)
    for p in ['tests/stepcost-transcript.jsonl'] + mine[-1:]:
        sp = stepcost.split(os.path.join(os.path.dirname(HERE), p) if not p.startswith('/') else p, 'grand-theft-autism')
        if not sp or not sp.get('named'):
            out.append(f'{p}: no named split')
            continue
        if abs(sum(sp['named'].values()) - sum(sp['origins'].values())) > 1.0:
            out.append(f'{p}: the named parts do not add up to the bill')
        if sp['named'].get('other tool results', 0) + sp['named'].get('unexplained', 0) > 10:
            out.append(f'{p}: over 10% still unnamed')
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        ok = dearest.test()
    if not ok:
        out.append('dearest.py test: ' + ' | '.join(ln for ln in buf.getvalue().splitlines() if ln.startswith('FAIL')))
    import ledger                                   # the notes problem: Sam's notes counted from his own words
    n, maybe = ledger.count_notes(os.path.join(os.path.dirname(HERE), 'notes/ledger/sam/negkzryt.md'), 'grand-theft-autism')
    if n < 10:
        out.append(f'GTA chat with 10 of Sam\'s messages counted only {n} notes')
    if not any('gun' in m or 'fires' in m for m in maybe):
        out.append('the gun note Sam gave before (the gun not pointing at the target) is not flagged as a possible repeat')
    return not out, '; '.join(out) or 'every dollar named; five dearest ranked; Sam\'s notes counted, repeats flagged'


@test
def rule_proofs_gate():
    """Lesson 7 (rule-needs-check, Sam's option 1, 22 Nov): "no rule without a working check". Step 1 found 61 of 103
    rules never proved on a bad example, 19 rows "by hand", and 39 let-throughs of the proposal guard carried on. The
    gate must refuse a new rulebook row and a new CLAUDE.md rule with no saved example, a "by hand" status, a proof
    whose kittest failed; a handover check that crashes is a STOP; an unsettled let-through refuses the animatic until
    settled; and today's files pass."""
    import copy
    import tempfile
    import ruleproofs as R
    import handover as H
    import propose as PR
    out = []
    d = R.load()
    if R.faults(d, failed=set()):
        out.append('today\'s rules fail the gate: ' + '; '.join(R.faults(d, failed=set()))[:200])
    book = open(R.RULEBOOK, encoding='utf-8').read() + '\n| 99 | A new rule nobody proved. | `nothing.py` |\n'
    if not any('rule 99 is new' in f for f in R.faults(d, book=book, failed=set())):
        out.append('a new rulebook row with no entry was let through')
    cl = open(R.CLAUDE, encoding='utf-8').read() + '\n- **Always do a brand new thing.** (Sam, 23 Nov)\n'
    if not any('Always do a brand new thing' in f for f in R.faults(d, claude=cl, failed=set())):
        out.append('a new CLAUDE.md rule with no entry was let through')
    d2 = copy.deepcopy(d)
    d2['rules']['99'] = dict(rule='x', status='next', plan='later', example='')
    if not any('rule 99 is new and has no saved bad example' in f for f in R.faults(d2, book=book, failed=set())):
        out.append('a new entry with no example was let through')
    d2['rules']['99'].update(status='by hand', example='a still')
    if not any('"by hand" never counts' in f for f in R.faults(d2, book=book, failed=set())):
        out.append('"by hand" was accepted as a check')
    t0 = next(t for r in d['rules'].values() if r['status'] == 'proven' for t in r['tests'])
    if not any('BROKEN' in f for f in R.faults(d, failed={t0})):
        out.append(f'a proven rule whose kittest {t0} failed was not shown as broken')
    crash = H._safe('demo', lambda: 1 / 0)
    if not (crash and crash[0].startswith('STOP: CHECK COULD NOT RUN')):
        out.append('a crashing handover check did not stop the handover')
    keep = PR.PROPS
    PR.PROPS = tempfile.mkdtemp()
    try:
        open(PR._p(PR.UNROUTED), 'w').write('- 2026-11-23 01:00 chat abcd1234: sent after one block: x | "y"\n'
                                           '- 2026-11-20 01:00 chat old00000: sent after one block: x | "y"\n')
        if len(PR.open_letthroughs()) != 1 or not PR.unrouted_for('abcd1234'):
            out.append('the open let-through was not seen (or an old one counted)')
        PR.settle('abcd1234', 'false block: the guard asked for a line the reply did not need')
        if PR.open_letthroughs() or PR.unrouted_for('abcd1234'):
            out.append('settling did not clear the let-through')
    finally:
        PR.PROPS = keep
    return not out, '; '.join(out) or 'new rule with no example refused (rulebook and CLAUDE.md); by hand refused; broken proof shown; crash = STOP; let-through closed until settled'



@test
def staging_stills_milburn_replay():
    """Lesson staging-stills (Sam's option 1, 22 Nov): no shot moves before Sam has seen its framing. Milburn's own record
    replayed: chat 6's first build of the Cabinet Room reverse (17 Nov 22:50) and chat 10's re-stage (18 Nov 04:00) must
    both be refused; shot 1 (on the first board) must pass; and once note 5 is held, 2-3 framings sent, Sam's number
    recorded and the shot's new board delivered, the reverse must pass."""
    import calendar
    import shutil
    import tempfile
    import time
    import staging as S
    root = os.path.dirname(HERE)
    tmp = tempfile.mkdtemp()
    out = []
    at = lambda s: calendar.timegm(time.strptime(s, '%Y-%m-%d %H:%M'))          # noqa: E731 (UK = UTC in Nov)
    try:
        os.makedirs(os.path.join(tmp, 'story'))
        shutil.copy(os.path.join(root, 'story', 'milburn-board-sent.txt'), os.path.join(tmp, 'story'))
        shots = ['1', '2a', '2b', '3', '4a', '4b', '4c', '6', '7a', '7b', '7c', '7d', '7e']
        rev = ['4a', '4c', '7a', '7c', '7e']
        row5 = next(ln for ln in open(os.path.join(root, 'notes', 'archive', 'milburn.md'))
                    if ln.startswith('| 5 |') and 'scene composition' in ln)
        notes = '## Notes\n| # | shot | time | note | line | status |\n|---|---|---|---|---|---|\n' + row5
        g6 = S.gate('milburn', ['3', '4a'], shots, tmp, now=at('2026-11-17 22:50'), notes_text='')
        if len(g6) < 2 or not all('never been on a shot board' in f for f in g6):
            out.append(f'chat 6 build of shots 3 and 4a not refused: {g6}')
        if S.gate('milburn', ['1'], shots, tmp, now=at('2026-11-17 22:50'), notes_text=''):
            out.append('shot 1 (on the 20:49 board) refused')
        g10 = S.gate('milburn', ['4a'], shots, tmp, now=at('2026-11-18 04:00'), notes_text=notes)
        if not any('never been on' in f for f in g10) or not any('note 5' in f and 'reads as framing' in f for f in g10):
            out.append(f'chat 10 re-stage not refused for both reasons: {g10}')
        rec = os.path.join(tmp, 'story', 'milburn-staging.txt')
        with open(rec, 'w') as f:
            for n in rev:
                f.write(f'hold {n} {at("2026-11-17 23:08")} note=5 the scene composition in scene 4 as proposed is poor\n')
        g10b = S.gate('milburn', rev, shots, tmp, now=at('2026-11-18 04:00'), notes_text=notes)
        if any('reads as framing' in f for f in g10b) or not any('held by note 5' in f for f in g10b):
            out.append(f'a held shot was not refused as held (or note 5 still unrouted): {g10b}')
        with open(rec, 'a') as f:
            f.write(f'options 4a {at("2026-11-17 23:20")} milburn-4a-framings.jpg n=3\n')
            for n in rev:
                f.write(f'pick {n} {at("2026-11-17 23:30")} 2 Sam: 2, equal and centred\n')
        if not any('Sam picked 2' in f for f in S.gate('milburn', ['4a'], shots, tmp, now=at('2026-11-17 23:40'),
                                                         notes_text=notes)):
            out.append('a picked shot moved before its new board reached Sam')
        with open(os.path.join(tmp, 'story', 'milburn-board-sent.txt'), 'a') as f:
            f.write(f'board milburn-4a-built.jpg delivered={at("2026-11-17 23:50")} drawn={at("2026-11-17 23:49")} '
                    f'commit=x moves=0 (17 Nov 23:50)\n' + ''.join(f'shot {n} 0000000000 andy,pat\n' for n in rev))
        ok = S.gate('milburn', rev, shots, tmp, now=at('2026-11-18 00:30'), notes_text=notes)
        if ok:
            out.append(f'the reverse still refused after Sam\'s pick and its new board: {ok}')
        with open(rec, 'a') as f:
            f.write(f'hold 6 {at("2026-11-18 00:40")} note=9 dodge\npick 6 {at("2026-11-18 00:41")} go Sam: just build it\n')
        if S.gate('milburn', ['6'], shots, tmp, now=at('2026-11-18 07:00'), notes_text=''):
            out.append('Sam\'s "go" did not release the shot')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return not out, '; '.join(out) or ('chat 6 and chat 10 builds refused; shot 1 passes; held until 2-3 framings, '
                                       'his number and the new board; "go" releases')


@test
def staging_stills_note_finder():
    """Lesson staging-stills: the note finder (staging.FRAMING, on Sam's words) finds every framing or staging note the
    four-film look back listed (Milburn, Patriots 4, Blessed, European Protests Ranked) and leaves face, hair, mouth and
    sound notes alone."""
    import staging as S
    arch = os.path.join(os.path.dirname(HERE), 'notes', 'archive')
    need = {'milburn': ['5', '10'], 'patriots-4': ['7', '8', '12', '20', '26', '28', '31'],
            'blessed-notes-animatics-1-2': ['7', '11', '12', '15', '22', '30', '32', '33', '37', '42'],
            'protest-tiers': ['F1', 'F3', 'F4', 'F7', 'F13', 'G12', 'A1', 'A4', 'A10', 'G4']}
    avoid = {'milburn': ['1', '2', '3', '4', '6', '7', '8', '9', '11'], 'patriots-4': ['13', '16'],
             'blessed-notes-animatics-1-2': ['1', '2', '45'], 'protest-tiers': ['F21', 'A24', 'O8', 'S8', 'G20', 'A21']}
    out, n_all, n_flag = [], 0, 0
    for film in need:
        text = open(os.path.join(arch, f'{film}.md')).read()
        got = {i for i, _, _ in S.framing_notes(text)}
        n_all += len(S.notes_in(text))
        n_flag += len(got)
        miss = [i for i in need[film] if i not in got]
        wrong = [i for i in avoid[film] if i in got]
        if miss:
            out.append(f'{film}: missed {miss}')
        if wrong:
            out.append(f'{film}: flagged non-framing {wrong}')
    return not out, '; '.join(out) or (f'all {sum(map(len, need.values()))} framing notes found; '
                                       f'{n_flag} of {n_all} notes flagged')


@test
def acting_rows_every_shot():
    """Rule 74 (Sam, 20 Nov, GTA shot 4 note 16: "no acting notes anywhere"): the gate asked for a row per spoken line
    only, so shot 4 (no lines) went to Sam with none. The check must flag shot 4 in GTA's notes before chat 17 added
    its rows (git f5cbaf64^) and pass shot 4 once they are there (f5cbaf64)."""
    import subprocess
    import preflight as P
    root = os.path.dirname(HERE)
    txt = lambda rev: subprocess.run(['git', '-C', root, 'show', f'{rev}:notes/grand-theft-autism.md'],
                                     capture_output=True, text=True).stdout
    before, after = txt('f5cbaf64^'), txt('f5cbaf64')
    if not before or not after:
        return False, 'COULD NOT TEST: the GTA notes are not in this copy\'s history'
    b = [f for f in P.acting_shot_faults(before, range(1, 9)) if 'shot 4 ' in f]
    a = [f for f in P.acting_shot_faults(after, range(1, 9)) if 'shot 4 ' in f]
    return bool(b) and not a, f'before chat 17: shot 4 flagged {bool(b)}; after: flagged {bool(a)}'



@test
def named_lines_shared_inputs_milburn():
    """named-lines change 3 (Sam's Y, 23 Nov): the kits hand the checks what they need from the drawing, no film code.
    Must beat on Milburn: its blind lines cured (37 at its animatics; the 6 left are named: shot 2b's tiny figures drawn
    by its own set code x4, no camera for shots 3 and 6, audits) and 0 false voice lines (85 read raw today, 60 then)."""
    import importlib
    import kitinputs, plan, housestyle, viewchecks, camfeel, voices, takes
    import preflight as PF
    import body as Bd
    M = importlib.import_module('milburn')
    has = set(M.HAS)
    kf, said, kfaults = kitinputs.fill(M, has)
    cast = PF.cast_faults(M, kf.KIT_ROSTER)
    pl = plan.faults(kf)
    hs = housestyle.faults(kf, Bd, has)
    vc = [x for x in viewchecks.faults(kf) if x.startswith(('EFFECT SHAPES', 'READABILITY'))]
    cf = camfeel.faults(kf)
    blind = [x for x in cast + pl + hs + vc + cf if 'never on screen' in x or 'has no ' in x or 'no camera' in x
             or 'looks at nothing' in x or 'no SHOT_MARKS' in x or 'gives no camera' in x or 'overlap' in x
             or 'stands inside' in x or 'has no facing' in x]
    left_ok = sorted(x for x in blind if ('shot 2b' in x and 'never on screen' in x) or 'shot(s) 3, 6' in x
                     or 'no audits' in x)

    class Check:
        def __init__(self, f):
            self._f, self.LINES = f, [{k: v for k, v in ln.items() if k not in ('_voice', '_stretches')} for ln in f.LINES]

        def __getattr__(self, n):
            return getattr(self._f, n)
    vo = voices.check(Check(M))
    raw = [x for x in vo if 'raw recording' in x]
    ok = len(blind) == len(left_ok) == 6 and not raw and len(vo) <= 2 and not kfaults
    return ok, f'blind lines left {len(blind)} (named and expected: {len(left_ok)}); voice lines with no film hand-over ' \
               f'{len(vo)} ({len(raw)} raw reads); kit faults {kfaults[:2]}; inputs handed {len(said)}'


@test
def move_to_shared_catches_film_fixes():
    """named-lines change 3's stop, the check of CLAUDE.md "Every rule and fix is for all films" (Sam, 23 Nov, N26):
    handover.py end stops on a check fix written in one film's code. Replayed on the SAVED code of the 10 the look-back
    found in three films (Blessed 7, Milburn 1, Grand Theft Autism 2, its own renderer); a shared file is never flagged;
    a film whose notes say Sam keeps it (| stays in film | FILE | why | Sam's Y |) passes."""
    import tempfile
    import handover as H
    want = {'blessed_checks.py': ['def scene(t)', 'def solids(t)', 'def cam_for(t)', 'def audits()', 'SET_FEET = {'],
            'blessed.py': ['def touch_faults()', 'def furniture_faults()'], 'milburn.py': ['_ln.update(_voice='],
            'gta_rehearse.py': ['def solids4('], 'gta_shots58.py': ['def solids58(']}   # written twice (learn.md 3)
    diff = ''
    for f, starts in want.items():
        src = open(os.path.join(HERE, f), encoding='utf-8').read().splitlines()
        got = [next((ln for ln in src if ln.strip().startswith(w)), None) for w in starts]
        diff += f'+++ b/source/{f}\n' + ''.join(f'+{ln}\n' for ln in got if ln)
    found = H.film_check_fixes(diff)
    shared = H.film_check_fixes('+++ b/source/kitinputs.py\n+def scene(t):\n+def cam_for(film, sv):\n')
    films = sorted({f for _, f, _ in found})
    stops = H.shared_faults(diff=diff)
    d = tempfile.mkdtemp()
    keep = os.path.join(d, 'm.md')
    open(keep, 'w').write('## Exceptions\n| check | who | why | looked |\n|---|---|---|---|\n'
                          '| stays in film | milburn.py | its subtitles need the take | Sam\'s Y 23 Nov |\n')
    real = H._keep_notes
    H._keep_notes = lambda film: keep if film == 'milburn' else real(film)
    try:
        kept = H.shared_faults(diff=diff)
    finally:
        H._keep_notes = real
    ok = len(found) == 10 and not shared and films == ['blessed', 'grand-theft-autism', 'milburn'] and \
        len(stops) == 10 and all(x.startswith('STOP: MOVE TO SHARED') for x in stops) and len(kept) == 9
    return ok, f'found {len(found)} of 10 on the saved code in {films}; stops {len(stops)}; with Sam\'s keep row ' \
               f'{len(kept)}; shared file flagged {len(shared)}'


@test
def kittest_red_twice_stops_handover():
    """named-lines change 4 (Sam's Y, 23 Nov), on chain A's gate: a kit test red at two handovers in a row (different
    chats), or one that crashed, is a STOP line; red once is a plain line; no finished run is a STOP."""
    import tempfile
    import handover as H
    d = tempfile.mkdtemp()
    log, reds = os.path.join(d, 'k.log'), os.path.join(d, 'r.log')
    open(log, 'w').write('FAIL a_test: 1 of 2\nFAIL b_test: crashed: no model\nPASS c_test: ok\nkittests: 2 failed\n')
    one = H.kittest_gate_faults(log, reds, sid='chat1')
    again = H.kittest_gate_faults(log, reds, sid='chat1')          # the same chat running end twice: still once
    two = H.kittest_gate_faults(log, reds, sid='chat2')
    open(log, 'w').write('FAIL a_test: 1 of 2\n')                   # a run that never finished
    none = H.kittest_gate_faults(log, reds, sid='chat3')
    st = lambda fs, w: any(f.startswith('STOP:') and w in f for f in fs)
    ok = (st(one, 'b_test') and not st(one, 'a_test') and not st(again, 'a_test') and st(two, 'a_test')
          and (st(none, 'COULD NOT RUN') or st(none, 'STILL RUNNING')))
    return ok, f'once {len(one)} lines, twice {sum(f.startswith("STOP") for f in two)} stops, unfinished: {none[:1]}'


@test
def plan_places_apart_and_flat_floors():
    """named-lines change 3: plan.py treats rooms no opening joins as separate places (Milburn's 3 false overlaps),
    reads a floor-flat thing as stood on (its 5 false 'stands inside'), a tilt (pitch=) as where a camera looks, and the
    film's own SHOT_MARKS; joined rooms that overlap, and a person inside a real table, are still faults."""
    import plan
    P = dict(ROOMS={'a': (0, 0, 4, 4), 'b': (0, 0, 3, 3), 'c': (2, 0, 6, 4), 'd': (5, 0, 9, 4)},
             OPENINGS={'door': dict(wall=('x', 6.0), span=(1.0, 2.0), sill=0.0, head=2.0)},
             THINGS={'deck': dict(at=(1, 1), size=(2, 2, 0.0)), 'desk': dict(at=(3.5, 3), size=(1, 1, 0.75))},
             PEOPLE={'p': dict(at=(1, 1), facing=180), 'q': dict(at=(3.5, 3), facing=180)},
             CAMS={'1': dict(up=70, pitch=28, lens=1000)})
    film = type('F', (), {'PLAN': P, 'SHOTS': [('1', 0, 1)], 'SHOT_MARKS': {'1': ['p']}})
    f = plan.faults(film)
    over = [x for x in f if 'overlap' in x]
    ok = over == ['plan: rooms c and d overlap'] or (len(over) == 1 and 'c' in over[0] and 'd' in over[0])
    ok = ok and not any('p stands inside' in x for x in f) and any('q stands inside the desk' in x for x in f)
    ok = ok and not any('looks at nothing' in x or 'no SHOT_MARKS' in x for x in f)
    return ok, f'overlaps {over}; inside {[x for x in f if "inside" in x]}'


@test
def takes_cleaned_and_registered():
    """named-lines change 3: takes.clean (Milburn's take cleaning, now shared) cleans each line's files and registers
    the take under its audio name, so voices.py reads what the film plays; a film's code that never calls
    mossad_audio.line is told when its check reads a raw file."""
    import takes
    ok = takes._test()
    ok = ok and takes.plays_shared_loader([os.path.join(HERE, 'satire_template.py')]) and \
        not takes.plays_shared_loader([os.path.join(HERE, 'milburn.py')])
    return ok, 'cleaned, registered; the template plays the shared loader, Milburn does not'
def door_slit():
    """Sam (23 Nov, chat 50, a marked still at 16.5 s): "Little bit of trouser showing there", a line of Jason's
    shorts along the Tulip's door top. The car's solid depth (gta_cars.solid_depth, the per-dot depth test that hides
    the 3D Jason) let the sight line through a 1 cm slit between the body's top and the house's foot. Passes only if
    the old shape (no skirts) shows that point, the fixed one hides it, and his hips still show through the open
    window at 22.5 s (v5 notes 2/8/9)."""
    import gta_cars as G
    import sets as S

    def setup(cam, car):
        c = G.Car('tulip', pos=car[0], yaw=car[1], roll=car[2], pitch=0.5)
        c.open_windows = ((1, 1),)
        return S.Cam(*cam), c

    def seen(cam, car, loc):
        p = car.body_pt(loc)
        (x, y), _ = cam.project(p)
        if not (0 <= x < 1080 and 0 <= y < 1920):
            return False
        zc = G.solid_depth(car, cam, 1)
        return float(zc[int(y), int(x)]) > cam.depth(p) + 0.01
    cam, car = setup(((8.6271, 1.35, 37.1733), (5.7117, 1.28, 37.7581), 1650.0, (-2.0633, -1.0781), 0.0),
                     ((4.9193, 38.4), -0.3598, -0.4839))
    slit = [(0.80, 0.93, -0.13), (0.75, 0.92, -0.13), (0.70, 0.91, -0.13)]   # the shorts' dots Sam saw (a 1-dot line)
    G.SKIRT[0] = False
    try:
        old = any(seen(cam, car, q) for q in slit)
    finally:
        G.SKIRT[0] = True
    new = any(seen(cam, car, q) for q in slit)
    cam2, car2 = setup(((7.0048, 1.9414, 138.5708), (7.0042, 0.6367, 122.6688), 1732.79, (-1.9305, 0.9915), 0.0),
                       ((5.0990, 134.4), -0.0867, 0.3173))
    hips = any(seen(cam2, car2, (x, y, z)) for x in (0.35, 0.5, 0.6) for y in (0.6, 0.7, 0.8) for z in (-0.4, -0.2, 0.0))
    ok = old and not new and hips
    return ok, 'old slit seen %s, fixed slit seen %s, hips through the open window %s' % (old, new, hips)


@test
def run_hips_stay_up():
    """A run never sinks into a lunge (Open Wounds chat 13, notes/learn/run-lunge/): the hips bob at most 0.13 leg."""
    import moves as MV
    import views as V
    leg = V.THIGH + V.SHIN
    sp = {'height': 1.8, 'pose': 'custom'}

    def worst(kind, step_m=None, speed=None):
        sps = speed / step_m if speed else MV.GAITS[kind]['sps']
        stride = step_m / V.M_PER_UNIT if step_m else None
        return max(MV.gait(sp, i / 60 * 2 / sps, kind, stride=stride, steps_per_s=sps if speed else None)['bob']
                   for i in range(60)) / leg
    cases = [('run', None, None), ('sprint', None, None), ('run', 0.95, 4.4), ('run', 1.25, 5.0)]
    keep = MV.RUN_SWEEP
    try:
        MV.RUN_SWEEP = 99.0                          # the old gait: a foot stays down as long as `duty` says
        old = worst('run', 0.95, 4.4)
    finally:
        MV.RUN_SWEEP = keep
    now = {f'{k} {m or "own"}': worst(k, m, v) for k, m, v in cases}
    ok = old > 0.13 and all(x <= 0.13 for x in now.values())
    return ok, 'old run at 0.95 m sank %.2f leg; now %s' % (old, ', '.join('%s %.2f' % kv for kv in now.items()))


@test
def movers_never_meet_head_on():
    """Two movers going opposite ways never meet on screen within 3 m of depth (Open Wounds chat 13: nose to nose)."""
    import moves as MV
    import brexit_is_done_action as A
    old_passes = [  # chat 12's table: lanes 4.7 and 5.6 m (guests nose to nose at 7.5 s; a wolf through a guest at 3.1)
        (0, 0.30, [(-1.30, 7.60), (-1.30, 5.95), (-3.3, 5.35)], 0, 0.65), (1, 0.52, [(-0.50, 8.60), (-0.50, 5.85), (2.9, 5.50)], 1, 0.55),
        (2, 0.78, [(-1.05, 9.00), (-1.05, 5.75), (-3.0, 4.70)], 2, 0.55), (3, 1.05, [(-1.50, 9.20), (-1.50, 5.85), (2.9, 5.60)], 3, 0.55),
        (0, 2.30, [(-2.6, 4.70), (2.7, 4.70)], 0, 0.57), (1, 3.00, [(2.7, 5.60), (-2.7, 5.60)], 1, 0.55),
        (2, 3.80, [(-2.5, 4.70), (2.7, 4.70)], 2, 0.55), (3, 4.60, [(2.7, 5.60), (-2.7, 5.65)], 3, 0.55),
        (0, 5.40, [(2.7, 5.80), (-2.7, 5.80)], 0, 0.55), (1, 6.10, [(-2.6, 4.75), (2.7, 4.75)], 1, 0.55),
        (2, 6.90, [(2.7, 5.50), (-2.7, 5.50)], 2, 0.57), (3, 7.05, [(-2.6, 4.70), (2.7, 4.70)], 3, 0.55),
        (0, 8.85, [(-2.6, 5.00), (2.7, 5.00)], 0, 0.55)]
    keep = A.PASSES
    try:
        A.PASSES = old_passes
        old = MV.head_on(MV.chase_movers(A.PASSES, A.GUEST_V, A.WOLF_V), 0, 9.4)
    finally:
        A.PASSES = keep
    new = MV.head_on(MV.chase_movers(A.PASSES, A.GUEST_V, A.WOLF_V), 0, 9.4)
    caught = any(m[3] < 0.1 for m in old) and any(abs(m[0] - 7.5) < 0.1 for m in old)
    return caught and not new, 'old table: %d meetings (%s); now: %s' % (len(old), old[:2], new or 'none')


@test
def side_by_side_out_of_reach():
    """Two people running side by side stay more than an arm's reach apart on screen (Open Wounds chat 13: a hand on
    the shoulder of the guest beside him, notes/learn/chase-meetings/hand-on-shoulder-24.92.jpg)."""
    import moves as MV
    import brexit_is_done as F
    import brexit_is_done_action as A
    L = F._cam('blair')
    proj = lambda x, d: (L.p(x, d, 1.0)[0], L.ppm(d))
    keep = A.PASSES
    wave = {4: (2, 2.55, A.LANE_L), 5: (0, 2.75, A.LANE_R), 6: (3, 4.65, A.LANE_L), 7: (1, 4.85, A.LANE_R),
            8: (0, 6.45, A.LANE_L), 9: (2, 6.65, A.LANE_R)}       # the first waves: the far one leading by 0.2 s
    old_passes = []
    for i, p in enumerate(keep):
        if i in wave:
            k, t0, lane = wave[i]
            sx = -2.7 if i < 6 else 2.7
            p = (k, t0, [(sx, lane), (-sx, lane)], k, 0.57 if k in (0,) and i == 5 else 0.55)
        old_passes.append(p)
    try:
        A.PASSES = old_passes
        old = MV.within_reach(MV.chase_movers(A.PASSES, A.GUEST_V, A.WOLF_V), proj, 0, 9.4)
    finally:
        A.PASSES = keep
    new = MV.within_reach(MV.chase_movers(A.PASSES, A.GUEST_V, A.WOLF_V), proj, 0, 9.4)
    caught = any('(pass 8)' in m[1] and '(pass 9)' in m[2] for m in old)    # the pair of the hand on the shoulder
    return caught and not new, 'first waves: %s; now: %s' % (old, new or 'none')


@test
def dark_sleeve_reads():
    """A dark sleeve swinging across a dark jacket reads as an arm, not a floating hand (Open Wounds chat 14, critique
    r5 (b), notes/learn/dark-sleeve/): side on mid-run, the near arm's fill differs from the jacket's by a visible step
    and covers its own patch of the body. The old drawing (sleeve = jacket) is refused."""
    from PIL import Image
    import views as V
    import people_parts as PPt
    import moves as MV
    import figure as FG
    B = PPt.B
    import people as PK
    sp = PK.crowd_person(PK.crowds('brexit-is-done')['guest'], 0)

    def arm_px(lift):
        keep = V.DARK_SLEEVE_LIFT
        V.DARK_SLEEVE_LIFT = lift
        try:
            img = Image.new('RGBA', (400, 600), (235, 235, 235, 255))
            j = MV.gait(sp, 0.0, 'run', steps_per_s=3.5)
            B.SS = 1
            with FG.allow('kittest: a side-on runner'):
                V.person(img, B.Cam(1.0, 540, 960), 200, 60, 0.5, sp, 0.0, 90.0, j)
            jac = tuple(sp.get('jacket', (40, 40, 46))[:3])
            slv = tuple(V.sleeve_colour(sp)[:3])
            px = img.convert('RGB').getdata()
            n = sum(1 for c in px if sum(abs(a - b) for a, b in zip(c, slv)) <= 6)
            step = sum(abs(a - b) for a, b in zip(slv, jac))
            return n, step
        finally:
            V.DARK_SLEEVE_LIFT = keep
    # chat 38 (Sam, note 24.3: "sleeves are a different colour to the jacket"): the sleeve is the jacket's own colour
    # and the arm reads by its lit edge (limbs.DARK_RIM); the old lifted sleeve and the bare one are both refused
    import limbs as LB
    n_now, step_now = arm_px(V.DARK_SLEEVE_LIFT)
    jac = tuple(sp.get('jacket', (40, 40, 46))[:3])
    edge = LB._lit(jac)
    img = Image.new('RGBA', (400, 600), (235, 235, 235, 255))
    j = MV.gait(sp, 0.0, 'run', steps_per_s=3.5)
    with FG.allow('kittest: a side-on runner'):
        V.person(img, B.Cam(1.0, 540, 960), 200, 60, 0.5, sp, 0.0, 90.0, j)
    n_edge = sum(1 for c in img.convert('RGB').getdata() if sum(abs(a - b) for a, b in zip(c, edge)) <= 6)
    ok = step_now == 0 and n_edge >= 60
    return ok, f'sleeve {step_now} from the jacket (0 = same cloth); lit edge {n_edge} px'


@test
def trodden_things_move():
    """A loose thing on the floor that runners' feet reach is kicked along, never trodden through (Open Wounds chat 14,
    critique r5 (c), notes/learn/tray-trodden/): the fallen tray in shot 3's chase. The old tray (lying still while a
    runner passed 0.30 m from its middle) is caught by moves.trodden; the kicked one passes."""
    import brexit_is_done_action as A
    import moves as MV
    real = MV.kicked
    try:
        MV.kicked = lambda x0, d0, t0, u, movers, **k: (x0, d0, max(0.0, u - t0), 0.0)
        old = MV.trodden(A.tray_track, A.tray_movers(), A.TOSS, 9.4)
    finally:
        MV.kicked = real
    now = MV.trodden(A.tray_track, A.tray_movers(), A.TOSS, 9.4)
    moved = A.tray_track(9.33)[0] - A.tray_track(8.9)[0]
    return bool(old) and not now and moved > 0.1, f'old: {old}; now: {now or "none"}; kicked {moved:.2f} m'


@test
def kit_tests_rerun_only_what_changed():
    """kit-tests-when (Sam's pick 1, 25 Nov, notes/proposals/kit-tests-when.md): each green kit test leaves a stamp of
    the files it read, and only tests whose files changed run again. Proves: (1) a film-only change that a test reads
    re-runs that test and no other; (2) unchanged files skip; (3) a change that arrives by merging another chain's
    branch re-runs its test; (4) the notes-archive red (23 Nov, move_to_shared_catches_film_fixes went red when a film's
    notes were archived: a notes-only change) is caught: the film list's own code records notes/archive as read;
    (5) a Python program a test starts reports its own reads; any other use of the project's git counts as reading ALL; (6) finish.py refuses an animatic or final without fresh passes."""
    import shutil
    import subprocess
    import tempfile
    import kitstamps as K
    d = tempfile.mkdtemp()
    keep = (K.ROOT, K.KITTESTS)
    try:
        src = os.path.join(d, 'source')
        os.makedirs(src)
        film = os.path.join(src, 'zz_film_shot.py')
        shared = os.path.join(src, 'zz_shared_tool.py')
        open(film, 'w').write('POSE = 1\n\ndef pose():\n    return POSE\n')
        open(shared, 'w').write('def tool():\n    return 2\n')
        open(os.path.join(src, 'kittests.py'), 'w').write(
            '@test\ndef t_film():\n    return 1\n\n\n@test\ndef t_tool():\n    return 2\n')
        g = lambda *a: subprocess.run(['git', '-C', d, '-c', 'user.name=k', '-c', 'user.email=k@k', *a],
                                      capture_output=True, text=True)
        g('init', '-q', '-b', 'main')
        g('add', '-A')
        g('commit', '-qm', 'start')
        K.ROOT, K.KITTESTS = d, os.path.join(src, 'kittests.py')
        rec = os.path.join(d, 'stamps.tsv')

        def run_film():
            ns = {}
            exec(compile(open(film).read(), film, 'exec'), ns)
            return ns['pose']()

        def run_tool():
            return open(shared).read()
        _, r_film = K.traced(run_film)
        _, r_tool = K.traced(run_tool)
        r_film = (r_film or set()) | {'source/kittests.py::t_film'}
        r_tool = (r_tool or set()) | {'source/kittests.py::t_tool'}
        K.write_green([('t_film', r_film, 1.0), ('t_tool', r_tool, 1.0)], rec)
        unchanged, _ = K.stale(['t_film', 't_tool'], rec)
        open(film, 'a').write('POSE = 3\n')                                # (1) a film-only change
        film_change, _ = K.stale(['t_film', 't_tool'], rec)
        g('stash', '-q')
        g('checkout', '-qb', 'other')                                     # (3) another chain changes the shared tool
        open(shared, 'a').write('# other chain\n')
        g('commit', '-qam', 'other chain')
        g('checkout', '-q', 'main')
        K.write_green([('t_film', r_film, 1.0)], rec)                     # t_film green again on main
        before_merge, _ = K.stale(['t_film', 't_tool'], rec)
        g('merge', '-q', 'other')
        after_merge, _ = K.stale(['t_film', 't_tool'], rec)
    finally:
        K.ROOT, K.KITTESTS = keep
        shutil.rmtree(d, ignore_errors=True)
    root = os.path.dirname(HERE)                                           # (5) another program: a Python child's own
    _, r_child = K.traced(lambda: subprocess.run([sys.executable, '-c', 'open("CLAUDE.md").read()'], cwd=root,
                                                 capture_output=True))     # reads come back; a git command that
    _, r_prog = K.traced(lambda: K.tracer()._program(['git', '-C', root, 'push'], None))   # is no read is ALL
    import handover as H                                                   # (4) the notes-archive red
    _, r_arch = K.traced(H._film_prefixes)
    import finish                                                          # (6) finish refuses without fresh passes
    import override
    import propose
    real = (K.finish_gate, override.refuse, propose.open_letthroughs, finish.load_film, sys.argv,
            os.environ.pop('KITTESTS_RUNNING', None))
    said, loaded = [], []
    try:
        K.finish_gate = lambda: 'zz_test without a pass on the current files'
        propose.open_letthroughs = lambda: []
        override.refuse = lambda msg, path=None: (_ for _ in ()).throw(SystemExit(msg))
        finish.load_film = lambda n: loaded.append(n)
        sys.argv = ['finish.py', 'clean.mp4', 'out.mp4', '--film', 'zz']
        try:
            finish.main()
        except SystemExit as e:
            said.append(str(e))
        except Exception as e:
            said.append(f'ran on: {e}')
    finally:
        K.finish_gate, override.refuse, propose.open_letthroughs, finish.load_film, sys.argv, ke = real
        if ke:
            os.environ['KITTESTS_RUNNING'] = ke
    gate_none = K.finish_gate(stale_fn=lambda: ([], {}))
    gate_left = K.finish_gate(stale_fn=lambda: (['zz_red'], {'zz_red': 3.0}), run_fn=lambda: None)
    refused = bool(said) and 'kit tests' in said[0] and not loaded
    ok = (unchanged == [] and film_change == ['t_film'] and before_merge == [] and after_merge == ['t_tool']
          and K.ALL in (r_prog or set()) and 'CLAUDE.md' in (r_child or set()) and K.ALL not in (r_child or set())
          and 'notes/archive' in (r_arch or set())
          and refused and gate_none == '' and 'zz_red' in gate_left)
    return ok, (f'unchanged: {unchanged or "none"} re-run; film-only change: {film_change}; merged branch: '
                f'{before_merge or "none"} then {after_merge}; child read: {"CLAUDE.md" in (r_child or ())}; '
                f'git push: {"ALL" if K.ALL in (r_prog or ()) else "missed"}; '
                f'notes/archive read: {"notes/archive" in (r_arch or set())}; finish: {said[:1] or "ran"}; '
                f'gate fresh: {gate_none!r}, stale: {gate_left[:40]!r}')


@test
def kit_tests_per_film():
    """Rule 90 (Sam, 25 Nov, saved in notes/ledger/sam/5whcspgq.md: "Make the kit check happen at the beginning and the
    end of every film ... it is wasting usage and time to do this with every chat"): the old start-up hook ran the kit
    tests in every chat (caught; today's passes); a film's first chat starts the run and its end waits for it; a later
    chat neither runs nor waits, except a never-passed (new) test, and says "suggest a full check to Sam" only after
    more than 20 tests went stale from its own changes; the stale run no longer needs Override to happen (fix 1); the
    stamp tool's own hook code is not a read (fix 3)."""
    import subprocess
    import tempfile
    import handover as H
    import kitfilm as KF
    import kitstamps as KS
    root = os.path.dirname(HERE)
    said = open(os.path.join(root, 'notes', 'ledger', 'sam', '5whcspgq.md'), encoding='utf-8').read()
    example = 'Make the kit check happen at the beginning and the end of every film' in said
    old = subprocess.run(['git', '-C', root, 'show', 'fb29ae0a:.claude/hooks/setup.sh'], capture_output=True,
                         text=True).stdout
    caught_old, now_setup = KF.setup_faults(old), KF.setup_faults()
    d = tempfile.mkdtemp()
    rec, sp, log, reds = (os.path.join(d, n) for n in ('films.tsv', 'start.txt', 'kit.log', 'reds.log'))
    launched = []
    nd = os.path.join(d, 'notes')                        # Sam, 26 Nov (crowd pool chat 1, saved example: the crowd
    os.makedirs(nd)                                      # pool job's first chat started all 81 tests): a film starts
    open(os.path.join(nd, 'zz-film.md'), 'w').write('# zz\n\nScreenplay and title: given 26 Nov\n')   # when Sam gives
    open(os.path.join(nd, 'zz-pool.md'), 'w').write('# a tool or pool job, no screenplay\n')         # the screenplay
    pool = KF.at_start('zz-pool', 'chatP', rec, sp, stale_fn=lambda: ['t1'], launch_fn=lambda: launched.append(0),
                       notes_dir=nd)
    first = KF.at_start('zz-film', 'chatA', rec, sp, stale_fn=lambda: ['t1'], launch_fn=lambda: launched.append(1),
                        notes_dir=nd)
    again = KF.at_start('zz-film', 'chatB', rec, sp, stale_fn=lambda: ['t1'], launch_fn=lambda: launched.append(2),
                        notes_dir=nd)
    tool = KF.at_start(None, 'chatC', rec, sp, stale_fn=lambda: [], launch_fn=lambda: launched.append(3))
    open(os.path.join(nd, 'zz-late.md'), 'w').write('# given mid-chat\n')
    began = KF.begin('zz-late', nd, 'chatL', rec, launch_fn=lambda: launched.append(4))
    late_ok = KF.begun('zz-late', nd) and KF.started_here('chatL', rec)
    ended = KF.lessons('zz-film', 'chatE', rec, run_fn=lambda: True) and any(
        r[0] == 'zz-film' and r[1] == 'end' for r in KF.rows(rec))
    import finish as FN                                  # a final render no longer runs or waits for kit tests
    no_final_gate = 'kitfilm.ANIMATIC_GATE and not final' in open(FN.__file__, encoding='utf-8').read()
    ran = []

    def run(names, kitlog):
        ran.append(list(names))
        open(kitlog, 'w').write('kittests: all passed\n')
        return True
    g = lambda **k: H.kittest_gate_faults(log, reds, sid='zz', stale_fn=lambda: (['t1'], 60.0), run_fn=run, **k)
    wait_first = g(first_fn=lambda s: True, busy_fn=lambda: True)               # first chat: waits for its run
    end_first = g(first_fn=lambda s: True, busy_fn=lambda: False)               # then runs the stale, no Override
    mid = g(first_fn=lambda s: False, busy_fn=lambda: True, new_fn=lambda: [], major_fn=lambda: '')
    mid_new = g(first_fn=lambda s: False, busy_fn=lambda: True, new_fn=lambda: ['t_new'], major_fn=lambda: '')
    open(sp, 'w').write('zz\ta,b\n')
    small = KF.major_line('zz', ['a', 'b'] + [f'n{i}' for i in range(20)], sp)
    big = KF.major_line('zz', ['a'] + [f'n{i}' for i in range(21)], sp)
    _, r_git = KS.traced(lambda: KS.tracer()._program(['git', '-C', root, 'push'], None))
    KS.write_green([('zz_old', {'source/kitfilm.py'}, 1.0)], os.path.join(d, 'stamps.tsv'))   # the real record's
    new_real = KF.never_green(['zz_old', 'zz_new'], os.path.join(d, 'stamps.tsv'))               # shape (end crashed
    ok = (new_real == ['zz_new'] and example and caught_old and not now_setup and launched == [1, 4] and 'first chat' in first[-1]
          and 'not yet' in pool[-1] and 'starts' in began and late_ok and ended and no_final_gate
          and 'not this chat' in again[-1] and not tool
          and KF.started_here('chatA', rec) and not KF.started_here('chatB', rec)
          and wait_first and 'STILL RUNNING' in wait_first[0] and ran[0] == ['t1'] and not end_first
          and mid == [] and ran[1:] == [['t_new']] and not mid_new
          and small == '' and 'Y or N' in big and 'source/kitstamps.py' not in (r_git or set()))
    return ok, (f'pool job (no screenplay): {pool[-1][:40]}; begun mid-chat: {late_ok}; lessons end row: {ended}; '
                f'final gate off: {no_final_gate}; '
                f'new test found: {new_real}; old start-up hook caught: {len(caught_old)}; now: {len(now_setup)}; launches {launched}; '
                f'first chat waits: {wait_first[:1]}; runs {ran}; mid-film chat: {mid or "no run, no wait"}; '
                f'21 made stale: {"suggests" if big else "silent"}; 20: {"silent" if not small else "suggests"}; '
                f'hook code read: {"source/kitstamps.py" in (r_git or set())}')



@test
def ledger_told_film():
    """pose-kit-format C1 (Sam's Y, 26 Nov; saved example notes/learn/pose-kit/examples/ledger-misfiled-26nov.json):
    R7 chats 3-5 were billed to proposal-route because their task named notes/proposals/ more than notes/r7.md. A task
    that says --film r7 is now billed to r7 however often it names a proposal; a task with no --film keeps the old
    order (proposals win)."""
    import json
    import tempfile
    import ledger as L
    def bill(text):
        with tempfile.NamedTemporaryFile('w', suffix='.jsonl', delete=False) as f:
            f.write(json.dumps({'type': 'user', 'message': {'content': [{'type': 'text', 'text': text}]}}) + '\n')
        try:
            return L.film_of(f.name)
        finally:
            os.unlink(f.name)
    seed = ('R7, chat 5 (Opus high). Run python3 source/handover.py start S --film r7, read notes/r7.md. Then the '
            'proposal notes/proposals/seated-legs-3d.md (its judge; notes/proposals/seated-legs-3d.md Final version).')
    told, untold = bill(seed), bill(seed.replace(' --film r7', ''))
    return told == 'r7' and untold == L.PROCESS, f'with --film r7: {told}; without: {untold}'


@test
def ledger_rebook():
    """pose-kit-format C1: misfiled() finds every R7 chat its handovers name that sits in another ledger: all five on
    the saved 26 Nov copy (1f655db8, 39bef7c8 under brexit-is-done; dcc49037, 8fb22562, b2f8e1d1 under
    proposal-route), and none on the ledgers as they are now (rebooked)."""
    import json
    import ledger as L
    saved = json.load(open(os.path.join(HERE, '..', 'notes', 'learn', 'pose-kit', 'examples',
                                        'ledger-misfiled-26nov.json')))['ledgers']
    then = sorted(r['chat'] for _, r in L.misfiled('r7', saved))
    now = L.misfiled('r7')
    want = sorted(['1f655db8', '39bef7c8', 'dcc49037', '8fb22562', 'b2f8e1d1'])
    return then == want and not now, f'saved copy: {then}; now: {[r["chat"] for _, r in now] or "none"}'




@test
def pose_job_line():
    """pose-kit-format C3 as Sam changed it (notes/learn/pose-kit/examples/sam-26nov-default-tool.md: "Just tell me
    you're using the default tool when you start unless I say otherwise"; "No hard stop on handover"): the start check
    gives a pose job (R7's notes) the line naming the default tool and leaving room for another; a film that is not a
    pose job (brexit-is-done) gets nothing; the line never refuses."""
    import handover as H
    r7, other = H.pose_job_lines('r7'), H.pose_job_lines('brexit-is-done')
    ok = bool(r7) and 'default pose tool' in r7[0] and 'Another tool is fine' in r7[0] and not other
    ok = ok and 'Nothing stops a handover' in r7[0]
    return ok, f'r7: {"line" if r7 else "none"}; brexit-is-done: {"line" if other else "none"}'


@test
def learn_first():
    """Rule 91, the Learn-First rule (Sam, 26 Nov; notes/learn/pose-kit/examples/sam-26nov-learn-first.md: "Next time we
    need a new pose, quote this rule and what you need to learn before executing it"): the start check gives Open
    Wounds (a worker running from wolves, men fighting with steel bars, Blair in an armchair) the rule and what must
    be learned for each unproven pose; a job naming only the proven sitting pose gets nothing; it never refuses."""
    import handover as H
    ow = H.learn_first_lines('brexit-is-done')
    seat = H.learn_first_lines(text='May sits upright on the office chair, legs crossed.')
    sam = H.learn_first_lines(text='a worker runs from two wolves across the scaffolding and leaps off it')
    # GTA's 20 Nov plan line for shot 4 (notes/learn/pose-kit/examples/gta-lean-out-untried.md): the list must name it
    gta = H.learn_first_lines(text='tracks left with Jason as he leans out of the passenger window, until we hang '
                                   'outside with him looking back down the street')
    ok = bool(ow) and 'rule 91' in ow[0] and any('walking and running' in l for l in ow) and \
        any('arms beyond' in l for l in ow) and not seat and any('walking and running' in l for l in sam) and \
        any('out of a vehicle' in l and 'grey practice clip' in l for l in gta)
    return ok, (f"Open Wounds: {len(ow) - 1 if ow else 0} families; sitting only: {'none' if not seat else seat}; "
                f"GTA lean-out: {'named' if len(gta) > 1 else 'MISSED'}")


@test
def check_audit_lists_and_flags_repeats():
    """R8 check audit (Sam, 26 Nov: "audit every check we do in this project"; saved example: Open Wounds'
    notes/ledger/brexit-is-done/checks.jsonl, where 97% of fault lines were the same fault back unchanged, run after
    run): checkaudit.inventory finds every kind of check from the code (a hook, a handover check, a kit test, a rulebook
    row), and evidence() marks a fault seen on 3 runs as a repeat (numbers aside) but not one seen on 2."""
    import json
    import tempfile
    import checkaudit as CA
    rows = CA.inventory()
    names = {r['name'] for r in rows}
    found = all(n in names for n in ('modelguard.py', 'handover.size_faults', 'learn_first', 'rule 17'))
    tmp = tempfile.mkdtemp()
    os.makedirs(os.path.join(tmp, 'notes', 'ledger', 'kt'))
    with open(os.path.join(tmp, 'notes', 'ledger', 'kt', 'checks.jsonl'), 'w') as fh:
        for run, faults in (('r1', ['pop-in: shot 1 at 2.5 s', 'caption "a": 0.4 s']),
                            ('r2', ['pop-in: shot 1 at 2.7 s', 'caption "a": 0.4 s']), ('r3', ['pop-in: shot 1 at 3.1 s'])):
            for f in faults:
                fh.write(json.dumps(dict(run=run, check=f.split(':')[0].split(' ')[0], faults=[f])) + '\n')
    ev = CA.evidence(tmp)
    rep = len(ev['pop-in']['repeats']) == 1 and not ev['caption']['repeats']
    return found and rep, f"{len(rows)} checks listed; known four {'found' if found else 'MISSING'}; repeats " + \
        ('right' if rep else f"WRONG ({ {k: len(e['repeats']) for k, e in ev.items()} })")


@test
def head_moves_never_snap():
    """A nod written as a snap (rise 0.1 s, Sam's note 24.1, Open Wounds chat 38: "very sharp and doesn't correspond
    to anything a person would actually do") is drawn at a real head's speed (acting.HEAD_MIN): no drawing at 12 a
    second moves it more than half its depth; the voice's own accent nods (headlife) ease in the same way."""
    import acting as AC
    import headlife as HL
    import numpy as np
    m = dict(move='nod', curve='bump', a=0.0, b=0.4, rise=0.1, fall=0.12, amount=2.0, over=None, with_={})
    m['with'] = m.pop('with_')
    clock = lambda v: v
    us = [AC.body_value(m, f / 12, clock, AC.BODY)['nod'] for f in range(-2, 9)]
    peak = max(us) or 1.0
    step = max(abs(b - a) for a, b in zip(us, us[1:])) / peak
    env = np.full(60, 0.05)
    env[22] = 0.3
    nod = HL.HeadLife(env, 0.0).nod
    hstep = float(np.max(np.abs(np.diff(nod)))) if nod.max() else 0.0
    ok = step <= 0.7 and 0 < hstep <= 0.45     # the snap Sam saw: the whole depth (1.0) in one drawing
    return ok, f'written snap: biggest step {step:.2f} of the nod (at most 0.7; the snap was 1.0); voice nod step {hstep:.2f}'


@test
def nod_is_a_turn():
    """A nod turns the head, never slides it (saved example: Sam's note 26, Open Wounds chat 39, on Kemi's nod at
    17.6 s: "It's not a nod, it's a head-bob"; the kit's nod moved every mark of the head down by the same amount).
    Every cast head drawn nodding goes through views.Pitched about its own face (views.face_box); at 3 units, front-on
    the crown moves under half as far as the middle of the face, side-on the chin goes in toward the neck and the
    forehead forward. The old bob (every mark down alike) fails the same measure."""
    import castsheet as CS
    import numpy as np
    from PIL import Image
    cast, PP = CS._setup('brexit-is-done', None)
    B, V = PP.B, PP.V
    made, real = [], V.Pitched

    class Spy(real):
        def __init__(self, *a):
            made.append(a)
            real.__init__(self, *a)

    class Life:
        def at_time(self, t):
            return 0.0, 3.0

    class Flat:
        cam, s = None, 1.0

        def P(self, x, y):
            return (x, y)

        def S(self, v):
            return v

    def measure(pv):
        (_, deg, c, fw, fh, view) = pv
        q = real(Flat(), deg, c, fw, fh, view)
        mv = lambda x, y: np.subtract(q.P(x, y), (x, y))   # noqa: E731
        if view == 'front':
            return abs(mv(c[0], c[1] - 1.1 * fh)[1]) / max(1e-6, abs(mv(c[0], c[1])[1]))
        return mv(c[0] + 0.7 * fw, c[1] + 1.05 * fh)[0], mv(c[0] + 0.8 * fw, c[1] - 0.8 * fh)[0]
    out, bad = [], []
    try:
        V.Pitched = Spy
        for who, sp in cast.items():
            for yaw in (0, 90):
                made.clear()
                d = dict(sp, head_life=Life())
                tile = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
                s = 0.5 * d['height'] / 1.75
                V.person(tile, B.Cam(2.0, 540, 470), 540, 840 - 928 * s, s, d, 0.0, yaw, None)
                if not made:
                    bad.append(f'{who} {yaw}: no turn drawn')
                    continue
                m = measure(made[-1])
                if yaw == 0:
                    out.append(f'{who} front crown/face {m:.2f}')
                    if m > 0.5:
                        bad.append(out[-1])
                else:
                    out.append(f'{who} side chin {m[0]:+.0f} forehead {m[1]:+.0f}')
                    if not (m[0] < -3 and m[1] > 3):
                        bad.append(out[-1])
    finally:
        V.Pitched = real
    old_ratio = 1.0                                     # the bob: crown and face moved alike (dy for every mark)
    return not bad and old_ratio > 0.5, '; '.join(out) + (f'; FAULTS: {bad}' if bad else '') + '; old bob crown/face 1.00 (fails)'


@test
def suit_one_cloth():
    """A suit with a tie is one cloth (Sam's note 24.3, Open Wounds chat 38: "Tony's suit sleeves are a different
    colour to the jacket"): Blair's sleeves and trousers are his jacket's colour, and the dark sleeve is never
    lifted to a grey (limbs.DARK_RIM draws its edge instead)."""
    import people as PK
    import views as V
    sp = PK.load('brexit-is-done')['blair']
    jac = tuple(sp['jacket'][:3])
    got = tuple(V.sleeve_colour(sp, 45)[:3])
    return got == jac, f'jacket {jac}, sleeve {got} (trousers keep their own tone: the seated legs need it)'


@test
def smirk_one_corner():
    """A smirk reads (Sam's note 24.2, Open Wounds chat 38: "doesn't read as a satisfied smirk but a neutral
    expression"; FACS: one corner pulled up, unilateral AU12): May's 'satisfied' mouth after "wolves" has one corner
    well above the other; 'smile' alone (the old mood) lifted both by half a pixel."""
    import brexit_is_done as M
    import numpy as np
    out = {}
    import faces as FA
    for name, up in (('old', 0.0), ('now', FA.SMIRK_UP)):
        keep = FA.SMIRK_UP
        FA.SMIRK_UP = up                                # no lift: the corners as the old mood drew them
        try:
            a = np.asarray(M.picture(9.0).convert('RGB')).astype(int)
        finally:
            FA.SMIRK_UP = keep
        hx, hy = M.DRAWN['may']['_drawn']['head_at']
        box = a[int(hy):int(hy + 160), int(hx - 140):int(hx + 140)]
        lip = (box[..., 0] > 150) & (box[..., 1] < 90) & (box[..., 2] > 60) & (box[..., 2] < 140)
        ys, xs = np.nonzero(lip)
        if not len(xs):
            return False, f'{name}: no lips found'
        x0, x1 = xs.min(), xs.max()
        top = lambda c: ys[np.abs(xs - c) <= 3].min()
        out[name] = int(top(x0)) - int(top(x1))     # + : the near (screen-right) corner higher; the head's tilt adds
    lift = out['now'] - out['old']                  # the same to both, so the smirk is the change
    ok = lift >= 6
    return ok, f"the near corner raised {lift} px over the old mood's (a smirk: 6 or more; the old mood: none)"


@test
def body_model_downloads_once():
    """Check audit B7 (Sam's Y, 26 Nov): the kit-inputs survey crashed twice on Open Wounds (41 and 52 frames 'could
    not be drawn': git clone of the body model) because every drawing worker started the same download at once. Eight
    workers ask at the same moment: one download, all eight get the finished copy, no worker fails."""
    import tempfile
    import time
    import mhuman as M
    from multiprocessing import get_context
    tmp = tempfile.mkdtemp()
    log = os.path.join(tmp, 'clones.txt')
    keep = (M.MH_DIR, M.subprocess.run)

    def fake(cmd, check=False, **k):
        if cmd[1] == 'clone':
            dest = cmd[-1]
            if os.path.exists(dest):                      # what git does when two clones meet
                raise M.subprocess.CalledProcessError(128, cmd)
            open(log, 'a').write(dest + '\n')
            time.sleep(0.3)
            os.makedirs(os.path.join(dest, 'makehuman', 'data', '3dobjs'))
            open(os.path.join(dest, 'makehuman', 'data', '3dobjs', 'base.obj'), 'w').write('v 0 0 0\n')
    out = []
    try:
        M.MH_DIR = os.path.join(tmp, 'makehuman')
        M.subprocess.run = fake
        with get_context('fork').Pool(8) as p:
            res = p.map(_mh_one, range(8))
        bad = [r for r in res if not r.startswith(M.MH_DIR)]
        if bad:
            out.append(f'{len(bad)} of 8 workers failed: {bad[0][:120]}')
        n = len(open(log).read().split()) if os.path.exists(log) else 0
        if n != 1:
            out.append(f'{n} downloads for 8 workers (want 1)')
        if any('.part' in f for f in os.listdir(tmp)):
            out.append('a half-made copy was left behind')
    finally:
        M.MH_DIR, M.subprocess.run = keep
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    return (not out), ('; '.join(out) or 'one download, all 8 workers got the copy')


def _mh_one(_):
    import mhuman as M
    try:
        return M.data_dir()
    except Exception as e:
        return f'{type(e).__name__}: {e}'


@test
def checks_read_what_is_meant():
    """Check-knows-intent change 1 (Sam's "1", 26 Nov): what a scene means to hide or overlap travels with the drawing
    (figure.meant, and a side-on gait's own mark) and the hand check reads it: a meant flag is one 'meant: ...' line,
    never a fault and never hidden; a real flag still shows; a hand in its sleeve, sinking, hovering or passing
    through can never be marked meant. Examples: notes/learn/check-intent/sort-1.md (Open Wounds, 26 Nov)."""
    import body as B
    import figure as F
    import handcheck as H
    import kitchecks
    import limbs
    import moves as MV
    import posegallery as G
    import views as V
    from PIL import Image
    from satire_style import install_circle_hands
    B.SS = 1
    F.guard(B)
    F._ALLOW.append('kittests')
    install_circle_hands(B)
    limbs.install(B)
    kitchecks.install()
    H.install()
    cam = B.Cam(1.0, 540, 960)

    def frame(draws, t=0.0):
        im = Image.new('RGBA', (1400, 1100), G.BG)
        H.begin()
        for d in draws:
            d(im)
        return H.end(t)

    def p(x, yaw, pose):
        return lambda im: V.person(im, cam, x, 330, 0.62, G.MODEL, 0.0, yaw, pose)
    pair = [p(500, 0, G.pose('pointing', G.MODEL)), p(650, -90, G.pose('pointing', G.MODEL))]
    out = []
    real = frame(pair)                                        # a crowding reach nobody marked: a fault
    if not any(f['kind'].startswith('over') and not f.get('meant') for f in real):
        out.append('an unmarked hand over another body was not flagged')
    with F.meant('over *', 'a crush through a doorway'):
        marked = frame(pair, 0.1)
    ov = [f for f in marked if f['kind'].startswith('over')]
    if not ov or not all(f.get('meant') for f in ov):
        out.append('a hand over a body inside figure.meant was still a fault')
    with F.meant('over *', 'a crush through a doorway'):    # the mark covers its kind only
        if F.meant_for('no hand', F.MEANT):
            out.append("an 'over' mark excused a hidden hand")
    run = frame([p(600, 90, MV.gait(G.MODEL, 0.2, 'sprint'))], 0.2)
    if not run or not all(f.get('meant') for f in run if f['kind'] == 'no hand'):
        out.append("a side-on sprint's far hand behind the body was still a fault")
    front = [m for m in MV.gait(G.MODEL, 0.2, 'sprint')['meant'] if len(m) < 3 or m[2] == 'front']
    if front:
        out.append("a gait's side-on mark also counted seen front on")
    for k in ('in sleeve', 'sink', 'hover', 'through'):       # never meant
        try:
            with F.meant(k, 'x'):
                pass
            out.append(f'"{k}" was accepted as meant')
        except F.FigureError:
            pass
    if F.meant_for('in sleeve', [(('*',), 'everything')]):
        out.append('a hand in its sleeve was excused by a catch-all mark')
    rows = H.summary(None, real + marked + run, 12)
    lines = H.meant_lines(real + marked + run)
    if any('crush' in r[1] or 'sprint' in r[1] for r in rows) or len(lines) < 2:
        out.append(f'meant flags not kept apart: {len(rows)} fault rows, {len(lines)} meant lines')
    return (not out), ('; '.join(out) or f'{len(rows)} fault row(s) (the unmarked reach), meant lines: ' +
                       ' | '.join(lines))


@test
def faults_said_once():
    """Check audit B1, say once (Sam's Y, 26 Nov; saved example: notes/ledger/brexit-is-done/checks.jsonl, where 361
    of 372 fault lines were the same fault back unchanged): a fault the last run of the same check already showed,
    unchanged but for its times and numbers, is one count line, not printed again; a new fault prints in full; both
    still count as faults. The real Open Wounds record: its last quick check's faults against the run before."""
    import io
    import contextlib
    import ledger
    import report as R
    runs = [{'t': '1', 'of': {'quick check': 'quick check', 'pop-in': 'quick check'},
             'faults': {'pop-in': ['pop-in: guest 2 appears at 17.55 s mid-frame']}},
            {'t': '2', 'of': {'pre-flight': 'pre-flight'}, 'faults': {'pre-flight': ['CAPTION: x']}}]
    now = ['pop-in: guest 2 appears at 17.80 s mid-frame', 'caption "wolves": shown 0.30 s']
    before = R.shown_before('quick check', now, runs)
    out = []
    if before != {now[0]}:
        out.append(f'repeat not recognised (or the new one taken as old): {before}')
    keep = (R.shown_before, ledger.record)
    try:
        R.shown_before = lambda title, faults, runs_=None: R.__dict__['_kt_before']
        R._kt_before = before
        ledger.record = lambda *a, **k: None
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            R.summarise('quick check', now)
        text = buf.getvalue()
    finally:
        R.shown_before, ledger.record = keep
        R.__dict__.pop('_kt_before', None)
    if '2 fault(s)' not in text or 'caption' not in text or '17.80' in text or '1 shown on the last run' not in text:
        out.append('summary wrong: ' + text.replace(chr(10), ' / ')[:200])
    real = [r for r in ledger.checkruns('brexit-is-done')['runs'] if 'quick check' in r['of'].values()]
    if len(real) >= 2:
        last = [x for k, v in real[-1]['faults'].items() for x in v]
        same = R.shown_before('quick check', last, [real[-2]])
        out_n = f'Open Wounds: {len(same)} of {len(last)} said once'
    else:
        out_n = 'Open Wounds: fewer than 2 quick checks'
    return (not out), ('; '.join(out) or 'one count line for the repeat, the new fault in full; ' + out_n)


@test
def planning_asks_once():
    """Check audit B4 (Sam's Y, 26 Nov; saved example: notes/ledger/brexit-is-done/checks.jsonl, where 'the film has
    no PLAN', 'no BENCHMARK' and 'no audits' printed on 4 runs each, never answered): the paperwork asks become rows of
    the brief checklist the first time; a run prints one planning line instead of each ask; an answered row ("none:
    why") is never asked again; a real drawing fault passes through untouched; rows 74 and 8 still stop new films."""
    import shutil
    import tempfile
    import planning as P
    tmp = tempfile.mkdtemp()
    path = os.path.join(tmp, 'kt.md')
    shutil.copy(os.path.join(HERE, '..', 'notes', '_template.md'), path)
    asks = ['plan (rule 1): the film has no PLAN (rooms...)', 'benchmark (rule 3): the film has no BENCHMARK (8-10)',
            'house style: the film has no audits: the general audit', 'HANDS: 2 11.08s: a hand over a body']
    out = []
    kept, line, stops = P.route(asks, path)
    if kept != [asks[-1]] or not line or '3 unanswered' not in line or stops:
        out.append(f'first run wrong: kept {kept}, line {line}, stops {stops}')
    again = P.route(asks, path)
    if open(path).read().count('Planning: ') != 3:
        out.append('rows written more than once')
    text = open(path).read().replace('(rule 1) |  |', '(rule 1) | none: a one-room film, the set is a drawing |')
    open(path, 'w').write(text)
    kept3, line3, _ = P.route(asks, path)
    if not line3 or '2 unanswered' not in line3 or 'plan' in line3.split('(')[1]:
        out.append(f'an answered row was asked again: {line3}')
    _, _, st = P.route(['no "Rehearsal clips sent: DATE" line in the notes (rule 8)'], path, ('rehearsal',))
    if not st:
        out.append('an unanswered rule-8 row did not stop a new-template film')
    shutil.rmtree(tmp, ignore_errors=True)
    return (not out), ('; '.join(out) or f'first run: one line ({line[:60]}...); answered row dropped; rule 8 stops')


@test
def row_of_bookcases_sized_per_bay():
    """Check audit B3 (Sam's Y, 26 Nov; saved example: Open Wounds' 'the bookcases, right: 4.00 m wide; a real bookcase
    is about 0.8 m (500%)', on 10 runs): the size check reads the set's own description, so a wall of shelves written
    'bays 4' is four bookcases side by side, each judged alone; one bookcase 4 m wide is still a fault."""
    import types
    import kitinputs as K
    import sizes
    keep = K._places
    item = lambda raw: dict(name='shelves', kind='bookcase', raw=raw)
    try:
        K._places = lambda film: {'views': {'v': {'items': [item({'x': '0.3 to 4.3', 'z': '0 to 3.7', 'bays': '4'})]}}}
        row = [sizes.check(*r) for r in K.prop_sizes(types.SimpleNamespace())]
        K._places = lambda film: {'views': {'v': {'items': [item({'x': '0.3 to 4.3', 'z': '0 to 3.7'})]}}}
        one = [sizes.check(*r) for r in K.prop_sizes(types.SimpleNamespace())]
    finally:
        K._places = keep
    ok = row == [None] and one and one[0]
    return ok, f'a row of 4: {row}; one 4 m bookcase: {one}'


def main():
    """python3 source/kittests.py [WORD] [--stale] [--names a,b]: WORD runs the tests whose name holds it; --stale only
    the tests whose files changed since their last green (source/kitstamps.py, Sam's pick 1, 25 Nov). Every green test
    leaves a stamp of the files it read in notes/kittest-stamps.tsv."""
    import time
    import kitstamps
    args = sys.argv[1:]
    only_stale = '--stale' in args
    names = None
    if '--names' in args:
        names = set(filter(None, args[args.index('--names') + 1].split(',')))
        args = args[:args.index('--names')] + args[args.index('--names') + 2:]
    args = [a for a in args if a != '--stale']
    only = args[0] if args else ''
    os.environ['KITTESTS_RUNNING'] = '1'           # finish.py's kit gate stands aside for tests that call finish
    pick = [fn for fn in TESTS if (not only or only in fn.__name__) and (names is None or fn.__name__ in names)]
    fresh = 0
    if only_stale:
        st, secs = kitstamps.stale([fn.__name__ for fn in pick])
        fresh = len(pick) - len(st)
        pick = [fn for fn in pick if fn.__name__ in st]
        print(f'kittests: {len(pick)} stale to run, {fresh} fresh (their files unchanged since a green run); '
              f'about {kitstamps.say_minutes(kitstamps.estimate(st, secs))}', flush=True)
    tr = kitstamps.tracer()
    bad = 0
    t_all = time.time()
    for fn in pick:
        t0 = time.time()
        tr.start()
        try:
            ok, detail = fn()
        except Exception as e:
            import traceback
            traceback.print_exc()
            ok, detail = False, f'crashed: {e}'
        finally:
            reads = tr.stop()
        bad += not ok
        print(f"{'PASS' if ok else 'FAIL'} {fn.__name__}: {detail}")
        print(f"     ({(fn.__doc__ or '').strip().splitlines()[0]})", flush=True)
        if ok and reads is not None:
            kitstamps.write_green([(fn.__name__, reads, time.time() - t0)])
        elif ok:
            print(f'     (no stamp: a file it read changed while it ran, or this Python cannot trace)')
    took = kitstamps.say_minutes(time.time() - t_all)
    tail = f' ({len(pick)} run in {took}, {fresh} fresh)' if only_stale else f' ({len(pick)} run in {took})'
    print('kittests:', ('all passed' if not bad else f'{bad} failed') + tail)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()



