"""Automatic whole-scene checks, run before every frame is rendered (stills and every frame of an animation).

Each check looks for something a viewer would notice at once: a hand not attached to its arm, an arm that
can't reach, a wrist bent further than a wrist bends, a hand sinking into (or floating above) what it
presses, a blade passing through fingers, a board hanging off the worktop, food off the board, a dent in the
jumper. A failed check stops the render and says what is wrong, in millimetres, so a fix to one part can't
silently break another.

    python3 checks.py shots/s1_chop.py [T]      run them all on a frame of a shot and print a report
"""
import numpy as np


def run(scene, verbose=True):
    import kitchen
    import mother
    problems, report = [], []

    def check(ok, what, detail):
        report.append(('ok  ' if ok else 'FAIL') + '  ' + what + ': ' + detail)
        if not ok:
            problems.append(what + ': ' + detail)

    fr, st = scene['frame'], scene['state']
    # every character's sleeves cover their forearms (a cut in the clothes can't take a sleeve away unseen)
    for name, cs in scene['chars'].items():
        top = cs.get('jumper', cs.get('top'))
        lo, d, vox = top[0], top[1], top[2]
        for s in 'RL':
            el, wr = cs['joints']['elbow.' + s], cs['joints']['wrist.' + s]
            covered = []
            for t in (0.25, 0.5, 0.75):
                i = np.round((el + (wr - el) * t - lo) / vox).astype(int)
                ok_i = np.all(i >= 0) and np.all(i < np.array(d.shape))
                covered.append(ok_i and d[tuple(i)] < 0)
            check(all(covered), f'{name}: {"right" if s == "R" else "left"} sleeve covers the forearm',
                  'covered' if all(covered) else 'bare in places')
    if st is not None:
        check_mother(scene, check)
    if 'daughter' in scene['chars']:
        check_daughter(scene, check)
    ham = fr['ham']
    # 5. the board lies flat and fully on the island; the food is on the board
    I, board = kitchen.ISLAND, fr['board']
    c, h = board.c, board.half
    corners = [c + np.array([sx * h[0], 0, sz * h[2]]) for sx in (-1, 1) for sz in (-1, 1)]
    inside = all(I['x0'] < q[0] < I['x1'] and I['z0'] < q[2] < I['z1'] for q in corners)
    check(inside, 'board fully on the island', 'all corners on the worktop' if inside else 'a corner overhangs')
    check(abs(c[1] - h[1] - I['top']) < 0.002, 'board sits on the worktop', f'{(c[1] - h[1] - I["top"]) * 1000:.1f} mm')
    rim = [ham.c + ham.frame() @ np.array([ham.R[0] * np.cos(t), 0, ham.R[2] * np.sin(t)])
           for t in np.linspace(0, 2 * np.pi, 24)]
    on = all(abs(q[0] - c[0]) < h[0] and abs(q[2] - c[2]) < h[2] for q in rim)
    check(on, 'ham on the board', 'within the board' if on else 'hangs over the edge')
    if verbose:
        print('\n'.join(report), flush=True)
    if problems:
        raise RuntimeError('scene checks failed:\n  ' + '\n  '.join(problems))
    return report


def check_mother(scene, check):
    import mother
    fr, st = scene['frame'], scene['state']
    spec = fr['mother']
    parts = mother.hand_parts()
    names = ('right', 'left')
    # 1. arms: each reaches what its hand holds, the hand is on the end of the arm, the wrist bends naturally
    for i, nm in enumerate(names):
        s = 'RL'[i]
        check(st['short'][i] < 0.002, nm + ' arm reaches', f'{st["short"][i] * 1000:.0f} mm short')
        o, R, w = st['hands'][i]
        gap = np.linalg.norm(w - st['joints']['wrist.' + s]) * 1000
        check(gap < 3, nm + ' hand joins its arm', f'{gap:.1f} mm gap')
        fl, dv, err = st['bends'][i]
        # the chopping hand is held firm: a strong chop keeps the wrist near straight (the director caught
        # 40-50 degree bends that the old anatomical limits let through)
        lim_fl, lim_dv = (30, 15) if i == 0 else (50, 25)
        check(abs(fl) <= lim_fl and abs(dv) <= lim_dv and err < 8, nm + ' wrist bends within its natural range',
              f'{fl:+.0f} deg up/down, {dv:+.0f} sideways, {err:.0f} deg left over')
        # the elbow bends the right way (never backwards) and not closed up
        sh, el = st['joints']['shoulder.' + s], st['joints']['elbow.' + s]
        bend = np.degrees(np.arccos(np.clip(((el - sh) / np.linalg.norm(el - sh)) @
                                            ((w - el) / np.linalg.norm(w - el)), -1, 1)))
        check(bend < 150, nm + ' elbow bend is possible', f'{bend:.0f} deg')
    # forearms never pass into her body (measured on the bent skin itself)
    from scipy.spatial import cKDTree
    b = mother.body()
    Vw = b.skin(st['pose'])
    skin = np.zeros(len(Vw), bool)
    skin[b.skin_idx] = True
    torso = skin & np.isin(b.label, [b.piece_names.index(n) for n in ('chest', 'hips')])
    tree = cKDTree(Vw[torso])
    for nm, s in zip(names, 'RL'):
        fa = skin & (b.label == b.piece_names.index('forearm.' + s))
        gap = tree.query(Vw[fa])[0].min()
        check(gap > 0.015, nm + ' forearm clear of her body', f'{gap * 100:.1f} cm')
    # 2. hands and food: the steadying hand presses a few millimetres in; the chopping hand stays clear of it
    ham, cleaver = fr['ham'], fr['cleaver']
    pts = mother.colliders(st)
    dl = ham.distance(pts[1])
    press = spec.get('press', 0.004)
    check(0.002 < -dl.min() < 0.007, 'left hand presses into the ham (2-7 mm, the meat dented round it)',
          f'{-dl.min() * 1000:.1f} mm deep (asked for {press * 1000:.0f})')
    dr = ham.distance(pts[0])
    check(dr.min() > 0.005, 'right hand clear of the ham', f'{dr.min() * 1000:.1f} mm')
    # 3. the blade: never through her fingers; above the meat unless this frame is a chop landing
    blade = cleaver.blade_points()
    near = np.linalg.norm(pts[1][:, None, :] - blade[None, ::7, :], axis=2).min()
    check(near > 0.004, 'blade clear of her left hand', f'{near * 1000:.0f} mm')
    gap = ham.distance(cleaver.edge_points()).min()
    if fr.get('blade_in_meat'):
        check(gap > -0.10, 'blade no deeper than the meat', f'{-gap * 100:.1f} cm in')
    else:
        check(gap > 0.0, 'cleaver clear of the meat', f'{gap * 100:.1f} cm above it')
    # 4. no dents or holes in the jumper: its front surface changes smoothly across her body
    lo, d, vox, part = st['jumper']
    J = st['joints']
    worst = 0.0
    base_y = J['spine05'][1] - mother.JUMPER['hem'] + 0.04
    for y in np.arange(base_y, J['neck01'][1] - 0.10, 0.02):
        j = int(round((y - lo[1]) / vox))
        zs = []
        for x in np.arange(-0.09, 0.091, 0.01):   # across the front of her (beyond that the body turns away)
            i = int(round((x + J['spine02'][0] - lo[0]) / vox))
            k = np.nonzero((d[i, j, :] < 0) & (part[i, j, :] == 0))[0]
            sleeve = np.any((d[i, j, :] < 0) & (part[i, j, :] != 0))  # a sleeve in front: not a dent
            zs.append(lo[2] + k.max() * vox if len(k) and not sleeve else np.nan)
        steps = np.abs(np.diff(np.array(zs)))
        if np.isfinite(steps).any():
            worst = max(worst, np.nanmax(steps))
    check(worst < 0.02, 'jumper front has no dents', f'largest step {worst * 100:.1f} cm between neighbours 1 cm apart')


def check_daughter(scene, check):
    """The girl: arms reach, hands on the ends of her arms, wrists bent naturally, hands resting on the worktop
    (touching, not sinking in), her forearms not passing into her body."""
    import daughter
    from mother import surface_points
    st = scene['chars']['daughter']
    spec = st['spec']
    # nothing of her passes into the island (her chest may lean over the worktop, never through its edge)
    import kitchen
    I = kitchen.ISLAND
    b = daughter.body()
    V = b.skin(st['pose'])
    shown = np.isin(np.arange(len(V)), b.skin_idx) & ~np.isin(
        b.label, [b.piece_names.index(n) for n in ('hand.L', 'hand.R', 'head')])  # (hands, head: finer pieces)
    V = V[shown]
    # the island's real shape: the worktop slab overhangs; the cupboards are set back 3 cm, the toe-kick 8 cm
    y = V[:, 1]
    inset = np.where(y > I['top'] - 0.03, 0.0, np.where(y > 0.10, 0.03, 0.08))
    inside = np.minimum.reduce([V[:, 0] - I['x0'] - inset, I['x1'] - inset - V[:, 0], V[:, 2] - I['z0'] - inset,
                                I['z1'] - inset - V[:, 2], I['top'] - y])
    deepest = inside.max()
    check(deepest < 0.003, 'girl: her body stays out of the island', f'{max(deepest, 0) * 1000:.0f} mm into it')
    for i, nm in enumerate(('her right', 'her left')):
        s = 'RL'[i]
        check(st['short'][i] < 0.002, 'girl: ' + nm + ' arm reaches', f'{st["short"][i] * 1000:.0f} mm short')
        o, R, w = st['hands'][i]
        gap = np.linalg.norm(w - st['joints']['wrist.' + s]) * 1000
        check(gap < 3, 'girl: ' + nm + ' hand joins its arm', f'{gap:.1f} mm gap')
        fl, dv, err = st['bends'][i]
        check(abs(fl) <= 50 and abs(dv) <= 25 and err < 10, 'girl: ' + nm + ' wrist bends naturally',
              f'{fl:+.0f} up/down, {dv:+.0f} sideways, {err:.0f} deg left over')
        low = (o + surface_points(daughter.hand_parts()[i][0]) @ R.T)[:, 1].min() - spec['rest_on']
        check(-0.002 < low < 0.003, 'girl: ' + nm + ' hand rests on the worktop', f'{low * 1000:+.1f} mm')


if __name__ == '__main__':
    import sys
    import shot
    fr = shot.load_recipe(sys.argv[1]).frame(float(sys.argv[2]) if len(sys.argv) > 2 else 0.0)
    run(shot.build(fr))
