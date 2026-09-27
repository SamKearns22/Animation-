"""Shot 3 (2.5 s), in the director's words: we see that she is smiling, looking at the girl - all is well. Then
she looks down at her hands and the camera follows her gaze to the chopping board, close up. We see the blade
fall towards her fingers, with intent and force, and cut to black before it lands (on the THUD). It says:
all is well; she can see full well what she is doing; she inexplicably does it anyway.

The blade lies across her outstretched fingers at their middle joints: it would take at least three of them.
(See story/animation-test.md and guides/movement.md.)"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s1_chop as S1  # noqa: E402
import s2_daughter as S2  # noqa: E402

DURATION = 2.5
FPS = 24
TOP = 0.36                              # lifted high for this one
FALL = 56                               # held at the top until here; it would land on frame 60, the cut to black
GLANCE = 14                             # her eyes drop to her hands (a saccade, with a blink)...
HEAD = (15, 26)                         # ...her head follows...
TRACK = (18, 40)                        # ...and the camera follows her gaze down to the board
# on twos; the fall on ones
TIMES = np.array(sorted(set(range(0, 56, 2)) | {56, 57, 58, 59})) / FPS
FACE = np.array([0.019, 1.602, -0.598])     # between her eyes (measured on her pose)
FINGERS = S1.HAM_C + S2.END_ALONG * S1.A + np.array([0, 0.125, 0])   # the tops of her middle finger joints
PASS = {56: 0.0, 57: 0.15, 58: 0.45, 59: 0.85}  # how far down to her fingers the blade has come: driven, speeding


def cleaver_h(f):
    fingers = FINGERS[1] - S1.BOARD.top - 0.001
    if f < FALL:
        return S2.END_H + (TOP - S2.END_H) * S1.between(f, 0, 46)   # a slow, deliberate lift; a moment held
    return TOP - (TOP - fingers) * PASS[int(round(f))]


def raised_cleaver(h):
    """Above the height it had at the end of shot 2 the blade is not simply lifted: her wrist cocks and her
    forearm turns, so the blade tips its spine back and turns (as anyone lifting a heavy blade high); coming
    down, it squares up again to land flat across her fingers."""
    import mhuman as MH
    from props import Cleaver
    c = S1.cleaver_at(h, S2.END_ALONG, S2.END_SLIDE)
    a = S1.ease((h - S2.END_H) / (TOP - S2.END_H))
    R = MH.axis_angle(c.R[:, 2], -12.0 * a) @ c.R
    R = MH.axis_angle(R[:, 0], -40.0 * a) @ R
    R = MH.axis_angle([0, 1.0, 0], 30.0 * a) @ R
    return Cleaver(c.o, R)


def frame(t):
    fr = S1.frame(47 / S1.FPS)
    n = t * FPS
    h = cleaver_h(n)
    cleaver = raised_cleaver(h)
    look_down = FINGERS + np.array([0, 0.01, 0])
    eye = S1.DAUGHTER_EYES if n < GLANCE else look_down
    head = S1.DAUGHTER_EYES + (look_down - S1.DAUGHTER_EYES) * S1.between(n, *HEAD)
    blink = {GLANCE: 1.0, GLANCE + 2: 0.5}.get(int(round(n)), 0.0)
    fr['mother'] = dict(fr['mother'], cleaver=cleaver, poles=S1.elbow_poles(h), head_look=head, eye_look=eye,
                        smile=1.0, blink=blink)
    fr['cleaver'] = cleaver
    fr['blade_in_meat'] = False
    # the camera: close on her face, then following her gaze down to her hands and the blade above them
    s = S1.between(n, *TRACK)
    end = FINGERS + np.array([0, 0.04, 0])            # her fingers on the ham, the blade above them
    target = FACE + (end - FACE) * s
    pos = target + np.array([0.16 - 0.04 * s, 0.04 + 0.34 * s, 0.78 - 0.20 * s])   # ending looking down on them
    fr['camera'] = dict(pos=tuple(pos), target=tuple(target), vfov=21.0)
    fr['focus'] = [FACE, FINGERS, cleaver.o + np.array([0, 0.05, 0])]
    return fr
