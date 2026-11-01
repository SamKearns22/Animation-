#!/usr/bin/env python3
"""The Jackdaw rig (Flying Whales, 1 Nov): 31 breakable parts in real metres, drawn flat in the house style through
the film's one locked camera (the same camera the whales use, so sizes, depth and draw order all agree).

Why parts in metres and not one painting: the camera never moves (rule 39), but the rig is smashed into pieces that
tip, spin and fall, the whole deck tips as one block and slides under, and five whales pass between its legs and
through its decks. A part drawn from its measurements through the camera tips the right way, hides behind the right
leg, and is cut off by the waterline as it sinks. Each part is simple boxes and tubes (no 3D rendering library): flat
colour, a lit and a shadow tone, one ink outline round every part and every box edge, corners hand-cut (a little
wobble on each corner, fixed per corner so nothing boils from frame to frame).

From Sam's Jackdaw references (references/flying-whales/rig-jackdaw-*): a yellow four-legged jacket with X bracing;
boxy grey and white decks on yellow deck girders, three storeys, railings; a helideck cantilevered out on a lattice
truss over an orange escape chute; a yellow crane pedestal with a red-and-white boom; the yellow JACKDAW board. From
the other refs and the approved Showstopper list: a flare boom with its flame, chimneys, a derrick, lifeboats, a
walkway stub, warm lit windows at dusk.

Sizes (notes "The world"): deck block 50 x 35 m, three storeys to 48 m; jacket legs 25 m from the water to the deck;
crane boom 35 m; flare boom 45 m; helideck about 20 m across; lifeboats 8.5 m.

Rig-local axes: X along the long side (east), Y across (north, away from the camera side), Z up; origin at the
jacket's centre on the sea. The rig is placed in the world (whale.py's axes: x right, y away from the camera, z up)
by PLACE.

    python3 source/flying_whales_rig.py sheet OUT.jpg       the rig in the film's frame beside a 14 m whale, the 31
                                                            parts numbered, a test of parts moving (for Sam)
    python3 source/flying_whales_rig.py still OUT.png [--small]   the film's frame at rest (placeholder sky and sea)
    python3 source/flying_whales_rig.py check               the line-work check on the rig alone
    python3 source/benchmark.py flying_whales_rig OUT.jpg   rule 3: ours beside the references, ticked

Use in the film:
    import flying_whales_rig as R
    cam = R.film_cam(small=False)
    st = R.State()                                   # every part at rest
    st.move('leg_SW', rot=(0, 25, 0), shift=(-3, -2, -6))   # degrees about the part's pivot, metres
    st.whole(rot=(0, -20, 0), pivot=(25, 0, 25), shift=(0, 0, -12))   # the finale: everything as one block
    spr = R.draw(cam, st, t)                         # a Sprite: .img, .xy, .depth_map (metres, for compositing)
    R.composite(frame, [spr, whale_sprite, ...])     # nearer pixels win, per pixel
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage as ND

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import whale as W                # noqa: E402  the camera, the whale (same camera for both)

NAME = 'flying-whales'
INK = W.INK

# colours (lit, shadow): every one kept above the line check's ink darkness (luma 85)
YELLOW = ((240, 198, 44), (198, 152, 34))
GREY = ((176, 180, 186), (132, 138, 148))
WHITE = ((230, 230, 224), (186, 190, 196))
DGREY = ((138, 142, 148), (108, 112, 122))
ORANGE = ((242, 124, 42), (202, 96, 36))
RED = ((214, 72, 60), (176, 64, 56))
BLUE = ((72, 122, 198), (58, 100, 168))
GREEN = ((98, 130, 98), (82, 110, 84))
GLASS = ((128, 156, 176), (108, 134, 154))
LIT_WINDOW = (255, 216, 122)                       # warm lit windows and deck lights (dusk refs): never tinted
RAIL = (226, 226, 218)
MARK_Y, MARK_W = (240, 206, 60), (238, 238, 232)  # helideck circle and H

LIGHT = np.array([0.72, -0.38, 0.58])              # the low dusk sun from the right, a little towards us
LIGHT = LIGHT / np.linalg.norm(LIGHT)

# where the rig stands in the world, and the film's camera (notes "The world": locked, about 120 m from the nearest
# corner, 8 m above the sea, the rig seen on the diagonal, the whole rig in frame with sky above for the smoke)
PLACE = dict(yaw=30.0, pos=(6.0, 0.0, 0.0))
CAM = dict(pos=(0.0, -150.0, 8.0), focal=1450.0, horizon=1250)
SEA_LEVEL = 0.0


class FilmCam(W.Cam):
    """whale.Cam looking level along +y, with the horizon lowered to `horizon` px (a shifted lens: verticals stay
    upright, as in the flat house style, while the frame shows the sky above the rig)."""
    def __init__(self, pos, focal, size, horizon):
        super().__init__(pos, 0.0, 0.0, focal, size)
        self.horizon = horizon

    def screen(self, P):
        q = self.cam(P)
        d = np.maximum(q[..., 1], 0.05)
        x = self.size[0] / 2 + self.focal * q[..., 0] / d
        y = self.horizon - self.focal * q[..., 2] / d
        return np.stack([x, y], -1), q[..., 1]


def film_cam(small=False, size=None):
    size = size or ((540, 960) if small else (1080, 1920))
    k = size[0] / 1080
    return FilmCam(CAM['pos'], CAM['focal'] * k, size, CAM['horizon'] * k)


# ------------------------------------------------ building blocks ---------------------------------------------------
def _jit(P, amt):
    """Hand-cut wobble: a fixed nudge per corner (the same corner always moves the same way, so shared corners stay
    joined and nothing boils)."""
    P = np.asarray(P, float)
    if amt <= 0:
        return P
    out = P.copy()
    for k, v in enumerate(((12.9898, 78.233, 37.719), (39.346, 11.135, 83.155), (73.156, 52.235, 9.151))):
        h = np.sin(P @ np.array(v)) * 43758.5453
        out[..., k] += (h - np.floor(h) - 0.5) * 2 * amt
    return out


class Part:
    def __init__(self, name, label, parent, pivot):
        self.name, self.label, self.parent = name, label, parent
        self.pivot = np.asarray(pivot, float)       # rig-local point it turns about when knocked
        self.faces = []                              # dict(pts, mat, prim, fold, centre, key)
        self.decals = []                             # dict(pts, colour, kind) flat paint on a face (windows, marks)
        self.strokes = []                            # (a, b, kind) lattice lines ('ink') and railings ('rail')
        self.texts = []                              # dict(pts (4 corners: tl, tr, br, bl), text)
        self.flame = None                            # rig-local point of a flare tip
        self._prim = 0

    def _new_prim(self):
        self._prim += 1
        return self._prim

    def box(self, x0, y0, z0, x1, y1, z1, mat, amt=0.3, windows=None, rails=None, decal_faces=None):
        """An axis-aligned box. windows: dict(faces='SWEN', rows=[z...], step, w, h, skip=[(axis lo, hi)]).
        rails: faces whose top edge gets a railing ('SWEN')."""
        c = np.array([x0 + x1, y0 + y1, z0 + z1]) / 2
        V = np.array([[x, y, z] for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)], float)
        J = _jit(V, amt)
        # corner index: (z, y, x) bits
        quads = {'B': (0, 1, 3, 2), 'T': (4, 6, 7, 5), 'S': (0, 4, 5, 1), 'N': (2, 3, 7, 6),
                 'W': (0, 2, 6, 4), 'E': (1, 5, 7, 3)}
        prim = self._new_prim()
        for f, q in quads.items():
            self.faces.append(dict(pts=J[list(q)], mat=mat, prim=prim, fold=True, centre=c, key=f))
        if windows:
            self._windows(x0, y0, z0, x1, y1, z1, **windows)
        for f in (rails or ''):
            self._rail(x0, y0, x1, y1, z1, f)

    def _face_frame(self, x0, y0, x1, y1, f):
        """A face's start corner, its along-the-face unit vector, its length, its outward normal."""
        if f == 'S':
            return np.array([x0, y0]), np.array([1.0, 0]), x1 - x0, np.array([0, -1.0])
        if f == 'N':
            return np.array([x1, y1]), np.array([-1.0, 0]), x1 - x0, np.array([0, 1.0])
        if f == 'W':
            return np.array([x0, y1]), np.array([0, -1.0]), y1 - y0, np.array([-1.0, 0])
        return np.array([x1, y0]), np.array([0, 1.0]), y1 - y0, np.array([1.0, 0])

    def _windows(self, x0, y0, z0, x1, y1, z1, faces='S', rows=(), step=3.0, w=1.3, h=0.9, skip=(), colour=None):
        for f in faces:
            o, u, L, n = self._face_frame(x0, y0, x1, y1, f)
            k = int((L - 2.0) // step)
            if k < 1:
                continue
            start = (L - (k - 1) * step) / 2
            for z in rows:
                for i in range(k):
                    s = start + i * step
                    p = o + u * s + n * 0.12
                    along = p[0] if abs(u[0]) > 0.5 else p[1]
                    if any(lo <= along <= hi for lo, hi in skip):
                        continue
                    a, b = p - u * w / 2, p + u * w / 2
                    self.decals.append(dict(pts=np.array([[a[0], a[1], z - h / 2], [b[0], b[1], z - h / 2],
                                                          [b[0], b[1], z + h / 2], [a[0], a[1], z + h / 2]]),
                                            colour=colour or LIT_WINDOW, kind='glow' if colour is None else 'paint',
                                            face=(self._prim, f)))

    def _rail(self, x0, y0, x1, y1, z, f, hgt=1.1, post=3.0):
        o, u, L, n = self._face_frame(x0, y0, x1, y1, f)
        o = o + n * 0.15
        a, b = o, o + u * L
        self.strokes.append((np.array([a[0], a[1], z + hgt]), np.array([b[0], b[1], z + hgt]), 'rail'))
        for i in range(int(L // post) + 1):
            p = o + u * min(L, i * post)
            self.strokes.append((np.array([p[0], p[1], z]), np.array([p[0], p[1], z + hgt]), 'rail'))

    def tube(self, a, b, r, mat, n=8, r1=None, amt=0.1, fold=False):
        """A prism of n sides from a to b, radius r (r1 at b: a taper)."""
        a, b = np.asarray(a, float), np.asarray(b, float)
        ax = b - a
        L = np.linalg.norm(ax)
        ax = ax / L
        ref = np.array([0, 0, 1.0]) if abs(ax[2]) < 0.9 else np.array([1.0, 0, 0])
        e1 = np.cross(ax, ref)
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(ax, e1)
        r1 = r if r1 is None else r1
        ang = [2 * math.pi * (k + 0.5) / n for k in range(n)]
        ra = np.array([a + r * (math.cos(t) * e1 + math.sin(t) * e2) for t in ang])
        rb = np.array([b + r1 * (math.cos(t) * e1 + math.sin(t) * e2) for t in ang])
        ra, rb = _jit(ra, amt), _jit(rb, amt)
        c = (a + b) / 2
        prim = self._new_prim()
        for k in range(n):
            q = np.array([ra[k], ra[(k + 1) % n], rb[(k + 1) % n], rb[k]])
            self.faces.append(dict(pts=q, mat=mat, prim=prim, fold=fold, centre=c, key=f's{k}'))
        self.faces.append(dict(pts=ra[::-1], mat=mat, prim=prim, fold=True, centre=c, key='a'))
        self.faces.append(dict(pts=rb, mat=mat, prim=prim, fold=True, centre=c, key='b'))

    def beam(self, a, b, w, h, mat, amt=0.15, up=(0, 0, 1)):
        """A box from a to b (its centre line), w wide and h tall across it."""
        a, b = np.asarray(a, float), np.asarray(b, float)
        ax = (b - a) / np.linalg.norm(b - a)
        side = np.cross(ax, np.asarray(up, float))
        if np.linalg.norm(side) < 1e-6:
            side = np.cross(ax, np.array([1.0, 0, 0]))
        side /= np.linalg.norm(side)
        upv = np.cross(side, ax)
        V = []
        for p in (a, b):
            for sy in (-1, 1):
                for sz in (-1, 1):
                    V.append(p + side * sy * w / 2 + upv * sz * h / 2)
        V = _jit(np.array(V), amt)
        # 0..3 at a: (-,-) (-,+) (+,-) (+,+); 4..7 at b
        quads = {'a': (0, 1, 3, 2), 'b': (4, 6, 7, 5), 'l': (0, 4, 5, 1), 'r': (2, 3, 7, 6),
                 'd': (0, 2, 6, 4), 'u': (1, 5, 7, 3)}
        c = (a + b) / 2
        prim = self._new_prim()
        for f, q in quads.items():
            self.faces.append(dict(pts=V[list(q)], mat=mat, prim=prim, fold=True, centre=c, key=f))

    def zigzag(self, A, B, n):
        """Lattice lacing between two chords A and B (each from start to end): n zigzag ink lines."""
        A0, A1 = (np.asarray(p, float) for p in A)
        B0, B1 = (np.asarray(p, float) for p in B)
        pts = []
        for i in range(n + 1):
            f = i / n
            pts.append((A0 + (A1 - A0) * f) if i % 2 == 0 else (B0 + (B1 - B0) * f))
        for p, q in zip(pts, pts[1:]):
            self.strokes.append((p, q, 'ink'))

    def prism_x(self, x0, x1, section, mat, amt=0.1):
        """A prism along X with a cross-section given as (y, z) points (anticlockwise seen from +X)."""
        S = np.asarray(section, float)
        n = len(S)
        ra = _jit(np.array([[x0, y, z] for y, z in S]), amt)
        rb = _jit(np.array([[x1, y, z] for y, z in S]), amt)
        c = np.array([(x0 + x1) / 2, S[:, 0].mean(), S[:, 1].mean()])
        prim = self._new_prim()
        for k in range(n):
            q = np.array([ra[k], ra[(k + 1) % n], rb[(k + 1) % n], rb[k]])
            self.faces.append(dict(pts=q, mat=mat, prim=prim, fold=True, centre=c, key=f's{k}'))
        self.faces.append(dict(pts=ra[::-1], mat=mat, prim=prim, fold=True, centre=c, key='a'))
        self.faces.append(dict(pts=rb, mat=mat, prim=prim, fold=True, centre=c, key='b'))


# ------------------------------------------------ the rig, part by part ---------------------------------------------
LEG_BOT = {'SW': (-13.0, -9.0), 'SE': (13.0, -9.0), 'NW': (-13.0, 9.0), 'NE': (13.0, 9.0)}
LEG_TOP = {'SW': (-11.0, -7.5), 'SE': (11.0, -7.5), 'NW': (-11.0, 7.5), 'NE': (11.0, 7.5)}
JACKET_TOP = 25.0
BAYS = (1.0, 12.5, 24.3)
FACE_LEGS = {'S': ('SW', 'SE'), 'N': ('NE', 'NW'), 'W': ('NW', 'SW'), 'E': ('SE', 'NE')}


def leg_at(leg, z):
    b, t = np.array(LEG_BOT[leg]), np.array(LEG_TOP[leg])
    p = b + (t - b) * z / JACKET_TOP
    return np.array([p[0], p[1], z])


def build():
    P = {}

    def part(name, label, parent, pivot):
        P[name] = Part(name, label, parent, pivot)
        return P[name]

    # the jacket: four battered legs (wider at the sea) and X bracing in two bays on each face
    for leg in ('SW', 'SE', 'NW', 'NE'):
        p = part(f'leg_{leg}', f'leg {leg}', None, leg_at(leg, 0))
        p.tube(leg_at(leg, -6), leg_at(leg, JACKET_TOP), 1.0, YELLOW, n=8, amt=0.08)
    for f, (l1, l2) in FACE_LEGS.items():
        for bay, (z0, z1) in (('low', BAYS[:2]), ('high', BAYS[1:])):
            p = part(f'brace_{f}_{bay}', f'bracing {f} {bay}', None, (leg_at(l1, z1) + leg_at(l2, z1)) / 2)
            p.tube(leg_at(l1, z1), leg_at(l2, z1), 0.55, YELLOW, n=6, amt=0.06)
            if bay == 'low':
                p.tube(leg_at(l1, z0), leg_at(l2, z0), 0.55, YELLOW, n=6, amt=0.06)
            p.tube(leg_at(l1, z0), leg_at(l2, z1), 0.45, YELLOW, n=6, amt=0.06)
            p.tube(leg_at(l2, z0), leg_at(l1, z1), 0.45, YELLOW, n=6, amt=0.06)

    # storey 1, the cellar deck: a yellow deck girder, grey modules set back with a railing on the ledge
    for half, (x0, x1) in (('W', (-25.0, 0.0)), ('E', (0.0, 25.0))):
        p = part(f'deck1_{half}', f'cellar deck {half}', None, (x0 if half == 'E' else x1, 0, 25))
        p.box(x0, -17.5, 25.0, x1, 17.5, 26.6, YELLOW, amt=0.4)
        mx0, mx1 = (x0 + 0.8, x1) if half == 'W' else (x0, x1 - 0.8)
        p.box(mx0, -16.7, 26.6, mx1, 16.7, 32.0, GREY, amt=0.45,
              windows=dict(faces='SWEN', rows=(29.3,), step=3.4, w=1.4, h=1.0,
                           skip=((3.0, 23.0),) if half == 'E' else ()),
              )
        p._rail(x0, -17.5, x1, 17.5, 26.6, 'S')
        p._rail(x0, -17.5, x1, 17.5, 26.6, 'W' if half == 'W' else 'E')

    # the JACKDAW board on the cellar deck's front (ref rig-jackdaw-close: yellow, black capitals)
    p = part('board', 'JACKDAW board', 'deck1_E', (12.0, -16.9, 27.6))
    p.box(3.0, -17.25, 27.4, 22.0, -16.75, 31.2, YELLOW, amt=0.12)
    p.texts.append(dict(pts=np.array([[3.7, -17.4, 30.85], [21.3, -17.4, 30.85], [21.3, -17.4, 27.75],
                                      [3.7, -17.4, 27.75]]), text='JACKDAW'))

    # storey 2, the process deck: yellow girder, white modules, two rows of lit windows
    for half, (x0, x1) in (('W', (-24.0, 0.0)), ('E', (0.0, 24.0))):
        p = part(f'deck2_{half}', f'process deck {half}', f'deck1_{half}', (x0 if half == 'E' else x1, 0, 32))
        p.box(x0, -16.5, 32.0, x1, 16.5, 33.2, YELLOW, amt=0.4)
        mx0, mx1 = (x0 + 0.8, x1) if half == 'W' else (x0, x1 - 0.8)
        p.box(mx0, -15.7, 33.2, mx1, 15.7, 40.0, WHITE, amt=0.45,
              windows=dict(faces='SWEN', rows=(35.4, 37.9), step=2.9, w=1.3, h=0.9,
                           skip=((-23.4, -5.0),) if half == 'W' else ()),
              )
        p._rail(x0, -16.5, x1, 16.5, 33.2, 'S')
        p._rail(x0, -16.5, x1, 16.5, 33.2, 'W' if half == 'W' else 'E')

    # two orange lifeboats on davits on the process deck's front (enclosed, as on North Sea rigs)
    for k, xc in enumerate((-18.8, -9.6)):
        p = part(f'lifeboat_{k + 1}', f'lifeboat {k + 1}', 'deck2_W', (xc, -16.2, 37.6))
        yc = -17.4
        sec = [(yc - 1.5, 34.5), (yc + 1.5, 34.5), (yc + 1.6, 35.6), (yc + 1.1, 37.0), (yc - 1.1, 37.0), (yc - 1.6, 35.6)]
        p.prism_x(xc - 4.2, xc + 4.2, sec, ORANGE)
        p.prism_x(xc - 3.0, xc + 3.0, [(yc - 0.9, 37.0), (yc + 0.9, 37.0), (yc + 0.6, 37.6), (yc - 0.6, 37.6)], ORANGE)
        for dx in (-3.4, 3.4):                       # the davit arms from the deck wall out over the boat
            p.beam((xc + dx, -15.7, 38.6), (xc + dx, yc, 38.6), 0.4, 0.5, DGREY)
            p.strokes.append((np.array([xc + dx, yc, 38.4]), np.array([xc + dx * 0.8, yc, 37.3]), 'ink'))

    # storey 3: the white control and living module (west), the grey process module (east)
    p = part('quarters', 'living module', 'deck2_W', (-5.0, 0, 40))
    p.box(-23.0, -15.0, 40.0, -5.0, 3.0, 47.0, WHITE, amt=0.3,
          windows=dict(faces='SWEN', rows=(42.2, 44.6), step=2.6, w=1.4, h=1.0))
    p.box(-19.0, -10.0, 47.0, -12.0, -4.0, 48.6, DGREY, amt=0.2)     # roof plant
    p = part('process', 'process module', 'deck2_E', (1.0, 0, 40))
    p.box(1.0, -12.0, 40.0, 21.0, 12.0, 46.0, GREY, amt=0.3,
          windows=dict(faces='SWEN', rows=(43.0,), step=3.2, w=1.4, h=1.0))

    # containers on the process deck roof (my set dressing: a blue and a red 20 ft container)
    p = part('cargo', 'containers', 'deck2_E', (9.0, -13.0, 40))
    p.box(2.0, -15.4, 40.0, 8.06, -12.8, 42.6, BLUE, amt=0.08)
    p.box(9.0, -15.4, 40.0, 15.06, -12.8, 42.6, RED, amt=0.08)

    # the yellow crane pedestal and cab (Jackdaw's yellow tower) and its red-and-white lattice boom
    p = part('crane_pedestal', 'crane pedestal', 'deck2_W', (-2.0, -12.0, 40))
    p.tube((-2.0, -12.0, 40.0), (-2.0, -12.0, 52.0), 1.9, YELLOW, n=8, amt=0.08)
    p.box(-4.6, -14.6, 52.0, 0.8, -9.6, 55.4, YELLOW, amt=0.15,
          windows=dict(faces='SW', rows=(54.0,), step=1.8, w=1.2, h=1.1, colour=GLASS[0]))
    root, tip = np.array([-4.2, -13.0, 53.4]), np.array([-30.0, -16.0, 71.0])
    p = part('crane_boom', 'crane boom', 'crane_pedestal', root)
    ax = (tip - root) / np.linalg.norm(tip - root)
    side = np.cross(ax, [0, 0, 1.0])
    side /= np.linalg.norm(side)
    up = np.cross(side, ax)
    chords = []
    for s in (-1, 1):
        a0 = root + side * s * 1.1
        a1 = tip + side * s * 0.35
        mid = a0 + (a1 - a0) * 0.82
        p.tube(a0, mid, 0.42, WHITE, n=6, amt=0.04)
        p.tube(mid, a1, 0.42, RED, n=6, amt=0.04)
        chords.append((a0, a1))
    top0 = root + up * 1.6
    top1 = tip + up * 0.3
    p.tube(top0, top1, 0.32, WHITE, n=6, amt=0.04)
    p.zigzag(chords[0], (top0, top1), 18)
    p.zigzag(chords[1], (top0, top1), 18)
    p.zigzag(chords[0], chords[1], 18)
    p.strokes.append((tip.copy(), tip + np.array([0, 0, -16.0]), 'ink'))         # the hoist line and hook block
    p.box(tip[0] - 0.5, tip[1] - 0.5, tip[2] - 17.4, tip[0] + 0.5, tip[1] + 0.5, tip[2] - 16.0, DGREY, amt=0.05)

    # the derrick: a tapering white lattice tower on its substructure
    p = part('derrick', 'derrick', 'process', (13.0, 5.0, 46))
    p.box(8.5, 0.5, 46.0, 17.5, 9.5, 48.2, DGREY, amt=0.2)
    base = [(8.8, 0.8), (17.2, 0.8), (17.2, 9.2), (8.8, 9.2)]
    top = [(12.0, 4.0), (14.0, 4.0), (14.0, 6.0), (12.0, 6.0)]
    legs = []
    for (bx, by), (tx, ty) in zip(base, top):
        a, b = np.array([bx, by, 48.2]), np.array([tx, ty, 76.0])
        p.tube(a, b, 0.45, WHITE, n=6, amt=0.04)
        legs.append((a, b))
    for i in range(4):
        A, B = legs[i], legs[(i + 1) % 4]
        p.zigzag(A, B, 9)
        for f in np.linspace(0.12, 0.92, 6):          # the girts across each face
            p.strokes.append((A[0] + (A[1] - A[0]) * f, B[0] + (B[1] - B[0]) * f, 'ink'))
    p.box(11.4, 3.4, 76.0, 14.6, 6.6, 78.0, DGREY, amt=0.1)                   # the crown block

    # chimneys: three exhaust stacks with red tops
    p = part('stacks', 'chimneys', 'process', (18.0, -4.0, 46))
    for (x, y, h) in ((16.6, -7.0, 58.0), (19.0, -7.0, 56.5), (17.8, -3.4, 59.0)):
        p.tube((x, y, 46.0), (x, y, h - 1.4), 0.9, GREY, n=8, amt=0.05)
        p.tube((x, y, h - 1.4), (x, y, h), 0.95, RED, n=8, amt=0.05)

    # the flare boom: a yellow triangular lattice out over the sea, the flare tip and its flame
    root, tip = np.array([24.0, 2.0, 40.5]), np.array([50.0, 0.0, 63.0])
    p = part('flare_boom', 'flare boom', 'deck2_E', root)
    ax = (tip - root) / np.linalg.norm(tip - root)
    side = np.cross(ax, [0, 0, 1.0])
    side /= np.linalg.norm(side)
    up = np.cross(side, ax)
    ch = []
    for off0, off1 in ((side * 1.4 - up * 0.8, side * 0.6 - up * 0.35), (-side * 1.4 - up * 0.8, -side * 0.6 - up * 0.35),
                       (up * 1.6, up * 0.7)):
        a, b = root + off0, tip + off1
        p.tube(a, b, 0.4, YELLOW, n=6, amt=0.04)
        ch.append((a, b))
    for i in range(3):
        p.zigzag(ch[i], ch[(i + 1) % 3], 16)
    p.tube(tip, tip + np.array([0, 0, 2.6]), 0.75, DGREY, n=8, amt=0.03)
    p.flame = tip + np.array([0, 0, 2.6])

    # the helideck on its lattice truss, out past the west end (ref rig-jackdaw-helipad), the orange chute below
    p = part('helideck', 'helideck', 'helideck_truss', (-26.0, 0.0, 45.4))
    cx, cy, R8 = -37.0, -1.0, 11.0
    oct_ = [(cx + R8 * math.cos(math.radians(22.5 + 45 * k)), cy + R8 * math.sin(math.radians(22.5 + 45 * k)))
            for k in range(8)]
    Vb = np.array([[x, y, 45.4] for x, y in oct_])
    Vt = np.array([[x, y, 46.4] for x, y in oct_])
    Vb, Vt = _jit(Vb, 0.15), _jit(Vt, 0.15)
    c = np.array([cx, cy, 45.9])
    prim = p._new_prim()
    for k in range(8):
        p.faces.append(dict(pts=np.array([Vb[k], Vb[(k + 1) % 8], Vt[(k + 1) % 8], Vt[k]]), mat=DGREY, prim=prim,
                            fold=False, centre=c, key=f's{k}'))
    p.faces.append(dict(pts=Vt, mat=GREEN, prim=prim, fold=True, centre=c, key='T'))
    p.faces.append(dict(pts=Vb[::-1], mat=DGREY, prim=prim, fold=True, centre=c, key='B'))
    ring_o, ring_i = 6.2, 5.0                        # the yellow touchdown circle and the white H (seen when it tips)
    for k in range(20):
        a0, a1 = 2 * math.pi * k / 20, 2 * math.pi * (k + 1) / 20
        q = [(cx + r * math.cos(a), cy + r * math.sin(a)) for r, a in ((ring_o, a0), (ring_o, a1), (ring_i, a1), (ring_i, a0))]
        p.decals.append(dict(pts=np.array([[x, y, 46.5] for x, y in q]), colour=MARK_Y, kind='paint', face=(prim, 'T')))
    for x0, y0, x1, y1 in ((cx - 2.0, cy - 2.6, cx - 1.2, cy + 2.6), (cx + 1.2, cy - 2.6, cx + 2.0, cy + 2.6),
                           (cx - 1.2, cy - 0.4, cx + 1.2, cy + 0.4)):
        p.decals.append(dict(pts=np.array([[x0, y0, 46.5], [x1, y0, 46.5], [x1, y1, 46.5], [x0, y1, 46.5]]),
                             colour=MARK_W, kind='paint', face=(prim, 'T')))

    p = part('helideck_truss', 'helideck truss', 'deck2_W', (-24.0, 0.0, 36.0))
    for y in (-7.5, 5.5):
        lo0, lo1 = np.array([-24.0, y, 33.6]), np.array([-44.0, y, 45.2])
        hi0, hi1 = np.array([-24.0, y, 45.2]), np.array([-46.5, y, 45.2])
        p.tube(lo0, lo1, 0.5, GREY, n=6, amt=0.05)
        p.tube(hi0, hi1, 0.45, GREY, n=6, amt=0.05)
        p.tube((-24.6, y, 40.0), (-24.6, y, 45.2), 0.5, GREY, n=6, amt=0.05)
        p.zigzag((lo0, lo1), (hi0, (hi1 + hi0) / 2 + (hi1 - hi0) * 0.38), 8)
    for f in np.linspace(0.1, 0.9, 4):
        p.strokes.append((np.array([-24.0 - 20 * f, -7.5, 33.6 + 11.6 * f]),
                          np.array([-24.0 - 20 * f, 5.5, 33.6 + 11.6 * f]), 'ink'))

    p = part('chute', 'escape chute', 'helideck_truss', (-31.0, -11.0, 44.6))
    p.tube((-31.0, -11.0, 44.6), (-38.0, -20.0, 30.5), 1.3, ORANGE, n=8, r1=1.1, amt=0.06)
    p.tube((-38.0, -20.0, 30.5), (-39.6, -21.8, 29.2), 1.6, RED, n=8, amt=0.04)

    # the walkway bridge stub off the east end (refs rig-legs-walkway-dusk, rig-night-bridge-flare)
    p = part('walkway', 'walkway stub', 'deck1_E', (25.0, -4.0, 26.0))
    a, b = np.array([25.0, -4.0, 26.0]), np.array([45.0, -17.0, 25.4])
    p.beam(a, b, 3.2, 0.7, GREY)
    ax = (b - a) / np.linalg.norm(b - a)
    side = np.cross(ax, [0, 0, 1.0])
    side /= np.linalg.norm(side)
    for s in (-1, 1):
        lo = (a + side * s * 1.6, b + side * s * 1.6)
        hi = (lo[0] + np.array([0, 0, 2.6]), lo[1] + np.array([0, 0, 2.6]))
        p.tube(hi[0], hi[1], 0.25, YELLOW, n=6, amt=0.03)
        p.zigzag(lo, hi, 12)
    return P


PARTS = build()
ORDER = list(PARTS)                                  # the numbers on the parts sheet


# ------------------------------------------------ moving the parts --------------------------------------------------
def _rotm(rot):
    rx, ry, rz = (math.radians(v) for v in rot)
    return W._rot('z', rz) @ W._rot('y', ry) @ W._rot('x', rx)


class State:
    """Where each part is: at rest unless moved. move(name, rot, shift, pivot): degrees about the part's pivot (x, y,
    z in rig axes), then a shift in metres; everything standing on it (PARTS[...].parent) goes with it. whole(rot, pivot, shift): every part together, after its own move (the
    finale's tip and slide). hide(name): a part that has sunk out of reach (never needed for the waterline: anything
    below the sea is cut off by itself)."""
    def __init__(self):
        self.moves = {}
        self.group = None
        self.hidden = set()

    def move(self, name, rot=(0, 0, 0), shift=(0, 0, 0), pivot=None):
        piv = PARTS[name].pivot if pivot is None else np.asarray(pivot, float)
        self.moves[name] = (_rotm(rot), piv, np.asarray(shift, float))
        return self

    def whole(self, rot=(0, 0, 0), pivot=(0, 0, 0), shift=(0, 0, 0)):
        self.group = (_rotm(rot), np.asarray(pivot, float), np.asarray(shift, float))
        return self

    def hide(self, name):
        self.hidden.add(name)
        return self

    def local(self, name, P):
        """A part's points after its own move, then each move of what it stands on (a sagging deck carries the
        modules, crane and lifeboats on it), then the whole-rig move."""
        P = np.asarray(P, float)
        n = name
        while n is not None:
            if n in self.moves:
                R, piv, sh = self.moves[n]
                P = (P - piv) @ R.T + piv + sh
            n = PARTS[n].parent
        if self.group is not None:
            R, piv, sh = self.group
            P = (P - piv) @ R.T + piv + sh
        return P


def _place_m():
    return W._rot('z', math.radians(PLACE['yaw']))


def to_world(P):
    return np.asarray(P, float) @ _place_m().T + np.asarray(PLACE['pos'], float)


def world_of(state, name, P):
    return to_world(state.local(name, P))


def boxes(state=None):
    """{part: its 8 corners in the world (m)}: a box round each part, for the whales' contact tests and the audit."""
    state = state or State()
    out = {}
    for name, p in PARTS.items():
        if name in state.hidden:
            continue
        V = np.concatenate([f['pts'] for f in p.faces])
        lo, hi = V.min(0), V.max(0)
        C = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
        out[name] = world_of(state, name, C)
    return out


# ------------------------------------------------ drawing -----------------------------------------------------------
class Sprite(W.Sprite):
    def __init__(self, img, xy, depth_map, bbox):
        super().__init__(img, xy, None, bbox, float(np.median(depth_map[np.isfinite(depth_map)])) if
                         np.isfinite(depth_map).any() else 1e9, None)
        self.depth_map = depth_map


def _newell(P):
    n = np.zeros(3)
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        n += np.array([(a[1] - b[1]) * (a[2] + b[2]), (a[2] - b[2]) * (a[0] + b[0]), (a[0] - b[0]) * (a[1] + b[1])])
    return n


def _waterclip(P):
    """Keep the part of a polygon above the sea (world z >= 0)."""
    keep, _ = W._clip([np.asarray(p, float) for p in P], [p[2] - SEA_LEVEL for p in P])
    return np.array(keep) if len(keep) >= 3 else None


def _split(P, maxlen=5.0):
    """A big quad cut into tiles of at most maxlen m, so near and far parts of one face sort properly."""
    if len(P) != 4:
        return [P]
    nu = max(1, int(math.ceil(np.linalg.norm(P[1] - P[0]) / maxlen)))
    nv = max(1, int(math.ceil(np.linalg.norm(P[3] - P[0]) / maxlen)))
    if nu == 1 and nv == 1:
        return [P]
    out = []
    for i in range(nu):
        for j in range(nv):
            def at(u, v):
                return (P[0] * (1 - u) * (1 - v) + P[1] * u * (1 - v) + P[2] * u * v + P[3] * (1 - u) * v)
            u0, u1, v0, v1 = i / nu, (i + 1) / nu, j / nv, (j + 1) / nv
            out.append(np.array([at(u0, v0), at(u1, v0), at(u1, v1), at(u0, v1)]))
    return out


def _flame_pts(t, size=1.0):
    """The flare's flame in its own plane (u across, v up, metres): a lumpy teardrop leaning with the wind, its lumps
    rolling up it (never a star: smooth lumps). Returns (outer, inner) point lists."""
    out = []
    for H, Wd, ph in ((10.0 * size, 3.4 * size, 0.0), (5.6 * size, 1.7 * size, 1.7)):
        pts = []
        n = 40
        for k in range(n):
            a = 2 * math.pi * k / n
            v = (1 - math.cos(a)) / 2                 # 0 at the base, 1 at the tip, round both sides
            side = 1 if a < math.pi else -1
            w = Wd * math.sin(math.pi * v ** 0.62) * (1 - 0.15 * v)
            lump = 1 + 0.16 * math.sin(9 * v - 7.5 * t + ph + side) + 0.08 * math.sin(17 * v - 13 * t + 2 * side)
            u = side * w * lump + 0.42 * H * v ** 2.2 + 0.35 * math.sin(3.1 * t + ph) * v ** 1.5
            pts.append((u, H * v * (1 + 0.06 * math.sin(5.3 * t + ph))))
        out.append(pts)
    return out


def _font(n, bold=True):
    try:
        return ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), n)
    except OSError:
        return ImageFont.load_default()


def _perspective_coeffs(dst, src):
    """PIL PERSPECTIVE coefficients mapping output points dst back to input points src."""
    A, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        b += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(b, float))


def draw(cam, state=None, t=0.0, light=None, ol=None, ss=2, tint=None, flame=True, only=None):
    """Draw the rig through cam. state: a State (None = at rest). t seconds (the flame). only: a set of part names
    to draw alone (the line check, the parts sheet). Returns a Sprite with .depth_map (metres; inf where empty)."""
    state = state or State()
    L = np.asarray(light if light is not None else LIGHT, float)
    L = L / np.linalg.norm(L)
    Wf, Hf = cam.size
    ol = ol if ol is not None else max(2.0, 5.0 * Wf / 1080)
    campos = cam.pos
    polys = []                                       # (depth, screen pts, colour, id)
    decals = []                                      # (depth, screen pts, colour, kind, width or None)
    texts = []
    ids = {}

    def nid(key):
        return ids.setdefault(key, len(ids) + 2)
    for name, p in PARTS.items():
        if name in state.hidden or (only is not None and name not in only):
            continue
        for f in p.faces:
            Pw = world_of(state, name, f['pts'])
            cw = world_of(state, name, f['centre'][None])[0]
            n = _newell(Pw)
            if np.linalg.norm(n) < 1e-9:
                continue
            if np.dot(n, Pw.mean(0) - cw) < 0:
                n = -n                               # outwards
            if np.dot(n, Pw.mean(0) - campos) >= 0:
                continue                             # faces away from us
            lit = np.dot(n / np.linalg.norm(n), L) > 0.08
            col = f['mat'][0 if lit else 1]
            key = (name, f['prim'], f['key']) if f['fold'] else (name, f['prim'], id(f['mat']))
            i = nid(key)
            for tile in _split(Pw, 3.0):
                Q = _waterclip(tile)
                if Q is None:
                    continue
                S2, d = cam.screen(Q)
                if (d < 0.5).any():
                    continue
                polys.append((float(np.linalg.norm(Q.mean(0) - campos)), S2, col, i))
        for dc in p.decals:
            Pw = world_of(state, name, dc['pts'])
            Q = _waterclip(Pw)
            if Q is None:
                continue
            S2, d = cam.screen(Q)
            if (d < 0.5).any():
                continue
            fid = 0
            if dc.get('face') is not None:
                fid = ids.get((name,) + tuple(dc['face']))
                if fid is None:
                    continue                         # its face is turned away
            decals.append((float(np.linalg.norm(Q.mean(0) - campos)), S2, dc['colour'], dc['kind'], None, fid))
        for a, b, kind in p.strokes:
            A, B = world_of(state, name, np.array([a, b]))
            n_seg = max(1, int(math.ceil(np.linalg.norm(B - A) / 3.0)))
            for k in range(n_seg):
                s0, s1 = A + (B - A) * k / n_seg, A + (B - A) * (k + 1) / n_seg
                if s0[2] < SEA_LEVEL and s1[2] < SEA_LEVEL:
                    continue
                if s0[2] < SEA_LEVEL or s1[2] < SEA_LEVEL:
                    lo, hi = (s0, s1) if s0[2] < s1[2] else (s1, s0)
                    lo = lo + (hi - lo) * ((SEA_LEVEL - lo[2]) / (hi[2] - lo[2]))
                    s0, s1 = lo, hi
                S2, d = cam.screen(np.array([s0, s1]))
                if (d < 0.5).any():
                    continue
                wpx = ol if kind == 'ink' else max(1.5, ol * 0.45)
                decals.append((float(np.linalg.norm((s0 + s1) / 2 - campos)), S2,
                               INK if kind == 'ink' else RAIL, kind, wpx, 0))
        for tx in p.texts:
            Pw = world_of(state, name, tx['pts'])
            if (Pw[:, 2] < SEA_LEVEL).any():
                continue
            n = _newell(Pw)
            if np.dot(n, Pw.mean(0) - campos) >= 0 and np.dot(-n, Pw.mean(0) - campos) >= 0:
                continue
            S2, d = cam.screen(Pw)
            if (d < 0.5).any():
                continue
            texts.append((S2, tx['text'], {v for k_, v in ids.items() if k_[0] == name}, n))
        if flame and p.flame is not None and (only is None or name in only):
            tip = world_of(state, name, p.flame[None])[0]
            if tip[2] > SEA_LEVEL:
                right = np.array([1.0, 0, 0])
                upw = np.array([0, 0, 1.0])
                dist = float(np.linalg.norm(tip - campos))
                for k, (pts, col) in enumerate(zip(_flame_pts(t), ((246, 140, 40), (255, 222, 90)))):
                    Pw = np.array([tip + right * u + upw * v for u, v in pts])
                    S2, d = cam.screen(Pw)
                    polys.append((dist - 0.5 - k * 0.2, S2, col, nid(('flame', k))))
    if not polys:
        return None
    allp = np.concatenate([p[1] for p in polys] + [d[1] for d in decals])
    x0, y0 = np.floor(allp.min(0)) - 4 * ol - 4
    x1, y1 = np.ceil(allp.max(0)) + 4 * ol + 4
    x0, y0 = max(x0, -Wf), max(y0, -Hf)
    x1, y1 = min(x1, 2 * Wf), min(y1, 2 * Hf)
    bw, bh = int(x1 - x0), int(y1 - y0)
    if bw < 2 or bh < 2:
        return None
    S = ss
    col = Image.new('RGB', (bw * S, bh * S), (0, 0, 0))
    idi = Image.new('I', (bw * S, bh * S), 0)
    dep = Image.new('I', (bw * S, bh * S), 0)
    dc_, di, dd = ImageDraw.Draw(col), ImageDraw.Draw(idi), ImageDraw.Draw(dep)

    def scr(P):
        return [((x - x0) * S, (y - y0) * S) for x, y in P]
    for depth, P, c, i in sorted(polys, key=lambda q: -q[0]):
        Q = scr(P)
        dc_.polygon(Q, fill=c, outline=c)
        di.polygon(Q, fill=i, outline=i)
        dd.polygon(Q, fill=int(depth * 100), outline=int(depth * 100))
    I = np.asarray(idi).astype(np.int64)
    D = np.asarray(dep).astype(np.int64)
    alpha = I > 0
    # the ink: the outside, every change of part, box face or colour, and every place one thing passes in front of
    # another (a jump in depth), all at one weight
    edge = np.zeros_like(alpha)
    for dy, dx in ((0, 1), (1, 0)):
        a1, a2 = I[:I.shape[0] - dy, :I.shape[1] - dx], I[dy:, dx:]
        e = a1 != a2
        edge[:I.shape[0] - dy, :I.shape[1] - dx] |= e
    k = max(3, int(round(ol * S)) | 1)
    ink = ND.maximum_filter(edge, size=k)
    Dm = np.where(alpha, D / 100.0, np.inf)
    Dmin = ND.minimum_filter(Dm, size=k)
    Dm = np.where(ink, Dmin, Dm)
    out = np.asarray(col).copy()
    out[ink] = INK
    full = alpha | ink
    glow = np.zeros_like(full)
    # the board's lettering, laid on its face where the face is seen
    for S2, text, tids, n in texts:
        fnt = _font(200)
        tw, th = fnt.getbbox(text)[2:]
        timg = Image.new('L', (tw + 20, 220), 0)
        ImageDraw.Draw(timg).text((10, 0), text, font=fnt, fill=255)
        timg = timg.crop(timg.getbbox())
        dst = scr(S2)
        src = [(0, 0), (timg.width, 0), (timg.width, timg.height), (0, timg.height)]
        co = _perspective_coeffs(dst, src)
        warped = np.asarray(timg.transform((bw * S, bh * S), Image.PERSPECTIVE, tuple(co), Image.BILINEAR)) > 110
        m = warped & np.isin(I, list(tids)) & ~ink
        out[m] = INK
    # flat paint on faces (windows, deck lights, helideck marks) and the 3D lines (lattice lacing, railings): each
    # shown only where nothing nearer stands in front of it
    if decals:
        dcol = Image.new('RGB', (bw * S, bh * S), (0, 0, 0))
        dmask = Image.new('L', (bw * S, bh * S), 0)
        ddep = Image.new('I', (bw * S, bh * S), 0)
        dglow = Image.new('L', (bw * S, bh * S), 0)
        dfid = Image.new('I', (bw * S, bh * S), 0)
        dtol = Image.new('L', (bw * S, bh * S), 0)
        a_, b_, c_, g_, f_, t_ = (ImageDraw.Draw(x) for x in (dcol, dmask, ddep, dglow, dfid, dtol))
        for depth, P, c, kind, wpx, fid in sorted(decals, key=lambda q: -q[0]):
            Q = scr(P)
            dval = int(depth * 100)
            tol = {'rail': 60, 'ink': 30}.get(kind, 30)      # cm a 3D line may sit behind a face tile's middle
            if wpx is None:
                for dr, v in ((a_, c), (b_, 255), (c_, dval), (g_, 255 if kind == 'glow' else 0), (f_, fid), (t_, tol)):
                    dr.polygon(Q, fill=v)
            else:
                w = max(1, int(round(wpx * S)))
                for dr, v in ((a_, c), (b_, 255), (c_, dval), (g_, 0), (f_, 0), (t_, tol)):
                    dr.line(Q, fill=v, width=w)
        dm = np.asarray(dmask) > 0
        dz = np.asarray(ddep) / 100.0
        fidm = np.asarray(dfid)
        on_face = (fidm > 0) & (I == fidm) & ~ink                 # paint: only on its own face, where it is seen
        free = (fidm == 0) & (dz <= Dm + np.asarray(dtol) / 100.0)   # 3D lines: where nothing nearer stands
        show = dm & (on_face | free)
        out[show] = np.asarray(dcol)[show]
        out[ink] = INK                               # outlines stay whole over railings and lacing
        glow |= show & (np.asarray(dglow) > 0)
        Dm = np.where(show, np.minimum(Dm, dz), Dm)
        full |= show
    if tint is not None:
        tr, tg, tb, tk = tint
        m = full & ~glow & ~np.all(out == INK, axis=-1)
        out[m] = (out[m] * (1 - tk) + np.array([tr, tg, tb]) * tk).astype(np.uint8)
    rgba = np.dstack([out, (full * 255).astype(np.uint8)])
    img = Image.fromarray(rgba, 'RGBA')
    if S != 1:
        img = img.resize((bw, bh), Image.LANCZOS)
        Dm = Dm[:bh * S, :bw * S].reshape(bh, S, bw, S).min(axis=(1, 3))
    bb = img.getbbox()
    bbox = (bb[0] + x0, bb[1] + y0, bb[2] + x0, bb[3] + y0) if bb else None
    return Sprite(img, (x0, y0), Dm.astype(np.float32), bbox)


def composite(frame, sprites):
    """Lay sprites over frame (RGBA) by depth, pixel by pixel: whatever is nearer the lens wins (a whale between the
    legs is hidden by the near legs and hides the far ones). A sprite with no depth_map uses its .depth."""
    Wf, Hf = frame.size
    base = np.asarray(frame.convert('RGBA')).astype(np.float32)
    zbuf = np.full((Hf, Wf), np.inf, np.float32)
    for spr in sprites:
        if spr is None:
            continue
        a = np.asarray(spr.img).astype(np.float32)
        h, w = a.shape[:2]
        x0, y0 = int(round(spr.xy[0])), int(round(spr.xy[1]))
        fx0, fy0, fx1, fy1 = max(0, x0), max(0, y0), min(Wf, x0 + w), min(Hf, y0 + h)
        if fx1 <= fx0 or fy1 <= fy0:
            continue
        sub = a[fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0]
        dm = getattr(spr, 'depth_map', None)
        if dm is None:
            dz = np.full(sub.shape[:2], spr.depth, np.float32)
        else:
            dz = dm[fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0]
        zb = zbuf[fy0:fy1, fx0:fx1]
        al = sub[..., 3:4] / 255.0
        win = (dz < zb)[..., None]
        al = al * win
        reg = base[fy0:fy1, fx0:fx1]
        reg[..., :3] = reg[..., :3] * (1 - al) + sub[..., :3] * al
        reg[..., 3:4] = np.maximum(reg[..., 3:4], al * 255)
        zbuf[fy0:fy1, fx0:fx1] = np.where((sub[..., 3] > 128) & (dz < zb), dz, zb)
    return Image.fromarray(base.astype(np.uint8), 'RGBA')


# ------------------------------------------------ the placeholder backdrop and sheets -------------------------------
SKY, SEA = (186, 150, 186), (92, 84, 128)


def backdrop(cam):
    """A PLACEHOLDER flat sky and sea (the dusk painting is the next stage), so the waterline reads."""
    Wf, Hf = cam.size
    im = Image.new('RGBA', (Wf, Hf), SKY + (255,))
    ImageDraw.Draw(im).rectangle([0, int(cam.horizon), Wf, Hf], fill=SEA + (255,))
    return im


def picture(t=0.0, state=None, small=False, whales=()):
    cam = film_cam(small)
    frame = backdrop(cam)
    sprs = [draw(cam, state, t)]
    for pose, pat, kw in whales:
        sprs.append(W.draw(cam, pose, pattern=pat, t=t, **kw))
    return composite(frame, sprs)


SCALE_WHALE = (W.Pose((-24.0, -36.0, 16.0), yaw=-62, pitch=6, roll=-8), 0, dict(flap=1.0, beat=0.6))
THROUGH_WHALE = (W.Pose(tuple(to_world((-1.0, 0.0, 6.6))), yaw=-78, pitch=4, roll=-5), 1, dict(flap=1.0, beat=0.8))


def _knocked():
    """A test of the parts moving (NOT the film's action): the west bracing knocked away and sinking, the west
    decks sagging and carrying what stands on them, the crane whipping over, a lifeboat dropping, the helideck hanging
    off, a brace sinking under the waterline."""
    st = State()
    st.move('brace_W_high', rot=(0, -50, 30), shift=(-14, -5, -12))
    st.move('brace_W_low', rot=(10, -70, 0), shift=(-12, 0, -9))
    st.move('deck1_W', rot=(0, 9, 0), shift=(0, 0, -2.5))
    st.move('deck2_W', rot=(0, 3, 0), shift=(0, 0, -0.6))
    st.move('helideck_truss', rot=(0, 16, 0), shift=(0, 0, -2))
    st.move('helideck', rot=(12, 20, 0), shift=(1, -2, -4))
    st.move('chute', rot=(0, 10, 10), shift=(1, -1, -3))
    st.move('lifeboat_1', rot=(20, 0, 0), shift=(-1, -6, -16))
    st.move('crane_boom', rot=(25, 25, 40), shift=(-2, 0, -4))
    st.move('cargo', rot=(25, 8, 0), shift=(-3, -4, -3))
    return st


def sheet(out):
    BG = (250, 248, 242)
    tw, th = 810, 1440
    cam = film_cam()
    tiles = []
    # 1. the film's frame at rest, with a whale at real size by the near corner, same camera
    im1 = picture(0.4, whales=[SCALE_WHALE]).convert('RGB')
    tiles.append(('1  the rig at rest, the film camera; a 14 m whale (Inky) by the near corner, same camera', im1))
    # 2. the 31 parts, numbered
    im2 = picture(0.4).convert('RGB')
    d = ImageDraw.Draw(im2)
    st = State()
    fnt = _font(26)
    for k, name in enumerate(ORDER):
        V = np.concatenate([f['pts'] for f in PARTS[name].faces])
        c = (V.min(0) + V.max(0)) / 2
        c[2] = max(c[2], 1.0)
        (sx, sy), _ = cam.screen(to_world(c))
        txt = str(k + 1)
        bx = fnt.getbbox(txt)
        r = 18
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255), outline=INK, width=3)
        d.text((sx - (bx[2] - bx[0]) / 2 - bx[0], sy - (bx[3] - bx[1]) / 2 - bx[1]), txt, fill=INK, font=fnt)
    tiles.append(('2  the 31 breakable parts (numbers in the list)', im2))
    # 3. parts moving on their own (a test, not the film's action)
    im3 = picture(0.9, state=_knocked(), whales=[THROUGH_WHALE]).convert('RGB')
    wb = W.draw(cam, THROUGH_WHALE[0], pattern=THROUGH_WHALE[1], t=0.9, **THROUGH_WHALE[2]).bbox
    cx_, cy_ = (wb[0] + wb[2]) / 2, (wb[1] + wb[3]) / 2
    det = im3.crop((int(cx_ - 150), int(cy_ - 95), int(cx_ + 150), int(cy_ + 95))).resize((900, 570), Image.LANCZOS)
    d3 = ImageDraw.Draw(im3)
    d3.rectangle([int(cx_ - 150), int(cy_ - 95), int(cx_ + 150), int(cy_ + 95)], outline=(255, 255, 255), width=4)
    im3.paste(det, (90, 120))
    d3.rectangle([90, 120, 990, 690], outline=(255, 255, 255), width=6)
    d3.text((104, 130), 'detail x3: the whale behind the near legs, in front of the far ones', fill=(255, 255, 255),
            font=_font(28))
    tiles.append(('3  test: parts knocked about (not the film\'s action); a whale (Blaze) between the legs: near legs '
                  'in front of it, far legs behind', im3))
    head = 120
    lw = 980
    S_ = Image.new('RGB', (tw * 3 + lw + 40, th + head + 80), BG)
    d = ImageDraw.Draw(S_)
    d.text((20, 20), 'FLYING WHALES: the Jackdaw rig (31 parts, real size, film camera)', fill=INK, font=_font(40))
    d.text((20, 72), 'sky and sea are PLACEHOLDERS (the dusk painting is the next stage); the flare flame moves',
           fill=(90, 90, 90), font=_font(24))
    for i, (lab, im) in enumerate(tiles):
        im = im.resize((tw, th), Image.LANCZOS)
        x = 10 + i * (tw + 10)
        S_.paste(im, (x, head + 40))
        words, line, yy = lab.split(' '), '', head + 4
        d.text((x, yy), lab[:62], fill=INK, font=_font(20))
        if len(lab) > 62:
            d.text((x, yy + 20), lab[62:], fill=INK, font=_font(20))
    x = 3 * (tw + 10) + 20
    d.text((x, head + 40), 'parts', fill=INK, font=_font(28))
    for k, name in enumerate(ORDER):
        p = PARTS[name]
        d.text((x, head + 84 + k * 36), f'{k + 1:2d}  {p.label}', fill=INK, font=_font(24))
    yy = head + 84 + len(ORDER) * 36 + 30
    for line in ('real sizes: deck block 50 x 35 m, decks to 48 m,', 'jacket 25 m to the deck, crane boom 35 m,',
                 'flare boom 45 m, helideck 20 m, lifeboats 8.5 m', '',
                 'my additions (say no if unwanted): the blue', 'and red containers; window rows and deck', 'lights; railings'):
        d.text((x, yy), line, fill=(90, 90, 90), font=_font(22))
        yy += 30
    S_.save(out, quality=88)
    return out


def check():
    import linecheck
    cam = film_cam()
    spr = draw(cam, State(), 0.4)
    lay = Image.new('RGBA', cam.size, (0, 0, 0, 0))
    spr.paste(lay)
    found, mask = linecheck.analyse(lay)
    for kd, x, y, det in found[:20]:
        print(f'{kd} at ({x}, {y}): {det}')
    print(f'{len(found)} line-work fault(s)' if found else 'rig line work: every shape outlined, one weight')
    return found, lay, mask


# ------------------------------------------------ rule 3: the benchmark ---------------------------------------------
BENCHMARK = [dict(place='the Jackdaw rig', at=0.4,
                  refs=['rig-jackdaw-close.jpg', 'rig-jackdaw-helipad.jpg', 'rig-jackdaw-wide.jpg'],
                  items=[('yellow jacket legs with X bracing, wider at the sea', 'done: 4 battered legs, 8 X panels'),
                         ('boxy decks on yellow deck girders, three storeys', 'done: cellar, process, top modules'),
                         ('railings round every deck edge', 'done: rails on each ledge and roof'),
                         ('helideck out to one side on a lattice truss', 'done: west end, grey truss'),
                         ('orange escape chute under the helideck', 'done: orange chute, red foot'),
                         ('yellow crane tower, red and white boom', 'done: yellow pedestal and cab, lattice boom'),
                         ('yellow JACKDAW board, black capitals', 'done: JACKDAW (Sam: the real name)'),
                         ('flare boom with flame; chimneys; warm lights at dusk', 'done: lattice boom, flame, 3 stacks'),
                         ('grey, white, red, orange, blue accents', 'done: containers, lifeboats, stacks'),
                         ('derrick and walkway stub (other refs)', 'done: lattice derrick, bridge stub')])]


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'sheet'
    if cmd == 'sheet':
        print(sheet(sys.argv[2]))
    elif cmd == 'still':
        picture(0.4, small='--small' in sys.argv).convert('RGB').save(sys.argv[2])
        print(sys.argv[2])
    elif cmd == 'check':
        check()


if __name__ == '__main__':
    main()
