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

Poses read at phone size (craft-first-round change 2, Sam 16 Nov; rules 38 and 41). Pre-flight REFUSES (gate_faults):
- a film with people and no SHOT_MARKS {shot: [who]} (the front-on check cannot run; with no rooms plan the labels
  are people's names and the check runs here on the drawing pass: 'turned from the lens');
- a body move in the acting list, or a gallery pose the film names whose row says "not yet looked at by eye", with
  no "Pose looked at:" line in the notes' Record. To clear one: look at its frame at phone size, then record it:
    python3 source/posecheck.py look FILM T [T ...]        one sheet, each frame at phone size (390 px wide)
    python3 source/posecheck.py seen FILM "KEY" T "what reads at phone size"   (KEY: "who, shot" or the pose row)
  Why: EPR's shrug failed twice (A12, A30): side on, palm hidden, a small lift: nothing read at phone size, and
  EPR had no SHOT_MARKS, so the front-on check never ran.
    python3 source/posecheck.py replay FILM               the refusals from the film's files alone (no drawing)
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


def take(t=None):
    """This frame's findings (and forget them); with t, also the facing check of films with no rooms plan."""
    out = list(FRAME)
    del FRAME[:]
    if t is not None and MARKS:
        out += _facing_faults(t)
    del FACING[:]
    return out


# ------------------------------------------------------------------------------- poses read at phone size
MARKS = {}           # film without a rooms plan: {shot: [names]} (set by preflight via set_marks)
SHOT_OF = [None]     # t -> shot name
OK_TURN = {}         # (shot, label) -> reason (the film's THREE_QUARTER_OK)
FACING = []          # (who, yaw) drawn this frame
LOOK_W = 390         # an iPhone's width in points: what Sam sees
LOOKED = 'Pose looked at:'
BEFORE = {'protest-tiers': 'in its final render when this was switched on (16 Nov): warned, not refused'}
UNSEEN = 'not yet looked at by eye'


def set_marks(film):
    """A film with people and no rooms plan: its SHOT_MARKS are checked here on the drawing pass (rule 38)."""
    MARKS.clear()
    MARKS.update({str(k): [str(x).lower() for x in v] for k, v in (shot_marks(film) or {}).items()})
    shots = list(getattr(film, 'SHOTS', []))
    SHOT_OF[0] = lambda t: next((str(s[0]) for s in shots if s[1] <= t < s[2]), None)
    OK_TURN.clear()
    OK_TURN.update({(str(a), str(b).lower()): why for a, b, *why in getattr(film, 'THREE_QUARTER_OK', ())})


def _facing_faults(t):
    shot = SHOT_OF[0](t) if SHOT_OF[0] else None
    out = []
    for who, yaw in FACING:
        for lb in MARKS.get(shot, ()):
            if lb in who.lower() and (shot, lb) not in OK_TURN:
                off = abs(((float(yaw) + 180.0) % 360.0) - 180.0)
                if off > 25:
                    out.append(dict(who=who, side='both', kind='turned from the lens', rule=38,
                                    text=f'shot {shot}: {who} is seen {view_label(yaw)} ({off:.0f} degrees off the lens): '
                                         'turn them, or list it in THREE_QUARTER_OK with the reason'))
    return out


def shot_marks(film):
    for src in (film, getattr(film, 'PLAN', None)):
        m = src.get('SHOT_MARKS') if isinstance(src, dict) else getattr(src, 'SHOT_MARKS', None)
        if m:
            return m
    return None


def acting_moves(notes):
    """The acting list's body moves: [(key 'who, shot', body, lands)]; a body '(not seen)' or blank is skipped."""
    out = []
    for m in re.finditer(r'^##+ *(?:The )?acting list.*?$(.*?)(?=^## |\Z)', notes, re.M | re.S | re.I):
        for line in m.group(1).splitlines():
            c = [x.strip() for x in line.strip().strip('|').split('|')]
            if len(c) < 6 or c[0] in ('line', '') or set(c[0]) <= set('-: '):
                continue
            body = c[4]
            if not body or body.lower().startswith(('(not seen', '-', 'none')):
                continue
            shot = re.split(r'[:,(]', c[2])[0].strip() or '?'
            out.append((f'{c[1]}, {shot}', body, c[5]))
    return out


def unseen_named(source):
    """Gallery rows the film's code names whose 'from' cell says not yet looked at by eye: [row name]."""
    rows = []
    with open(os.path.join(ROOT, 'guides', 'pose-gallery.md')) as f:
        for line in f:
            c = [x.strip() for x in line.split('|')]
            if len(c) > 4 and c[2].startswith('`') and UNSEEN in c[3]:
                kit = re.findall(r"moves\.pose\(sp, '(\w+)'", c[2]) + re.findall(r'posegallery\.(\w+)\(', c[2])
                if any(re.search(rf"""pose\([^)]*['"]{k}['"]|posegallery\.{k}\(""", source) for k in kit):
                    rows.append(c[1])
    return rows


def looked(notes):
    """Keys with a 'Pose looked at:' line in the notes (lowercase)."""
    return {m.group(1).strip().lower() for m in re.finditer(rf'{LOOKED} *([^|]+)\|', notes)}


def gate_faults(source, notes, has, marks, rooms_plan=False):
    """Pre-flight's refusals (strings) for a film's code text, notes text, HAS and SHOT_MARKS."""
    if 'people' not in has:
        return []
    out = []
    if not marks:
        out.append('poses (rule 38): a film with people has no SHOT_MARKS {shot: [who]}, so the front-on check cannot '
                   'run: add it (people\'s names, or plan marks with a rooms plan)')
    done = looked(notes)
    todo = [(k, f'the body move "{b[:60]}"') for k, b, _ in acting_moves(notes)] + \
           [(r, f'the gallery pose "{r}" (never looked at by eye)') for r in unseen_named(source)]
    for key, what in todo:
        if key.lower() not in done:
            out.append(f'poses (rule 41): {what} ({key}) is not yet looked at at phone size in its own shot: '
                       f'posecheck.py look FILM T, then posecheck.py seen FILM "{key}" T "what reads"')
    return out


def _film_files(name):
    import glob
    mod = name.replace('-', '_')
    return sorted(glob.glob(os.path.join(HERE, mod + '.py')) + glob.glob(os.path.join(HERE, mod + '_*.py')))


def _notes_of(name):
    for p in (os.path.join(ROOT, 'notes', name.replace('_', '-') + '.md'),
              os.path.join(ROOT, 'notes', 'archive', name.replace('_', '-') + '.md')):
        if os.path.exists(p):
            return p
    return None


def look(name, times, out_dir):
    """One sheet: each frame at phone size, labelled with its time and shot."""
    import importlib
    from PIL import Image, ImageDraw
    film = importlib.import_module(name.replace('-', '_'))
    shots = list(getattr(film, 'SHOTS', []))
    tiles = []
    for t in times:
        im = film.frame_image(t).convert('RGB')
        im = im.resize((LOOK_W, round(im.height * LOOK_W / im.width)), Image.LANCZOS)
        shot = next((str(s[0]) for s in shots if s[1] <= t < s[2]), '?')
        lab = Image.new('RGB', (LOOK_W, 24), (255, 255, 255))
        ImageDraw.Draw(lab).text((6, 6), f'{t:.2f} s, shot {shot}, phone size', fill=(0, 0, 0))
        tile = Image.new('RGB', (LOOK_W, im.height + 24), (255, 255, 255))
        tile.paste(lab, (0, 0))
        tile.paste(im, (0, 24))
        tiles.append(tile)
    sheet = Image.new('RGB', (sum(x.width + 10 for x in tiles) + 10, max(x.height for x in tiles) + 20), (200, 200, 200))
    x = 10
    for tile in tiles:
        sheet.paste(tile, (x, 10))
        x += tile.width + 10
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f'{name}-poselook.jpg')
    sheet.save(path, quality=90)
    return path


def seen_record(name, key, t, what):
    """Write the 'Pose looked at:' line into the notes' Record (after the sheet was looked at)."""
    path = _notes_of(name)
    if not path:
        raise SystemExit('no notes file for ' + name)
    sheet = os.path.join(ROOT, 'renders', f'{name}-poselook.jpg')
    if not os.path.exists(sheet):
        raise SystemExit(f'no look sheet ({os.path.relpath(sheet, ROOT)}): run posecheck.py look {name} {t} first')
    if len(what.split()) < 4:
        raise SystemExit('say what reads at phone size (a few words: the move, the hands, the face)')
    text = open(path).read()
    import datetime
    line = f'- {LOOKED} {key} | {float(t):.2f} s | phone size, {datetime.date.today():%d %b}: {what}'
    m = re.search(r'^## Record.*$', text, re.M)
    if m:
        text = text[:m.end()] + '\n' + line + text[m.end():]
    else:
        text += '\n## Record (pre-flight reads these lines here; never archive them)\n' + line + '\n'
    open(path, 'w').write(text)
    return line


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
        if MARKS and not V.PROBE:
            FACING.append(((sp or {}).get('name', 'someone'), yaw))
        return real_person(img, cam, x, y, s, sp, t, yaw, joints, head_yaw, tilt=tilt)
    person.__dict__.update(real_person.__dict__)
    _swap(real_person, person)

    real_draw = lying.draw

    def draw(img, cam, k, sp, t=0.0, light=None, surfaces=None, prts=None):
        lying_drawn(cam, k, sp, surfaces)
        return real_draw(img, cam, k, sp, t, light=light, surfaces=surfaces, prts=prts)
    draw.__doc__ = real_draw.__doc__
    _swap(real_draw, draw)


def _main():
    a = sys.argv[1:]
    if a and a[0] == 'look':
        print(look(a[1], [float(x) for x in a[2:]], os.path.join(ROOT, 'renders')))
        return True
    if a and a[0] == 'seen':
        print(seen_record(a[1], a[2], a[3], ' '.join(a[4:])))
        return True
    if a and a[0] == 'replay':
        src = '\n'.join(open(p).read() for p in _film_files(a[1]))
        notes = open(_notes_of(a[1])).read()
        has = set(re.findall(r"'(people|rooms|voices|effects|props)'", (re.search(r'^HAS *=.*$', src, re.M) or
                                                                         re.search('$', '')).group(0))) or {'people'}
        marks = re.search(r'SHOT_MARKS *=', src)
        got = gate_faults(src, notes, has, bool(marks))
        print(f'{a[1]}: {len(got)} refusal(s)')
        for x in got:
            print(' -', x)
        return True
    return False


if __name__ == '__main__' and _main():
    pass
elif __name__ == '__main__':
    import posegallery
    import sitting
    g = gallery()
    print('standing (kit name -> row):', g['standing'])
    print('seated:', sorted(g['sitting']))
    print('lying:', sorted(g['lying']))
    print('avoid (standing):', {k: sorted(v) for k, v in posegallery.AVOID.items()})
    print('avoid (seated):', {k: sorted(v) for k, v in sitting.AVOID.items()})
