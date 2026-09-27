"""Shot 2 (1.5 s): the daughter across the island, seen from her mother's eyes - a straw-haired waif in a
droopy felt Santa hat, her forearms on the worktop, staring over it with a blank, mildly curious look,
watching her mother cut. (See story/animation-test.md.) For now: its first frame."""
import numpy as np

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s1_chop as S1  # noqa: E402

DURATION = 1.5
# where she stands: across the island, a little to her mother's left, close against its edge, up on tiptoe
# (at 1.16 m her shoulders are just below the worktop - on tiptoe, leaning in, her chest rises above its edge)
GIRL = np.array([0.30, 0.05, 0.51])


def frame(t):
    f = S1.frame(0.0)                      # the kitchen, the props and the mother as in shot 1
    mom_eyes = np.array([0.02, 1.60, -0.60])
    # she stares at her mother's hands - the raised cleaver and the hand on the meat
    girl = dict(position=GIRL, yaw=180.0, lean=12.0, look_at=np.array([-0.14, 1.26, -0.50]),
                head_share=0.45, rest_on=0.92,
                hands={'R': (GIRL + np.array([0.045, 0.87, -0.36]), (-0.9, 0.0, -0.45)),
                       'L': (GIRL + np.array([-0.045, 0.87, -0.36]), (0.9, 0.0, -0.45))},
                # forearms folded on the worktop, elbows near its edge
                poles=(GIRL + np.array([0.16, 0.90, -0.20]), GIRL + np.array([-0.16, 0.90, -0.20])))
    target = GIRL + np.array([0.0, 1.05, -0.10])
    return dict(t=t, camera=dict(pos=tuple(mom_eyes), target=tuple(target), vfov=19.0), pov=True,
                face='daughter', front_wall=True, mother=f['mother'], daughter=girl, board=f['board'], ham=f['ham'],
                cleaver=f['cleaver'], extras=f['extras'], shadow_focus=(0.25, 1.0, 0.25),
                focus=[target + np.array([0, 0.05, 0]), target + np.array([0.1, 0.12, 0]),
                       GIRL + np.array([0.0, 0.93, -0.21])])
