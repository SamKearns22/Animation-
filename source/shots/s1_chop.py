"""Shot 1 (2 s): the mother at the kitchen island, the cleaver raised over the ham, her left hand pressing
the meat steady. She chops two neat 1 cm slices, which tip over onto the board. After the first chop her eyes
find her daughter across the island (a blink with the glance; her head follows); the second chop falls while
she looks at the girl, not the blade, and a warm smile slowly grows. (See story/animation-test.md and
guides/movement.md for the timings.)"""
import numpy as np

from props import Board, Ham, Cleaver, PastryPlate, slice_lying
from rig import unit

DURATION = 2.0
FPS = 24
CAMERA = dict(pos=(0.85, 1.60, 2.30), target=(0.36, 1.37, -0.55), vfov=19.0)
DAUGHTER_EYES = np.array([0.30, 1.05, 0.62])   # across the island, almost opposite her, a little to her left

ANGLE = -30.0                                   # the ham lies at this angle; the blade comes down across it
A = np.array([np.cos(np.radians(ANGLE)), 0.0, np.sin(np.radians(ANGLE))])     # along the ham
BLADE = np.array([-np.sin(np.radians(ANGLE)), 0.0, np.cos(np.radians(ANGLE))])  # along the blade, to its tip
CUT = np.array([-0.110, 0.985, -0.360])
BOARD = Board((-0.03, 0.940, -0.330), (0.285, 0.020, 0.190))
HAM_C = CUT + 0.072 * A
HAM_C[1] = BOARD.top + 0.058
FIRST_CUT = -0.087                              # the ham's cut face at the start (along it from its middle)
SLICE = 0.010                                    # each chop takes a 1 cm slice
HOVER = 0.189                                   # the blade's edge held this far above the board at the start
TOP = 0.27                                      # ...and lifted to here before each chop
GRIP_ROLL = 112                                  # the hand's turn about the handle (found in the first frame)

# the timeline, in frames (24 a second)
CHOPS = (12, 28)                                # frames where the blade meets the board
GLANCE = 14                                     # her eyes jump to her daughter (a saccade: one frame)
HEAD = (15, 25)                                 # her head follows
SMILE = (17, 40)                                # the smile grows (about a second: warm, not posed)
# drawings: on twos, but the chops (lift top, fall, impact, jolt) on ones
TIMES = np.array(sorted(set(range(0, 48, 2)) | set(range(9, 16)) | set(range(25, 32)))) / FPS


def ease(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def between(f, f0, f1):
    return ease((f - f0) / (f1 - f0))


def cleaver_path(f):
    """(height of the edge above the board, how far along the ham it is, whether it is in the meat)."""
    c1, c2 = CHOPS
    a1, a2 = FIRST_CUT + SLICE, FIRST_CUT + 2 * SLICE

    def fall(f, fc):                       # from the top, accelerating (gravity plus her arm): 3 frames
        s = (f - (fc - 3)) / 3.0
        return TOP * (1 - s * s)

    def jolt(f, fc):                       # the blade bounces a few millimetres off the board and settles
        return {0: 0.0, 1: 0.006, 2: 0.002}.get(int(round(f - fc)), 0.001)

    if f <= c1 - 3:
        h = HOVER + (TOP - HOVER) * between(f, 2, c1 - 3)        # anticipation: lifted a little higher
        along = a1
    elif f <= c1:
        h, along = fall(f, c1), a1
    elif f <= c1 + 3:
        h, along = jolt(f, c1), a1
    elif f <= c2 - 3:
        h = 0.001 + (TOP - 0.001) * between(f, c1 + 3, c2 - 3)
        along = a1 + SLICE * ease((h - 0.12) / 0.10)             # moves over for the next slice once clear
    elif f <= c2:
        h, along = fall(f, c2), a2
    elif f <= c2 + 3:
        h, along = jolt(f, c2), a2
    else:
        h, along = 0.001 + 0.06 * between(f, c2 + 4, 44), a2    # rests, then eases up a little
    return h, along, h < 0.115


def ham_at(f):
    c1, c2 = CHOPS
    cut, falling = FIRST_CUT, []
    for k, fc in enumerate(CHOPS):
        if f < fc:
            break
        a0 = FIRST_CUT + k * SLICE
        cut = a0 + SLICE
        s = np.clip((f - fc - 1) / 5.0, 0.0, 1.0)
        tip = 90.0 * s * s
        if f - fc == 7:
            tip = 84.0                                            # a small bounce as it lands
        falling.append((a0, a0 + SLICE, tip, BOARD.top + 0.0005 + 0.010 * k, s * s))
    first_slice = HAM_C - 0.147 * A + np.cross(A, [0, 1.0, 0]) * 0.115
    first_slice[1] = BOARD.top + 0.0035
    return Ham(HAM_C, ANGLE, cut=cut, slices=[slice_lying(first_slice, -ANGLE + 25)], falling=falling)


def cleaver_at(h, along, slide=0.0):
    """The cleaver with its edge h above the board, over the point `along` the ham (and slid `slide` along
    its own length, away from her)."""
    edge = HAM_C + along * A + slide * BLADE
    edge[1] = BOARD.top + 0.001 + h
    edge[2] -= 0.10 * min(h, TOP)                    # the lift swings back towards her a little (an arc)
    th = np.radians(12.0 * min(h, TOP) / TOP)        # the wrist cocks the blade's tip up as it rises
    x = BLADE * np.cos(th) + np.array([0, 1.0, 0]) * np.sin(th)
    y = -BLADE * np.sin(th) + np.array([0, 1.0, 0]) * np.cos(th)
    return Cleaver(edge, np.stack([x, y, A], 1))


def elbow_poles(h):
    return (np.array([-0.265, 1.120, -0.690 - 0.05 * (1 - min(h, TOP) / TOP)]),  # the elbow drops back as the
            np.array([0.175, 1.105, -0.575]))                                  # blade comes down


def frame(t):
    f = t * FPS
    board = BOARD
    ham = ham_at(f)
    h, along, in_meat = cleaver_path(f)
    cleaver = cleaver_at(h, along)
    # where she looks: the ham, until her eyes jump to her daughter; the head follows a moment later
    on_ham = HAM_C + (FIRST_CUT + 1.5 * SLICE) * A + np.array([0, 0.04, 0])
    eye = on_ham if f < GLANCE else DAUGHTER_EYES
    head = on_ham + (DAUGHTER_EYES - on_ham) * between(f, *HEAD)
    blink = {GLANCE: 0.5, GLANCE + 1: 1.0, GLANCE + 2: 0.75, GLANCE + 3: 0.5, GLANCE + 4: 0.25}.get(int(round(f)), 0.0)
    smile = 0.1 + 0.9 * between(f, *SMILE)
    mom = dict(position=(0.0, 0.0, -0.79), yaw=0.0, lean=6.0, head_look=head, eye_look=eye, smile=smile,
               blink=blink, cleaver=cleaver, ham=ham, press_along=0.045, press=0.004, grip_roll=GRIP_ROLL,
               poles=elbow_poles(h))
    # a plate of cherry tartlets with iced mistletoe, cooling on the worktop by where her daughter stands
    plate = PastryPlate((-0.05, 0.92, 0.22))
    return dict(t=t, camera=CAMERA, mother=mom, board=board, ham=ham, cleaver=cleaver, extras=[plate],
                blade_in_meat=in_meat)
