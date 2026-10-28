#!/usr/bin/env python3
"""handcheck: every arm ends in a visible hand, in every frame and every view it is seen in (film-quality-rules 41;
Patriots 3 notes 18 and 21: an arm wrapped round a head with no hands, seen from behind; hands pushed back into
their own sleeves while he flapped).

How it looks: each person views.py draws is drawn a second time, alone, on a clear layer, with each sleeve and hand in
its own key colour (views.PROBE), and each hand also alone on a layer of its own (so its whole size is known). Then:
- NO HAND: an arm whose sleeve shows (at least a hand's worth of it) but whose hand shows less than 35% of itself:
  a hidden hand ('none'), a hand behind the head or the back, an arm wrapped round a head;
- IN SLEEVE: a forearm pointing at the lens (shown at under 60% of its length) whose hand comes back towards the
  shoulder on screen by over a quarter of a forearm, for two frames or more: the hand sits against the upper arm,
  read as pushed into the sleeve rather than at its end (note 18: 28-42% back then; 10-16% once fixed);
- OVER: in the frame, everyone's layers stacked in drawing order: a hand lying mostly over the body of someone at
  about the same distance (a touch the film did not list: Patriots 3 note 1, the reach that read as a cuddle). A hand
  hidden behind someone nearer the lens is ordinary staging and is not flagged.
An arm counts as seen when a real stretch of it shows (past the shoulder by over half the upper arm); a hand off the
edge of the frame is skipped; a pose that hides its hands on purpose says so (j['tucked']: moves.pose's arms folded,
pockets, behind the back).
A hand drawn by a prop (binoculars that bring their own fists) counts for the nearer arm.
Meant exceptions go in the film's HANDS_OK: [(who, side or '*', kind, t0, t1, why)] (who and kind as fnmatch patterns,
kind one of 'no hand', 'in sleeve', 'over *'); a hand over someone the film lists in ALLOWED_CONTACTS
or TOUCHES at that time is fine too.

Only people drawn by views.person are seen (the satire kit, lying.stand's flat people); the 3D bodies drawn by
lying.draw (cameras steeper than 40 degrees) and older films' own figures are not.

Pre-flight runs it on every frame it draws (rule 41); on its own:
    python3 source/handcheck.py FILM [OUT_DIR] [--span T0 T1] [--every N]
draws every Nth frame (default 1: every frame), prints the faults and saves OUT_DIR/FILM-hands.jpg: each fault's first
frame, cropped round the person, the hands circled.
"""
import fnmatch
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

KEYS = {'L': ((255, 0, 255), (0, 255, 255)), 'R': ((255, 128, 0), (0, 255, 0))}   # (sleeve, hand) per arm
PROP_HAND = (255, 255, 0)     # a hand drawn by a prop (gesture_hand called from outside views.hand)
SEEN = 1.0                    # an arm is seen when this many hands' worth of its sleeve shows
SHOWN = 0.35                  # ... and its hand must show at least this share of itself
SHORT, BACK = 0.6, 0.25       # a forearm shown at under this share of its length (pointing at the lens) whose hand comes
                              # back towards the shoulder by over this share of a forearm: pushed into the sleeve
HELD = {'in sleeve': 2}       # frames in a row a kind must last to count (one in-between frame of a fast move is not seen)
OVER = 0.5                    # a hand with over half of it on someone else's body is over them, when they stand
NEAR = 0.1                    # ... at about the same distance (drawing scales within 10%): nearer, it is just in front
EXPECT = math.pi * 25 * 23    # a hand's area in person units (burnham.gesture_hand: a 25 x 23 circle)

FRAME = []                    # the people probed in the frame being drawn
FOUND = []                    # raw findings: dict(t, where, who, side, kind, box)
ACTIVE = [False]              # probing only between begin() and end(): never the frames other checks draw
INSTALLED = []


def _key(img):
    a = np.asarray(img)
    rgb, alpha = a[:, :, :3], a[:, :, 3] > 128

    def m(c):
        return alpha & (rgb[:, :, 0] == c[0]) & (rgb[:, :, 1] == c[1]) & (rgb[:, :, 2] == c[2])
    return a[:, :, 3] > 40, m


def _draw(img, cam, x, y, s, sp, t, yaw, joints, head_yaw, tilt):
    """views.person without any wrapper (the probe must not be logged by the other checks)."""
    if tilt is None:
        return V._person(img, cam, x, y, s, sp, t, yaw, joints, head_yaw, None)
    old = V._E[0]
    V._E[0] = tilt[0]
    try:
        return V._person(img, cam, x, y, s, sp, t, yaw, joints, head_yaw, tilt[1])
    finally:
        V._E[0] = old


def probe(img, args):
    """Draw one person again, alone, sleeves and hands keyed; note what shows. args: views.person's arguments."""
    cam, x, y, s, sp, t, yaw, joints, head_yaw, tilt = args
    size = img.size
    lay = Image.new('RGBA', size, (0, 0, 0, 0))
    full = {sd: Image.new('RGBA', size, (0, 0, 0, 0)) for sd in 'LR'}
    props = []                                      # hands a prop draws: (local wrist, layer)
    real_hand = B.gesture_hand
    inside = []

    def prop_hand(p, el, wr, shape, skin, extra=None, t_=0.0):
        if inside:                                  # views.hand's own call: already keyed
            return real_hand(p, el, wr, shape, skin, extra, t_)
        one = Image.new('RGBA', size, (0, 0, 0, 0))
        real_hand(B.Pen(one, p.cam), el, wr, shape, PROP_HAND, extra, t_)
        props.append((p.cam.P(*wr), one))
        return real_hand(p, el, wr, shape, PROP_HAND, extra, t_)

    real_vhand = V.hand

    def vhand(p, j2, side, sp_, shape):
        inside.append(1)
        try:
            return real_vhand(p, j2, side, sp_, shape)
        finally:
            inside.pop()

    V.PROBE.update({'L': KEYS['L'], 'R': KEYS['R'], 'full': {sd: (lambda p, sd=sd: B.Pen(full[sd], p.cam)) for sd in 'LR'}})
    B.gesture_hand, V.hand = prop_hand, vhand
    n_log = len(F.LOG)
    try:
        j2 = _draw(lay, cam, x, y, s, sp, t, yaw, joints, head_yaw, tilt)
    except Exception:
        return None
    finally:
        V.PROBE.clear()
        B.gesture_hand, V.hand = real_hand, real_vhand
        del F.LOG[n_log:]
    boxes = [b for b in [lay.getbbox()] + [im.getbbox() for im in full.values()] + [o.getbbox() for _, o in props] if b]
    if not boxes:
        return None
    x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)       # kept: only the box round this person
    x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
    cut = lambda im: im.crop((x0, y0, x1, y1))
    lay, full, props = cut(lay), {sd: cut(im) for sd, im in full.items()}, [(q, cut(o)) for q, o in props]
    body, m = _key(lay)
    k = B.Local(cam, x, y, s).S(1.0)                # screen pixels per person unit
    bob = (joints or {}).get('bob', 0.0)
    L = B.Local(cam, x, y + bob * s, s, -1 if V.snap(yaw)[1] else 1)   # the frame views.person draws the arms in
    if tilt is not None:
        L = V.Tilted(L, tilt[1], 928.0 - bob)
    pt = {q + sd: np.array(L.P(*j2[q + sd])) - (x0, y0) for q in ('sh', 'el', 'wr') for sd in 'LR'}
    wr = {sd: pt['wr' + sd] for sd in 'LR'}
    out = dict(name=sp.get('name', 'someone'), body=body, k=k, expect=EXPECT * k * k, arms={}, at=(x0, y0, x1, y1),
               size=size,
               ink=B.Pen(lay, L).w(2.6), tucked=(joints or {}).get('tucked'))
    hand_px = {sd: m(KEYS[sd][1]) for sd in 'LR'}
    full_px = {sd: _key(full[sd])[1](KEYS[sd][1]) for sd in 'LR'}
    shown_prop = m(PROP_HAND)
    for (pt, one) in props:                         # a prop's fists count for the nearer arm
        sd = min('LR', key=lambda q: math.dist(np.array(pt) - (x0, y0), wr[q]))
        mask = _key(one)[1](PROP_HAND)
        full_px[sd] |= mask
        hand_px[sd] |= shown_prop & mask
    for sd in 'LR':
        sh2, el2, wr2 = (np.array(j2[q + sd][:2], float) for q in ('sh', 'el', 'wr'))
        u, v = sh2 - el2, wr2 - el2
        fold = math.degrees(math.acos(max(-1.0, min(1.0, float(u @ v) / ((np.hypot(*u) * np.hypot(*v)) or 1.0)))))
        out['arms'][sd] = dict(fold=fold, fore=float(np.hypot(*v)) / (F.FORE * 0.98),
                               sleeve=m(KEYS[sd][0]), hand=hand_px[sd], full=full_px[sd],
                               shape=(j2.get('hand') or {}).get(sd, 'fist'), sh=pt['sh' + sd], el=pt['el' + sd],
                               reach=F.UPPER * k)
    return out


def _part(pp, other):
    """The other person's body, in this person's box."""
    ax0, ay0, ax1, ay1 = pp['at']
    bx0, by0, bx1, by1 = other['at']
    out = np.zeros(pp['body'].shape, bool)
    ix0, iy0, ix1, iy1 = max(ax0, bx0), max(ay0, by0), min(ax1, bx1), min(ay1, by1)
    if ix1 > ix0 and iy1 > iy0:
        out[iy0 - ay0:iy1 - ay0, ix0 - ax0:ix1 - ax0] = other['body'][iy0 - by0:iy1 - by0, ix0 - bx0:ix1 - bx0]
    return out


def _seen(arm, mask, expect):
    """An arm is seen when a real stretch of it shows: a hand's worth of sleeve, reaching past the shoulder by over
    half the upper arm (from behind, an arm reaching forward shows only at the shoulder: that is not seen)."""
    if mask.sum() < SEEN * expect:
        return False
    ys, xs = np.nonzero(mask)
    far = np.hypot(xs - arm['sh'][0], ys - arm['sh'][1]).max()
    return far > 0.55 * arm['reach']


def frame_faults(people):
    """Every fault in one frame, from the probes in drawing order."""
    out = []
    if not people:
        return out
    w, h = people[0]['size']
    top = np.full((h, w), -1, np.int16)             # who is on top at each pixel
    for i, pp in enumerate(people):
        x0, y0, x1, y1 = pp['at']
        top[y0:y1, x0:x1][pp['body']] = i
    for i, pp in enumerate(people):
        x0, y0, x1, y1 = pp['at']
        mine = top[y0:y1, x0:x1] == i
        for sd, a in pp['arms'].items():
            whole = int(a['full'].sum())
            if a['shape'] != 'none' and whole < SHOWN * pp['expect']:
                continue                            # the hand is off the edge of the frame
            expect = whole if whole else pp['expect']
            sleeve, hand = a['sleeve'], a['hand']
            box = pp['at']
            if pp['tucked'] and hand.sum() < SHOWN * expect:
                continue                            # a pose that hides its hands on purpose (arms folded, pockets)
            if _seen(a, sleeve, expect) and hand.sum() < SHOWN * expect:
                out.append(dict(who=pp['name'], side=sd, kind='no hand', box=box,
                                text=f"an arm with no hand ({'its hand hidden' if a['shape'] == 'none' else 'the hand covered'})"))
                continue
            back = a['fore'] * math.cos(math.radians(a['fold']))   # how far the hand comes back towards the shoulder
            if hand.sum() >= SHOWN * expect and a['fore'] < SHORT and back > BACK:
                out.append(dict(who=pp['name'], side=sd, kind='in sleeve', box=box,
                                text=f"the hand pushed back into its own sleeve (the forearm points at the lens and "
                                     f"doubles back: shown at {a['fore'] * 100:.0f}% of its length, the hand "
                                     f"{back * 100:.0f}% of a forearm back towards the shoulder)"))
            # in the frame (everyone stacked in drawing order): a hand over the body of someone at about the same
            # distance. (A hand hidden behind someone nearer the lens is ordinary staging: not a fault.)
            vis_hand = hand & mine
            if vis_hand.sum():
                for o, other in enumerate(people):
                    if o < i and abs(other['k'] / pp['k'] - 1) < NEAR and \
                            (vis_hand & _part(pp, other)).sum() > OVER * vis_hand.sum():
                        out.append(dict(who=pp['name'], side=sd, kind=f"over {other['name']}", box=box,
                                        text=f"the hand over {other['name']}'s body (a touch not listed)"))
    return out


# ------------------------------------------------------------------------------------------------ hooking in
def install():
    """Probe everyone views.person draws (after the other checks' own wrappers). Safe to call twice."""
    if INSTALLED:
        return
    INSTALLED.append(1)
    real = V.person

    def person(img, cam, x, y, s, sp, t, yaw, joints=None, head_yaw=None, tilt=None):
        j2 = real(img, cam, x, y, s, sp, t, yaw, joints, head_yaw, tilt=tilt)
        if ACTIVE[0] and not V.PROBE:
            got = probe(img, (cam, x, y, s, sp, t, yaw, joints, head_yaw, tilt))
            if got:
                FRAME.append(got)
        return j2
    person._hands = True
    person._logged = getattr(real, '_logged', False)   # kitchecks' wrapper inside: it must not wrap again
    for m in list(sys.modules.values()):
        try:
            for k, v in list(vars(m).items()):
                if v is real:
                    setattr(m, k, person)
        except TypeError:
            continue


def begin():
    del FRAME[:]
    ACTIVE[0] = True


def end(t, where=''):
    """The frame is drawn: its faults, noted (and returned)."""
    ACTIVE[0] = False
    got = [dict(f, t=t, where=where) for f in frame_faults(FRAME)]
    del FRAME[:]
    FOUND.extend(got)
    return got


def _allowed(film, f):
    for ent in getattr(film, 'HANDS_OK', ()):
        who, side, kind, t0, t1 = ent[:5]
        if fnmatch.fnmatchcase(f['who'], who) and side in ('*', f['side']) and fnmatch.fnmatchcase(f['kind'], kind) \
                and t0 - 1e-6 <= f['t'] <= t1 + 1e-6:
            return True
    if f['kind'].startswith('over '):
        other = f['kind'][5:]
        for ent in list(getattr(film, 'ALLOWED_CONTACTS', ())) + list(getattr(film, 'TOUCHES', ())):
            a, b, t0, t1 = ent[:4]
            names = {str(a).split('.')[0].lower(), str(b).split('.')[0].lower()}
            if {f['who'].lower(), other.lower()} <= names and t0 <= f['t'] <= t1:
                return True
    return False


def summary(film, found=None, fps=12):
    """The faults, one line per run of frames (who, which arm, what kind): 'HANDS: ...'."""
    found = FOUND if found is None else found
    runs = {}
    for f in sorted(found, key=lambda f: f['t']):
        if _allowed(film, f):
            continue
        key = (f['who'], f['side'], f['kind'])
        r = runs.setdefault(key, [])
        if r and f['t'] - r[-1][-1]['t'] <= 3.5 / fps:
            r[-1].append(f)
        else:
            r.append([f])
    out = []
    every = min((b['t'] - a['t'] for a, b in zip(found, found[1:]) if b['t'] > a['t']), default=1 / fps)
    for (who, side, kind), rs in runs.items():
        for r in rs:
            if every <= 1.5 / fps and len(r) < HELD.get(kind, 1):
                continue                            # (checked on every frame) too brief to be seen
            a, b = r[0]['t'], r[-1]['t']
            span = f'{a:.2f} s' if len(r) == 1 else f'{a:.2f}-{b:.2f} s, {len(r)} frames checked'
            out.append((a, f"HANDS: {r[0]['where'] or f'{a:.2f} s'}: {who}'s {'left' if side == 'L' else 'right'} arm: "
                           f"{r[0]['text']} ({span}; rule 41)", r[0]))
    out.sort(key=lambda x: x[0])
    return out


def sheet(film, rows, path):
    """Each fault's first frame, cropped round the person, the probe's hands circled, labelled."""
    tiles = []
    font = ImageFont.truetype(B.SANS, 22)
    for a, text, f in rows[:24]:
        im = film.frame_image(a).convert('RGB')
        sc = im.width / 1080
        x0, y0, x1, y1 = f['box'] or (0, 0, im.width, im.height)
        pad = int(60 * sc)
        x0, y0, x1, y1 = max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)
        crop = im.crop((x0, y0, x1, y1))
        crop.thumbnail((360, 520))
        tile = Image.new('RGB', (360, 600), (24, 24, 28))
        tile.paste(crop, ((360 - crop.width) // 2, 0))
        d = ImageDraw.Draw(tile)
        words, line, y = text.split(': ', 2)[-1].split(), '', 525
        for w in words:
            if font.getlength(line + ' ' + w) > 345:
                d.text((8, y), line, font=font, fill=(255, 220, 120))
                line, y = w, y + 24
            else:
                line = (line + ' ' + w).strip()
        d.text((8, y), line, font=font, fill=(255, 220, 120))
        d.text((8, 4), f"{a:.2f} s  {f['who']} {f['side']}", font=font, fill=(255, 255, 255))
        tiles.append(tile)
    if not tiles:
        return None
    cols = min(4, len(tiles))
    out = Image.new('RGB', (cols * 360, ((len(tiles) + cols - 1) // cols) * 600), (10, 10, 12))
    for i, tl in enumerate(tiles):
        out.paste(tl, ((i % cols) * 360, (i // cols) * 600))
    out.save(path, quality=85)
    return path


# ------------------------------------------------------------------------------------------------ on its own
_FILM = [None]


def _one(i_fps):
    i, fps = i_fps
    film = _FILM[0]
    t = i / fps
    shot = next((s[0] for s in getattr(film, 'SHOTS', []) if s[1] <= t < s[2]), '')
    F.CONTEXT['where'] = f'{shot} {t:.2f}s'
    begin()
    try:
        film.frame_image(t)
    except Exception as e:                          # the drawing's own checks are pre-flight's job
        del FRAME[:]
        ACTIVE[0] = False
        return [dict(t=t, where=F.CONTEXT['where'], who='(frame)', side='L', kind='error', box=None,
                     text=f'the frame did not draw: {str(e)[:120]}')]
    return end(t, F.CONTEXT['where'])


def run(film, span=None, every=1, fps=None):
    """Every Nth frame of the film (or of span), on all processor cores; returns the summary rows."""
    import kitchecks
    F.guard(B)
    F._ALLOW.append('handcheck: the drawing checks are pre-flight\'s job')
    kitchecks.install()
    install()
    fps = fps or getattr(film, 'FPS', 12)
    end_t = getattr(film, 'BLACK_AT', getattr(film, 'DUR', 0))
    a, b = span or (0.0, end_t)
    frames = [(i, fps) for i in range(int(round(a * fps)), int(round(b * fps)), every)]
    _FILM[0] = film
    B.SS = 1
    from multiprocessing import Pool
    found = []
    with Pool(os.cpu_count()) as pool:
        for got in pool.imap(_one, frames, chunksize=2):
            found += got
    return summary(film, found, fps)


def main():
    import importlib
    args = [x for x in sys.argv[1:]]
    span, every = None, 1
    if '--span' in args:
        k = args.index('--span')
        span = (float(args[k + 1]), float(args[k + 2]))
        del args[k:k + 3]
    if '--every' in args:
        k = args.index('--every')
        every = int(args[k + 1])
        del args[k:k + 2]
    name = args[0]
    out = args[1] if len(args) > 1 else os.path.join(HERE, 'data')
    film = importlib.import_module(name)
    rows = run(film, span, every)
    for _, text, _ in rows:
        print(text)
    print('handcheck:', 'clean' if not rows else f'{len(rows)} fault(s)')
    if rows:
        os.makedirs(out, exist_ok=True)
        print('sheet:', sheet(film, rows, os.path.join(out, f'{name}-hands.jpg')))
    sys.exit(1 if rows else 0)


if __name__ == '__main__':
    main()
