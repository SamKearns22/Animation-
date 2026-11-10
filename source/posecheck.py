#!/usr/bin/env python3
"""posecheck: every pose a film takes from the kit, checked against the pose gallery as it is drawn (Job G step 5;
film-quality-rules 41 and 42). Pre-flight installs it (before handcheck, whose frames carry its faults).

It notes each pose a film takes by name (posegallery.pose, moves.pose, sitting.pose, lying.lie) and, whenever that
pose is drawn on a checked frame, the view it is seen from, and flags:
- 'avoid view': a pose seen from a view its gallery row lists under "avoid" (posegallery.AVOID, sitting.AVOID);
- 'untested pose': a pose taken by name that has no row in guides/pose-gallery.md (rule 42: test it from every view
  first: posegallery.py --all, sitting.py sheet, lying.py check; then add its row);
- every lying body drawn (lying.draw): lying.body_faults (no neck, an arm held up in the air, both arms on one side).
A pose a film builds by hand (its own joints) is not seen here: list it in the plan as new, priced in the estimate.

    python3 source/posecheck.py        the gallery as this check reads it (names and avoid views)
"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)

BASE = {'standing', 'relaxed'}          # the plain stance every person stands in (tested: kittests standing_legs...)
TAGS = collections.OrderedDict()        # id(joints) -> (kind, name, joints): the pose each named call returned
FRAME = []                              # this frame's findings: dict(who, side, kind, text, rule)
INSTALLED = []
ON = [True]                             # kittests switch it off again when done
_GALLERY = []


def gallery():
    """What guides/pose-gallery.md lists: {'standing': {kit name: row name}, 'sitting': {names}, 'lying': {names}}."""
    if _GALLERY:
        return _GALLERY[0]
    out = {'standing': {}, 'sitting': set(), 'lying': set()}
    with open(os.path.join(ROOT, 'guides', 'pose-gallery.md')) as f:
        for line in f:
            cells = [c.strip() for c in line.split('|')]
            if len(cells) < 4 or not cells[2].startswith('`'):
                continue
            row, call = cells[1], cells[2]
            for m in re.findall(r"moves\.pose\(sp, '(\w+)'", call):
                out['standing'][m] = row
            if 'posegallery.' in call:
                out['standing'][row] = row
            out['sitting'].update(re.findall(r"sitting\.pose\(sp, '([^']+)'", call))
            out['lying'].update(re.findall(r"lying\.lie\(sp, '(\w+)'", call))
    _GALLERY.append(out)
    return out


def view_label(yaw, mirrored=True):
    """The gallery's name for a facing (degrees, as views.person takes it)."""
    a = ((float(yaw) + 180.0) % 360.0) - 180.0
    b = int(round(abs(a) / 45.0)) * 45
    if b == 45 and a < 0 and mirrored:
        return 'mirrored'
    return {0: 'front', 45: 'three-quarter', 90: 'side', 135: 'three-quarter back', 180: 'behind'}[b]


def _tag(kind, name, j):
    TAGS[id(j)] = (kind, name, j)
    while len(TAGS) > 4000:
        TAGS.popitem(last=False)


def _note(sp, side, kind, text, rule):
    import handcheck as H
    if H.ACTIVE[0] and ON[0]:
        FRAME.append(dict(who=(sp or {}).get('name', 'someone'), side=side, kind=kind, text=text, rule=rule))


def seen(sp, yaw, joints):
    """views.person is drawing `joints` facing `yaw`: a named pose's view checked against its gallery row."""
    got = TAGS.get(id(joints))
    if got is None or got[2] is not joints:
        return
    kind, name, _ = got
    g = gallery()
    if kind == 'standing':
        if name in BASE:
            return
        row = g['standing'].get(name)
        if row is None:
            _note(sp, 'both', 'untested pose', f"the pose '{name}' has no row in the pose gallery: test it from every "
                  'view first (posegallery.py --all) and add its row', 42)
            return
        import posegallery
        label = view_label(yaw)
        why = posegallery.AVOID.get(row, {}).get(label)
        if why:
            _note(sp, 'both', 'avoid view', f"'{row}' seen from the {label}, a view the gallery says to avoid "
                  f'({why})', 42)
    elif kind == 'sitting':
        if name not in g['sitting']:
            _note(sp, 'both', 'untested pose', f"the seated pose '{name}' has no row in the pose gallery: test it "
                  '(sitting.py sheet) and add its row', 42)
            return
        import sitting
        label = view_label(yaw, mirrored=False)
        why = sitting.AVOID.get(name, {}).get(label)
        if why:
            _note(sp, 'both', 'avoid view', f"seated '{name}' seen from the {label}, a view the gallery says to "
                  f'avoid ({why})', 42)


def lying_drawn(cam, k, sp, surfaces):
    """lying.draw is drawing body `k`: its pose is in the gallery, and Sam's lying notes hold (lying.body_faults)."""
    import lying
    name = getattr(k, 'pose', None)
    if name is not None and name not in gallery()['lying']:
        _note(sp, 'both', 'untested pose', f"the lying pose '{name}' has no row in the pose gallery: test it "
              '(lying.py check) and add its row', 42)
    import lying_flat
    if lying_flat.face_up_away(cam, k):
        _note(sp, 'both', 'lying: face up away', 'lying on the back, head away from the camera: the face can only be '
              'drawn sat up staring at us (Sam, 10 Nov); move the camera to the side or above', 42)
    surf = [('floor', surfaces[0][0], surfaces[0][1])] if surfaces else None
    for text in lying.body_faults(k, sp, surf, cam, who=''):
        text = text[2:] if text.startswith(': ') else text
        side = 'L' if ' left ' in text else 'R' if ' right ' in text else 'both'
        kind = 'lying: no neck' if 'neck' in text else 'lying: arms one side' if 'crosses' in text else \
            'lying: arm held up'
        _note(sp, side, kind, text, 41)


def take():
    """This frame's findings (and forget them)."""
    out = list(FRAME)
    del FRAME[:]
    return out


def _swap(real, new):
    """Point every module's reference to `real` at `new` (as handcheck.install does)."""
    for m in list(sys.modules.values()):
        try:
            for k, v in list(vars(m).items()):
                if v is real:
                    setattr(m, k, new)
        except TypeError:
            continue


def install():
    """Tag the named poses and watch views.person and lying.draw. Safe to call twice."""
    if INSTALLED:
        return
    INSTALLED.append(1)
    import lying
    import moves
    import posegallery
    import sitting
    import views as V

    def wrap_pose(mod, attr, kind, name_of):
        real = getattr(mod, attr)

        def f(*a, **kw):
            j = real(*a, **kw)
            _tag(kind, name_of(a, kw), j)
            return j
        f.__doc__ = real.__doc__
        _swap(real, f)

    wrap_pose(moves, 'pose', 'standing', lambda a, kw: a[1] if len(a) > 1 else kw.get('name'))
    wrap_pose(posegallery, 'pose', 'standing', lambda a, kw: a[0] if a else kw.get('name'))
    wrap_pose(sitting, 'pose', 'sitting', lambda a, kw: a[1] if len(a) > 1 else kw.get('name'))

    real_person = V.person

    def person(img, cam, x, y, s, sp, t, yaw, joints=None, head_yaw=None, tilt=None):
        if joints is not None and not V.PROBE:
            seen(sp, yaw, joints)
        return real_person(img, cam, x, y, s, sp, t, yaw, joints, head_yaw, tilt=tilt)
    person.__dict__.update(real_person.__dict__)
    _swap(real_person, person)

    real_draw = lying.draw

    def draw(img, cam, k, sp, t=0.0, light=None, surfaces=None, prts=None):
        lying_drawn(cam, k, sp, surfaces)
        return real_draw(img, cam, k, sp, t, light=light, surfaces=surfaces, prts=prts)
    draw.__doc__ = real_draw.__doc__
    _swap(real_draw, draw)


if __name__ == '__main__':
    import posegallery
    import sitting
    g = gallery()
    print('standing (kit name -> row):', g['standing'])
    print('seated:', sorted(g['sitting']))
    print('lying:', sorted(g['lying']))
    print('avoid (standing):', {k: sorted(v) for k, v in posegallery.AVOID.items()})
    print('avoid (seated):', {k: sorted(v) for k, v in sitting.AVOID.items()})
