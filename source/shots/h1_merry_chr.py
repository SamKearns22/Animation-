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
                # from the dark landing, a metre back from the doorway, level at head height; a 35 mm-like lens
                # shifted down (walls stay upright) so the floor shows; the dark doorcase frames the room
                camera=dict(pos=(0.0, 1.62, 1.45), target=(0.0, 1.62, -5.2), vfov=40.0, shift=-0.30),
                man=MAN, dressing=[dress],
                # the eye goes to the present first, then along the writing to the man at the last r
                focus=[(-1.65, 0.85, -2.87), (-0.95, 0.85, -2.87), (-0.9, 1.3, -5.15), (0.2, 1.3, -5.15),
                       (0.87, 1.2, -5.1)],
                contrast_budget=1.0, exposure=1.7, frame_depth=1.75,
                shadow_focus=(-0.6, 0.9, -3.6))
