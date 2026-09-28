"""Shot 2 (1.5 s): the daughter across the island, seen from her mother's eyes - a straw-haired waif in a
droopy felt Santa hat, her forearms on the worktop, staring over it with a blank, mildly curious look,
watching her mother cut. In the foreground her mother slowly raises the cleaver again and moves it along the
ham towards her own fingers; the girl's eyes follow the blade up (her head stays still), and she blinks once.
(See story/animation-test.md and guides/movement.md.)"""
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


FPS = 24
END_H, END_ALONG = 0.20, -0.035        # where the cleaver is at the end of this shot (shot 3 carries on from it)
END_SLIDE = 0.035                      # (slid along its length, away from her: her hand clear of her body)
TIMES = np.arange(0, 36, 2) / FPS      # on twos
BLINK = {14: 1.0, 16: 0.5}             # (drawings) a quick close, a slower opening


def cleaver_path(f):
    """Carries on from the end of shot 1: the blade rising slowly from resting just above the board and moving
    along the ham to over her fingers."""
    h0, a0, _ = S1.cleaver_path(47)
    s = S1.between(f, 0, 35)
    h = h0 + (END_H - h0) * s
    k = S1.ease((h - 0.12) / 0.08)                                  # moves along once clear of the meat
    return h, a0 + (END_ALONG - a0) * k, END_SLIDE * k


def frame(t):
    f = S1.frame(47 / S1.FPS)              # the kitchen, the props and the mother as at the end of shot 1
    n = t * FPS
    h, along, slide = cleaver_path(n)
    cleaver = S1.natural_cleaver(h, along, slide)
    f['mother'] = dict(f['mother'], cleaver=cleaver, poles=S1.elbow_poles(h))
    f['cleaver'] = cleaver
    f['blade_in_meat'] = h < 0.115
    mom_eyes = np.array([0.02, 1.60, -0.60])
    # she stares at her mother's hands - the raised cleaver and the hand on the meat
    # her head stays turned to her mother's hands; her eyes follow the blade (smooth pursuit)
    girl = dict(position=GIRL, yaw=180.0, lean=10.0, head_look=np.array([-0.14, 1.26, -0.50]),
                look_at=cleaver.o + np.array([0, 0.05, 0]), blink=BLINK.get(int(round(n)), 0.0),
                head_share=0.45, rest_on=0.92,
                hands={'R': (GIRL + np.array([0.06, 0.84, -0.22]), (-0.95, 0.0, -0.3)),
                       'L': (GIRL + np.array([-0.06, 0.84, -0.22]), (0.95, 0.0, -0.3))},
                # forearms folded on the worktop, elbows near its edge
                poles=(GIRL + np.array([0.22, 0.92, -0.14]), GIRL + np.array([-0.22, 0.92, -0.14])))
    target = GIRL + np.array([-0.11, 1.00, -0.11])
    return dict(t=t, camera=dict(pos=tuple(mom_eyes), target=tuple(target), vfov=31.0), pov=True,
                face='daughter', front_wall=True, mother=f['mother'], daughter=girl, board=f['board'], ham=f['ham'],
                cleaver=cleaver, blade_in_meat=f['blade_in_meat'], extras=f['extras'] + [StepStool((GIRL[0], 0.04, GIRL[2]))], shadow_focus=(0.25, 1.0, 0.25),
                focus=[target + np.array([0, 0.05, 0]), target + np.array([0.1, 0.12, 0]),
                       GIRL + np.array([0.0, 0.93, -0.21])])
