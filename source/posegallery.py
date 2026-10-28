#!/usr/bin/env python3
"""posegallery: poses drawn and tested once, from every view, then picked by films (film-quality-rules 42; the list
with notes is guides/pose-gallery.md). A film picks a pose from here; only a pose not in the gallery is built new,
listed in the plan, then added here once it passes.

    python3 source/posegallery.py [OUT.jpg] [--all] [--only NAME,NAME]

draws each gallery pose on a plain model from the front, three-quarter, side, three-quarter back and behind (the
side and three-quarter views facing right; facing left is the same drawing mirrored), runs the hand check (rule 41:
handcheck.py) on every drawing, and saves ONE labelled sheet (rule 48): a row per pose, OK or the fault under each
view. --all adds every other pose in moves.pose. It prints each pose's result, for the gallery's "tested" column.

Each pose is a function of the person's design (sp) returning views' joints, so it fits anyone's shoulders; the ones
here came from films (the source is noted) and are now the kit's.
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import burnham as B          # noqa: E402
import figure as F           # noqa: E402
import views as V            # noqa: E402
from ed import INK           # noqa: E402

MODEL = dict(name='Model', skin=(236, 196, 166), hair='crop', hair_c=(84, 62, 44), jacket=(64, 92, 132),
             sleeve=(64, 92, 132), trousers=(52, 54, 62), shoe=(30, 28, 30), hw=70, hh=90, jaw='round')
VIEWS = [(0, 'front'), (45, 'three-quarter'), (90, 'side'), (135, 'three-quarter back'), (180, 'behind')]


def _sw(sp):
    return sp.get('shoulders', 150)


# ------------------------------------------------------------------------------------------------ the poses
def arms_folded(sp):
    """Forearms level across the chest, the right over the left, hands tucked (moves.pose; hidden on purpose)."""
    import moves
    return moves.pose(sp, 'arms_folded')


def hands_up(sp):
    """Hands up (surrender, "don't shoot"): both palms up beside the head, elbows bent out and down."""
    j = V.standing(sp)
    for s, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, s, (sg * (_sw(sp) + 90), -180.0, 80.0), 'down', 'palm')    # wide and a little forward: seen side on
    j['head_dy'] = -4
    return j


def pointing(sp, target=None):
    """Pointing at something with the right hand, the left on the hip (moves.pose 'point')."""
    import moves
    return moves.pose(sp, 'point', target=target)


def binoculars(sp, lean=4.0):
    """Field binoculars to the eyes, a hand on each barrel, elbows out (Patriots 3's Loader, shot 2; hands moved out
    past the head after note 21, so they show from behind too)."""
    j = V.standing(sp)
    j['lean'] = lean
    for side, sg in (('L', -1), ('R', 1)):
        V.arm_to(j, side, (sg * 96.0, -120.0, 104.0), 'down', 'fist')
    j['face_props'] = [_binoculars(lean, sp)]
    return j


def _binoculars(lean, sp):
    """6x30 binoculars at the eyes: two barrels out from the face (end on from the front: two dark lenses); unseen
    from behind (the head hides them). The hands are the arms' own, at the barrels' outer sides."""
    def draw(p, j2):
        yaw = j2['yaw']
        if yaw in (135, 180):
            return
        tubes = []
        for sg in (-1, 1):
            a = V.project(V.leaned((sg * 34.0, -160.0, 70.0), lean), yaw)
            b = V.project(V.leaned((sg * 34.0, -166.0, 152.0), lean), yaw)
            tubes.append(((a[1] + b[1]) / 2, a[0], b[0]))
        tubes.sort()
        for _, a, b in tubes:
            dx, dy = b[0] - a[0], b[1] - a[1]
            n = math.hypot(dx, dy)
            if n < 20:
                p.ell(b[0], b[1], 21, 21, (30, 30, 32), INK, 2.0)
                p.ell(b[0], b[1], 13, 13, (60, 76, 92), INK, 1.4)
                continue
            nx, ny = -dy / n, dx / n
            p.poly([(a[0] + nx * 15, a[1] + ny * 15), (b[0] + nx * 19, b[1] + ny * 19), (b[0] - nx * 19, b[1] - ny * 19),
                    (a[0] - nx * 15, a[1] - ny * 15)], (36, 36, 38), INK, 2.0)
        for sd in 'LR':                                  # the hands over the barrels (in front of the face)
            V.hand(p, j2, sd, sp, 'fist')
    return draw


def salute(sp, k=1.0, steep=0.62, out=0.3):
    """The salute (Patriots 3, refs salute-1, -2): the right arm straight out, forward and up, the hand flat; k eases
    it up (0 down, 1 up) round the shoulder, never across the man beside him. `steep`: how far up."""
    j = V.standing(sp)
    sh = j['shR']
    reach = (F.UPPER + F.FORE) * 0.97 + F.HAND['palm']
    d1 = np.array([out, -steep, max(0.3, 1.0 - steep)])
    d1 /= np.linalg.norm(d1)
    d0 = np.array([min(0.25, out + 0.05), 0.95, 0.2])
    d0 /= np.linalg.norm(d0)
    w = math.acos(max(-1.0, min(1.0, float(d0 @ d1))))
    d = (math.sin((1 - k) * w) * d0 + math.sin(k * w) * d1) / math.sin(w)
    V.arm_to(j, 'R', tuple(np.array(sh) + d * reach * (0.92 + 0.08 * k)), 'out', 'palm')
    j['head_dy'] = -4 * k
    return j


def rifle(sp):
    """Hands on a gun: a rifle held across the body at port arms, the right hand at the grip by the hip, the left on
    the handguard by the shoulder (the hands over it, as the house draws held things)."""
    j = V.standing(sp)
    butt, muzzle = (150.0, 470.0, 60.0), (-150.0, -30.0, 120.0)
    V.arm_to(j, 'R', (90.0, 380.0, 90.0), 'down', 'fist')
    V.arm_to(j, 'L', (-80.0, 110.0, 108.0), 'down', 'fist')

    def gun(p, j2):
        yaw = j2['yaw']
        a, b = V.project(butt, yaw)[0], V.project(muzzle, yaw)[0]
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / n, dx / n
        p.poly([(a[0] + nx * 16, a[1] + ny * 16), (a[0] + dx * 0.35 + nx * 12, a[1] + dy * 0.35 + ny * 12),
                (b[0] + nx * 6, b[1] + ny * 6), (b[0] - nx * 6, b[1] - ny * 6),
                (a[0] + dx * 0.35 - nx * 12, a[1] + dy * 0.35 - ny * 12), (a[0] - nx * 16, a[1] - ny * 16)],
               (92, 64, 40), INK, 2.0)
        p.poly([(a[0] + dx * 0.45 + nx * 10, a[1] + dy * 0.45 + ny * 10), (a[0] + dx * 0.9 + nx * 6, a[1] + dy * 0.9 + ny * 6),
                (a[0] + dx * 0.9 - nx * 6, a[1] + dy * 0.9 - ny * 6), (a[0] + dx * 0.45 - nx * 10, a[1] + dy * 0.45 - ny * 10)],
               (46, 46, 50), INK, 1.8)
    gun.held = True
    j['props'] = [gun]
    j['grip'] = {'L', 'R'}
    return j


FLAPS = {   # Patriots 3's arms darting about (shot 7), after note 18: the hands at the sleeves' ends
    'up': {'L': (-300.0, -80.0, 50.0), 'R': (300.0, -80.0, 50.0)},
    'pat': {'L': (-290.0, 170.0, 70.0), 'R': (290.0, 170.0, 70.0)},
}


def flapping(sp, name='up'):
    """Flapping the arms ("keep it down!"): 'up' (hands high and wide) or 'pat' (patting the air down); key them in
    turn for the flap (Patriots 3, note 18: hands at the sleeves' ends, not folded back into them)."""
    j = V.standing(sp)
    for s in 'LR':
        V.arm_to(j, s, FLAPS[name][s], 'out', 'palm')
    return j


GALLERY = [   # (name, pose(sp) -> joints, where it came from)
    ('arms folded', arms_folded, 'moves.pose (hands tucked on purpose)'),
    ('hands up', hands_up, 'new, 28 Oct'),
    ('pointing', pointing, 'moves.pose'),
    ('binoculars', binoculars, 'Patriots 3, note 21'),
    ('salute', salute, 'Patriots 3'),
    ('hands on a gun', rifle, 'new, 28 Oct'),
    ('flapping (up)', lambda sp: flapping(sp, 'up'), 'Patriots 3, note 18'),
    ('flapping (pat)', lambda sp: flapping(sp, 'pat'), 'Patriots 3, note 18'),
]


AVOID = {   # views a pose fails the hand check in (rule 41): a film never uses it from there
    'hands on a gun': {'behind': 'both hands hidden by his back: show him three-quarter back instead'},
}


def pose(name, sp):
    """A gallery pose by name, for this person."""
    return next(f for n, f, _ in GALLERY if n == name)(sp)


# ------------------------------------------------------------------------------------------------ the sheet
def test(name, build, sp=MODEL):
    """Draw one pose from every view with the hand check on: [(view name, picture, faults)]."""
    import handcheck as H
    out = []
    for deg, label in VIEWS:
        im = Image.new('RGBA', (600, 900), (226, 222, 214, 255))
        H.begin()
        V.person(im, B.Cam(1.0, 540, 960), 300, 230, 0.62, sp, 0.0, float(deg), build(sp))   # world = canvas pixels
        faults = H.end(0.0, f'{name}, {label}')
        out.append((label, im, faults))
    return out


results = {}                  # the last run: {pose: views that failed}


def main():
    import handcheck as H
    import kitchecks
    import limbs
    args = sys.argv[1:]
    out = next((a for a in args if a.endswith('.jpg')), os.path.join(HERE, 'data', 'pose-gallery.jpg'))
    gallery = list(GALLERY)
    if '--all' in args:
        import moves
        have = {'arms_folded', 'point'}
        gallery += [(n.replace('_', ' '), (lambda sp, n=n: moves.pose(sp, n)), 'moves.pose') for n in moves.POSES
                    if n not in have and n != 'standing']
    if '--only' in args:
        keep = args[args.index('--only') + 1].split(',')
        gallery = [g for g in gallery if g[0] in keep]
    B.SS = 1
    F.guard(B)
    F._ALLOW.append('the pose gallery')
    from satire_style import install_circle_hands
    install_circle_hands(B)                      # the house style, as every satire film draws it
    limbs.install(B)
    kitchecks.install()
    H.install()
    font = ImageFont.truetype(B.SANS, 22)
    tw, th = 220, 330
    sheet = Image.new('RGB', (190 + tw * len(VIEWS), (th + 56) * len(gallery)), (16, 16, 20))
    d = ImageDraw.Draw(sheet)
    bad = 0
    results.clear()
    for r, (name, build, src) in enumerate(gallery):
        y = r * (th + 56)
        d.text((10, y + 10), name, font=font, fill=(255, 255, 255))
        d.text((10, y + 40), src[:18], font=ImageFont.truetype(B.SANS, 16), fill=(170, 170, 170))
        res = test(name, build)
        results[name] = {label for label, _, fs in res if fs}
        for c, (label, im, faults) in enumerate(res):
            tile = im.convert('RGB').crop((60, 40, 540, 760)).resize((tw, th))
            x = 190 + c * tw
            sheet.paste(tile, (x, y))
            msg = 'OK' if not faults else ('AVOID: ' if label in AVOID.get(name, {}) else '') + \
                '; '.join(f"{f['side']}: {f['kind']}" for f in faults)
            d.text((x + 6, y + th + 4), label, font=ImageFont.truetype(B.SANS, 16), fill=(200, 200, 200))
            d.text((x + 6, y + th + 26), msg[:24], font=ImageFont.truetype(B.SANS, 17),
                   fill=(140, 230, 140) if not faults else (255, 160, 110))
        fails = [(label, f) for label, _, fs in res for f in fs]
        new = {label for label, _ in fails} - set(AVOID.get(name, {}))
        bad += bool(new)
        print(f"{name}: " + ('tested clean from all 5 views' if not fails else
                             '; '.join(f"{label}: {f['side']} {f['text']}" for label, f in fails) +
                             ('' if not new else ' -- NOT in AVOID: fix the pose or list the view')))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    sheet.save(out, quality=85)
    print('sheet:', out)
    if __name__ == '__main__':
        sys.exit(1 if bad else 0)
    return bad


if __name__ == '__main__':
    main()
