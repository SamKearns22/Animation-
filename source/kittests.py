#!/usr/bin/env python3
"""kittests: each shared-kit check tested against the film fault that taught it (Build list 27 Oct: "each with a test").
A test puts the old, faulty version back for a moment (from git history, written out here), and passes only if the
check catches the old version AND passes the fixed one.

    python3 source/kittests.py            all of them (a few minutes)
    python3 source/kittests.py hands      only the tests whose name contains 'hands'
"""
import math
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


# ------------------------------------------------------------------------------------------------ running them
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
