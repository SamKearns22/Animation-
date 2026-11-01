"""Patriots 4: the wide view from the Patriot's seat (shots 9 'his view' and 13 'reaction'; Sam, 1 Nov, animatic 2
note 26: "build the wide view").

The rest of the film is the camera turning on the spot over the coins (patriots4_room.PanCam), where everyone is drawn
at one distance. That cannot show two people 90 degrees apart round the table, so these two shots use a real camera
(a pinhole, in the plan's metres) at the Patriot's place, 3 o'clock: Romesh at 6 on the left, Bash at 9 straight
across, both STANDING at it (no chairs round this table: Sam, 1 Nov), hands on its rim; the same table (one size:
patriots4_room.TABLE_SCALE, as in Claudia's close-up) and coin pile, the room and its ceiling painted behind
(patriots4_room.room). Everyone faces the lens (rule 38; Romesh's likeness head has only a front view).

    python3 source/patriots4_wide.py OUT.jpg [T]     one frame of the wide view, for building
"""
import math
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import views as V                # noqa: E402
import patriots4_room as RM      # noqa: E402
import patriots4_plan as PL      # noqa: E402
from ed import INK, curve, oval  # noqa: E402

# ------------------------------------------------------------------------------------------------ the camera (metres)
CAM_AT = (1.15, -0.02)   # x east, z north: just behind the Patriot's head at his seat (clock 3, 0.62 m out): from
                         # nearer, the table and coins swelled far bigger than in Claudia's close-up (note 25)
EYE = 1.55               # about his eye height, looking a little down past his shoulder (bottom left)
HEADING = 252.0          # degrees (0 north, 90 east): between Romesh (6) and Bash (9)
FOCAL = 920.0            # pixels (a 61 degree field across the 1080 frame)
HORIZON_Y = 640.0        # where the eye line sits on screen (the camera looks a little down at the table)
BG_TURN = -14.0          # the painted room is drawn as seen from the table's centre; this camera is 1.15 m east of
                         # it, so the walls 3-4 m off sit about 14 degrees further round (and the wall torch at 242
                         # degrees no longer crowns Romesh's head; the Round Table hall is behind him, as in shot 3)
TABLE_R = 0.45           # the table's radius in metres: the drawn size (patriots4_room.TABLE_RX at the people's scale,
                         # Claudia's close-up), not the plan's old 0.37 m figure
COIN_R, COIN_T = 0.042, 0.018


def proj(x, y, z):
    """World point (metres) -> screen (pixels of the 1080 x 1920 frame) and its depth (metres from the lens)."""
    h = math.radians(HEADING)
    dx, dz = x - CAM_AT[0], z - CAM_AT[1]
    d = dx * math.sin(h) + dz * math.cos(h)
    u = dx * math.cos(h) - dz * math.sin(h)
    d = max(d, 0.05)
    return (540.0 + FOCAL * u / d, HORIZON_Y + FOCAL * (EYE - y) / d), d


def ppm(d):
    """Pixels per metre at depth d."""
    return FOCAL / d


def screen_cam():
    """burnham's camera for drawing straight in frame pixels."""
    return B.Cam(1.0, 540, 960)


# ------------------------------------------------------------------------------------------------ people
def seat_of(who):
    return PL.PEOPLE[who]['at']


def body(who, height_m):
    """(neck base x, y on screen for this person standing at their mark), drawing scale, scale for their height, depth."""
    x, z = seat_of(who)
    (sx, floor_y), d = proj(x, 0.0, z)
    s = ppm(d) * V.M_PER_UNIT                       # the scale patriots3_cast.person wants for a 1.75 m person
    s_real = s * height_m / 1.75
    return (sx, floor_y - 928.0 * s_real), s, s_real, d


YAW = {'romesh': 45.0, 'bash': 0.0}   # Romesh sits at the table's left side as seen from 3 o'clock: his body turned
                                      # to it (his hands reach its rim), his face to the lens (his likeness head is
                                      # front only: THREE_QUARTER_OK); Bash is straight across, front on
HANDS = {'romesh': (90.0, 190.0), 'bash': (112.0, 120.0)}   # (hands apart, reach forward), person units


def standing_hands(sp, j, s_real, neck, rim, who='bash'):
    """Standing at the table (as in every other shot, ref 03), both palms on its rim: `rim(x)` gives the rim's screen
    y at screen x."""
    yaw = YAW[who]
    apart, reach = HANDS[who]
    for side, sg in (('L', -1), ('R', 1)):
        hx = sg * apart
        y = 300.0
        for _ in range(3):                                   # aim the palm at the rim as it is seen on screen
            V.arm_to(j, side, (hx, y, reach), 'back', 'palm')
            (px, py), _d = V.project(j['wr' + side], yaw)
            sx = neck[0] + px * s_real
            want = (rim(sx) - neck[1]) / s_real
            y += want - py
        V.arm_to(j, side, (hx, y, reach), 'back', 'palm')
    return j


# ------------------------------------------------------------------------------------------------ the table and coins
def circle(r, y, n=160):
    return [proj(r * math.cos(a), y, r * math.sin(a))[0] for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]


def rim_y(x, r=TABLE_R):
    """The table's far rim (the side the people sit behind) at screen x: the top-most point of the outline there."""
    pts = circle(r, PL.TABLE_H, 360)
    best = None
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        if min(x0, x1) <= x <= max(x0, x1) and x0 != x1:
            y = y0 + (y1 - y0) * (x - x0) / (x1 - x0)
            best = y if best is None else min(best, y)
    if best is None:                                         # off the table's side: its nearest edge point
        best = min(pts, key=lambda q: abs(q[0] - x))[1]
    return best + 8.0


def pedestal(p, cx, cy, fx, fy, k):
    """patriots4_room.pedestal (turned legs round a central column, on a round plinth with a lit ring at the floor,
    ref 12) in metres. The other shots only show its top under the rim; seen whole here its legs are drawn stouter,
    as in ref 12, or they read as scratches."""
    w = 0.065 * k
    p.poly([(fx - 0.2 * k, fy - 0.07 * k), (fx + 0.2 * k, fy - 0.07 * k), (fx + 0.23 * k, fy + 0.02 * k),
            (fx - 0.23 * k, fy + 0.02 * k)], RM.PEDESTAL, INK, 2.0)                     # the plinth
    p.poly(oval(fx, fy + 0.02 * k, 0.33 * k, 0.07 * k, 40), (232, 170, 90), INK, 2.0)  # the lit ring at the floor
    p.poly(oval(fx, fy + 0.01 * k, 0.26 * k, 0.05 * k, 40), RM.PEDESTAL, INK, 1.8)
    y0 = cy + 0.03 * k
    for dx in (-0.16, 0.16, -0.075, 0.075):           # spaced as patriots4_room.pedestal's (+-84, +-34 of 332)
        leg(p, cx + dx * k, y0, fy - 0.07 * k, w)
    leg(p, cx, y0, fy - 0.07 * k, w * 1.15)


LEG, LEG_L = (120, 54, 34), (156, 84, 54)   # the table's own reddish wood: the room's darker pedestal brown is the
                                            # floor's colour, and seen whole against it only its outlines showed


def leg(p, x, y0, y1, w):
    """patriots4_room.turned_leg (a collar, a round bulb, a slim neck, a foot) in the table's wood."""
    RM.turned_leg(p, x, y0, y1, w, LEG, LEG_L)


def table(img):
    """The round winner's table (patriots4_room.table_top's colours and rings) in true perspective, with its edge band
    and the pedestal under it."""
    cam = screen_cam()
    p = B.Pen(img, cam)
    top = PL.TABLE_H
    (cx, cy), d = proj(0.0, top, 0.0)
    (fx, fy), _ = proj(0.0, 0.0, 0.0)
    pedestal(p, cx, cy, fx, fy, ppm(d))
    edge = [proj(TABLE_R * math.cos(a), top, TABLE_R * math.sin(a))[0] for a in np.linspace(0, 2 * math.pi, 200)]
    low = [proj(TABLE_R * math.cos(a), top - 0.04, TABLE_R * math.sin(a))[0] for a in np.linspace(0, 2 * math.pi, 200)]
    p.poly(low, RM.TABLE_D, INK, 2.4)                       # the edge band (the top's thickness)
    for i in range(len(edge) - 1):
        p.poly([edge[i], edge[i + 1], low[i + 1], low[i]], RM.TABLE_D, None)
    p.poly(circle(TABLE_R, top), RM.TABLE_RIM, INK, 2.6)
    p.poly(circle(TABLE_R * 0.955, top), RM.TABLE, INK, 2.0)
    p.poly(circle(TABLE_R * 0.84, top), RM.CREAM, INK, 1.6)
    p.poly(circle(TABLE_R * 0.8, top), RM.TABLE, INK, 1.6)
    p.poly(circle(TABLE_R * 0.5, top), RM.TABLE_D, None)


def coin_pile(img):
    """The coin pile as patriots4_room.coin_pile builds it (about 7 tiers, tallest in the middle, covering most of the
    top, a few scattered round its base), laid out in metres and seen from this camera."""
    cam = screen_cam()
    p = B.Pen(img, cam)
    rng = np.random.default_rng(4)
    step = COIN_R * 1.6
    stacks = []
    for j in range(-5, 6):
        for i in range(-5, 6):
            x, z = (i + (j % 2) * 0.5) * step, j * step * 0.9
            r = math.hypot(x, z) / (TABLE_R * 0.74)
            if r > 1.0:
                continue
            n = int(round(7.6 * (1 - r) + rng.uniform(-0.4, 0.6)))
            if n <= 0:
                continue
            stacks.append((x + rng.uniform(-0.004, 0.004), z + rng.uniform(-0.004, 0.004), n))
    for _ in range(6):                                       # a few scattered near the rim
        a = rng.uniform(0, 2 * math.pi)
        stacks.append((TABLE_R * 0.8 * math.cos(a), TABLE_R * 0.8 * math.sin(a), 1))
    stacks.sort(key=lambda s: -proj(s[0], PL.TABLE_H, s[1])[1])   # far first
    for x, z, n in stacks:
        for kk in range(n):
            (sx, sy), d = proj(x, PL.TABLE_H + kk * COIN_T, z)
            k = ppm(d) * COIN_R / RM.COIN_RX
            RM.coin(p, sx + k * rng.uniform(-3, 3), sy + RM.COIN_T * k, k)


# ------------------------------------------------------------------------------------------------ the room behind
def room(img, t):
    """The painted room (patriots4_room.room) turned to this camera's heading, at its field of view; its eye line on
    this camera's horizon."""
    z = FOCAL * math.pi / 180.0 / RM.K
    cy = RM.HORIZON - (HORIZON_Y - 960.0) / z
    pc = RM.PanCam(HEADING + BG_TURN, z, cy)
    RM.room(img, pc, t)
    return pc


def sheet(out, t=40.5):
    import patriots4 as P4
    B.SS = 1
    im = P4.frame_image(t).convert('RGB')
    im.save(out, quality=88)
    return out


if __name__ == '__main__':
    print(sheet(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 40.5))
