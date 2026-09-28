"""Horror shot 'Merry Chr' (story/horror-merry-chr.md): a still, centred look into the spare room from its
doorway at head height, as if transfixed. The present on the bed; 'Merry Chr' in blood on the bare back wall;
the man kneeling at the last r, slamming his forehead into it.

Animated: the camera and the room never move. Only he moves - pulled back ~6 cm from his neck and upper back,
a short hold, then a fast strike (3 frames, on ones) into the same wet spot, a dull recoil and settle, every
0.9 s like a machine - and the fairy lights flash brokenly (their glow on the walls with them). The blood
does not grow (the director: he is drained, there is no more blood to give); the wall stays as in the still."""
import numpy as np

import spare_room as R

FPS = 24
DURATION = 3.0
MAN = dict(position=(0.87, -4.85), yaw=180.0, lean=14.0, nod=30.0, head_roll=-3.0, wall_z=R.BACK_Z)
# his forehead meets the wall on these frames (0.9 s apart: 21.6 frames, so 22 and 21 in turn)
IMPACTS = (10, 32, 53)
PULL = dict(upper=-6.0, nod=-11.0)       # fully pulled back (~6 cm): his upper back and neck straighten
STRIKE = 3                                # frames the strike takes


def pull_back(f):
    """How far he is pulled back from the wall at frame f (0: forehead on the wall, 1: fully back), and how
    long since the last impact (frames)."""
    prev = [i for i in IMPACTS if i <= f + 1e-9]
    nxt = [i for i in IMPACTS if i > f + 1e-9]
    last = prev[-1] if prev else IMPACTS[0] - 21.6
    to = (nxt[0] if nxt else IMPACTS[-1] + 21.6) - f
    since = f - last
    if to <= STRIKE:                                   # the strike: accelerating all the way in, no easing
        u = 1 - to / STRIKE
        return 1 - u * u, since
    if since < 1.0:                                    # the impact, and the dull recoil a frame later
        return 0.22 * since, since
    if since < 5.0:                                    # settling, a few millimetres off the wall
        return 0.22 - 0.14 * (since - 1) / 4, since
    if since < 13.0:                                   # drawn back, slow out of the settle and into the hold
        u = (since - 5) / 8
        return 0.08 + 0.92 * u * u * (3 - 2 * u), since
    return 1.0, since                                  # the short hold


def man_spec(f):
    import man
    p, since = pull_back(f)
    # the impact thrown through his shoulders: forward and down on the frame of impact, gone in a few frames
    jolt = 2.5 * np.exp(-since / 1.5) if since < 6 else 0.0
    # the dead arms: carried back with his shoulders on the pull, a small late swing after each impact
    sw = 0.012 * np.exp(-since / 8) * np.sin(since / 24 * 2 * np.pi * 1.1)
    return dict(MAN_ANIM(), upper=PULL['upper'] * p, nod=MAN['nod'] + PULL['nod'] * p, jolt=jolt,
                swing=(sw, 0.8 * sw * np.cos(0.3)), wall=R.BACK_Z, impact=abs(since) < 1e-6)


_REST = {}


def rest():
    """His pose at the moment of contact (as in the still): where his body sits, and where his forehead
    meets the wall - the same spot every strike."""
    if not _REST:
        import man
        st = man.solve(MAN)
        st['verts'] = man.body().skin(st['pose'])
        f = man.forehead(st)
        _REST.update(root=st['pose'].position.tolist(), contact=(float(f[0]), float(f[1])))
    return _REST


def MAN_ANIM():
    d = {k: v for k, v in MAN.items() if k != 'wall_z'}
    d['root'] = rest()['root']
    return d


def dress(b, chars, t=0.0):
    import man
    import merry_chr
    contact = rest()['contact']
    if 'state' not in _REST:          # the things on the floor are laid round him as in the still, so they never shift
        _REST['state'] = man.prepare(man.solve(MAN))
    merry_chr.build(b, man_state=_REST['state'], contact=contact, r_centre=(contact[0] - 0.02, contact[1] - 0.02), t=t)


def drawing_times():
    """On twos, but on ones round each strike (from the start of the strike to just after the recoil)."""
    fr = set(range(0, int(DURATION * FPS), 2))
    for i in IMPACTS:
        fr |= set(range(i - STRIKE, i + 3))
    return np.array(sorted(f for f in fr if 0 <= f < DURATION * FPS)) / FPS


TIMES = drawing_times()


def frame(t, still=False):
    import merry_chr
    if still:
        man_, dressing, glow = MAN, [lambda b, c: dress(b, c, 0.0)], None
    else:
        man_ = man_spec(t * FPS)
        dressing = [lambda b, c: dress(b, c, t)]
        glow = merry_chr.glow(t, side_z=R.SIDE_GLOW_Z)
    return dict(set='spare_room', glow=glow,
                # from the dark landing, just back from the doorway (only the edge of its opening shows), level at head height; a 35 mm-like lens
                # shifted down (walls stay upright) so the floor shows; the dark doorcase frames the room
                camera=dict(pos=(0.0, 1.62, 1.10), target=(0.0, 1.62, -5.2), vfov=40.0, shift=-0.30),
                man=man_, dressing=dressing,
                # the eye goes to the present first, then along the writing to the man at the last r
                focus=[(-1.65, 0.85, -2.87), (-0.95, 0.85, -2.87), (-0.9, 1.3, -5.15), (0.2, 1.3, -5.15),
                       (0.87, 1.2, -5.1)],
                contrast_budget=1.0, exposure=1.7, frame_depth=1.75,
                shadow_focus=(-0.6, 0.9, -3.6))
