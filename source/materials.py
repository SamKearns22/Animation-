"""Materials shared by every shot: colour, shine, mirror, glow, soft light wrap (skin) and surface pattern,
plus the renderer's default scene parameters. The drawing (graphite.py) also decides from these which
things are the characters, which are props and which keep their colour."""
import numpy as np

import sdf3d as S

# ---------------------------------------------------------------------------
# Materials: colour, shine, mirror, glow, soft light wrap (skin), surface pattern
# ---------------------------------------------------------------------------
MATS = []


def material(rgb, spec=0.0, shin=10.0, refl=0.0, emit=0.0, wrap=0.0, tex=0):
    MATS.append(list(rgb) + [spec, shin, refl, emit, wrap, tex])
    return len(MATS) - 1


SKIN = material((0.80, 0.60, 0.50), spec=0.10, shin=14, wrap=0.35, tex=S.T_SKIN)
LIPS = material((0.64, 0.34, 0.32), spec=0.22, shin=26, wrap=0.3, tex=S.T_SKIN)
LID = material((0.79, 0.58, 0.49), spec=0.08, shin=14, wrap=0.35, tex=S.T_LID)
EYE = material((0.86, 0.84, 0.82), spec=0.9, shin=220, tex=S.T_EYE)
NOSTRIL = material((0.36, 0.20, 0.17), wrap=0.3)
HAIR = material((0.060, 0.043, 0.034), spec=0.15, shin=50, tex=S.T_HAIR)
KNIT = material((0.80, 0.71, 0.58), wrap=0.25, tex=S.T_KNIT)
NAIL = material((0.84, 0.66, 0.60), spec=0.35, shin=40, wrap=0.2)
WOOD = material((0.66, 0.48, 0.31), spec=0.05, shin=12, tex=S.T_WOODGRAIN)
MEAT = material((0.60, 0.29, 0.08), spec=0.65, shin=70, refl=0.05, tex=S.T_MEAT)   # honey-mustard glaze
HAMPINK = material((0.86, 0.52, 0.47), spec=0.25, shin=30, wrap=0.2)
PINEAPPLE = material((0.96, 0.78, 0.24), spec=0.45, shin=40, wrap=0.2)
CHERRY = material((0.62, 0.02, 0.06), spec=0.9, shin=120, refl=0.05)
PAPER = material((0.96, 0.95, 0.92), spec=0.02, shin=8, wrap=0.3)
BONE = material((0.80, 0.74, 0.62), spec=0.1, shin=20, wrap=0.1)
STEEL = material((0.30, 0.31, 0.33), spec=0.9, shin=90, refl=0.05, tex=S.T_STEEL)
HANDLE = material((0.10, 0.065, 0.045), spec=0.4, shin=50)
PAINT = material((0.88, 0.875, 0.855), spec=0.10, shin=30)
BLACKMETAL = material((0.035, 0.035, 0.035), spec=0.6, shin=60, refl=0.08)
MARBLE = material((0.93, 0.93, 0.915), spec=0.45, shin=110, refl=0.14, tex=S.T_MARBLE)
WALL = material((0.90, 0.885, 0.865), spec=0.02, shin=8)
FLOOR = material((0.60, 0.47, 0.34), spec=0.25, shin=40, refl=0.05, tex=S.T_WOODGRAIN)
OUTSIDE = material((1.0, 1.0, 1.0), emit=1.55, tex=S.T_WINDOW)
BULB = material((1.0, 0.86, 0.62), emit=5.0)
WAX = material((0.94, 0.915, 0.86), spec=0.12, shin=20, wrap=0.55)
FLAME = material((1.0, 0.78, 0.45), emit=6.0)
NEEDLES = material((0.06, 0.11, 0.07), spec=0.1, shin=15, tex=S.T_NEEDLES)
TRAY = material((0.55, 0.50, 0.44), spec=0.05, shin=10, tex=S.T_TRAY)
GOLD = material((0.78, 0.62, 0.30), spec=0.9, shin=80, refl=0.2)
IVORY = material((0.92, 0.90, 0.86), spec=0.5, shin=60)
BAUBLE_RED = material((0.62, 0.04, 0.06), spec=0.9, shin=90, refl=0.15)
FAIRY = material((1.0, 0.86, 0.55), emit=3.5)
CEILING = material((0.93, 0.925, 0.91), spec=0.0, shin=5)
DOWNLIGHT = material((1.0, 0.95, 0.86), emit=3.5)
CLEMENTINE = material((0.86, 0.42, 0.10), spec=0.35, shin=40, wrap=0.2)
CERAMIC = material((0.80, 0.80, 0.78), spec=0.5, shin=60, refl=0.06)
WARMWALL = material((0.80, 0.72, 0.60), spec=0.02, shin=8)


def mat_table():
    return np.array(MATS, dtype=np.float64)

TROUSERS = material((0.10, 0.10, 0.12), spec=0.08, shin=12, wrap=0.2)
FELT = material((0.70, 0.06, 0.08), spec=0.02, shin=6, wrap=0.35)            # the daughter's Santa hat
FUR = material((0.95, 0.94, 0.90), spec=0.02, shin=5, wrap=0.4)
STRAW_HAIR = material((0.62, 0.50, 0.30), spec=0.15, shin=40, tex=S.T_HAIR)   # her straw-coloured hair


def new_params():
    SP = np.zeros(128)
    SP[60], SP[61] = 0.28, 0.08  # sky fill, flat fill
    SP[62:65] = (1.0, 0.98, 0.96)
    SP[46:49] = (1.0, 0.0, 0.0)
    return SP



def default_lights(key_dir=(0.55, 0.45, 0.70)):
    k = np.asarray(key_dir, float)
    k /= np.linalg.norm(k)
    # type, x, y, z, r, g, b, shadow (0 none, 1 traced, 2 shadow map), softness, range, first map, maps
    return np.array([[0, *k, 1.25, 1.18, 1.08, 2, 10.0, 0, 0, 1],
                     [0, -0.6, 0.3, -0.5, 0.30, 0.30, 0.32, 0, 6.0, 0, 0, 0]], dtype=np.float64)


