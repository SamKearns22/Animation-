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
    finally:
        E.PASSES = real
    return bool(none) and ok is None and bool(faults) and named is None, \
        f'no pass: {bool(none)}; pass: {ok is None}; 3 faults: {bool(faults)}; named: {named is None}'


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
def incremental_preflight_fingerprints():
    """Rule 59 as amended 3 Nov (Sam: a small fix should not re-check the whole film): the film's settings fingerprint is
    the same run to run, changes when an allow-list changes, and the check-code fingerprint exists; so an incremental
    pre-flight can trust an earlier clean run only when nothing it depends on has changed."""
    import preflight as P
    import types
    film = types.SimpleNamespace(HANDS_OK=[('a', '*', 'no hand', 0, 1, 'x')], SHOTS=[('s', 0, 1)], NAME='x',
                                 CALLBACK=lambda: 1, LINES=[{'n': 1}])
    a, b = P._config_hash(film), P._config_hash(film)
    film.HANDS_OK.append(('b', '*', 'no hand', 0, 1, 'y'))
    c = P._config_hash(film)
    film.CALLBACK = lambda: 2                        # a function's memory address never counts
    d = P._config_hash(film)
    return a == b and a != c and c == d and bool(P._checks_hash()), \
        f'same twice: {a == b}; allow-list change seen: {a != c}; stable over function addresses: {c == d}'


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
