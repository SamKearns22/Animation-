#!/usr/bin/env python3
"""MAP  focus (front-on focus C2, Sam: "Y to all", 19 Nov; notes/proposals/front-on-focus.md, Final version).
Where a front-on person is looking, shown the BoJack way (notes/proposals/front-on-focus/bojack-sheet.jpg) on their
own front face, so glasses, hair, beards and piercings keep their front design. One setting in the person's spec:

    sp['focus']        -1 (looking to screen left) .. 0 (straight out) .. +1 (screen right)
    sp['focus_tilt']   optional: the head's tilt in degrees (default 6 x focus: the top leans toward the look)
    sp['focus_turn']   optional: 0..1, how much of the shallow turn (default 1: about 15 degrees at full focus)
    sp['focus_eyes']   optional: the pupils' own focus (the moves kit's `keys focus` sets it 0.17 s ahead: eyes lead)

It MOVES WHOLE PIECES, never warps pixels: both pupils toward the corner; the eyes, brows, glasses, nose, mouth and
the lines round them slide toward the look inside the unchanged outline (the nose and mouth further than the eyes,
the near eye a touch more than the far one: a real head turned about 15 degrees, measured off a sphere, at about 85%: hunt 1 (19 Nov) could not read
the direction at phone size at 60%);
the nose tip turned further than its bridge; the brows uneven (the brow on the look's side up, the other down); the
far ear tucked a little behind the head, the near one out; the whole head tilted up to 6 degrees round the chin.
Hair, ears' shape, the outline, beards' jaw, stubble stay where the front head draws them (tilted with the head).
focus 0 with no tilt hands back the head's own Face: every finished film draws exactly as before (kittest
focus_front_heads holds Andy, Kemi, a Milburn frame and a Protest Tiers frame pixel for pixel).

Used by facehouse._head (the house head) and people_parts._front_head (the people kit's invented faces):
    F = focus.Focus(face, sp, L)      then draw each part through F.whole / F.eyes / F.brows / F.lens / F.nose /
                                       F.mouth / F.lines / F.ears / F.marks (piercings), and give the eyes focus.look(sp)
    python3 source/focus.py sheet OUT.jpg     Andy and Kemi at focus -1, 0, +1, phone size, and one close-up

Map: amounts 45 | Piece 60 | Focus 90 | sheet 155
"""
import math
import os
import sys

TILT = 6.0            # degrees of head tilt at full focus
LOOK = 1.3            # the pupils' sideways look at full focus (traitors_cast.eye: 1 = into the corner)
# face units (shares of the face's height) each piece slides at full focus, near side / far side where it has two
EYES = (0.09, 0.075)
BROW_UP = (0.012, -0.03)  # (near, far: the look's side) brow heights: the look's side lifted, the other lowered
NOSE, TIP = 0.1, 0.05   # the bridge slides NOSE, the tip that much further
MOUTH = 0.1
LINES = 0.09
EARS = (0.015, -0.04)     # the near ear out, the far ear tucked behind the head
# These are the kept strength. Option 1 (1.7x these, 20 Nov) was refused by Sam: "the facial features have slid
# over so far that they no longer look human" (notes/proposals/front-on-focus/retirement-and-handover.md, chat 2b).


def amounts(sp):
    """(focus, tilt in degrees, turn) for a person's spec; all zero when they look straight out."""
    f = max(-1.0, min(1.0, float(sp.get('focus', 0.0) or 0.0)))
    tilt = float(sp.get('focus_tilt', TILT * f))
    turn = max(0.0, min(1.0, float(sp.get('focus_turn', 1.0))))
    return f, tilt, turn


def look(sp):
    """The eyes' sideways look with the focus added (the pupils lead)."""
    f = max(-1.0, min(1.0, float(sp.get('focus_eyes', amounts(sp)[0]) or 0.0)))   # the eyes may lead (acting.py)
    base = float(sp.get('look', 0.0) or 0.0)
    return max(-1.4, min(1.4, base + LOOK * f)) if f else base


class Piece:
    """A face mapper (f(u, v) -> pixels, f.pts) that slides one part of the face as a whole: du across, plus a
    per-side slide and lift (index 0 our left, u < 0; 1 our right) for parts drawn once a side (eyes, brows, lenses,
    ears), a tip(v) for the nose, and the head's tilt (rot). Points at or past `edge` (glasses' arms at the ears)
    stay on the head. Anything else (tq, hx, cx, top, x) is the head's own Face."""

    def __init__(self, base, du=0.0, side=(0.0, 0.0), lift=(0.0, 0.0), tip=None, edge=None, rot=None):
        self.base, self.du, self.side, self.lift, self.tip, self.edge, self.rot = base, du, side, lift, tip, edge, rot

    def __call__(self, u, v):
        if self.edge is not None and abs(u) >= self.edge:
            uu, vv = u, v
        else:
            i = 1 if u > 0 else 0
            uu = u + self.du + self.side[i] + (self.tip(v) if self.tip else 0.0)
            vv = v + self.lift[i]
        x, y = self.base(uu, vv)
        return self.rot(x, y) if self.rot else (x, y)

    def pts(self, uvs):
        return [self(u, v) for u, v in uvs]

    def __getattr__(self, k):
        return getattr(self.base, k)


class Focus:
    """The pieces of one front head, for one frame. Off (focus 0, no tilt): every piece IS the head's Face."""

    def __init__(self, base, sp, L, room=None):
        """room: how far (face units) the far side's eye, brow and lens may slide before the outermost of them
        (usually the glasses' far rim) would cross the face's outline; None for no limit."""
        f, tilt, turn = amounts(sp)
        self.f, self.tilt, self.on = f, tilt, bool(f or tilt)
        if not self.on:
            self.whole = self.eyes = self.brows = self.lens = self.nose = self.mouth = self.lines = self.ears = base
            self.marks = base
            return
        rot = None
        if tilt:
            px, py = base(0.0, 1.0)                          # round the chin: the head stays on its neck
            a = math.radians(tilt)
            c, s = math.cos(a), math.sin(a)

            def rot(x, y):
                dx, dy = x - px, y - py
                return px + dx * c - dy * s, py + dx * s + dy * c
        k = f * turn
        far = 1 if k > 0 else 0                              # the side the look is on (our right for +)
        near = 1 - far

        def two(pair):                                        # (near, far) amounts -> (our left, our right) slides
            out = [0.0, 0.0]
            fa = pair[1] * k if room is None else math.copysign(min(abs(pair[1] * k), max(0.0, room)), k)
            out[near], out[far] = pair[0] * k, fa             # the far rim stays inside the outline (Andy's glasses)
            return tuple(out)

        def lifts(pair):
            out = [0.0, 0.0]
            out[near], out[far] = pair[0] * abs(k), pair[1] * abs(k)
            return tuple(out)
        eye_y, nose_y = L['eye_y'], L['nose_y']
        span = max(nose_y - eye_y, 1e-3)
        edge = L['fw'] * 0.5
        self.whole = Piece(base, rot=rot)
        self.eyes = Piece(base, side=two(EYES), rot=rot)
        self.lens = Piece(base, side=two(EYES), edge=edge, rot=rot)
        self.brows = Piece(base, side=two(EYES), lift=lifts(BROW_UP), rot=rot)
        self.nose = Piece(base, du=NOSE * k, tip=lambda v: TIP * k * max(0.0, min(1.0, (v - eye_y) / span)), rot=rot)
        self.mouth = Piece(base, du=MOUTH * k, rot=rot)
        self.lines = Piece(base, du=LINES * k, rot=rot)
        ears = [0.0, 0.0]                                     # the far ear in (toward the middle), the near one out
        ears[far], ears[near] = -math.copysign(EARS[1], k) * abs(k), -math.copysign(EARS[0], k) * abs(k)
        self.ears = Piece(base, side=tuple(ears), rot=rot)
        self.marks = ByHeight(self, eye_y + 0.06, nose_y + 0.01)   # piercings: brow, nose or lip, by height


class ByHeight:
    """Small marks drawn anywhere on the face (piercings): each goes with the piece at its height."""

    def __init__(self, F, brow_below, nose_below):
        self.F, self.b, self.n = F, brow_below, nose_below

    def __call__(self, u, v):
        F = self.F
        return (F.brows if v < self.b else F.nose if v < self.n else F.mouth)(u, v)

    def pts(self, uvs):
        return [self(u, v) for u, v in uvs]

    def __getattr__(self, k):
        return getattr(self.F.whole, k)


# ------------------------------------------------------------------------------------------------ the test sheet
BOX = (340, 150, 740, 640)    # head and shoulders of someone standing in a medium shot (1080 x 1920 frame)


def _cast(people_file, who):
    import people as PK
    from satire_style import install_circle_hands
    import people_parts as PP
    install_circle_hands(PP.B)
    got = PK.load(people_file)
    return PK.install({w: got[w] for w in who}), PP.B, PP.V


def bust(sp, focus, B, V, w=390, extra=None):
    """One person in a medium shot, drawn the way films draw them, at this focus; the head-and-shoulders box,
    w pixels wide."""
    from PIL import Image
    B.SS = 1
    cam = B.Cam(1.0, 540, 960)
    s = 0.5 * sp['height'] / 1.75
    tile = Image.new('RGBA', (1080, 1920), (236, 232, 226, 255))
    V.person(tile, cam, 540, 840 - 928 * s, s, dict(sp, focus=focus, **(extra or {})), 0.0, 0.0, V.standing(sp))
    im = tile.crop(BOX).convert('RGB')
    return im.resize((w, int(w * im.height / im.width)), Image.LANCZOS)


def sheet(out, people_file='facetool', who=('andy', 'kemi')):
    """Each person at focus left, 0, right, at about the size a medium shot shows on a phone (the sheet is a
    phone's width), labelled; then one close-up of the first at 0 and right."""
    from PIL import Image, ImageDraw, ImageFont
    cast, B, V = _cast(people_file, who)
    font = ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'DejaVuSans-Bold.ttf'), 30)
    cols = ((-1.0, 'looking LEFT'), (0.0, 'straight (today)'), (1.0, 'looking RIGHT'))
    tw = 390
    rows = [[bust(cast[w], c, B, V, tw) for c, _ in cols] for w in who]
    th = rows[0][0].height
    big = [bust(cast[who[0]], c, B, V, 585) for c in (0.0, 1.0)]
    H = 60 + len(who) * (th + 50) + 50 + big[0].height
    img = Image.new('RGB', (3 * tw, H), (250, 248, 244))
    d = ImageDraw.Draw(img)
    for j, (_, lab) in enumerate(cols):
        d.text((j * tw + 12, 14), lab, font=font, fill=(20, 20, 20))
    y = 60
    for w, row in zip(who, rows):
        d.text((12, y), w.title(), font=font, fill=(120, 40, 30))
        y += 40
        for j, im in enumerate(row):
            img.paste(im, (j * tw, y))
        y += th + 10
    d.text((12, y + 6), f'Close-up: {who[0].title()} straight, then looking right', font=font, fill=(20, 20, 20))
    y += 50
    for j, im in enumerate(big):
        img.paste(im, (j * big[0].width, y))
    img.save(out, quality=88)
    return out


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        print(sheet(sys.argv[2]))
    else:
        print(__doc__)
