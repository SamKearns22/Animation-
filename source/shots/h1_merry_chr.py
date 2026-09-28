"""Horror shot 'Merry Chr' (story/horror-merry-chr.md): a still, centred look into the spare room from its
doorway at head height, as if transfixed. The present on the bed; 'Merry Chr' in blood on the bare back wall;
the man kneeling at the last r with his forehead against it."""
import numpy as np

import spare_room as R

DURATION = 1.0
MAN = dict(position=(0.87, -4.85), yaw=180.0, lean=14.0, nod=30.0, head_roll=-3.0, wall_z=R.BACK_Z)


def dress(b, chars):
    import man
    import merry_chr
    f = man.forehead(chars['man'])
    contact = (float(f[0]), float(f[1]))
    merry_chr.build(b, man_state=chars['man'], contact=contact, r_centre=(contact[0] - 0.02, contact[1] - 0.02), t=chars.get('t', 0.0))


def frame(t):
    return dict(set='spare_room',
                camera=dict(pos=(0.0, 1.62, 0.35), target=(0.0, 0.85, -5.2), vfov=60.0),
                man=MAN, dressing=[dress],
                # the eye goes to the present first, then the writing and the man at the last r
                focus=[(-1.25, 0.85, -2.45), (0.85, 1.2, -5.1), (-0.6, 1.3, -5.15)],
                shadow_focus=(-0.3, 0.9, -3.4))
