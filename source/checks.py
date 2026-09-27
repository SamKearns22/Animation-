"""Automatic whole-scene checks, run before every render (and later, on every frame of an animation).

Each check looks for something a viewer would notice at once: a hand not attached to its arm, a hand sinking
into (or floating above) what it touches, an arm pushing into the body, limbs of impossible length, a board
hanging off the worktop, food off the board. A failed check stops the render and says what is wrong, in
millimetres, so a fix to one part can't silently break another.

    python3 checks.py        run them all and print a report
"""
import numpy as np


def _torso_clearance(MS, p):
    """Roughly how far a point is outside the jumper's torso (negative = inside), from the body profile."""
    prof = MS.BODY_PROFILE[::-1]
    y = np.clip(p[1], prof[0, 0], prof[-1, 0])
    w, fr, bk = (np.interp(y, prof[:, 0], prof[:, c]) for c in (1, 2, 3))
    zz = p[2] - MS.body_cz(y)
    D, N = (fr, 2.3) if zz > 0 else (bk, 2.4)
    F = ((abs(p[0]) / w) ** N + (abs(zz) / D) ** N) ** (1 / N)
    r = np.hypot(p[0], zz)
    return r * (1 - 1 / max(F, 1e-6))


def run(MS=None, verbose=True):
    if MS is None:
        import mother_scene as MS
    problems, report = [], []

    def check(ok, what, detail):
        report.append(('ok  ' if ok else 'FAIL') + '  ' + what + ': ' + detail)
        if not ok:
            problems.append(what + ': ' + detail)

    parts = MS.get_mh_hands()
    names = ('right hand', 'left hand')
    # 1. every hand is joined to its sleeve
    for (origin, R, w, f), part, nm in zip(MS.HANDS, parts, names):
        gap = np.linalg.norm(origin + R @ part[1] - w) * 1000
        check(gap < 3, nm + ' joins its sleeve', f'{gap:.1f} mm gap')
    # 2. the resting hand touches the food without sinking into it; the chopping hand stays clear of it
    pts = [origin + MS._surface_points(part[0]) @ R.T for (origin, R, _, _), part in zip(MS.HANDS, parts)]
    dl = MS.ham_distance(pts[1])
    check(0.002 < -dl.min() < 0.007, 'left hand presses into the ham (2-7 mm, the meat dented round it)',
          f'{-dl.min() * 1000:.1f} mm deep')
    dr = MS.ham_distance(pts[0])
    check(dr.min() > 0.01, 'right hand clear of the ham', f'{dr.min() * 1000:.1f} mm')
    # 2b. the cleaver hovers before the chop: its edge clearly above the meat (a visible gap), not touching the
    # fingers of her other hand
    Rb = np.stack([MS.BLADE_B, [0, 1.0, 0], MS.RACK_A], 1)
    centre = MS.BLADE_O + MS.BLADE_B * 0.030 + np.array([0, 0.040, 0])
    u, v, w = np.meshgrid(np.linspace(-1, 1, 41), np.linspace(-1, 1, 21), (-1, 1), indexing='ij')
    blade = centre + np.stack([u.ravel() * 0.100, v.ravel() * 0.049, w.ravel() * 0.0016], 1) @ Rb.T
    edge = blade[blade[:, 1] < blade[:, 1].min() + 1e-6]
    gap = MS.ham_distance(edge).min()
    check(0.02 < gap < 0.09, 'cleaver hovers over the meat (2-9 cm gap)', f'{gap * 100:.1f} cm')
    near = np.linalg.norm(pts[1][:, None, :] - blade[None, ::7, :], axis=2).min()
    check(near > 0.005, 'blade clear of her left hand', f'{near * 1000:.0f} mm')
    # 3. arms: sensible lengths, forearms not pushing into her body
    for sh, el, wr, nm in ((MS.R_SHOULDER, MS.R_ELBOW, MS.R_WRIST, 'right'), (MS.L_SHOULDER, MS.L_ELBOW, MS.L_WRIST,
                                                                           'left')):
        up, lo = np.linalg.norm(el - sh), np.linalg.norm(wr - el)
        check(0.26 < up < 0.36 and 0.22 < lo < 0.30, nm + ' arm lengths',
              f'upper {up * 100:.0f} cm, forearm {lo * 100:.0f} cm')
        clear = min(_torso_clearance(MS, el + (wr - el) * t) for t in np.linspace(0.15, 1, 12))
        check(clear > 0.045, nm + ' forearm clear of her body', f'{clear * 100:.1f} cm from the jumper')
    # 4. no dents or holes in the jumper: its front surface changes smoothly across her body
    lo, d, vox, part = MS.get_body_grid()  # part: 0 torso, 1-2 sleeves (sleeves in front are not dents)
    worst = 0.0
    for y in np.arange(0.90, 1.40, 0.02):
        j = int(round((y - lo[1]) / vox))
        zs = []
        for x in np.arange(-0.12, 0.121, 0.01):
            i = int(round((x - lo[0]) / vox))
            k = np.nonzero((d[i, j, :] < 0) & (part[i, j, :] == 0))[0]
            zs.append(lo[2] + k.max() * vox if len(k) else np.nan)
        zs = np.array(zs)
        if np.isfinite(zs).all():
            worst = max(worst, np.abs(np.diff(zs)).max())
    check(worst < 0.02, 'jumper front has no dents', f'largest step {worst * 100:.1f} cm between neighbours 1 cm apart')
    # 5. the board lies flat and fully on the island; the food is on the board
    I = MS.ISLAND
    c, h = MS.BOARD_C, MS.BOARD_HALF
    corners = [c + np.array([sx * h[0], 0, sz * h[2]]) for sx in (-1, 1) for sz in (-1, 1)]
    inside = all(I['x0'] < q[0] < I['x1'] and I['z0'] < q[2] < I['z1'] for q in corners)
    check(inside, 'board fully on the island', 'all corners on the worktop' if inside else 'a corner overhangs')
    check(abs(c[1] - h[1] - I['top']) < 0.002, 'board sits on the worktop', f'{(c[1] - h[1] - I["top"]) * 1000:.1f} mm')
    Rh_ = np.stack([MS.RACK_A, [0, 1.0, 0], MS.HAM_ACROSS], 1)
    rim = [MS.HAM_C + Rh_ @ np.array([MS.HAM_R[0] * np.cos(t), 0, MS.HAM_R[2] * np.sin(t)])
           for t in np.linspace(0, 2 * np.pi, 24)]
    on = all(abs(q[0] - c[0]) < h[0] and abs(q[2] - c[2]) < h[2] for q in rim)
    check(on, 'ham on the board', 'within the board' if on else 'hangs over the edge')
    if verbose:
        print('\n'.join(report))
    if problems:
        raise RuntimeError('scene checks failed:\n  ' + '\n  '.join(problems))
    return report


if __name__ == '__main__':
    run()
