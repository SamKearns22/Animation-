#!/usr/bin/env python3
"""kittests: each shared-kit check tested against the film fault that taught it (Build list 27 Oct: "each with a test").
A test puts the old, faulty version back for a moment (from git history, written out here), and passes only if the
check catches the old version AND passes the fixed one.

    python3 source/kittests.py            all of them (a few minutes)
    python3 source/kittests.py hands      only the tests whose name contains 'hands'
"""
import math
import re
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


def _hand_faults(film, times, who=None):
    """handcheck's findings for these frames of a film (drawn here, one after another)."""
    import burnham as B
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
    """Rule 42: every gallery pose passes the hand check from every view except those its AVOID lists."""
    import posegallery as PG
    argv = sys.argv
    sys.argv = ['posegallery', os.path.join(HERE, 'data', 'pose-gallery.jpg')]
    try:
        bad = PG.main()
    finally:
        sys.argv = argv
    want = {n: set(v) for n, v in PG.AVOID.items()}
    got = {n: v for n, v in PG.results.items() if v}
    return not bad and got == want, f'{len(PG.results)} poses; failing views {got or "none"} (AVOID lists {want})'


# ------------------------------------------------------------------------------------------------ rule 43: looks
@test
def looks_at_the_shot_camera():
    """Patriots 3 note 11: the Loader's profile at the Gunner (41-42.6 s) read as looking at the wall."""
    import burnham as B
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
    import burnham as B
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
        named = E.lock_fault('x', faults_named=True)
        E.write_pass('x', 0)
        final_quick = E.lock_fault('x', final=True)           # pictures not yet checked: no final
        E.write_pass('x', 0, pictures=True)
        final_ok = E.lock_fault('x', final=True)
    finally:
        E.PASSES = real
    return bool(none) and ok is None and bool(faults) and named is None and bool(final_quick) and final_ok is None, \
        (f'no pass: {bool(none)}; pass: {ok is None}; 3 faults: {bool(faults)}; named: {named is None}; '
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
    import burnham as B
    import patriots3_cast as C
    import views as V
    B.SS = 1

    def seen():
        out = []
        for deg in (0, 40, 180):
            im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
            out.append(V.person(im, B.Cam(1.0, 540, 960), 540, 700, 0.8, dict(C.GUNNER), 0.0, deg)['_drawn']['mouth'])
        return out
    real = B.mouth
    a = seen()
    B.mouth = lambda *x, **k: None
    try:
        b = seen()
    finally:
        B.mouth = real
    return a == [True, True, None] and b == [False, False, None], f'with mouth: {a}; mouth removed: {b}'


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
    import burnham as B
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
    import burnham as B
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
    import burnham as B
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
    ok = f'({C.HELPER}, model opus' in line and refused == list(C.READ_ONLY) and (builtin or own)
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
    import burnham as B
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
def estimate_forecast_and_alarm():
    """Rule 24 (Job M; Sam, 13 Nov): the stages' forecast is spent / share of the plan done x estimate, an unplanned
    round pushes it up; the budget stop fires at the budget and at every 10% over it, once each, and cannot be
    switched off (an old alarms_off does nothing)."""
    import ledger
    d = {'film': 'zz', 'estimate': 10.0, 'chats': [{'cost': 0.0, 'round': None, 'notes': 0, 'repeats': []}],
         'checks': {}, 'stages': ledger.parse_stages('cast 3, sets 2, moves 2, animatic1 1, round 1.5, final 0.5'),
         'alarms_off': 'old switch'}
    spend = lambda x: d['chats'][0].update(cost=x)
    spend(3.0); ledger.mark_stage(d, 'cast')
    on_plan = ledger.forecast(d)                                   # 3 of 3 planned: lands at 10
    spend(7.0)
    mid = ledger.forecast(d)[2]                                    # 7 + (2 + 1 + 1.5 + .5) x 1 = 12
    ledger.mark_stage(d, 'sets')
    over = ledger.forecast(d)[2]                                   # 7 of 5 planned: lands at 14
    under = ledger.budget_stop(d) is None                          # 7 of 10: quiet
    spend(10.0); at = ledger.budget_stop(d); again = ledger.budget_stop(d)
    spend(10.9); quiet = ledger.budget_stop(d) is None             # 109%: not yet the next step
    spend(11.0); five = ledger.budget_stop(d)                      # 110%: stops again
    spend(13.0); jump = ledger.budget_stop(d); step = d['budget_stop']   # 130%: one stop, at step 4
    ledger.mark_stage(d, 'moves'); ledger.mark_stage(d, 'animatic1'); ledger.mark_stage(d, 'round')
    extra = ledger.mark_stage(d, 'round')                          # a second round, not in the plan: no share
    ok = (on_plan == (3.0, 3.0, 10.0) and mid == 12.0 and over == 14.0 and under and at and 'Stop' in at
          and again is None and quiet and five and jump and step == 4 and extra.get('unplanned') and extra['pct'] == 0)
    return ok, f'on plan {on_plan}, mid-stage {mid}, after sets {over}, stops at 100% {bool(at)}, once {again is None}, ' \
               f'110% {bool(five)}, 130% step {step}, alarms_off ignored {bool(at)}'


@test
def stage_share_stop():
    """Rule 24 (Sam, 11 Nov): the chat is stopped when a stage reaches its share (before: only a quarter over the film's
    whole estimate), once, and again half a share on; a stage under its share, or already marked done, is quiet."""
    import ledger
    d = {'film': 'zz', 'estimate': 10.0, 'chats': [{'cost': 0.0, 'round': None, 'notes': 0, 'repeats': []}],
         'checks': {}, 'stages': ledger.parse_stages('cast 3, sets 2, moves 2, animatic1 1, round 1.5, final 0.5')}
    spend = lambda x: d['chats'][0].update(cost=x)
    spend(2.9); under = ledger.stage_alarm(d)                      # cast at 2.9 of 3
    spend(3.1); first, again = ledger.stage_alarm(d), ledger.stage_alarm(d)
    old_way = 3.1 >= d['estimate']                                 # the only spend stop before: the whole estimate
    spend(4.7); half_on = ledger.stage_alarm(d)                    # 1.5 shares
    ledger.mark_stage(d, 'cast')
    spend(6.0); sets_under = ledger.stage_alarm(d)                 # sets at 1.3 of 2
    spend(6.8); sets_stop = ledger.stage_alarm(d)                  # sets at 2.1 of 2, the film at 68% of its estimate
    ok = (under is None and first and "'cast'" in first and 'stop this work' in first and again is None and not old_way
          and half_on and sets_under is None and sets_stop and "'sets'" in sets_stop and 'moves 2' in sets_stop)
    return ok, (f"cast at 2.9 of 3: quiet {under is None}; at 3.1: stopped {bool(first)}, once {again is None}; half a "
                f"share on: {bool(half_on)}; sets at 2.1 of 2 with the film at 68% of its estimate: stopped "
                f"{bool(sets_stop)} (before: nothing until 100%)")


@test
def copies_in_a_group():
    """Job K (Sam: Y, 10 Nov): two people drawn from one copy in one frame are flagged (Ad-Vanced Notice's officers
    before they were varied); a varied pair passes; COPIES_OK lets a meant pair through."""
    import types
    from PIL import Image
    import burnham as B
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
    a likeness head never is (Vance stays as measured)."""
    import numpy as np
    from PIL import Image
    import burnham as B
    import views as V
    import patriots4_cast as P4
    import ad_vanced_notice_cast as AC
    B.SS = 1

    def face(sp):
        im = Image.new('RGBA', (1080, 1920), (238, 234, 228, 255))
        V.person(im, B.Cam(1.0, 540, 960), 540, 1150, 2.2, dict(sp), 0.0, 0)
        return np.asarray(im.convert('L'), np.int16)
    plain = dict(AC.MAN, lopsided=None)
    changed = float((np.abs(face(AC.MAN) - face(plain)) > 40).mean())
    likeness = [n for n, sp in AC.CAST.items() if n != 'man' and P4.lop(sp)]
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
    import burnham as B
    import views as V
    import ad_vanced_notice_cast as C
    import turnhead as TH
    from ed import curve
    B.SS = 1

    def head(sp, yaw):
        im = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
        V.person(im, B.Cam(1.0, 540, 960), 540, 1060, 1.25, dict(sp), 0.0, yaw)
        return np.asarray(im.crop((375, 620, 705, 1020)).convert('RGB')).astype(int)
    out = []
    # 1. a person with a measured front design but no turned head: recorded (pre-flight names it), then built
    keep = TH.PEOPLE.pop('man')
    del TH.MISSING[:], TH.SEEN[:]
    try:
        head(C.MAN, 90)
    finally:
        TH.PEOPLE['man'] = keep
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
    # 4. Vance's turned heads unchanged (pixel for pixel, as drawn before the shared tool, 8 Nov note 44)
    vh = hashlib.md5(b''.join(head(C.VANCE, y).astype(np.uint8).tobytes() for y in (45, 90, 135, 180))).hexdigest()
    out.append(f'Vance unchanged: {vh == VANCE_TURNED_MD5}')
    ok = caught and fixed and new_g >= old_g + 15 and new_h < old_h - 0.06 and vh == VANCE_TURNED_MD5
    return ok, '; '.join(out)


VANCE_TURNED_MD5 = 'f17956f352af1555f79635c0fdf11811'   # main line c6b007a, before the shared tool


@test
def lying_shirt_and_nape():
    """Job I lying fixes (Sam, 11 Nov, for every character): slumped against a wall the shirt was a stiff box (lying
    16: square shoulders, straight sides), now bent as cloth (lying_flat.Slump); lying with the back of the head to
    us, the neck was drawn again over the head as a square block (18, a blindfold with the driver's hair band), now
    the head is inked all round with no neck over it (turnhead, nape_in_head). Standing views are untouched."""
    import numpy as np
    from PIL import Image
    import burnham as B
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
def lying_neck_from_behind():
    """Job I lying 18 (Sam, 11 Nov, "fix the neck in 14 and 18", a repeated note): curled up and seen from behind,
    the head sat straight on the collar with no neck (the shirt's back and the arm round the head were drawn over
    it) and the back collar stood up beside the head like a block. Now the neck rises out of the collar, which
    wraps its foot. Measured: the neck's own pixels left showing (drawn in a test colour), and the collar's turn."""
    import numpy as np
    import burnham as B
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
    from ed import oval
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
    try:
        finish.main()
    except SystemExit as e:
        return None, str(e)
    finally:
        sys.argv = argv
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
    import burnham as B
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
    hit = [w for _, w, _ in P.find('blessed', "note 28: the escort should look like an HM Prison officer", 3)]
    return pg * 100 < code * 15 and 'blessed.py:307' in hit, f'page {pg} tokens, code {code}; note 28 -> {hit}'


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
    users = [os.path.basename(f) for f in glob.glob(os.path.join(HERE, '*.py')) if os.path.basename(f) not in
             ('people.py', 'people_parts.py', 'people_famous.py', 'people_walliams.py', 'people_turned.py', 'page.py',
              'kittests.py') and re.search(r'^\s*(import people\b|from people\b)',
             open(f, encoding='utf-8').read(), re.M)]
    if users:                                      # Sam (13 Nov): no film uses the kit until he approves it
        bad.append(f'films using the kit before Sam approves it: {users}')
    tmp = os.path.join(HERE, 'data', 'kittest-people')
    import blessed as BL0
    press = K.crowds('blessed')['press']                # chat 4d: the press pack, a crowd of 31 from 16 lines
    for i in range(31):
        f, k = BL0.press_sp(i, 0), K.crowd_person(press, i, 0, BL0.press_sp(i, 0)['kit'])
        if any(f.get(q) != k.get(q) for q in ('skin', 'hair_c', 'jacket', 'trousers', 'shirt', 'shoe', 'shoulders',
                                             'height', 'hw', 'seed')) or f['face_m'] != k['kit_face']['m']:
            bad.append(f'journalist {i + 1} not as the film drew them')
            break
    out, scores = K.replicate('blessed', tmp, [(8.6, 'jury'), (5.6, 'oath'), (59.5, 'walliams'), (20.5, 'van'),
                                               (24.0, 'escort'), (60.5, 'gates2')], film_keys=True)
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
    import blessed as BL
    import blessed_cast as BC
    TC = BC.TC
    caught = K.faults(dict(judge=BC.JUDGE)) == []
    keep = TC.HEADS['judge']
    TC.HEADS['judge'] = TC._head                   # the old fault (notes 13, 15): the judge on the house head
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
                                        + ', '.join(f'{lb} {d:.2f}%' for _, lb, d, _ in scores) + f' differ; a changed line shows ({seen:.2f}%)')


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
    users = [os.path.basename(f) for f in glob.glob(os.path.join(HERE, '*.py')) if not os.path.basename(f).startswith(
             ('places', 'page.py', 'kittests.py')) and re.search(r'^\s*(import places\b|from places\b|import places_)',
             open(f, encoding='utf-8').read(), re.M)]
    if users:                                      # Sam (13 Nov): no film uses the kit until he approves it
        bad.append(f'films using the kit before Sam approves it: {users}')
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


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else ''
    bad = 0
    for fn in TESTS:
        if only and only not in fn.__name__:
            continue
        try:
            ok, detail = fn()
        except Exception as e:
            import traceback
            traceback.print_exc()
            ok, detail = False, f'crashed: {e}'
        bad += not ok
        print(f"{'PASS' if ok else 'FAIL'} {fn.__name__}: {detail}")
        print(f"     ({(fn.__doc__ or '').strip().splitlines()[0]})")
    print('kittests:', 'all passed' if not bad else f'{bad} failed')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
