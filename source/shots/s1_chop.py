"""Shot 1 (2 s): the mother at the kitchen island, the cleaver raised over the ham, her left hand pressing
the meat steady. She chops two slices; her eyes find her daughter across the island; she smiles.
(See story/animation-test.md.) For now: its first frame, the approved still."""
import numpy as np

from props import Board, Ham, Cleaver, PastryPlate, slice_lying
from rig import unit

DURATION = 2.0
CAMERA = dict(pos=(0.85, 1.60, 2.30), target=(0.36, 1.37, -0.55), vfov=19.0)
DAUGHTER_EYES = np.array([0.30, 1.05, 0.62])   # across the island, almost opposite her, a little to her left

ANGLE = -30.0                                   # the ham lies at this angle; the blade comes down across it
A = np.array([np.cos(np.radians(ANGLE)), 0.0, np.sin(np.radians(ANGLE))])     # along the ham
BLADE = np.array([-np.sin(np.radians(ANGLE)), 0.0, np.cos(np.radians(ANGLE))])  # along the blade, to its tip
CUT = np.array([-0.110, 0.985, -0.360])         # where the next cut falls
HOVER = 0.165                                    # the cleaver held up this far before the chop


def frame(t):
    board = Board((-0.03, 0.940, -0.330), (0.285, 0.020, 0.190))
    ham_c = CUT + 0.072 * A
    ham_c[1] = board.top + 0.058
    first_slice = CUT - 0.075 * A + np.cross(A, [0, 1.0, 0]) * 0.075
    first_slice[1] = board.top + 0.0035
    ham = Ham(ham_c, ANGLE, cut=-0.087, slices=[slice_lying(first_slice, -ANGLE + 25)])
    cleaver = Cleaver(CUT + np.array([0, HOVER, 0]) - 0.008 * A, np.stack([BLADE, [0, 1.0, 0], A], 1))
    mom = dict(position=(0.0, 0.0, -0.79), yaw=0.0, lean=6.0, look_at=DAUGHTER_EYES, smile=1.0,
               cleaver=cleaver, ham=ham, press_along=0.045, press=0.004,
               poles=(np.array([-0.265, 1.120, -0.690]), np.array([0.175, 1.105, -0.575])))
    # a plate of cherry tartlets with iced mistletoe, cooling on the worktop by where her daughter stands
    plate = PastryPlate((-0.05, 0.92, 0.22))
    return dict(t=t, camera=CAMERA, mother=mom, board=board, ham=ham, cleaver=cleaver, extras=[plate])
