"""Shot 2 (1.5 s): the daughter across the island, seen from her mother's eyes - a straw-haired waif in a
droopy felt Santa hat, her forearms on the worktop, staring over it with a blank, mildly curious look,
watching her mother cut. (See story/animation-test.md.) For now: its first frame."""
import numpy as np

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s1_chop as S1  # noqa: E402

DURATION = 1.5
GIRL = np.array([0.30, 0.0, 0.50])        # where she stands: across the island, a little to her mother's left


def frame(t):
    f = S1.frame(0.0)                      # the kitchen, the props and the mother as in shot 1
    mom_eyes = np.array([0.02, 1.60, -0.60])
    girl = dict(position=GIRL, yaw=180.0, lean=8.0, look_at=f['ham'].c + np.array([0.0, 0.03, 0.0]),
                head_share=0.6, rest_on=0.92,
                hands={'R': (GIRL + np.array([0.07, 0.92, -0.21]), (-0.3, 0.0, -1.0)),
                       'L': (GIRL + np.array([-0.07, 0.92, -0.21]), (0.3, 0.0, -1.0))},
                poles=(GIRL + np.array([0.20, 0.97, -0.14]), GIRL + np.array([-0.20, 0.97, -0.14])))
    target = GIRL + np.array([0.0, 1.00, -0.08])
    return dict(t=t, camera=dict(pos=tuple(mom_eyes), target=tuple(target), vfov=24.0), pov=True,
                face='daughter', mother=f['mother'], daughter=girl, board=f['board'], ham=f['ham'],
                cleaver=f['cleaver'], shadow_focus=(0.25, 1.0, 0.25),
                focus=[target + np.array([0, 0.05, 0]), target + np.array([0.1, 0.12, 0]),
                       GIRL + np.array([0.0, 0.93, -0.21])])
