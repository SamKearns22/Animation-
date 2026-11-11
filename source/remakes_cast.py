#!/usr/bin/env python3
"""Remakes (the Ocarina of Time remake satire, Sam 10 Nov): the children and the gunman, in the house style, from
Sam's references (references/remakes/03-18). Drawn fresh in our flat look with the remake's designs (Decision 10),
never traced. The creatures (Kaepora Gaebora, Navi, the Goron) are in remakes_creatures.py.

MAP (rule 61)
  colours .............. top of file
  kid head (front) ..... _kid_outline, _eye, _brows, _kid_mouth, kid_head; hair and headgear per child: _hair_*
  Link's turned heads .. link_head_side, link_head_back
  kid torsos (front) ... _tunic_link, _dress_zelda, _dress_malon, _tunic_saria, _body_ruto; kid_torso
  kid side/back ........ kid_torso_view (Link: tunic fringe, belt, strap, sheath, shield)
  sleeves .............. _arm (short or puffed sleeves over a bare arm; Ruto's forearm fins)
  legs ................. _leg (boots with folded cuffs, Ruto's bare feet)
  props ................ milk_bottle, ocarina, rifle; the Kokiri Sword: kokiri_hilt, kokiri_sheath, link_hilt
  gunman ............... GUNMAN (the Patriot's balaclava, a helmet, a plate vest), vest, helmet
  the people ........... LINK, ZELDA, MALON, SARIA, RUTO, GUNMAN; MOODS; person(); poses()
  sheets ............... alone(WHO, OUT) one character beside its references; faces(OUT)

    python3 source/remakes_cast.py alone WHO OUT.jpg     one character, every view it needs, beside its references
    python3 source/remakes_cast.py faces WHO OUT.jpg     its faces large
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import burnham as B              # noqa: E402
import patriots3_cast as P3      # noqa: E402  (the balaclava; its hooks pass everyone else straight through)
import views as V                # noqa: E402
import mouths                    # noqa: E402
import moves                     # noqa: E402
import figure as F               # noqa: E402
from traitors_cast import clip_convex   # noqa: E402
from ed import INK, curve, open_curve, oval   # noqa: E402

REF = os.path.join(ROOT, 'references', 'remakes')
WHITE = V.WHITE                  # eye whites (the look check finds them by this colour)
SHINE = (255, 255, 255)
BLUSH = (244, 196, 184)                 # a faint warmth, not cartoon circles (Sam: not chibi)

# ------------------------------------------------------------------------------------------------ colours
KID_SKIN = (250, 216, 192)
L_HAIR, L_HAIR_D = (240, 198, 96), (196, 146, 54)
L_CAP, L_CAP_D = (92, 136, 54), (62, 98, 38)
L_TUNIC, L_TUNIC_D = (74, 112, 46), (52, 82, 32)
L_SHIRT = (124, 160, 74)
LEATHER, LEATHER_D = (124, 78, 44), (88, 54, 30)
BEAD = (178, 52, 40)
SILVER = (196, 200, 206)
BOOT, BOOT_CUFF = (112, 72, 42), (196, 160, 110)
WOOD, WOOD_D = (160, 108, 60), (116, 74, 40)
BLUE_EYE, GREEN_EYE, PURPLE_EYE = (66, 128, 214), (64, 168, 112), (140, 84, 190)

Z_HAIR = (244, 210, 120)
Z_VEIL, Z_VEIL_D = (246, 244, 236), (208, 204, 196)
Z_PURPLE, Z_PURPLE_D = (128, 70, 150), (92, 46, 110)
Z_SLEEVE = (178, 206, 232)
GOLD, GOLD_D = (226, 182, 70), (170, 126, 40)
Z_SKIRT = (246, 244, 238)

M_HAIR, M_HAIR_D = (222, 98, 52), (176, 66, 34)
M_SCARF = (240, 200, 70)
M_BLOUSE = (150, 136, 120)
M_SLEEVE = (110, 150, 206)
M_APRON, M_APRON_D = (132, 92, 62), (96, 64, 42)
M_SKIRT = (128, 84, 160)
M_HEM = (80, 120, 196)

S_HAIR, S_HAIR_D = (164, 214, 70), (118, 168, 44)
S_TOP = (58, 96, 52)
S_TUNIC, S_TUNIC_D = (102, 150, 74), (74, 116, 52)
S_SHORTS = (64, 104, 54)

R_SKIN, R_SKIN_D = (226, 232, 236), (178, 190, 200)
R_FIN, R_FIN_D = (98, 200, 190), (54, 150, 146)
R_TOE = (236, 168, 176)

U = 1.0 / V.M_PER_UNIT


def dk(c, k=0.7):
    return B.dk(c, k)


# ================================================================================================ the kid head (front)
def _kid_outline(hx, hy, hw, hh, chin=1.0):
    """A child's head: a big round cranium, full cheeks, a small soft chin (the remake's toddler-ish faces)."""
    return curve([(hx - hw, hy - 4), (hx - hw * 0.93, hy - hh * 0.62), (hx - hw * 0.62, hy - hh * 0.96),
                  (hx, hy - hh * 1.06), (hx + hw * 0.62, hy - hh * 0.96), (hx + hw * 0.93, hy - hh * 0.62),
                  (hx + hw, hy - 4), (hx + hw * 0.97, hy + hh * 0.34), (hx + hw * 0.8, hy + hh * 0.7),
                  (hx + hw * 0.44, hy + hh * 0.95 * chin), (hx, hy + hh * 1.02 * chin), (hx - hw * 0.44, hy + hh * 0.95 * chin),
                  (hx - hw * 0.8, hy + hh * 0.7), (hx - hw * 0.97, hy + hh * 0.34)], 5)


def _eye(p, ex, ey, sgn, w, h, iris, lid=0.0, low=0.0, look=0.0, gaze_dy=0.0, pupil=1.0, closed=None, lashes=False):
    """A big round child's eye: the white, the coloured iris kept inside it, the pupil, two shines, a heavy upper lid.
    lid 0-1 lowers the upper lid (sceptical, deadpan), low lifts the lower lid (a squint), pupil < 1 shrinks it (shock).
    closed: 'smile' (an arch: happy, a wink) or 'shut' (a squeezed line)."""
    us = np.linspace(-1, 1, 17)
    if closed:
        if closed == 'smile':
            pts = [(ex + w * u, ey - h * 0.35 * (1 - u * u)) for u in us]
        else:
            pts = [(ex + w * u, ey + h * 0.05 * (1 - u * u) + sgn * u * 3) for u in us]
        p.line(pts, INK, 3.4)
        if lashes:
            p.line([pts[-1 if sgn > 0 else 0], (ex + sgn * (w + 10), ey - h * 0.2)], INK, 2.6)
        return
    top = [(ex + w * u, ey - h * (1 - u * u) ** 0.7 * (1 - lid) * 0.98 - h * 0.1 * sgn * u) for u in us]
    bot = [(ex + w * u, ey + h * (1 - u * u) ** 0.5 * 0.92 * (1 - low)) for u in us]
    opening = top + bot[::-1][1:-1]
    p.poly(opening, WHITE, None)
    cx, cy = ex + look * w * 0.42, ey + 4 + gaze_dy * h * 0.4
    circ = lambda r, ox=0.0, oy=0.0: [(cx + ox + r * math.cos(a), cy + oy + r * math.sin(a) * 1.08)
                                      for a in np.linspace(0, 2 * math.pi, 28, endpoint=False)]
    ri = w * 0.74 * (0.9 + 0.1 * pupil)
    ring = clip_convex(opening[::-1], circ(ri))
    if len(ring) >= 3:
        p.poly(ring, iris, None)
        dark = clip_convex(opening[::-1], circ(ri, 0, -ri * 0.36))
        inner = clip_convex(dark, circ(ri)) if len(dark) >= 3 else []
        if len(inner) >= 3:
            p.poly(inner, dk(iris, 0.72), None)                   # the iris darker under the lid (depth)
    pu = clip_convex(opening[::-1], circ(ri * 0.46 * pupil))
    if len(pu) >= 3:
        p.poly(pu, INK, None)
    if pupil > 0.6:                                               # two shines: the life in a cartoon child's eye
        p.ell(cx - ri * 0.34, cy - ri * 0.36, ri * 0.19, ri * 0.19, SHINE, None)   # one shine: less doll-like
    p.line(bot[3:-3], dk(KID_SKIN, 0.6), 1.6)
    p.line(top, INK, 4.2)                                         # the heavy upper lid line
    if lashes:                                                    # girls: two lashes flicked out at the outer corner
        o = top[-1] if sgn > 0 else top[0]
        for k, (dx, dy) in enumerate(((10, -8), (12, 2))):
            p.line([(o[0] - sgn * 4, o[1] + k * 3), (o[0] + sgn * dx, o[1] + dy)], INK, 2.6)


def _brows(p, fx, ey, gap, h, c, inner, outer, w=3.6, length=30, one=None, each=None):
    """Two short arched brows. inner/outer: how far each end rises (+) or drops (-) in units; one = (side, rise)
    lifts a single brow (sceptical)."""
    for sgn in (-1, 1):
        x0, x1 = fx + sgn * (gap - length * 0.45), fx + sgn * (gap + length * 0.55)
        if each:                                                      # each brow its own (inner, outer) rise
            inner, outer = each[sgn]
        y0, y1 = ey - h - 18 - inner, ey - h - 14 - outer
        if one and one[0] == sgn:
            y0, y1 = y0 - one[1], y1 - one[1] * 1.2
        mid = ((x0 + x1) / 2, min(y0, y1) - 6)
        pts = open_curve([(x0, y0), mid, (x1, y1)], 6)
        p.line(pts, INK, w * 1.6 + 2.6)
        p.line(pts, c, w * 1.6)


class _Grown:
    """A pen that draws k times bigger about (cx, cy): the mouths grow with the head (line widths kept)."""
    def __init__(self, p, cx, cy, k):
        self.p, self.cx, self.cy, self.k = p, cx, cy, k

    def _q(self, pts):
        return [(self.cx + (x - self.cx) * self.k, self.cy + (y - self.cy) * self.k) for x, y in pts]

    def poly(self, pts, *a, **kw):
        return self.p.poly(self._q(pts), *a, **kw)

    def line(self, pts, *a, **kw):
        return self.p.line(self._q(pts), *a, **kw)

    def ell(self, cx, cy, rx, ry, *a, **kw):
        (x, y), = self._q([(cx, cy)])
        return self.p.ell(x, y, rx * self.k, ry * self.k, *a, **kw)


MOUTH_K = {'smug': 1.35, 'unsure': 1.5, 'horror': 1.6, 'deadpan': 1.45, 'sceptical': 1.35}   # Link 5: these must read on a phone


def _kid_mouth(p, sp, fx, my, mood, lip=(176, 84, 84)):
    """The child mouths each mood needs; talking uses the series' shared shapes (mouths.py)."""
    m = sp.get('mouth', 'rest')
    if not (isinstance(m, str) and m.startswith('v:') and m != 'v:rest'):
        p = _Grown(p, fx, my, sp['hw'] / 118.0 * MOUTH_K.get(mood, 1.0))
    if isinstance(m, str) and m.startswith('v:') and m != 'v:rest':
        mouths.draw(p, dict(sp, lips=False), fx, my, m[2:])
        return
    inside, teeth, tongue = (96, 34, 40), (250, 248, 244), (214, 104, 110)
    if mood in ('smile', 'hopeful', 'smug', 'wink', 'unsure'):
        wv = {'smile': 22, 'hopeful': 26, 'smug': 20, 'wink': 22, 'unsure': 16}[mood]
        tilt = {'smug': 8, 'wink': 6, 'unsure': -5}.get(mood, 0)
        if mood == 'hopeful':                                         # an open, eager smile
            shape = curve([(fx - wv, my - 4), (fx, my - 2), (fx + wv, my - 4), (fx + wv * 0.6, my + 14), (fx, my + 18),
                           (fx - wv * 0.6, my + 14)], 4)
            p.poly(shape, inside, INK, 2.6)
            p.poly(curve([(fx - wv * 0.7, my - 2), (fx + wv * 0.7, my - 2), (fx + wv * 0.5, my + 4), (fx - wv * 0.5, my + 4)], 3),
                   teeth, None)
            p.ell(fx, my + 12, wv * 0.4, 5, tongue, None)
            p.poly(shape, None, INK, 2.6)
            return
        if mood == 'unsure':                                          # a wobbly, lopsided "er..."
            p.line(open_curve([(fx - wv, my + 4), (fx - wv * 0.5, my - 2), (fx, my + 4), (fx + wv * 0.5, my + 1),
                               (fx + wv, my - 6)], 6), INK, 3.6)
            return
        p.line(open_curve([(fx - wv, my - 2 + tilt * 0.2), (fx - wv * 0.4, my + 6), (fx + wv * 0.4, my + 5 - tilt * 0.6),
                           (fx + wv, my - 4 - tilt)], 6), INK, 3.4)
        return
    if mood in ('aghast', 'terrified'):
        wv, hv = (30, 34) if mood == 'aghast' else (26, 22)
        if mood == 'terrified':                                       # a wobbling, open-mouthed lip
            shape = curve([(fx - wv, my + 4), (fx - wv * 0.5, my - 6), (fx, my - 2), (fx + wv * 0.5, my - 6), (fx + wv, my + 4),
                           (fx + wv * 0.6, my + hv), (fx, my + hv - 4), (fx - wv * 0.6, my + hv)], 4)
        else:
            shape = oval(fx, my + 10, wv * 0.62, hv * 0.7, 30)
        p.poly(shape, inside, INK, 2.8)
        p.ell(fx, my + 10 + hv * 0.35, wv * 0.3, hv * 0.16, tongue, None)
        p.poly(shape, None, INK, 2.8)
        return
    if mood == 'wince':                                               # gritted teeth
        shape = curve([(fx - 28, my), (fx, my - 6), (fx + 28, my), (fx + 22, my + 14), (fx, my + 16), (fx - 22, my + 14)], 3)
        p.poly(shape, teeth, INK, 2.6)
        p.line([(fx - 26, my + 6), (fx + 26, my + 6)], dk(teeth, 0.7), 1.6)
        for k in (-14, -4, 6, 16):
            p.line([(fx + k, my - 3), (fx + k, my + 13)], dk(teeth, 0.7), 1.4)
        return
    if mood == 'horror':                                              # flat horror: a small, slack open mouth
        shape = curve([(fx - 18, my + 10), (fx - 8, my), (fx + 8, my), (fx + 18, my + 10), (fx + 12, my + 18),
                       (fx - 12, my + 18)], 3)                         # corners dragged down, slack and open
        p.poly(shape, inside, INK, 2.6)
        p.ell(fx, my + 3, 9, 2.5, (250, 248, 244), None)               # a glimpse of top teeth
        p.poly(shape, None, INK, 2.6)
        return
    if mood == 'sceptical':                                           # note 31 (Sam: "uuuuuh, okay?"): a small
        p.line(open_curve([(fx - 20, my + 5), (fx - 8, my + 1), (fx + 4, my + 5), (fx + 14, my + 1), (fx + 24, my - 7)], 5),
               INK, 3.6)                                              # wavering line hitched up at one corner: an
        p.line(open_curve([(fx + 22, my - 13), (fx + 28, my - 7), (fx + 25, my)], 4), INK, 2.4)   # awkward half-smile
        return                                                        # he doesn't mean
    if mood == 'deadpan':
        p.line([(fx - 18, my + 2), (fx + 14, my + 2), (fx + 20, my + 5)], INK, 3.6)
        return
    if mood == 'shy':                                                 # a small closed smile tucked to one side
        p.line(open_curve([(fx - 10, my + 2), (fx + 2, my + 6), (fx + 12, my + 1)], 4), INK, 3.0)
        return
    if mood == 'pout':
        p.ell(fx, my + 4, 8, 6, lip, INK, 2.2)
        return
    p.line(open_curve([(fx - 16, my), (fx, my + 6), (fx + 16, my)], 4), INK, 3.2)   # a soft resting smile


MOODS = {   # child faces: lids, pupils, brows (inner, outer rise; one = a single brow), mouth
    'neutral': dict(),
    'smile': dict(brows=(4, 0), mouth='smile'),
    'unsure': dict(brows=(20, -8), mouth='unsure', look=0.0),                      # line 2: "I think so?"
    'sceptical': dict(lid=(0.2, 0.0), each={-1: (16, -6), 1: (40, 34)}, mouth='sceptical', look=0.7, turn=-0.7,
                      wide=1.04),   # line 4: "Ok?" (note 31; Sam: "a look that conveys: uuuuuh, okay?"): bemused and
                    # uneasy, not hostile: one brow hiked high, the other tilted up at its inner end (worry), eyes
                    # wide and slid sideways at KG, head turned a little off, the mouth an awkward hitched line
    'doubtful': dict(lid=(0.38, 0.38), brows=(-18, -18), brow_w=9.0, brow_len=46, mouth='unsure', look=0.45),   # note 58 (Sam,
                    # 11 Nov, replaces note 31's look; Sam: brows level, low, close over the eyes): head straight on, heavy flat brows (not
                    # arched or worried), lids a little heavy, eyes slid slightly aside: unsure, sceptical, doubtful
    'aghast': dict(pupil=0.55, brows=(22, 14), mouth='aghast', wide=1.12),         # line 6: "Oh my god!"
    'wince': dict(lid=(0.5, 0.5), low=0.3, brows=(14, -6), mouth='wince'),         # line 8: "I can't do this"
    'horror': dict(pupil=0.42, low=0.15, brows=(24, -6), mouth='horror', wide=1.06),          # line 10: "This is horrible"
    'deadpan': dict(lid=(0.6, 0.6), brows=(-10, -8), mouth='deadpan'),            # line 12: "I am 9 years old"
    'terrified': dict(pupil=0.6, brows=(22, -8), mouth='terrified', wide=1.1, tears=True),   # line 14: "go home"
    'down': dict(gaze_dy=1.5, lid=(0.55, 0.55), brows=(6, 2), mouth='shy', tip=0.12, blush=1.7),   # Zelda: head and
                    # eyes down, lids heavy (pass 1); soft brows, a small tucked smile, pinker cheeks: shy, not startled
                    # (pass 2 read the raised brows and round mouth as startled)
    'hopeful': dict(brows=(12, 2), mouth='hopeful'),                              # Malon
    'smug': dict(lid=(0.36, 0.36), brows=(-2, 6), mouth='smug'),                   # Saria, Ruto
    'wink': dict(lid=(0.2, 0.2), closed=(1, 'smile'), brows=(0, 6), mouth='wink'),   # Saria winks at Link
    'vain': dict(lid=(0.56, 0.56), brows=(10, 14), one=(1, 12), mouth='smug', look=0.7, gaze_dy=0.5,   # arched
                                                                         # brows, not knitted (pass 2: read cross)
                 tip=-0.07),        # Ruto: chin up, looking down her nose
}


def kid_head(img, p, sp, t, hx, hy):
    hw, hh, skin = sp['hw'], sp['hh'], sp['skin']
    who = sp['who']
    mood = MOODS[sp.get('mood', 'neutral')]
    fx = hx + sp.get('turn', mood.get('turn', 0.0)) * hw * 0.16
    HAIR_BACK.get(who, lambda *a: None)(p, sp, hx, hy, hw, hh)
    if sp.get('ears', True):
        for sgn in (-1, 1):                                          # long pointed Hylian ears, out and a little up
            x = hx + sgn * hw * 0.92
            ear = curve([(x, hy - 14), (x + sgn * 30, hy - 30), (x + sgn * 92, hy - 64), (x + sgn * 50, hy + 4),
                         (x + sgn * 16, hy + 34), (x - sgn * 6, hy + 24)], 4)
            p.poly(ear, skin, INK, 2.6)
            p.line(open_curve([(x + sgn * 8, hy - 6), (x + sgn * 48, hy - 34), (x + sgn * 30, hy + 4), (x + sgn * 12, hy + 20)], 4),
                   dk(skin, 0.76), 1.8)
    outline = _kid_outline(hx, hy, hw, hh, sp.get('chin', 1.0))
    p.poly(outline, skin, INK, 2.8)
    tip = hh * mood.get('tip', 0.0)                                  # the head tipped down (+) or chin up (-): the
    ey = hy + hh * 0.2 + tip                                         # features slide on the face
    gap, ew, eh = hw * 0.4, hw * 0.22, hh * 0.22 * mood.get('wide', 1.0)   # big, but not anime-huge (Sam)
    for sgn in (-1, 1):                                              # cheeks: a soft flush
        bl = mood.get('blush', 1.0)
        p.ell(fx + sgn * hw * 0.58, ey + hh * 0.38, hw * 0.12 * bl, hh * 0.05 * bl,
              BLUSH if bl <= 1 else (238, 170, 168), None)
    lids = mood.get('lid', (0.0, 0.0))
    for k, sgn in enumerate((-1, 1)):
        closed = None
        if mood.get('closed') and mood['closed'][0] == sgn:
            closed = mood['closed'][1]
        if sp.get('blink'):
            closed = 'shut'
        _eye(p, fx + sgn * gap, ey, sgn, ew, eh, sp.get('iris', BLUE_EYE), lids[k],
             mood['lows'][k] if 'lows' in mood else mood.get('low', 0.0),
             sp.get('look', mood.get('look', 0.0)), sp.get('gaze_dy', mood.get('gaze_dy', 0.0)), mood.get('pupil', 1.0),
             closed, sp.get('lashes', False))
    if mood.get('tears'):                                            # wet eyes: a tear welling at each lower lid
        for sgn in (-1, 1):
            p.poly(curve([(fx + sgn * (gap + ew * 0.5), ey + eh * 0.8), (fx + sgn * (gap + ew * 0.7), ey + eh * 1.5),
                          (fx + sgn * (gap + ew * 0.4), ey + eh * 1.6)], 3), (170, 214, 246), INK, 1.6)
    ny = hy + hh * 0.5 + tip * 0.9                                   # a small button nose
    p.line(open_curve([(fx - 4, ny - 8), (fx + 6, ny), (fx - 2, ny + 6)], 4), dk(skin, 0.62), 2.4)
    _kid_mouth(p, sp, fx, hy + hh * 0.7 + tip * 0.75, mood.get('mouth', 'rest'), sp.get('lip_c', (176, 84, 84)))
    p.poly(outline, None, INK, 2.8)
    HAIR_FRONT.get(who, lambda *a: None)(p, sp, hx, hy, hw, hh)
    inner, outer = mood.get('brows', (0, 0))                         # brows over the fringe, as the remake's cartoon
    _brows(p, fx, ey, gap, eh, sp.get('brow_c', dk(sp.get('hair_c', L_HAIR), 0.5)), inner * 1.35, outer * 1.35,
           w=mood.get('brow_w', 4.4), length=mood.get('brow_len', 40), one=mood.get('one'),
           each=mood.get('each'))                    # does: they must read at phone size (Link 5)
    return fx


# ------------------------------------------------------------------------------------------------ hair and headgear
def _strands(p, pts, c, w=1.8):
    p.line(open_curve(pts, 4), c, w)


def _link_cap_tail(p, hx, hy, hw, hh):
    """The cap's big floppy tail (ref 04): it flops over from the crown and hangs fat and heavy behind his left ear
    (screen right) to the shoulder, a blunt rounded end, a fold down its length and a few rows of weave."""
    tail = curve([(hx + hw * 0.2, hy - hh * 1.3), (hx + hw * 1.05, hy - hh * 1.12), (hx + hw * 1.56, hy - hh * 0.5),
                  (hx + hw * 1.72, hy + hh * 0.4), (hx + hw * 1.66, hy + hh * 1.2), (hx + hw * 1.46, hy + hh * 1.42),
                  (hx + hw * 1.22, hy + hh * 1.26), (hx + hw * 1.1, hy + hh * 0.5), (hx + hw * 0.9, hy - hh * 0.3)], 5)
    p.poly(tail, L_CAP_D, INK, 2.8)
    p.line(open_curve([(hx + hw * 1.12, hy - hh * 0.7), (hx + hw * 1.4, hy + hh * 0.1), (hx + hw * 1.44, hy + hh * 1.0)], 4),
           dk(L_CAP_D, 0.72), 2.2)                                   # the fold
    for k in range(4):                                               # the weave across it
        y = hy - hh * 0.3 + k * hh * 0.38
        p.line(open_curve([(hx + hw * (1.16 + 0.02 * k), y), (hx + hw * 1.4, y + hh * 0.06),
                           (hx + hw * (1.62 - 0.02 * k), y)], 3), L_CAP, 1.6)


def _link_hair_back(p, sp, hx, hy, hw, hh):
    """The blond bowl cut to the jaw (refs 03, 04), and the cap's long tail hanging behind to his left."""
    _link_cap_tail(p, hx, hy, hw, hh)
    hair = curve([(hx - hw * 1.08, hy + hh * 0.5), (hx - hw * 1.1, hy - hh * 0.4), (hx - hw * 0.7, hy - hh * 0.95),
                  (hx + hw * 0.7, hy - hh * 0.95), (hx + hw * 1.1, hy - hh * 0.4), (hx + hw * 1.08, hy + hh * 0.5),
                  (hx + hw * 0.9, hy + hh * 0.62), (hx - hw * 0.9, hy + hh * 0.62)], 4)
    p.poly(hair, L_HAIR_D, INK, 2.6)


def _bead(p, x, y, r=11):
    """One red wooden bead on Link's cap band (ref 04), with a shine."""
    p.ell(x, y, r, r, BEAD, INK, 1.8)
    p.ell(x - r * 0.35, y - r * 0.35, r * 0.3, r * 0.3, (230, 130, 110), None)


def _link_hair_front(p, sp, hx, hy, hw, hh):
    """The fringe over the forehead in pointed locks, side locks over the cheeks, and the woven green cap on top
    with its band of red beads (ref 04)."""
    fr = [(hx - hw * 1.02, hy + hh * 0.42), (hx - hw * 1.04, hy - hh * 0.4), (hx - hw * 0.6, hy - hh * 0.72),
          (hx + hw * 0.6, hy - hh * 0.72), (hx + hw * 1.04, hy - hh * 0.4), (hx + hw * 1.02, hy + hh * 0.42),
          (hx + hw * 0.9, hy + hh * 0.2), (hx + hw * 0.84, hy - hh * 0.05), (hx + hw * 0.62, hy - hh * 0.1),
          (hx + hw * 0.5, hy - hh * 0.06), (hx + hw * 0.34, hy - hh * 0.22), (hx + hw * 0.16, hy - hh * 0.04),
          (hx - hw * 0.02, hy - hh * 0.24), (hx - hw * 0.2, hy - hh * 0.06), (hx - hw * 0.4, hy - hh * 0.2),
          (hx - hw * 0.56, hy - hh * 0.04), (hx - hw * 0.76, hy - hh * 0.12), (hx - hw * 0.86, hy + hh * 0.18)]
    p.poly(fr, sp['hair_c'], INK, 2.6)
    for a, b in ((-0.5, -0.1), (-0.1, 0.25), (0.3, 0.6), (-0.85, -0.6), (0.62, 0.9)):
        _strands(p, [(hx + hw * a, hy - hh * 0.62), (hx + hw * (a + b) / 2, hy - hh * 0.3), (hx + hw * b, hy - hh * 0.12)],
                 L_HAIR_D)
    cap = curve([(hx - hw * 1.14, hy - hh * 0.5), (hx - hw * 1.0, hy - hh * 1.12), (hx - hw * 0.3, hy - hh * 1.46),
                 (hx + hw * 0.5, hy - hh * 1.44), (hx + hw * 1.12, hy - hh * 1.04), (hx + hw * 1.24, hy - hh * 0.44),
                 (hx + hw * 0.6, hy - hh * 0.6), (hx - hw * 0.4, hy - hh * 0.62)], 4)   # big and soft (Link 4)
    p.poly(cap, L_CAP, INK, 2.8)
    for k in range(9):                                               # the weave: a few rows of stitches, not a texture
        u = -0.85 + k * 0.22
        p.line(open_curve([(hx + hw * u, hy - hh * 0.66), (hx + hw * (u + 0.05), hy - hh * 0.9),
                           (hx + hw * (u + 0.12), hy - hh * (1.26 - 0.1 * abs(u)))], 4), L_CAP_D, 1.6)
    band = [(hx - hw * 1.08, hy - hh * 0.5), (hx - hw * 0.4, hy - hh * 0.64), (hx + hw * 0.6, hy - hh * 0.62),
            (hx + hw * 1.18, hy - hh * 0.46), (hx + hw * 1.18, hy - hh * 0.6), (hx + hw * 0.6, hy - hh * 0.76),
            (hx - hw * 0.4, hy - hh * 0.78), (hx - hw * 1.04, hy - hh * 0.64)]
    p.poly(band, L_CAP_D, INK, 2.2)
    for k in range(8):                                               # the red beads along the band: big enough to
        u = -0.9 + k * 0.28                                          # read on a phone (pass 1: "cap - no beads")
        yb = hy - hh * (0.6 + 0.08 * (1 - (u - 0.1) ** 2)) + 2
        _bead(p, hx + hw * u, yb)


def _zelda_back(p, sp, hx, hy, hw, hh):
    """The white cloth veil behind the head, ending at the neck so her gold collar shows (ref 10; pass 1: the veil's
    grey drop read as a grey collar)."""
    p.poly(curve([(hx - hw * 1.12, hy - hh * 0.5), (hx - hw * 1.2, hy + hh * 0.5), (hx - hw * 1.16, hy + hh * 1.02),
                  (hx + hw * 1.16, hy + hh * 1.02), (hx + hw * 1.2, hy + hh * 0.5), (hx + hw * 1.12, hy - hh * 0.5),
                  (hx, hy - hh * 1.12)], 4), dk(Z_VEIL, 0.93), INK, 2.6)
    p.poly(curve([(hx - hw * 0.98, hy - hh * 0.2), (hx - hw * 1.02, hy + hh * 0.6), (hx - hw * 0.8, hy + hh * 0.9),
                  (hx + hw * 0.8, hy + hh * 0.9), (hx + hw * 1.02, hy + hh * 0.6), (hx + hw * 0.98, hy - hh * 0.2)], 4),
           Z_HAIR, INK, 2.2)                                         # blond hair under the veil


def _zelda_front(p, sp, hx, hy, hw, hh):
    """The veil framing the face, the purple padded headband with its gold triforce plate, a blond fringe."""
    fr = [(hx - hw * 0.94, hy - hh * 0.1), (hx - hw * 0.8, hy - hh * 0.6), (hx + hw * 0.8, hy - hh * 0.6),
          (hx + hw * 0.94, hy - hh * 0.1), (hx + hw * 0.7, hy - hh * 0.22), (hx + hw * 0.4, hy - hh * 0.3),
          (hx + hw * 0.05, hy - hh * 0.2), (hx - hw * 0.3, hy - hh * 0.32), (hx - hw * 0.7, hy - hh * 0.2)]
    p.poly(curve(fr, 3), sp['hair_c'], INK, 2.4)
    veil = [(hx - hw * 1.18, hy + hh * 0.9), (hx - hw * 1.2, hy - hh * 0.4), (hx - hw * 0.9, hy - hh * 1.0),
            (hx, hy - hh * 1.16), (hx + hw * 0.9, hy - hh * 1.0), (hx + hw * 1.2, hy - hh * 0.4), (hx + hw * 1.18, hy + hh * 0.9),
            (hx + hw * 1.0, hy + hh * 0.86), (hx + hw * 1.0, hy - hh * 0.3), (hx + hw * 0.8, hy - hh * 0.62),
            (hx - hw * 0.8, hy - hh * 0.62), (hx - hw * 1.0, hy - hh * 0.3), (hx - hw * 1.0, hy + hh * 0.86)]
    p.poly(veil, Z_VEIL, INK, 2.6)
    for u in (-1.1, 1.1):
        p.line(open_curve([(hx + hw * u, hy - hh * 0.3), (hx + hw * u * 1.03, hy + hh * 0.3), (hx + hw * u, hy + hh * 0.8)], 4),
               Z_VEIL_D, 1.8)
    band = curve([(hx - hw * 1.08, hy - hh * 0.5), (hx - hw * 0.7, hy - hh * 0.86), (hx, hy - hh * 0.96),
                  (hx + hw * 0.7, hy - hh * 0.86), (hx + hw * 1.08, hy - hh * 0.5), (hx + hw * 0.82, hy - hh * 0.56),
                  (hx, hy - hh * 0.72), (hx - hw * 0.82, hy - hh * 0.56)], 4)
    p.poly(band, Z_PURPLE, INK, 2.4)
    for u in (-0.6, -0.3, 0.3, 0.6):                                  # the padding's quilted lines
        p.line([(hx + hw * u, hy - hh * 0.62 - abs(u) * -6), (hx + hw * u * 1.04, hy - hh * 0.86 + abs(u) * 10)], Z_PURPLE_D, 1.6)
    ty = hy - hh * 0.82
    p.poly([(hx - 26, ty + 16), (hx, ty - 20), (hx + 26, ty + 16)], GOLD, INK, 2.0)    # the triforce plate
    p.poly([(hx - 13, ty - 2), (hx + 13, ty - 2), (hx, ty + 16)], GOLD_D, INK, 1.4)


def _malon_back(p, sp, hx, hy, hw, hh):
    """Behind the head: only the hair round the head; its long fall is drawn behind her body (malon_long_hair)."""
    p.poly(curve([(hx - hw * 1.12, hy - hh * 0.3), (hx - hw * 1.16, hy + hh * 0.9), (hx + hw * 1.16, hy + hh * 0.9),
                  (hx + hw * 1.12, hy - hh * 0.3), (hx, hy - hh * 1.1)], 4), M_HAIR_D, INK, 2.6)


def malon_long_hair(p, sp):
    """Long red hair to the waist behind her (refs 13, 14), drawn before her body so her shoulders and blouse show."""
    hx, hy, hw, hh = 0.0, -150.0 + sp.get('head_dy', 0.0), sp['hw'], sp['hh']
    p.poly(curve([(hx - hw * 1.12, hy - hh * 0.3), (hx - hw * 1.2, hy + hh * 1.0), (hx - hw * 1.16, hy + hh * 2.4),
                  (hx - hw * 0.96, hy + hh * 3.3), (hx - hw * 0.5, hy + hh * 3.5), (hx, hy + hh * 3.3),   # to her waist
                  (hx + hw * 0.5, hy + hh * 3.5), (hx + hw * 0.96, hy + hh * 3.3), (hx + hw * 1.16, hy + hh * 2.4),
                  (hx + hw * 1.18, hy + hh * 1.0), (hx + hw * 1.12, hy - hh * 0.3), (hx, hy - hh * 1.1)], 4),
           M_HAIR_D, INK, 2.6)


def _malon_front(p, sp, hx, hy, hw, hh):
    """A side-swept fringe and long locks falling over both shoulders in front."""
    top = [(hx - hw * 1.08, hy + hh * 0.6), (hx - hw * 1.08, hy - hh * 0.5), (hx - hw * 0.6, hy - hh * 1.0),
           (hx + hw * 0.4, hy - hh * 1.1), (hx + hw * 1.0, hy - hh * 0.7), (hx + hw * 1.1, hy - hh * 0.1),
           (hx + hw * 1.06, hy + hh * 0.6), (hx + hw * 0.94, hy + hh * 0.1), (hx + hw * 0.7, hy - hh * 0.36),
           (hx + hw * 0.2, hy - hh * 0.5), (hx - hw * 0.3, hy - hh * 0.3), (hx - hw * 0.7, hy - hh * 0.36),
           (hx - hw * 0.92, hy + hh * 0.0)]
    p.poly(curve(top, 3), sp['hair_c'], INK, 2.6)
    for a in (-0.7, -0.3, 0.2, 0.6):
        _strands(p, [(hx + hw * (a + 0.2), hy - hh * 0.96), (hx + hw * a, hy - hh * 0.66), (hx + hw * (a - 0.1), hy - hh * 0.4)],
                 M_HAIR_D)
    for sgn in (-1, 1):                                                # the locks down over the shoulders
        x = hx + sgn * hw * 1.0
        lock = curve([(x - sgn * 6, hy + hh * 0.2), (x + sgn * 20, hy + hh * 0.6), (x + sgn * 26, hy + hh * 1.4),
                      (x + sgn * 22, hy + hh * 2.4), (x + sgn * 8, hy + hh * 3.2), (x - sgn * 10, hy + hh * 3.3),
                      (x - sgn * 16, hy + hh * 2.4), (x - sgn * 12, hy + hh * 1.4), (x - sgn * 14, hy + hh * 0.7)], 4)
        p.poly(lock, sp['hair_c'], INK, 2.4)                           # one lock each side over the shoulder, down
        _strands(p, [(x + sgn * 6, hy + hh * 0.7), (x + sgn * 10, hy + hh * 1.6), (x + sgn * 4, hy + hh * 2.6),
                     (x - sgn * 2, hy + hh * 3.1)], M_HAIR_D)          # to her waist (pass 2: hair too short)


def _saria_back(p, sp, hx, hy, hw, hh):
    p.poly(curve([(hx - hw * 1.14, hy + hh * 0.5), (hx - hw * 1.16, hy - hh * 0.4), (hx - hw * 0.7, hy - hh * 1.02),
                  (hx + hw * 0.7, hy - hh * 1.02), (hx + hw * 1.16, hy - hh * 0.4), (hx + hw * 1.14, hy + hh * 0.5),
                  (hx + hw * 0.9, hy + hh * 0.7), (hx - hw * 0.9, hy + hh * 0.7)], 4), S_HAIR_D, INK, 2.6)


def _saria_front(p, sp, hx, hy, hw, hh):
    """The bright lime bob (ref 16): a full blunt fringe, the sides flicking out at the jaw."""
    top = [(hx - hw * 1.12, hy + hh * 0.56), (hx - hw * 1.36, hy + hh * 0.66), (hx - hw * 1.12, hy + hh * 0.28),
           (hx - hw * 1.1, hy - hh * 0.5), (hx - hw * 0.62, hy - hh * 1.06), (hx + hw * 0.62, hy - hh * 1.06),
           (hx + hw * 1.1, hy - hh * 0.5), (hx + hw * 1.12, hy + hh * 0.28), (hx + hw * 1.36, hy + hh * 0.66),
           (hx + hw * 1.12, hy + hh * 0.56), (hx + hw * 0.9, hy + hh * 0.3), (hx + hw * 0.84, hy - hh * 0.2),
           (hx + hw * 0.5, hy - hh * 0.18), (hx + hw * 0.3, hy - hh * 0.26), (hx, hy - hh * 0.18),
           (hx - hw * 0.3, hy - hh * 0.26), (hx - hw * 0.5, hy - hh * 0.18), (hx - hw * 0.84, hy - hh * 0.2),
           (hx - hw * 0.9, hy + hh * 0.3)]
    p.poly(top, sp['hair_c'], INK, 2.6)
    for a in (-0.6, -0.2, 0.2, 0.6):
        _strands(p, [(hx + hw * a * 0.8, hy - hh * 0.9), (hx + hw * a, hy - hh * 0.5), (hx + hw * a * 1.05, hy - hh * 0.26)],
                 S_HAIR_D)


def _fin_pts(hx, hy, hw, hh, pts):
    return [(hx + hw * u, hy + hh * v) for u, v in pts]


def _ruto_back(p, sp, hx, hy, hw, hh):
    """Her small fan fins where ears would be (refs 07, 08): teal, pink at the root, ribbed."""
    for sgn in (-1, 1):
        x, y = hx + sgn * hw * 0.9, hy + hh * 0.06
        fan = curve([(x, y - hh * 0.16), (x + sgn * hw * 0.3, y - hh * 0.3), (x + sgn * hw * 0.42, y - hh * 0.04),
                     (x + sgn * hw * 0.3, y + hh * 0.22), (x, y + hh * 0.2)], 4)
        p.poly(fan, R_FIN, INK, 2.2)
        p.ell(x + sgn * hw * 0.04, y + hh * 0.02, hw * 0.06, hh * 0.12, R_TOE, None)
        for a in (-0.22, 0.0, 0.18):
            p.line([(x + sgn * hw * 0.04, y + hh * 0.02), (x + sgn * hw * 0.36, y + hh * a)], R_FIN_D, 1.6)


def _ruto_front(p, sp, hx, hy, hw, hh):
    """The Zora head: the skull itself grows up and OUT into a broad flat-topped teal fish head, widest near the top
    and narrowing down into her temples (refs 07, 08). No brim, no underside, no lobes past the face (passes 1-2:
    the domes with a rim read as a mushroom helmet). One inked outline that runs on into the face's sides; its
    lower edge on the forehead is a soft colour change dipping to a point over the brow."""
    side = [(0.97, -0.12), (1.04, -0.44), (1.24, -0.74), (1.44, -0.96), (1.46, -1.16), (1.2, -1.3), (0.6, -1.38),
            (0, -1.4)]
    top = _fin_pts(hx, hy, hw, hh, side + [(-u, v) for u, v in side[::-1][1:]])
    edge = _fin_pts(hx, hy, hw, hh, [(-0.97, -0.24), (-0.8, -0.56), (-0.46, -0.72), (-0.16, -0.6), (0, -0.48),
                                     (0.16, -0.6), (0.46, -0.72), (0.8, -0.56), (0.97, -0.24)])
    p.poly(curve(top + edge, 4), R_FIN, None)
    mid = tuple(int(a * 0.55 + b * 0.45) for a, b in zip(R_SKIN, R_FIN))      # pale skin growing up into the teal
    p.poly(curve(_fin_pts(hx, hy, hw, hh, [(0.97, -0.24), (0.98, -0.46), (0.8, -0.78), (0.5, -0.88), (0, -0.92),
                                            (-0.5, -0.88), (-0.8, -0.78), (-0.98, -0.46), (-0.97, -0.24),
                                            (-0.8, -0.56), (-0.46, -0.72), (-0.16, -0.6), (0, -0.48), (0.16, -0.6),
                                            (0.46, -0.72), (0.8, -0.56)]), 4), mid, None)
    p.line(open_curve(top, 6), INK, 2.8)
    p.ell(hx - hw * 0.6, hy - hh * 1.1, hw * 0.3, hh * 0.06, (176, 236, 228), None, rot=-0.2)   # shines
    p.ell(hx + hw * 0.8, hy - hh * 1.02, hw * 0.1, hh * 0.04, (176, 236, 228), None, rot=0.3)


HAIR_BACK = {'link': _link_hair_back, 'zelda': _zelda_back, 'malon': _malon_back, 'saria': _saria_back,
             'ruto': _ruto_back}
HAIR_FRONT = {'link': _link_hair_front, 'zelda': _zelda_front, 'malon': _malon_front, 'saria': _saria_front,
              'ruto': _ruto_front}


# ------------------------------------------------------------------------------------------------ Link's turned heads
def link_head_side(img, p, sp, t, hx, hy):
    """Link in profile facing right (the wall shot): the big round skull, a small up-turned nose, a big eye seen side
    on, the long ear pointing back, the bowl cut and the cap's tail hanging back."""
    hw, hh, skin = sp['hw'], sp['hh'], sp['skin']
    mood = MOODS[sp.get('mood', 'neutral')]
    p.poly(curve([(hx - hw * 0.1, hy - hh * 1.3), (hx - hw * 1.2, hy - hh * 1.0), (hx - hw * 1.7, hy - hh * 0.1),
                  (hx - hw * 1.72, hy + hh * 0.9), (hx - hw * 1.5, hy + hh * 1.2), (hx - hw * 1.3, hy + hh * 0.9),
                  (hx - hw * 1.1, hy + hh * 0.1), (hx - hw * 0.7, hy - hh * 0.4)], 4),
           L_CAP_D, INK, 2.6)                                        # the cap's fat tail flopping back
    head = curve([(hx - hw * 0.92, hy), (hx - hw * 0.86, hy - hh * 0.7), (hx - hw * 0.3, hy - hh * 1.06),
                  (hx + hw * 0.4, hy - hh * 0.98), (hx + hw * 0.86, hy - hh * 0.5), (hx + hw * 0.92, hy + hh * 0.1),
                  (hx + hw * 1.02, hy + hh * 0.42), (hx + hw * 0.92, hy + hh * 0.52), (hx + hw * 0.9, hy + hh * 0.7),
                  (hx + hw * 0.7, hy + hh * 0.94), (hx + hw * 0.3, hy + hh * 1.0), (hx - hw * 0.2, hy + hh * 0.86),
                  (hx - hw * 0.6, hy + hh * 0.5)], 4)
    p.poly(head, skin, INK, 2.8)
    p.ell(hx + hw * 0.5, hy + hh * 0.56, hw * 0.12, hh * 0.05, BLUSH, None)
    ex, ey = hx + hw * 0.6, hy + hh * 0.2
    w, h = hw * 0.13, hh * 0.27 * mood.get('wide', 1.0)
    fear = sp.get('mood') == 'terrified'                             # Sam, 11 Nov: staring, absolutely terrified,
    if fear:                                                         # down into KG's eyes: the eye huge, white all
        w, h = hw * 0.21, hh * 0.36                                  # round a pinprick pupil aimed down at him
    lid = mood.get('lid', (0, 0))[1]
    us = np.linspace(-1, 1, 13)
    top = [(ex + w * u, ey - h * (1 - u * u) ** 0.5 * (1 - lid)) for u in us]
    bot = [(ex + w * u, ey + h * (1 - u * u) ** 0.5 * 0.9) for u in us]
    opening = top + bot[::-1][1:-1]
    p.poly(opening, WHITE, None)
    if fear:
        gx, gy = sp.get('stare', (0.5, 0.86))                        # unit direction to KG's eyes (right and down)
        ix, iy = ex + w * 0.42 * gx, ey + h * 0.42 * gy
        p.poly(oval(ix, iy, w * 0.46, h * 0.36, 24), sp.get('iris', BLUE_EYE), None)
        p.poly(oval(ix + w * 0.06 * gx, iy + h * 0.05 * gy, w * 0.17, h * 0.13, 16), INK, None)
        p.ell(ix - w * 0.16, iy - h * 0.14, w * 0.1, w * 0.1, SHINE, None)
        p.line(top + bot[::-1], INK, 3.4)
        p.line(top, INK, 4.6)
    else:
        ring = clip_convex(opening[::-1], oval(ex + w * 0.3, ey + 4, w * 0.9, h * 0.7, 24)[::-1][::-1])
        if len(ring) >= 3:
            p.poly(ring, sp.get('iris', BLUE_EYE), None)
        pu = clip_convex(opening[::-1], oval(ex + w * 0.4, ey + 4, w * 0.45 * mood.get('pupil', 1.0), h * 0.36 * mood.get('pupil', 1.0), 20))
        if len(pu) >= 3:
            p.poly(pu, INK, None)
        p.ell(ex + w * 0.1, ey - h * 0.3, w * 0.24, w * 0.24, SHINE, None)
        p.line(top, INK, 4.2)
    inner, outer = mood.get('brows', (0, 0))
    if fear:
        inner, outer = 30, -16                                       # the brow steep: hiked at the nose, pinched down
    p.line(open_curve([(ex - w * 1.2, ey - h - 14 - outer), (ex, ey - h - 22 - (inner + outer) / 2),
                       (ex + w * 1.0, ey - h - 16 - inner)], 4), dk(sp['hair_c'], 0.7), 5.6)
    my = hy + hh * 0.72
    m = mood.get('mouth', 'rest')
    if fear:                                                         # a tear welling and running, sweat flying,
        tw = 3 * math.sin(t * 22)                                    # the mouth a wide wobbling wail with teeth
        p.poly(curve([(ex - w * 0.2, ey + h * 0.9), (ex + w * 0.2, ey + h * 1.05), (ex + w * 0.15, ey + h * 1.9),
                      (ex - w * 0.3, ey + h * 1.8)], 3), (170, 214, 246), INK, 1.8)
        for k, (dx, dy) in enumerate(((-0.5, -1.25), (-0.15, -1.5), (-0.95, -0.9))):
            p.poly(curve([(hx + hw * dx, hy + hh * dy - 16), (hx + hw * dx + 9, hy + hh * dy + 6),
                          (hx + hw * dx - 9, hy + hh * dy + 6)], 3), (170, 214, 246), INK, 1.6)
        mo = [(hx + hw * 0.5, my - 16), (hx + hw * 0.74, my - 22 + tw), (hx + hw * 0.88, my - 12),
              (hx + hw * 0.86, my + 8 - tw), (hx + hw * 0.68, my + 14), (hx + hw * 0.5, my + 6 + tw)]
        p.poly(curve(mo, 4), (96, 34, 40), INK, 2.6)
        p.poly([(hx + hw * 0.6, my - 18), (hx + hw * 0.84, my - 16), (hx + hw * 0.84, my - 9), (hx + hw * 0.6, my - 11)],
               WHITE, INK, 1.4)
    elif m in ('aghast', 'terrified', 'horror'):
        p.poly(curve([(hx + hw * 0.8, my - 6), (hx + hw * 0.92, my), (hx + hw * 0.86, my + 18), (hx + hw * 0.72, my + 10)], 3),
               (96, 34, 40), INK, 2.4)
    else:
        p.line([(hx + hw * 0.88, my), (hx + hw * 0.72, my + 2)], INK, 3.0)
    hair = [(hx - hw * 0.94, hy + hh * 0.5), (hx - hw * 1.0, hy - hh * 0.5), (hx - hw * 0.5, hy - hh * 0.96),
            (hx + hw * 0.4, hy - hh * 0.96), (hx + hw * 0.9, hy - hh * 0.46), (hx + hw * 0.88, hy - hh * 0.1),
            (hx + hw * 0.7, hy - hh * 0.2), (hx + hw * 0.6, hy - hh * 0.02), (hx + hw * 0.4, hy - hh * 0.16),
            (hx + hw * 0.1, hy - hh * 0.06), (hx - hw * 0.08, hy + hh * 0.1), (hx - hw * 0.3, hy - hh * 0.02),
            (hx - hw * 0.5, hy + hh * 0.44), (hx - hw * 0.7, hy + hh * 0.3)]
    p.poly(hair, sp['hair_c'], INK, 2.6)
    x = hx - hw * 0.22                                               # the ear, swept back and up, drawn OVER the bowl
    ear = curve([(x + 14, hy + 2), (x - 30, hy - 30), (x - 150, hy - 84), (x - 60, hy + 14), (x - 14, hy + 40),
                 (x + 16, hy + 30)], 4)                              # cut (pass 2: the hair hid it, side view earless)
    p.poly(ear, skin, INK, 2.6)
    p.line(open_curve([(x - 2, hy + 2), (x - 80, hy - 48), (x - 40, hy + 8), (x - 6, hy + 22)], 4), dk(skin, 0.76), 1.8)
    p.poly(curve([(hx - hw * 1.04, hy - hh * 0.4), (hx - hw * 0.8, hy - hh * 1.2), (hx + hw * 0.1, hy - hh * 1.44),
                  (hx + hw * 0.8, hy - hh * 1.0), (hx + hw * 0.84, hy - hh * 0.5), (hx + hw * 0.3, hy - hh * 0.62),
                  (hx - hw * 0.5, hy - hh * 0.5)], 4), L_CAP, INK, 2.8)
    p.poly(curve([(hx - hw * 1.04, hy - hh * 0.4), (hx + hw * 0.84, hy - hh * 0.5), (hx + hw * 0.82, hy - hh * 0.64),
                  (hx - hw * 1.0, hy - hh * 0.56)], 2), L_CAP_D, INK, 2.0)
    for k in range(6):
        _bead(p, hx - hw * 0.8 + k * hw * 0.32, hy - hh * (0.48 + 0.03 * k))


def link_head_back(img, p, sp, t, hx, hy):
    """The back of his head (the opening shot's foreground, ref 01): the bowl cut, the ears' points out past it, the
    woven cap with its spiral, its tail hanging down his back."""
    hw, hh, skin = sp['hw'], sp['hh'], sp['skin']
    for sgn in (-1, 1):
        x = hx + sgn * hw * 0.9
        p.poly(curve([(x, hy - 14), (x + sgn * 30, hy - 30), (x + sgn * 92, hy - 64), (x + sgn * 50, hy + 4), (x + sgn * 10, hy + 30)], 4),
               skin, INK, 2.6)
    p.poly(_kid_outline(hx, hy, hw, hh), L_HAIR_D, INK, 2.8)
    p.poly(curve([(hx - hw * 1.08, hy + hh * 0.5), (hx - hw * 1.1, hy - hh * 0.4), (hx - hw * 0.7, hy - hh * 0.95),
                  (hx + hw * 0.7, hy - hh * 0.95), (hx + hw * 1.1, hy - hh * 0.4), (hx + hw * 1.08, hy + hh * 0.5),
                  (hx + hw * 0.5, hy + hh * 0.72), (hx - hw * 0.5, hy + hh * 0.72)], 4), sp['hair_c'], INK, 2.6)
    for a in (-0.7, -0.35, 0.0, 0.35, 0.7):
        _strands(p, [(hx + hw * a * 0.6, hy - hh * 0.5), (hx + hw * a, hy), (hx + hw * a * 1.02, hy + hh * 0.6)], L_HAIR_D)
    cap = curve([(hx - hw * 1.16, hy - hh * 0.4), (hx - hw * 1.0, hy - hh * 1.14), (hx, hy - hh * 1.46),
                 (hx + hw * 1.0, hy - hh * 1.14), (hx + hw * 1.16, hy - hh * 0.4), (hx + hw * 0.6, hy - hh * 0.5),
                 (hx - hw * 0.6, hy - hh * 0.5)], 4)
    p.poly(cap, L_CAP, INK, 2.8)
    sp_pts = [(hx + hw * 0.46 * (a / 12.0) * math.cos(a), hy - hh * 1.0 + hh * 0.3 * (a / 12.0) * math.sin(a))
              for a in np.linspace(0.5, 12.0, 40)]
    p.line(sp_pts, L_CAP_D, 2.6)                                    # the woven spiral (ref 01)
    tail = curve([(hx - hw * 0.1, hy - hh * 0.9), (hx + hw * 0.8, hy - hh * 0.7), (hx + hw * 1.0, hy + hh * 0.3),
                  (hx + hw * 0.8, hy + hh * 1.3), (hx + hw * 0.5, hy + hh * 1.5), (hx + hw * 0.2, hy + hh * 1.3),
                  (hx + hw * 0.1, hy + hh * 0.4)], 4)                # fat, hanging to his left (ref 04)
    p.poly(tail, L_CAP_D, INK, 2.6)
    p.poly([(hx - hw * 1.1, hy - hh * 0.4), (hx + hw * 1.1, hy - hh * 0.4), (hx + hw * 1.08, hy - hh * 0.54),
            (hx - hw * 1.08, hy - hh * 0.54)], L_CAP_D, INK, 2.0)
    for k in range(9):
        _bead(p, hx - hw * 0.96 + k * hw * 0.24, hy - hh * 0.47)


# ================================================================================================ the kids' bodies
def _neck(p, sp):
    p.poly([(-34, -70), (34, -70), (36, 14), (-36, 14)], sp['skin'], INK, 2.4)   # short and thick: a child's


def _body(sw, bottom, flare=1.0):
    """The child's torso shape (shoulders round, a soft belly), the hem flaring by `flare`."""
    return curve([(-30, -4), (-sw * 0.72, 8), (-sw, 46), (-sw - 4, 160), (-sw * 0.96, 300), (-sw * B.HEM * flare, bottom),
                  (sw * B.HEM * flare, bottom), (sw * 0.96, 300), (sw + 4, 160), (sw, 46), (sw * 0.72, 8), (30, -4)], 3)


def _fringe(p, x0, x1, y, c, n=9, depth=26):
    """A frayed hem (Link's tunic, ref 03): a row of rough points."""
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append((x, y))
        if i < n:
            pts.append((x + (x1 - x0) / n / 2, y + depth * (0.7 + 0.3 * ((i * 37) % 5) / 4)))
    p.poly([(x0, y - 20)] + pts + [(x1, y - 20)], c, INK, 2.0)


def _tunic_link(img, p, sp):
    sw, bottom = sp['shoulders'], sp['bottom']
    _neck(p, sp)
    body = _body(sw, bottom, 1.12)
    p.poly(body, L_TUNIC, INK, 2.6)
    _fringe(p, -sw * B.HEM * 1.12, sw * B.HEM * 1.12, bottom - 6, L_TUNIC, 11)
    p.poly(curve([(-70, -10), (70, -10), (78, 30), (0, 74), (-78, 30)], 3), L_SHIRT, INK, 2.4)   # the knit shirt's neck
    for sgn in (-1, 1):                                                   # its collar points
        p.poly([(sgn * 6, 6), (sgn * 62, -8), (sgn * 50, 40)], L_SHIRT, INK, 2.0)
    p.poly([(sw * 0.5, 10), (-sw * 0.2, 290), (-sw * 0.36, 280), (sw * 0.34, 4)], LEATHER, INK, 2.2)   # the chest strap
    # over his left shoulder (screen right), as from behind and in refs 03, 04 (it carries the sword)
    for k in range(4):
        y = 300 + k * 40
        x = -sw * 0.5 + (sw * 0.7) * (y - 10) / 280 if y < 290 else 0
    belt = [(-sw * 0.97, 300), (sw * 0.97, 300), (sw * 0.98, 344), (-sw * 0.98, 344)]
    p.poly(belt, LEATHER, INK, 2.4)
    p.ell(0, 322, 30, 30, SILVER, INK, 2.4)                                # the round silver buckle
    p.ell(0, 322, 16, 16, dk(SILVER, 0.7), INK, 1.6)
    for x in np.linspace(-sw * 0.8, sw * 0.8, 7):                         # the tunic's weave: a few vertical ribs
        p.line([(x * 0.96, 360), (x * 1.08, bottom - 20)], L_TUNIC_D, 1.6)
    for x in np.linspace(-sw * 0.6, sw * 0.6, 5):
        p.line([(x, 90), (x * 1.04, 280)], L_TUNIC_D, 1.4)


def _dress_zelda(img, p, sp):
    sw, bottom = sp['shoulders'], sp['bottom']
    _neck(p, sp)
    skirt = [(-sw * 0.9, 300), (-sw * 1.5, bottom), (sw * 1.5, bottom), (sw * 0.9, 300)]   # no curve: it bowed
    p.poly(skirt, Z_SKIRT, INK, 2.6)
    p.poly([(-sw * 1.5, bottom - 50), (sw * 1.5, bottom - 50), (sw * 1.52, bottom), (-sw * 1.52, bottom)], Z_PURPLE, INK, 2.2)
    for x in (-0.9, -0.4, 0.4, 0.9):
        p.line([(sw * x * 0.7, 330), (sw * x * 1.3, bottom - 54)], dk(Z_SKIRT, 0.86), 1.8)
    p.poly(_body(sw, 330), Z_SLEEVE, INK, 2.6)                             # the pale blue bodice
    tab = [(-sw * 0.5, 40), (sw * 0.5, 40), (sw * 0.56, 300), (sw * 0.6, bottom - 70), (-sw * 0.6, bottom - 70),
           (-sw * 0.56, 300)]
    p.poly(tab, Z_PURPLE, INK, 2.6)                                       # the purple tabard to below the knee: purple
    inset = [(-sw * 0.42, 70), (sw * 0.42, 70), (sw * 0.5, bottom - 96), (-sw * 0.5, bottom - 96)]   # with gold
    p.poly(inset, None, GOLD_D, 7.0)                                      # trim and embroidery (pass 1: read gold);
    p.poly(inset, None, GOLD, 4.4)                                        # a bold band with a dark edge, as thin gold
    for y in np.linspace(150, bottom - 170, 5):                           # lines on purple read pink (pass 2)
        sc = open_curve([(-sw * 0.26, y), (-sw * 0.1, y - 12), (0, y), (sw * 0.1, y + 12), (sw * 0.26, y)], 4)
        p.line(sc, GOLD_D, 5.6)
        p.line(sc, GOLD, 3.4)
    ey = bottom - 150                                                     # the royal crest low on it (ref 10)
    p.poly([(-30, ey + 24), (0, ey - 30), (30, ey + 24)], GOLD, INK, 1.8)
    collar = curve([(-sw * 1.0, 6), (-sw * 0.5, -14), (sw * 0.5, -14), (sw * 1.0, 6), (sw * 0.7, 70), (0, 96),
                    (-sw * 0.7, 70)], 4)
    p.poly(collar, GOLD, INK, 2.6)                                        # the gold collar over the shoulders
    p.line(open_curve([(-sw * 0.74, 40), (0, 70), (sw * 0.74, 40)], 4), GOLD_D, 2.0)
    p.ell(0, 62, 13, 13, (90, 150, 220), INK, 1.8)


def rough_band(half, y0, y1):
    return [(-half, y0), (half, y0), (half, y1), (-half, y1)]


def _dress_malon(img, p, sp):
    sw, bottom = sp['shoulders'], sp['bottom']
    _neck(p, sp)
    skirt = [(-sw * 0.9, 300), (-sw * 1.36, bottom), (sw * 1.36, bottom), (sw * 0.9, 300)]  # the hem below ground
    p.poly(skirt, M_SKIRT, INK, 2.6)
    p.poly([(-sw * 1.36, bottom - 44), (sw * 1.36, bottom - 44), (sw * 1.38, bottom), (-sw * 1.38, bottom)], M_HEM, INK, 2.2)
    for k in range(9):                                                    # the blue meander along the hem (ref 14)
        x = -sw * 1.2 + k * sw * 0.3
        p.line([(x, bottom - 10), (x, bottom - 34), (x + sw * 0.14, bottom - 34), (x + sw * 0.14, bottom - 20)],
               (238, 234, 226), 2.4)
    p.poly(_body(sw, 330), M_BLOUSE, INK, 2.6)
    apron = [(-sw * 0.6, 300), (sw * 0.6, 300), (sw * 0.76, bottom - 70), (-sw * 0.76, bottom - 70)]
    p.poly(apron, M_APRON, INK, 2.4)
    for y in np.linspace(360, bottom - 110, 5):                           # its woven pattern rows
        p.line([(-sw * 0.6, y), (sw * 0.6, y)], M_APRON_D, 2.2)
        for x in np.linspace(-sw * 0.5, sw * 0.5, 5):
            p.poly([(x - 8, y + 14), (x, y + 6), (x + 8, y + 14), (x, y + 22)], M_APRON_D, None)
    p.poly([(-sw * 0.97, 290), (sw * 0.97, 290), (sw * 0.97, 320), (-sw * 0.97, 320)], LEATHER, INK, 2.2)   # belt
    scarf = curve([(-sw * 0.8, 0), (sw * 0.8, 0), (sw * 0.5, 70), (0, 130), (-sw * 0.5, 70)], 3)
    p.poly(scarf, M_SCARF, INK, 2.4)                                      # the yellow neckerchief
    p.line(open_curve([(-sw * 0.4, 40), (0, 90), (sw * 0.4, 40)], 4), dk(M_SCARF, 0.8), 1.8)
    p.ell(0, 30, 16, 14, (100, 170, 220), INK, 1.8)                       # its brooch


def _tunic_saria(img, p, sp):
    sw, bottom = sp['shoulders'], sp['bottom']
    _neck(p, sp)
    w = sw * B.HEM * 1.02                                                 # green shorts showing under the hem (ref 16)
    p.poly([(-w, bottom - 60), (w, bottom - 60), (w * 0.98, bottom + 64), (w * 0.12, bottom + 64), (0, bottom + 30),
            (-w * 0.12, bottom + 64), (-w * 0.98, bottom + 64)], S_SHORTS, INK, 2.4)
    p.poly(_body(sw, bottom, 1.08), S_TUNIC, INK, 2.6)
    for k in range(3):                                                    # the swirl pattern on the tunic
        cx, cy = (-sw * 0.45 + k * sw * 0.45), 200 + (k % 2) * 60
        p.line([(cx + 26 * (a / 9) * math.cos(a), cy + 26 * (a / 9) * math.sin(a)) for a in np.linspace(0.5, 9, 24)],
               S_TUNIC_D, 2.2)
    p.poly(curve([(-sw * 0.6, -40), (sw * 0.6, -40), (sw * 0.7, 30), (0, 60), (-sw * 0.7, 30)], 3), S_TOP, INK, 2.4)  # high collar
    p.line(open_curve([(-30, 30), (0, 90), (30, 30)], 4), (200, 170, 100), 2.0)    # the pendant's cord
    p.ell(0, 96, 12, 14, (226, 150, 64), INK, 1.8)
    sgn = 1                                                               # the fringed shoulder on her left (ref 16)
    p.poly(curve([(sgn * sw * 0.4, 6), (sgn * (sw + 20), 30), (sgn * (sw + 26), 110), (sgn * sw * 0.7, 90)], 3), S_TOP, INK, 2.2)
    _fringe(p, sgn * sw * 0.66, sgn * (sw + 26), 96, S_TOP, 5, 22)
    p.poly([(-sw * 0.97, 300), (sw * 0.97, 300), (sw * 0.97, 336), (-sw * 0.97, 336)], LEATHER, INK, 2.2)
    p.ell(sw * 0.3, 318, 13, 13, (210, 120, 60), INK, 1.6)               # the bead on her belt


def _body_ruto(img, p, sp):
    """Bare Zora skin with the teal fin top at the chest and fins hanging from the hips."""
    sw = sp['shoulders']
    p.poly(curve([(-40, -70), (40, -70), (46, -20), (62, 14), (-62, 14), (-46, -20)], 3), R_SKIN, INK, 2.4)
    body = curve([(-50, -10), (-sw * 0.72, 8), (-sw * 0.92, 46), (-sw * 0.82, 200), (-sw * 0.6, 300), (-sw * 0.96, 430),
                  (-sw * 0.82, 500), (sw * 0.82, 500), (sw * 0.96, 430), (sw * 0.6, 300), (sw * 0.82, 200), (sw * 0.92, 46),
                  (sw * 0.72, 8), (50, -10)], 3)
    p.poly(body, R_SKIN, INK, 2.6)
    p.poly(curve([(-sw * 0.8, 90), (0, 110), (sw * 0.8, 90), (sw * 0.7, 170), (0, 196), (-sw * 0.7, 170)], 3), R_FIN, INK, 2.2)
    for sgn in (-1, 1):                                                   # the fins hanging from her hips (ref 07):
        fin = curve([(sgn * sw * 0.78, 392), (sgn * (sw + 30), 410), (sgn * (sw + 78), 470), (sgn * (sw + 66), 600),
                     (sgn * (sw + 30), 540), (sgn * sw * 0.86, 470)], 4)     # rooted on the hip, flaring out and down
        p.poly(fin, R_FIN, INK, 2.2)
        p.line(open_curve([(sgn * sw * 0.9, 420), (sgn * (sw + 40), 480), (sgn * (sw + 60), 570)], 4), R_FIN_D, 1.8)
    p.line(open_curve([(-sw * 0.5, 470), (0, 500), (sw * 0.5, 470)], 4), R_SKIN_D, 1.8)
    p.line(open_curve([(-sw * 0.3, 240), (0, 260), (sw * 0.3, 240)], 4), R_SKIN_D, 1.6)


TORSO = {'link': _tunic_link, 'zelda': _dress_zelda, 'malon': _dress_malon, 'saria': _tunic_saria, 'ruto': _body_ruto}


SHEATH, SHEATH_D = (104, 68, 42), (72, 46, 28)
GRIP, POMMEL = (92, 58, 34), (70, 44, 26)
STEEL = (168, 174, 184)
SWORD_U = (0.57, -0.82)         # the sheath's line up his back, towards the hilt (front view; mirrored from behind)


def _unit(u):
    n = math.hypot(*u) or 1.0
    return u[0] / n, u[1] / n


def kokiri_hilt(p, m, u):
    """The Kokiri Sword's hilt (Sam, 10 Nov; ref 03): a small steel guard with curled ends at the sheath's mouth `m`,
    a short brown wrapped grip along `u`, a round flat wooden pommel cap."""
    ux, uy = _unit(u)
    vx, vy = -uy, ux
    g, L = 30.0, 96.0
    p.poly(curve([(m[0] + vx * g, m[1] + vy * g), (m[0] + vx * g + ux * 14, m[1] + vy * g + uy * 14),
                  (m[0] - vx * g + ux * 14, m[1] - vy * g + uy * 14), (m[0] - vx * g, m[1] - vy * g)], 2), STEEL, INK, 2.2)
    for sg in (-1, 1):                                                # the guard's curled ends
        cx, cy = m[0] + sg * vx * (g + 6) + ux * 4, m[1] + sg * vy * (g + 6) + uy * 4
        p.ell(cx, cy, 8, 8, STEEL, INK, 1.8)
    a = (m[0] + ux * 14, m[1] + uy * 14)
    b = (m[0] + ux * L, m[1] + uy * L)
    w = 11.0
    p.poly([(a[0] + vx * w, a[1] + vy * w), (b[0] + vx * w, b[1] + vy * w), (b[0] - vx * w, b[1] - vy * w),
            (a[0] - vx * w, a[1] - vy * w)], GRIP, INK, 2.2)
    for k in range(1, 5):                                             # the wrap: a few slanted turns
        t0, t1 = 14 + (L - 14) * (k - 0.6) / 5, 14 + (L - 14) * k / 5
        p.line([(m[0] + ux * t0 + vx * w, m[1] + uy * t0 + vy * w), (m[0] + ux * t1 - vx * w, m[1] + uy * t1 - vy * w)],
               dk(GRIP, 0.7), 1.8)
    p.ell(b[0] + ux * 8, b[1] + uy * 8, 20, 12, POMMEL, INK, 2.2, rot=math.atan2(vy, vx))   # the round flat cap
    p.ell(b[0] + ux * 6, b[1] + uy * 6, 10, 5, dk(POMMEL, 1.3), None, rot=math.atan2(vy, vx))


def kokiri_sheath(p, m, u, length=400.0):
    """Its carved wooden sheath (ref 03) from the mouth `m` down against `u`: wide at the mouth, tapering to a
    rounded tip, a carved line down it and two leather bands."""
    ux, uy = _unit(u)
    vx, vy = -uy, ux
    tip = (m[0] - ux * length, m[1] - uy * length)
    w0, w1 = 26.0, 16.0
    end = [(tip[0] + vx * w1 * math.cos(a) - ux * w1 * math.sin(a), tip[1] + vy * w1 * math.cos(a) - uy * w1 * math.sin(a))
           for a in np.linspace(0, math.pi, 9)]                           # the rounded tip, a half circle
    p.poly([(m[0] + vx * w0, m[1] + vy * w0)] + end + [(m[0] - vx * w0, m[1] - vy * w0)], SHEATH, INK, 2.4)
    p.line([(m[0] - ux * 30, m[1] - uy * 30), (tip[0] + ux * 20, tip[1] + uy * 20)], SHEATH_D, 2.0)
    for t in (40.0, length - 70):
        w = w0 + (w1 - w0) * t / length + 2
        c = (m[0] - ux * t, m[1] - uy * t)
        p.poly([(c[0] + vx * w + ux * 9, c[1] + vy * w + uy * 9), (c[0] + vx * w - ux * 9, c[1] + vy * w - uy * 9),
                (c[0] - vx * w - ux * 9, c[1] - vy * w - uy * 9), (c[0] - vx * w + ux * 9, c[1] - vy * w + uy * 9)],
               LEATHER_D, INK, 1.8)


# where the hilt leaves the body, per view (torso units: the sheath runs from his right hip up to his left shoulder)
HILT_AT = {'front': ((92.0, 2.0), SWORD_U), 'back': ((-92.0, 2.0), (-SWORD_U[0], SWORD_U[1])),
           'side': ((-58.0, 0.0), (-0.42, -0.91))}


def link_hilt(p, hv, sp, hdx, hy):
    """Drawn after his head (a head prop), so the hilt shows over the cap's tail as in ref 03; its guard sits on the
    shoulder line, so it reads as coming from behind him."""
    if hv in HILT_AT:
        m, u = HILT_AT[hv]
        kokiri_hilt(p, m, u)


def kid_torso_view(img, p, sp, view, seated=False):
    """Link turned (the wall shot side on; the opening shot from behind): the plain torso in his tunic, then the
    fringe, belt, chest strap and, from behind, the wooden shield on his back."""
    _torso_view(img, p, sp, view, seated)
    if sp.get('who') != 'link':
        return
    sw, bottom = sp['shoulders'], sp['bottom']
    if view == 'side':
        x0, x1 = -sw * 0.62, sw * 0.66
    else:
        x0, x1 = -sw * 1.0, sw * 1.0
    _fringe(p, x0 * 1.12, x1 * 1.12, bottom - 6, L_TUNIC, 7 if view == 'side' else 11)
    p.poly([(x0, 300), (x1, 300), (x1, 344), (x0, 344)], LEATHER, INK, 2.4)
    if view == 'side':
        p.ell(x1 - 10, 322, 14, 26, SILVER, INK, 2.0)
        p.poly([(x0 * 0.9, 20), (x1 * 0.7, 300), (x1 * 0.4, 300), (x0 * 0.9, 50)], LEATHER, INK, 2.0)
        kokiri_sheath(p, (x0 + 8, 30), (-0.06, -1.0), 330)                 # the sheath down his back, its tip under the shield
        # the shield seen from the side but turned a little to us (pass 3: edge-on read as no shield): its face shows
        # as a broad wooden slab standing off his back, planks, a rim and a sliver of the red mark
        sh = curve([(x0 + 4, 40), (x0 - 40, 52), (x0 - 64, 190), (x0 - 52, 320), (x0 - 22, 372), (x0 + 6, 340),
                    (x0 + 8, 190)], 3)
        p.poly(sh, WOOD, INK, 2.6)
        for k in (0.33, 0.66):
            p.line([(x0 + 4 - 52 * k, 50 + 6 * k), (x0 + 2 - 40 * k, 350 - 10 * k)], WOOD_D, 2.0)
        p.poly(curve([(x0 - 34, 150), (x0 - 12, 148), (x0 - 20, 250)], 2), (196, 60, 48), INK, 1.8)
        p.line([(x0 + 6, 40), (x0 + 8, 340)], WOOD_D, 3.0)            # its thickness, the edge nearest his back
    if view == 'back':                                                    # the wooden Kokiri shield on his back
        shield = curve([(-sw * 0.7, 40), (sw * 0.7, 40), (sw * 0.76, 200), (sw * 0.5, 330), (0, 380), (-sw * 0.5, 330),
                        (-sw * 0.76, 200)], 3)
        p.poly([(-sw * 0.5, 0), (sw * 0.7, 290), (sw * 0.6, 310), (-sw * 0.6, 14)], LEATHER, INK, 2.0)
        m, u = HILT_AT['back']
        kokiri_sheath(p, (m[0] + 6, m[1] + 14), u, 360)                   # the sheath across his back, tip at his right hip
        p.poly(shield, WOOD, INK, 2.6)
        for x in (-0.3, 0.0, 0.3):
            p.line([(sw * x, 50), (sw * x * 0.9, 360)], WOOD_D, 2.0)
        p.poly(curve([(-sw * 0.3, 140), (sw * 0.3, 140), (0, 260)], 2), (196, 60, 48), INK, 2.0)   # a plain red mark
    for x in np.linspace(x0 * 0.8, x1 * 0.8, 5):
        p.line([(x, 360), (x * 1.06, bottom - 20)], L_TUNIC_D, 1.6)


# ================================================================================================ sleeves and legs
def _sleeve_cap(p, sh, el, colour, length, width, fray=False, puff=False):
    end = (sh[0] + (el[0] - sh[0]) * length, sh[1] + (el[1] - sh[1]) * length)
    st = (sh[0] - (el[0] - sh[0]) * 0.18, sh[1] - (el[1] - sh[1]) * 0.18)
    if puff:
        mx, my = (st[0] + end[0]) / 2, (st[1] + end[1]) / 2
        ang = math.atan2(end[1] - st[1], end[0] - st[0])
        p.ell(mx, my, math.hypot(end[0] - st[0], end[1] - st[1]) / 2 + 6, width * 1.2, colour, INK, 2.4, rot=ang)
        return
    dx, dy = end[0] - st[0], end[1] - st[1]
    n = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / n * width, dx / n * width
    ux, uy = dx / n, dy / n
    edge = []
    if fray:                                                     # a frayed cuff of rough points (Link, ref 03)
        for i in range(7):
            u = -1 + 2 * i / 6
            d = 16 if i % 2 else 2
            edge.append((end[0] + nx * u + ux * d, end[1] + ny * u + uy * d))
    else:
        edge = [(end[0] + nx, end[1] + ny), (end[0] - nx, end[1] - ny)]
    p.poly([(st[0] + nx, st[1] + ny)] + edge + [(st[0] - nx, st[1] - ny)], colour, INK, 2.4)


def _arm(p, j2, side, sp, shape=None):
    """Sleeves: Link's short frayed sleeve, Malon's puffed blue one, Zelda's puff over a long sleeve; Ruto's forearm
    fins. Everyone else (the gunman) passes straight through."""
    kind = sp.get('sleeves')
    if not kind or V.PROBE:
        return _ARM(p, j2, side, sp, shape)
    sh, el, wr = j2['sh' + side], j2['el' + side], j2['wr' + side]
    if kind == 'bare' and sp.get('who') == 'ruto':                # her forearm fins, under the arm's edge
        _ruto_arm_fin(p, el, wr, side)
    if kind in ('short', 'puff_short', 'bare'):
        _ARM(p, j2, side, dict(sp, sleeve=sp['skin'], jacket=sp['skin']), shape)
    else:
        _ARM(p, j2, side, sp, shape)
    if kind == 'short':
        _sleeve_cap(p, sh, el, sp['sleeve_c'], 0.62, 36, fray=sp.get('fray', False))
    elif kind in ('puff_short', 'puff_long'):
        _sleeve_cap(p, sh, el, sp['sleeve_c'], 0.66, 38, puff=True)


def _ruto_arm_fin(p, el, wr, side):
    """A fin rooted along the outer edge of Ruto's forearm, hanging out and down from it (ref 07; pass 1: the old
    ones floated off the arm). Drawn before the arm, so the arm overlaps its root."""
    dx, dy = wr[0] - el[0], wr[1] - el[1]
    n = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / n, dx / n
    out = -1 if side == 'L' else 1
    if nx * out < 0:
        nx, ny = -nx, -ny
    at = lambda u, k=0.0: (el[0] + dx * u + nx * k, el[1] + dy * u + ny * k)
    b0, b1 = at(0.12, 6), at(0.78, 6)
    tip = (at(0.3)[0] + nx * 70 + out * 20, at(0.3)[1] + ny * 70 + 90)
    fin = curve([b0, b1, (at(0.7)[0] + nx * 40, at(0.7)[1] + ny * 40 + 30), tip, (at(0.1)[0] + nx * 30, at(0.1)[1] + ny * 30 + 20)], 4)
    p.poly(fin, R_FIN, INK, 2.2)
    p.line(open_curve([at(0.45, 10), (tip[0] * 0.6 + at(0.45)[0] * 0.4, tip[1] * 0.6 + at(0.45)[1] * 0.4)], 3), R_FIN_D, 1.8)


def _leg(p, j, side, yaw, sp):
    _LEG(p, j, side, yaw, sp)
    if sp.get('boot_cuff'):                                       # boots with a folded tan cuff below the knee (ref 03)
        knee3, foot3 = V.knee_of(j, side), j['foot' + side]
        knee, foot = V.project(knee3, yaw)[0], V.project(foot3, yaw)[0]
        at = lambda u: (knee[0] + (foot[0] - knee[0]) * u, knee[1] + (foot[1] - knee[1]) * u)
        V.tube(p, [at(0.14), foot], [34, 29], sp['shoe'])          # boots to just under the knee: less bare leg
        c = at(0.14)
        p.poly(curve([(c[0] - 40, c[1] - 6), (c[0] + 40, c[1] - 6), (c[0] + 36, c[1] + 26), (c[0] - 36, c[1] + 26)], 2),
               sp['boot_cuff'], INK, 2.2)


# ================================================================================================ props
def _hand_at(j2, side, extra=14):
    el, wr = j2['el' + side], j2['wr' + side]
    dx, dy = wr[0] - el[0], wr[1] - el[1]
    n = math.hypot(dx, dy) or 1.0
    return (wr[0] + dx / n * extra, wr[1] + dy / n * extra)


def milk_bottle(side='R'):
    """Malon's milk bottle held out (Decision 11): a plain glass bottle of milk, a blue cap and a plain cow-patch
    label (no real brand), the hand over its middle."""
    def draw(p, j2):
        cx, cy = _hand_at(j2, side, 10)
        p.poly(curve([(cx - 34, cy - 40), (cx - 34, cy + 70), (cx - 26, cy + 80), (cx + 26, cy + 80), (cx + 34, cy + 70),
                      (cx + 34, cy - 40), (cx + 16, cy - 76), (cx + 16, cy - 110), (cx - 16, cy - 110), (cx - 16, cy - 76)], 2),
               (248, 248, 244), INK, 2.4)
        p.poly([(cx - 18, cy - 112), (cx + 18, cy - 112), (cx + 18, cy - 130), (cx - 18, cy - 130)], (80, 120, 196), INK, 2.0)
        p.poly([(cx - 34, cy - 10), (cx + 34, cy - 10), (cx + 34, cy + 40), (cx - 34, cy + 40)], (214, 150, 90), INK, 1.8)
        for ox, oy in ((-16, 4), (12, 22)):
            p.ell(cx + ox, cy + oy, 9, 6, (60, 40, 30), None)
        p.line([(cx - 24, cy - 70), (cx - 24, cy - 20)], (255, 255, 255), 3)
    draw.held = True
    return draw


def ocarina(side='R', colour=WOOD):
    """Saria's wooden ocarina held at her chest (ref 16): a fat teardrop with a mouthpiece and finger holes."""
    def draw(p, j2):
        hx_, cy = _hand_at(j2, side, 4)                  # her hand holds only its round end; the rest, with its
        k = 1.3                                          # holes and mouthpiece, shows clear of the hand (pass 2:
        cx = hx_ - 58 * k                                # it hid under the hand as a blob)
        p.poly(curve([(cx - 50 * k, cy), (cx - 20 * k, cy - 30 * k), (cx + 30 * k, cy - 26 * k), (cx + 50 * k, cy),
                      (cx + 30 * k, cy + 26 * k), (cx - 20 * k, cy + 30 * k)], 4), colour, INK, 2.6)
        p.poly([(cx - 46 * k, cy - 8 * k), (cx - 72 * k, cy - 10 * k), (cx - 72 * k, cy + 10 * k), (cx - 46 * k, cy + 8 * k)],
               dk(colour, 0.8), INK, 2.2)                # the mouthpiece points away from the hand
        p.line(open_curve([(cx - 30 * k, cy - 18 * k), (cx + 10 * k, cy - 22 * k), (cx + 34 * k, cy - 14 * k)], 4),
               B.lt(colour, 1.25) if hasattr(B, 'lt') else (196, 150, 98), 3.0)   # a carved highlight
        for ox, oy in ((-24, -6), (-4, -10), (16, -6), (-12, 12)):
            p.ell(cx + ox * k, cy + oy * k, 5.5, 5.5, INK, None)
    draw.held = True
    return draw


# ================================================================================================ the gunman
GUN_VEST, GUN_VEST_D = (62, 64, 66), (40, 42, 44)
GUN_CAMO, GUN_CAMO_D = (108, 106, 86), (78, 78, 62)
GUN_HELM = (70, 74, 70)
GUN_JACKET = (92, 96, 84)


def vest(p, view, sp):
    """A grey-black plate carrier with pouches over the olive jacket (refs 17, 18), in the torso's own frame."""
    sw = sp['shoulders']
    if view in ('front', 'back'):
        x0, x1 = -sw * 0.82, sw * 0.82
    elif view == 'side':
        x0, x1 = -sw * 0.56, sw * 0.62
    else:
        x0, x1 = -sw * 0.86, sw * 0.7
    p.poly(curve([(x0, 30), (x0 + 40, 10), (x1 - 40, 10), (x1, 30), (x1 + 6, 380), (x0 - 6, 380)], 2), GUN_VEST, INK, 2.6)
    if view in ('front', 'three'):
        for k in range(3):                                         # the magazine pouches across the front
            x = x0 + 30 + k * (x1 - x0 - 60) / 2.0 - 30
            p.poly([(x, 250), (x + 60, 250), (x + 60, 370), (x, 370)], GUN_VEST_D, INK, 2.0)
            p.line([(x, 280), (x + 60, 280)], INK, 1.6)
        for y in (110, 150, 190):                                  # the webbing loops
            p.line([(x0 + 20, y), (x1 - 20, y)], GUN_VEST_D, 2.4)
        p.poly([(x1 - 90, 60), (x1 - 30, 60), (x1 - 30, 100), (x1 - 90, 100)], (150, 140, 110), INK, 1.6)   # a plain patch
    if view == 'side':
        p.poly([(x1 - 10, 230), (x1 + 34, 230), (x1 + 34, 360), (x1 - 10, 360)], GUN_VEST_D, INK, 2.0)


def gun_mask(p, view, sp, hx, hy):
    """His full-face mask (ref 18): the Patriot's balaclava shape but smooth, with no knit ribs, and a black
    respirator over the mouth and chin with a round filter (pass 2: the ribbed knit and jutting chin read as a beard
    side on)."""
    ribs = P3._ribs
    P3._ribs = lambda *a, **k: None
    try:
        P3.balaclava(p, view, sp, hx, hy)
    finally:
        P3._ribs = ribs
    rc, fc = (52, 54, 58), (84, 88, 92)
    if view == 'side':
        p.poly(curve([(hx + 30, hy + 22), (hx + 84, hy + 26), (hx + 100, hy + 56), (hx + 84, hy + 96), (hx + 40, hy + 104),
                      (hx + 22, hy + 70)], 4), rc, INK, 2.4)
        p.ell(hx + 92, hy + 62, 16, 26, fc, INK, 2.2)                     # the filter, side on
        p.ell(hx + 96, hy + 62, 6, 12, rc, None)
    elif view in ('front', 'three'):
        fx = hx + (0.4 * sp.get('hw', 76) if view == 'three' else 0.0)
        p.poly(curve([(fx - 40, hy + 26), (fx + 40, hy + 26), (fx + 50, hy + 70), (fx + 24, hy + 104), (fx - 24, hy + 104),
                      (fx - 50, hy + 70)], 4), rc, INK, 2.4)
        p.ell(fx, hy + 70, 22, 22, fc, INK, 2.2)                           # the round filter at the front
        p.ell(fx, hy + 70, 9, 9, rc, None)


def gun_helmet(p, view, sp, hx, hy):
    """A dark grey combat helmet over the balaclava, with goggles pushed up on its front (ref 18)."""
    hw, hh = sp['hw'], sp['hh']
    if view == 'side':
        dome = curve([(hx - hw * 1.06, hy - 10), (hx - hw * 0.96, hy - hh * 0.8), (hx - hw * 0.2, hy - hh * 1.22),
                      (hx + hw * 0.7, hy - hh * 1.06), (hx + hw * 1.04, hy - hh * 0.5), (hx + hw * 1.1, hy - hh * 0.36),
                      (hx - hw * 0.2, hy - hh * 0.3), (hx - hw * 0.9, hy + 6)], 4)
        p.poly(dome, GUN_HELM, INK, 2.8)
        p.ell(hx + hw * 0.66, hy - hh * 0.8, hw * 0.24, hh * 0.15, (40, 40, 44), INK, 2.0, rot=0.5)   # the goggles
        p.ell(hx + hw * 0.7, hy - hh * 0.8, hw * 0.14, hh * 0.09, (120, 150, 160), None, rot=0.5)     # on the helmet,
        p.line([(hx - hw * 0.6, hy - hh * 0.6), (hx + hw * 0.5, hy - hh * 0.8)], (40, 40, 44), 5)        # not a peak
        return
    dome = curve([(hx - hw * 1.16, hy - hh * 0.2), (hx - hw * 1.06, hy - hh * 0.86), (hx - hw * 0.5, hy - hh * 1.24),
                  (hx + hw * 0.5, hy - hh * 1.24), (hx + hw * 1.06, hy - hh * 0.86), (hx + hw * 1.16, hy - hh * 0.2),
                  (hx + hw * 0.9, hy - hh * 0.3), (hx, hy - hh * 0.5), (hx - hw * 0.9, hy - hh * 0.3)], 4)
    p.poly(dome, GUN_HELM, INK, 2.8)
    if view in ('front', 'three'):
        for sgn in (-1, 1):                                        # the goggles pushed up on the helmet
            p.ell(hx + sgn * hw * 0.38, hy - hh * 0.8, hw * 0.3, hh * 0.18, (40, 40, 44), INK, 2.2)
            p.ell(hx + sgn * hw * 0.38, hy - hh * 0.8, hw * 0.2, hh * 0.11, (120, 150, 160), None)
        p.line([(hx - hw * 0.1, hy - hh * 0.8), (hx + hw * 0.1, hy - hh * 0.8)], (40, 40, 44), 5)


def rifle(side='R'):
    """The gunman's black rifle (ref 17): a long barrel, a scope on top, a long curved magazine, a stock; held across
    him at the ready, pointing to his left (screen right) into the trees. Drawn from the near hand along +x."""
    def draw(p, j2):
        cx, cy = _hand_at(j2, side, 14)
        g = (34, 34, 38)
        p.poly([(cx - 190, cy - 20), (cx - 40, cy - 34), (cx - 40, cy + 18), (cx - 130, cy + 36), (cx - 196, cy + 96),
                (cx - 218, cy + 60)], (44, 42, 40), INK, 2.4)                     # the stock, its butt dropping into
                                                                                  # the shoulder pocket
        p.poly([(cx - 50, cy - 36), (cx + 160, cy - 36), (cx + 160, cy + 6), (cx - 50, cy + 10)], g, INK, 2.4)  # receiver
        p.poly([(cx + 160, cy - 26), (cx + 330, cy - 26), (cx + 330, cy - 10), (cx + 160, cy - 10)], g, INK, 2.2)  # barrel
        p.poly([(cx + 330, cy - 30), (cx + 356, cy - 30), (cx + 356, cy - 6), (cx + 330, cy - 6)], g, INK, 2.0)   # muzzle
        p.poly(curve([(cx + 40, cy + 6), (cx + 86, cy + 6), (cx + 96, cy + 110), (cx + 60, cy + 116)], 2), g, INK, 2.2)  # magazine
        p.poly([(cx - 10, cy - 70), (cx + 110, cy - 70), (cx + 110, cy - 44), (cx - 10, cy - 44)], (52, 52, 56), INK, 2.0)  # scope
        p.ell(cx + 110, cy - 57, 8, 15, (120, 170, 190), INK, 1.6)
        p.poly([(cx + 20, cy - 44), (cx + 30, cy - 36), (cx + 70, cy - 36), (cx + 80, cy - 44)], g, INK, 1.6)
    draw.held = True
    return draw


# ================================================================================================ the people
KID = dict(skin=KID_SKIN, hw=124, hh=138, head_dy=-22, shoulders=118, chin=1.08, outfit='custom', full=True, pose='custom',
           glove=KID_SKIN, shoe=BOOT, iris=BLUE_EYE, mouth='rest')
LINK = dict(KID, who='link', name='Link', hair_c=L_HAIR, jacket=L_TUNIC, sleeve=L_SHIRT, sleeves='short',
            sleeve_c=L_SHIRT, fray=True, trousers=KID_SKIN, bottom=600, boot_cuff=BOOT_CUFF, height=1.22)
ZELDA = dict(KID, who='zelda', name='Zelda', hair_c=Z_HAIR, iris=GREEN_EYE, jacket=Z_SLEEVE, sleeve=Z_SLEEVE,
             sleeves='puff_long', sleeve_c=Z_SLEEVE, trousers=Z_SKIRT, shoe=(120, 90, 140), bottom=900, lashes=True,
             height=1.2)
MALON = dict(KID, who='malon', name='Malon', hair_c=M_HAIR, jacket=M_BLOUSE, sleeve=M_SLEEVE, sleeves='puff_short',
             sleeve_c=M_SLEEVE, trousers=M_SKIRT, shoe=(96, 62, 40), bottom=880, lashes=True, height=1.18,
             ears=False)
SARIA = dict(KID, who='saria', name='Saria', hair_c=S_HAIR, jacket=S_TUNIC, sleeve=S_TOP, trousers=KID_SKIN,
             shoe=(90, 66, 44), boot_cuff=(70, 110, 56), bottom=520, lashes=True, height=1.2)
RUTO = dict(KID, who='ruto', name='Ruto', skin=R_SKIN, glove=R_SKIN, hair_c=R_FIN, iris=PURPLE_EYE, jacket=R_SKIN,
            sleeve=R_SKIN, sleeves='bare', trousers=R_SKIN, shoe=R_SKIN, bottom=500, lashes=True, ears=False,
            brow_c=(120, 140, 150), lip_c=(150, 120, 170), height=1.22,
            head_dy=-2)       # her head sits lower on a short thick neck (pass 2: a stalk neck)
GUNMAN = dict(P3.PATRIOT, name='Gunman', who='gunman', patches=False, belly=False, jacket=GUN_JACKET,
              sleeve=GUN_JACKET, trousers=GUN_CAMO, shoe=(30, 28, 26), glove=(36, 36, 38), height=1.8,
              brows='fierce', brow_w=5.4, lid=6)    # an aggressive glare: brows pulled down hard, heavy lids (Sam)
CAST = {'link': LINK, 'zelda': ZELDA, 'malon': MALON, 'saria': SARIA, 'ruto': RUTO, 'gunman': GUNMAN}
KIDS = ('link', 'zelda', 'malon', 'saria', 'ruto')


def _drawn_height(sp):
    """The drawing's height in person units: soles at 928 up to the top of the head (or headgear)."""
    top = -150 + sp.get('head_dy', 0) - sp.get('hh', 90) * {'ruto': 1.44, 'link': 1.46}.get(sp.get('who'), 1.1)
    return 928 - top


def scale_for(sp, s):
    """Scale s is for our standard 1.75 m adult; each of the cast is drawn at their own height."""
    adult = 928 + 150 + 92 * 1.06
    return s * (sp.get('height', 1.75) / 1.75) * adult / _drawn_height(sp)


# ------------------------------------------------------------------------------------------------ the hooks
_head, _torso, _head_view, _torso_view = B.head, B.torso, V.head_view, V.torso_view
_ARM, _LEG, _HAND = V.arm, V.leg, V.hand


def head(img, p, sp, t, hx, hy):
    if sp.get('who') in KIDS:
        return kid_head(img, p, sp, t, hx, hy)
    return _head(img, p, sp, t, hx, hy)


def torso(img, p, sp, t):
    if sp.get('who') == 'malon':
        malon_long_hair(p, sp)
    if sp.get('who') in KIDS:
        return TORSO[sp['who']](img, p, sp)
    return _torso(img, p, sp, t)


def head_view(img, p, sp, t, view, hx=0.0, hy=-150.0):
    who = sp.get('who')
    if who in KIDS:
        if view == 'front':
            return kid_head(img, p, sp, t, hx, hy)
        if who == 'link' and view == 'side':
            return link_head_side(img, p, sp, t, hx, hy)
        if who == 'link' and view == 'back':
            return link_head_back(img, p, sp, t, hx, hy)
        raise ValueError(f'{who} has no {view} view built (rule 38: only the views the shots use)')
    return _head_view(img, p, sp, t, view, hx, hy)


def torso_view(img, p, sp, view, seated=False):
    if sp.get('who') in KIDS:
        return kid_torso_view(img, p, sp, view, seated)
    return _torso_view(img, p, sp, view, seated)


KID_HAND_R = 36        # the house circle hand, sized to a child's big head (26 on an adult with a 92 head; pass 1 P6:
                       # at 26 the children's hands read as dots)


def hand(p, j2, side, sp, shape):
    """The children's hands: the house circle, at a child's size against the head; a point keeps the house finger."""
    if sp.get('who') not in KIDS or V.PROBE or shape in ('point', 'point_up', 'none'):
        return _HAND(p, j2, side, sp, shape)
    el, wr = j2['el' + side], j2['wr' + side]
    dx, dy = wr[0] - el[0], wr[1] - el[1]
    n = math.hypot(dx, dy) or 1.0
    cx, cy = wr[0] + dx / n * 20, wr[1] + dy / n * 20
    p.ell(cx, cy, KID_HAND_R, KID_HAND_R * 0.94, sp.get('glove', sp['skin']), INK, 2.6)


B.head, B.torso, V.head_view, V.torso_view = head, torso, head_view, torso_view
V.arm, V.leg, V.hand = _arm, _leg, hand


def gunman_dress(j):
    j['body_props'] = [P3.patriot_jacket, lambda p, view, sp: vest(p, view, sp)] + j.get('body_props', [])
    j['head_props'] = [gun_mask, gun_helmet] + j.get('head_props', [])
    j['_dressed'] = True
    return j


def person(img, cam, x, y, s, sp, t=0.0, yaw=0, j=None, head_yaw=None):
    """Draw one of the cast at their own height (s is the scale for a 1.75 m adult; x, y the neck base)."""
    j = j or V.standing(sp)
    if sp.get('who') == 'gunman' and not j.get('_dressed'):
        gunman_dress(j)
    if sp.get('who') == 'link' and link_hilt not in j.get('head_props', []):
        j['head_props'] = j.get('head_props', []) + [link_hilt]       # the Kokiri Sword's hilt over his left shoulder
    return V.person(img, cam, x, y, scale_for(sp, s), dict(sp), t, yaw, j, head_yaw)


def poses(who):
    """Each child's line-up pose (Decision 11) and Link's shrug; the gunman's rifle into the trees (line 5)."""
    sp = CAST[who]
    sw = sp['shoulders']
    if who == 'zelda':                                      # hands clasped in front, low
        j = V.standing(sp)
        V.arm_to(j, 'L', (-8.0, 330.0, 70.0), 'down', 'fist')
        V.arm_to(j, 'R', (8.0, 330.0, 74.0), 'down', 'fist')
        return {'clasped': j}
    if who == 'malon':                                      # holding the milk bottle up in front of her chest
        j = V.standing(sp)                                  # to us, hopeful (pass 1: it sat at her waist)
        V.arm_to(j, 'R', (70.0, 170.0, 230.0), 'down', 'grip')
        j['props'] = [milk_bottle('R')]
        j['grip'], j['wrap'] = {'R'}, {'R'}                 # the bottle over her sleeve, her hand over the bottle
        j['_mood'] = 'hopeful'
        return {'bottle': j}
    if who == 'saria':                                      # nonchalant: hand on hip, elbow out; ocarina at her chest
        j = V.standing(sp)
        V.arm_to(j, 'L', (-(sw + 6), 300.0, 0.0), 'out')
        V.arm_to(j, 'R', (40.0, 190.0, 120.0), 'down', 'grip')
        j['props'] = [ocarina('R')]
        j['grip'] = {'R'}
        j['footL'] = (-70, V.ANKLE_Y - 6, 30.0)
        j['_mood'] = 'smug'
        return {'nonchalant': j}
    if who == 'ruto':                                       # vain: hands on hips, weight on one leg, chin up
        j = moves.pose(sp, 'hips')
        for s_, sg in (('L', -1), ('R', 1)):
            V.arm_to(j, s_, (sg * (sw * 0.72), 345.0, 0.0), 'out')   # on the edge of her waist, not over the chest
        x, y, z = j['shR']                                  # (pass 2: arms inside chest); one shoulder cocked up,
        j['shR'] = (x, y - 16, z)                           # weight on the right foot under her, the left leg out
        j['footR'] = (14, V.ANKLE_Y, 0.0)                   # to the side on its toe: a posed, vain stance (pass 2:
        j['footL'] = (-118, V.ANKLE_Y - 26, 40.0)           # weight even)
        j['toeL'] = 14
        j['_mood'] = 'vain'
        return {'hips': j}
    if who == 'link':                                       # the shrug: shoulders up, elbows in at his sides, forearms
        j = V.standing(sp)                                  # out, palms up (pass 1: arms out wide read as a T-pose)
        for s_, sg in (('L', -1), ('R', 1)):
            x, y, z = j['sh' + s_]
            j['sh' + s_] = (x, y - 34, z)                  # pass 2: hands up at the chest and wide read "ta-da".
            V.arm_to(j, s_, (sg * (sw + 136), 205.0, 50.0), (0.5, 1.0, -0.2), 'palm')   # Now: elbows tucked in at
        j['head_dy'] = 14                                   # his waist, forearms out sideways at belt height, palms
        j['_mood'] = 'unsure'                               # up, head sunk between raised shoulders
        j['_mood'] = 'unsure'
        return {'shrug': j}
    if who == 'gunman':                                     # aiming into the trees (ref 17; line 5): side on, the
        j = V.standing(sp)                                  # rifle up at the shoulder, cheek down to it, looking
        V.arm_to(j, 'R', (-20.0, -48.0, 170.0), (0.0, 1.0, -0.6), 'grip')   # along the scope (pass 1: rifle low,
        V.arm_to(j, 'L', (30.0, -54.0, 340.0), 'down', 'grip')  # eyes at us). Pass 2: the near arm (R in this view)
        j['props'] = [rifle('R')]                           # runs to the trigger hand, elbow down; the rifle raised so the
        j['grip'] = {'L', 'R'}                              # scope is at his eye, the stock's butt dropping into his
        j['head_dy'] = 40                                   # shoulder; his head down onto the stock
        j['_yaw'] = 90
        return {'aiming': j}
    return {}


# ================================================================================================ the sheets
VIEWS_NEEDED = {'link': (0, 90, 180), 'gunman': (0, 90)}   # rule 38: only the views the shots use
REFS = {'link': ['03-link.jpg', '04-link.jpg', '01-kg.jpg'], 'zelda': ['09-zelda.jpg', '10-zelda.jpg'],
        'malon': ['13-malon.jpg', '14-malon.jpg'], 'saria': ['15-saria.jpg', '16-saria.jpg'],
        'ruto': ['07-ruto.jpg', '08-ruto.jpg'], 'gunman': ['17-soldiers.jpg', '18-soldiers.jpg']}
FACES_NEEDED = {'link': ('neutral', 'unsure', 'sceptical', 'aghast', 'wince', 'horror', 'deadpan', 'terrified'),
                'zelda': ('neutral', 'down'), 'malon': ('neutral', 'hopeful'), 'saria': ('smug', 'wink'),
                'ruto': ('neutral', 'vain'), 'gunman': ()}


def _font(n):
    return ImageFont.truetype(os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf'), n)


def _tile(draw_fn, w=600, h=1100, bg=(236, 232, 224)):
    lay = Image.new('RGBA', (1080, 1920), bg + (255,))
    draw_fn(lay)
    return lay


def figure_tile(who, yaw=0, j=None, mood=None, s=1.0, crop=None):
    sp = dict(CAST[who])
    if mood:
        sp['mood'] = mood
    cam = B.Cam(1.0, 540, 960)
    lay = Image.new('RGBA', (1080, 1920), (236, 232, 224, 255))
    import copy
    person(lay, cam, 540, 700, s, sp, 0.0, yaw, copy.deepcopy(j) if j else None)
    if crop:
        return lay.crop(crop)
    bg = np.array([236, 232, 224])                                   # crop to the drawing, a margin round it (Link 7)
    a = np.abs(np.asarray(lay.convert('RGB')).astype(int) - bg).sum(2) > 12
    ys, xs = np.where(a)
    m = 40
    return lay.crop((max(0, xs.min() - m), max(0, ys.min() - m), min(1080, xs.max() + m), min(1920, ys.max() + m)))


def face_tile(who, mood, yaw=0, mouth=None):
    sp = dict(CAST[who], mood=mood)
    if mouth:
        sp['mouth'] = mouth
    cam = B.Cam(1.0, 540, 960)
    lay = Image.new('RGBA', (1080, 1920), (236, 232, 224, 255))
    person(lay, cam, 540, 1000, 2.0, sp, 0.0, yaw)
    return lay.crop((140, 260, 940, 1160)).resize((400, 450))


def alone(who, out):
    """One character alone at full size beside every reference of it (rule 89): each view it needs, its poses, its
    faces, and a 1.75 m adult outline for scale."""
    B.SS = 1
    tiles = [(f'{who} {("front", "", "", "side", "", "", "back")[[0, 0, 0, 90, 0, 0, 180].index(y)]}'.strip(),
              figure_tile(who, y)) for y in VIEWS_NEEDED.get(who, (0,))]
    for name, j in poses(who).items():
        tiles.append((name, figure_tile(who, j.get('_yaw', 0), j, j.get('_mood'))))
    refs = [Image.open(os.path.join(REF, f)).convert('RGB') for f in REFS[who]]
    faces = [(m, face_tile(who, m)) for m in FACES_NEEDED.get(who, ())]
    th = max(t.height for _, t in tiles)
    row1 = sum(t.width for _, t in tiles) + 40 * len(tiles)
    refw = sum(int(r.width * 600 / r.height) for r in refs) + 30 * len(refs)
    W = max(row1, refw, 450 * len(faces)) + 60
    H = 80 + th + 60 + 660 + (560 if faces else 0)
    img = Image.new('RGB', (W, H), (250, 248, 244))
    d = ImageDraw.Draw(img)
    d.text((30, 20), f'{CAST[who]["name"]} (Remakes): drawn alone beside the references', font=_font(40), fill=(30, 30, 30))
    x = 30
    for name, t in tiles:
        img.paste(t.convert('RGB'), (x, 80))
        d.text((x + t.width // 2, 80 + t.height + 20), name, font=_font(28), fill=(40, 40, 40), anchor='mm')
        x += t.width + 40
    x, y = 30, 80 + th + 60
    for f, r in zip(REFS[who], refs):
        r = r.resize((int(r.width * 600 / r.height), 600))
        img.paste(r, (x, y))
        d.text((x + 6, y + 606), 'ref ' + f, font=_font(24), fill=(40, 40, 40))
        x += r.width + 30
    y += 660
    for i, (m, t) in enumerate(faces):
        img.paste(t.convert('RGB'), (30 + 450 * i, y))
        d.text((30 + 450 * i + 200, y + 470), m, font=_font(28), fill=(40, 40, 40), anchor='mm')
    img.save(out, quality=88)
    return out


def cast_sheet(out):
    """All nine at their true heights on one ground line (Link's front for scale), a metre ruler at the left, names
    and heights under them; Navi floats at Link's shoulder. The look Sam signs off before the shots are built."""
    import remakes_creatures as CR
    B.SS = 1
    W_, H_, G = 4250, 1900, 1640                                        # canvas, the ground line
    img = Image.new('RGBA', (W_, H_), (242, 238, 230, 255))
    cam = B.Cam(1.0, B.W / 2, B.H / 2)                                  # world units are canvas pixels
    d = ImageDraw.Draw(img)
    px_m = (928 + 150 + 92 * 1.06) / 1.75                               # pixels per metre at s = 1 (scale_for's adult)
    for k in range(0, 5):                                               # the ruler: a line every half metre
        y = G - k * 0.5 * px_m
        d.line([(110, y), (W_ - 40, y)], fill=(222, 216, 204), width=2)
        d.text((40, y - 16), f'{k * 0.5:.1f} m', font=_font(26), fill=(120, 112, 100))
    d.line([(110, G), (W_ - 40, G)], fill=(150, 140, 124), width=4)
    labels = []
    gx = 300                                                            # the gunman (1.8 m), front
    sp = CAST['gunman']
    person(img, cam, gx, G - 928 * scale_for(sp, 1.0), 1.0, sp)
    labels.append((gx, f'gunman {sp["height"]:.2f} m'))
    kx = 1060                                                           # KG, standing, wings folded, kindly
    CR.kg(img, cam, kx, G - 328, 1.0, mood='kindly', tail=0.55)
    labels.append((kx, 'Kaepora Gaebora'))
    gox = 1990                                                          # the Goron in his dress
    CR.goron(img, cam, gox, G, 1.0)
    labels.append((gox, 'Goron'))
    for i, who in enumerate(('link', 'zelda', 'malon', 'saria', 'ruto')):
        x = 2700 + i * 340
        sp = CAST[who]
        person(img, cam, x, G - 928 * scale_for(sp, 1.0), 1.0, sp)
        labels.append((x, f'{CAST[who]["name"]} {sp["height"]:.2f} m'))
    CR.navi(img, cam, 2700 + 170, G - 1.05 * px_m, 1.0)                 # Navi at Link's shoulder
    labels.append((2700 + 170, 'Navi'))
    d = ImageDraw.Draw(img)
    for x, name in labels:
        d.text((x, G + 50 + (40 if name == 'Navi' else 0)), name, font=_font(30), fill=(40, 40, 40), anchor='mm')
    d.text((40, 30), 'Remakes: the cast at true heights', font=_font(44), fill=(30, 30, 30))
    img.convert('RGB').save(out, quality=88)
    return out


if __name__ == '__main__':
    if sys.argv[1] == 'alone':
        print(alone(sys.argv[2], sys.argv[3]))
    elif sys.argv[1] == 'castsheet':
        print(cast_sheet(sys.argv[2]))
