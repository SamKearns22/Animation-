"""Shot 2 (1.5 s): the daughter across the island, seen from her mother's eyes - a straw-haired waif in a
droopy felt Santa hat, her forearms on the worktop, staring over it with a blank, mildly curious look,
watching her mother cut. (See story/animation-test.md.) For now: its first frame."""
import numpy as np

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s1_chop as S1  # noqa: E402
from props import StepStool  # noqa: E402

DURATION = 1.5
# where she stands: across the island, a little to her mother's left, close against its edge
# (at 1.16 m her shoulders are just below the worktop; standing on a little step stool, leaning in, her chest
# rises above its edge)
GIRL = np.array([0.30, 0.08, 0.50])


def frame(t):
    f = S1.frame(0.0)                      # the kitchen, the props and the mother as in shot 1
    mom_eyes = np.array([0.02, 1.60, -0.60])
    # she stares at her mother's hands - the raised cleaver and the hand on the meat
    girl = dict(position=GIRL, yaw=180.0, lean=10.0, look_at=np.array([-0.14, 1.26, -0.50]),
                head_share=0.45, rest_on=0.92,
                hands={'R': (GIRL + np.array([0.06, 0.84, -0.22]), (-0.95, 0.0, -0.3)),
                       'L': (GIRL + np.array([-0.06, 0.84, -0.22]), (0.95, 0.0, -0.3))},
                # forearms folded on the worktop, elbows near its edge
                poles=(GIRL + np.array([0.22, 0.92, -0.14]), GIRL + np.array([-0.22, 0.92, -0.14])))
    target = GIRL + np.array([-0.11, 1.00, -0.11])
    return dict(t=t, camera=dict(pos=tuple(mom_eyes), target=tuple(target), vfov=31.0), pov=True,
                face='daughter', front_wall=True, mother=f['mother'], daughter=girl, board=f['board'], ham=f['ham'],
                cleaver=f['cleaver'], extras=f['extras'] + [StepStool((GIRL[0], 0.04, GIRL[2]))], shadow_focus=(0.25, 1.0, 0.25),
                focus=[target + np.array([0, 0.05, 0]), target + np.array([0.1, 0.12, 0]),
                       GIRL + np.array([0.0, 0.93, -0.21])])
