#!/usr/bin/env python3
"""viewchecks: the checks of what the camera shows (guides/film-quality-rules.md rules 15-18 and 20), for any film.

Why: Prepper Minister's notes 11-16, 20, 45 and 48 (props across a back, star flashes), 13 (effects drawn over people),
57 (the plasma swapped sides of Wes across a cut) and 2, 27, 41, 46 (props too small to read on a phone) were all things
a computer can find. Each is tested on the result:

  props turned (rule 20)   every person drawn holding something (views.py, logged by kitchecks) is redrawn alone at
                           every 30 degrees: from behind nothing held is drawn over the back; from the side the prop
                           stays on the side they face (a prop at a fixed screen angle ends up behind them)
  effect shapes (rule 15)  EFFECTS = [(name, kind, draw(img))]: each effect drawn alone; a 'burst' must be a lumpy,
                           uneven blob (a star or regular spikes fail); nothing but 'sparks' may be motion lines
                           (three or more thin parallel streaks)
  direction (rule 16)      movers(t) -> [(name, (x, y, z))] (bolts, plasma, thrown things) and everyone in scene(t): at
                           every cut (a new shot, or the camera jumping) anything moving keeps its screen direction and
                           its side of each person, unless DIRECTION_SWAPS = [(name, cut time, why)] says it swaps
  effects hidden (rule 17) effect_points(t) -> [(name, (x, y, z), radius)] and EFFECT_SWITCH = [(module, function)]
                           (what draws the effects, switched off to see them): an effect behind any figure (people,
                           robots, creatures) must not be drawn over it
  readability (rule 18)    JOKE_PROPS = [(name, [times], (x, y, z) or fn(t), size in metres)]: each prop a joke needs,
                           its size on screen; under 40 px (of 1920) it fails; sheet() puts each at phone size

    python3 source/viewchecks.py FILM [SHEET.jpg]     every check (draws every 3rd frame for the prop test: minutes)
Pre-flight runs them all (the prop test on its own drawing pass).
"""
import importlib
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
READABLE = 40                 # pixels (of 1920): a prop a joke needs is at least this big on screen
BEHIND = 50                   # pixels: a held prop this far onto the side someone faces away from sits behind them


# ------------------------------------------------------------------------------------------------ rule 20
def _prop_key(name, j, where=''):
    """One test per person, prop, shot and rough hold (where the wrists are, to 60 units): a machete down at the side
    and the same machete raised by the shoulder are tested apart."""
    hold = tuple(int(round(v / 60)) for sd in 'LR' for v in (j.get('wr' + sd) or (0, 0, 0))[:3])
    return (name, str(where).split(' ')[0], hold,
            tuple(sorted(getattr(d, '__qualname__', type(d).__name__) for d in j.get('props', []))))


def _blank_like(d):
    def blank(p, j2):
        return None
    for k in ('held', 'own_fists', 'quad', 'qz', 'along'):
        if hasattr(d, k):
            setattr(blank, k, getattr(d, k))
    return blank


def turn_faults(poses, tested=None):
    """Redraw each logged person-with-a-prop alone at every 30 degrees. poses: kitchecks.POSES entries (where, name,
    sp, joints, t). Returns faults; `tested` (a set) skips a person and prop already turned."""
    import burnham as B
    import views as V
    tested = set() if tested is None else tested
    out = []
    cam = B.Cam(1.0, 540, 960)
    s, X, Y = 0.8, 540, 700
    keep = B.SS
    B.SS = 1
    for where, name, sp, j, t in poses:
        key = _prop_key(name, j, where)
        if key in tested or not j.get('props'):
            continue
        tested.add(key)
        bare = dict(j)                                    # the same person with each prop drawn as nothing, so the
        bare['props'] = [_blank_like(d) for d in j['props']]   # arms are drawn exactly as with it (held or not)
        for yaw in range(0, 360, 30):
            a = Image.new('RGBA', (B.W, B.H), (0, 0, 0, 0))
            b = Image.new('RGBA', (B.W, B.H), (0, 0, 0, 0))
            try:
                r = V.person(a, cam, X, Y, s, sp, t, yaw, joints=j)
                V.person(b, cam, X, Y, s, sp, t, yaw, joints=bare)
            except Exception as e:                     # a prop that cannot be drawn from some side is a fault too
                out.append(f'PROP TURN: {where}: {name} could not be drawn at {yaw} degrees: {str(e)[:80]}')
                break
            d = r.get('_drawn', {}) if isinstance(r, dict) else {}
            if d.get('held_over_back'):
                out.append(f'PROP TURN: {where}: {name} turned to {yaw} degrees: what they hold is drawn over their back')
                break
            A, Bm = np.asarray(a).astype(int), np.asarray(b).astype(int)
            prop = (np.abs(A - Bm).sum(2) > 60) & (A[..., 3] > 0)
            if prop.sum() < 30:
                continue
            ys, xs = np.nonzero(prop)
            face = math.sin(math.radians(yaw))            # + facing screen right, - facing left (side on only)
            if abs(face) > 0.97 and (xs.mean() - X) * np.sign(face) < -BEHIND * s:
                out.append(f'PROP TURN: {where}: {name} turned to {yaw} degrees: what they hold sits behind them '
                           f'(drawn at a fixed screen angle, not aimed with the body?)')
                break
            if math.cos(math.radians(yaw)) < -0.8:        # from behind: nothing held across the back or shoulders
                torso = np.zeros_like(prop)
                torso[int(Y - 10 * s):int(Y + 440 * s), :] = True
                body = (Bm[..., 3] > 0) & torso
                if body.sum() and (prop & body).sum() > max(300, 0.01 * body.sum()):
                    out.append(f'PROP TURN: {where}: {name} seen from behind ({yaw} degrees): what they hold is drawn '
                               f'across their back')
                    break
    B.SS = keep
    return out


# ------------------------------------------------------------------------------------------------ rule 15
def _radial(mask):
    ys, xs = np.nonzero(mask)
    cy, cx = ys.mean(), xs.mean()
    ang = (np.degrees(np.arctan2(ys - cy, xs - cx)) + 360) % 360
    rad = np.hypot(ys - cy, xs - cx)
    prof = np.zeros(180)
    np.maximum.at(prof, (ang // 2).astype(int) % 180, rad)
    for i in np.nonzero(prof == 0)[0]:                    # fill empty bins from their neighbours
        prof[i] = max(prof[(i - 1) % 180], prof[(i + 1) % 180])
    return prof


def star_fault(mask):
    """A star or regular spikes: the outline's distance from the middle rises and falls in deep, evenly spaced points.
    Returns why, or None for a lumpy, uneven burst."""
    prof = _radial(mask)
    sm = np.convolve(np.r_[prof[-3:], prof, prof[:3]], np.ones(5) / 5, 'same')[3:-3]
    peaks = [i for i in range(180) if sm[i] >= sm[i - 1] and sm[i] > sm[(i + 1) % 180] and
             sm[i] >= sm[(i - 6) % 180] and sm[i] >= sm[(i + 6) % 180]]
    if len(peaks) < 4:
        return None
    lows = [min(sm[(a + k) % 180] for k in range(((b - a) % 180) + 1)) for a, b in zip(peaks, peaks[1:] + peaks[:1])]
    depth = np.mean([sm[p] for p in peaks]) / max(1e-6, np.mean(lows))
    gaps = np.diff(sorted(peaks) + [sorted(peaks)[0] + 180])
    even = np.std(gaps) / max(1e-6, np.mean(gaps))
    tips = np.array([sm[p] for p in peaks])
    same = np.std(tips) / max(1e-6, np.mean(tips))      # a lumpy burst's lobes differ; a drawn spike ring's don't
    if depth > 1.6:
        return f'a star ({len(peaks)} points, {depth:.1f}x deeper than its gaps)'
    if depth > 1.12 and even < 0.2 and same < 0.04:
        return f'regular spikes ({len(peaks)}, evenly spaced, all the same length)'
    return None


def lines_fault(mask):
    """Motion lines: three or more thin streaks lying side by side, parallel."""
    from scipy import ndimage
    lab, n = ndimage.label(mask)
    thin = []
    for k in range(1, min(n, 200) + 1):
        ys, xs = np.nonzero(lab == k)
        if len(xs) < 20:
            continue
        c = np.cov(np.vstack([xs, ys]))
        w, v = np.linalg.eigh(c)
        if w[0] <= 0 or math.sqrt(w[1] / max(w[0], 1e-6)) > 6:
            thin.append(math.degrees(math.atan2(v[1, 1], v[0, 1])) % 180)
    for a in thin:
        if sum(1 for b in thin if min(abs(a - b), 180 - abs(a - b)) < 8) >= 3:
            return f'{len(thin)} thin streaks, three or more parallel (motion lines)'
    return None


def shape_faults(film):
    """Rule 15: each listed effect drawn alone and its shape tested (the off-style list in guides/satire.md)."""
    if not hasattr(film, 'EFFECTS'):
        return ['EFFECT SHAPES: the film has no EFFECTS list ([(name, kind, draw(img))], [] for none): rule 15']
    import burnham as B
    out = []
    keep = B.SS
    B.SS = 1
    for name, kind, draw in film.EFFECTS:
        img = Image.new('RGBA', (B.W, B.H), (0, 0, 0, 0))
        draw(img)
        mask = np.asarray(img)[..., 3] > 0
        if mask.sum() < 50:
            out.append(f'EFFECT SHAPES: {name} draws nothing in its test')
            continue
        why = star_fault(mask) if kind in ('burst', 'flash') else None
        why = why or (lines_fault(mask) if kind not in ('sparks', 'trail', 'bolt') else None)
        if why:
            out.append(f'EFFECT SHAPES: {name} ({kind}) is {why}: off-style (guides/satire.md, The look)')
    B.SS = keep
    return out


# ------------------------------------------------------------------------------------------------ rule 16
def _cam_step(a, b):
    """How far the camera moves between two frames: (metres, degrees, zoom); None if it can't be read."""
    if not all(hasattr(c, 'pos') and hasattr(c, 'f') for c in (a, b)):
        return None
    zoom = abs(math.log(getattr(b, 'focal', 1.0) / getattr(a, 'focal', 1.0)))
    return math.dist(a.pos, b.pos), math.degrees(math.acos(max(-1.0, min(1.0, float(np.dot(a.f, b.f)))))), zoom


def cuts(film):
    """Every cut: (time of the first frame after it, shot before, shot after): a new shot, or the camera jumping (a
    step far bigger than the frames either side: a fast pan or a camera riding a bolt is not a cut)."""
    fps = film.FPS
    end = min(film.DUR, getattr(film, 'BLACK_AT', film.DUR))
    shot_of = lambda t: next((s[0] for s in film.SHOTS if s[1] <= t < s[2]), film.SHOTS[-1][0])
    n = int(end * fps)
    cams = [film.cam_for(i / fps) for i in range(n)]
    shots = [shot_of(i / fps) for i in range(n)]
    steps = [_cam_step(cams[i - 1], cams[i]) if i else None for i in range(n)]
    out = []
    for i in range(1, n):
        if shots[i] != shots[i - 1]:
            out.append((i / fps, shots[i - 1], shots[i]))
            continue
        st = steps[i]
        if st is None:
            continue
        nb = [steps[k] for k in (i - 1, i + 1) if 0 < k < n and steps[k] is not None]
        big = lambda q, j, floor: q[j] > floor and q[j] > 3 * max([x[j] for x in nb] + [floor / 3])
        if big(st, 0, 0.3) or big(st, 1, 12.0) or big(st, 2, 0.25):        # moved, turned or zoomed
            out.append((i / fps, shots[i - 1], shots[i]))
    return out


def direction_faults(film):
    """Rule 16: across every cut, each mover keeps its screen direction and its side of everyone on screen."""
    if not hasattr(film, 'movers'):
        return []
    import audit as A
    fps = film.FPS
    dt = 1.0 / fps
    swaps = getattr(film, 'DIRECTION_SWAPS', ())
    out = []

    def scr(cam, p):
        pr = A._project(film, cam, np.asarray(p, float)[None])
        if pr is None or pr[2][0] < 0.3:
            return None
        x, y = float(pr[0][0]), float(pr[1][0])
        return (x, y) if -100 < x < 1180 and -100 < y < 2020 else None
    for t, before, after in cuts(film):
        t0 = t - dt                                       # the last frame before the cut
        ca, cb = film.cam_for(t0), film.cam_for(t)
        ma = {n: p for n, p in film.movers(t0)}
        mb = {n: p for n, p in film.movers(t)}
        ma2 = {n: p for n, p in film.movers(t0 - dt)}
        mb2 = {n: p for n, p in film.movers(t + dt)}
        people = {}
        for tt, cam, key in ((t0, ca, 0), (t, cb, 1)):
            for th in film.scene(tt):
                if any(s.part in ('body', 'head') for s in th.solids) and th.kind != 'set':
                    q = scr(cam, th.pos)
                    if q:
                        people.setdefault(th.name, [None, None])[key] = q
        for n in set(ma) & set(mb):
            if any(n == s[0] and abs(s[1] - t) < 0.2 for s in swaps):
                continue
            a1, a0 = scr(ca, ma[n]), scr(ca, ma2.get(n, ma[n]))
            b0, b1 = scr(cb, mb[n]), scr(cb, mb2.get(n, mb[n]))
            if not (a1 and b0):
                continue
            if a0 and b1:
                va, vb = a1[0] - a0[0], b1[0] - b0[0]
                if abs(va) > 4 and abs(vb) > 4 and va * vb < 0:
                    out.append(f'DIRECTION: cut at {t:.2f} s ({before} > {after}): {n} moves '
                               f'{"right" if va > 0 else "left"} before it and {"right" if vb > 0 else "left"} after')
            for who, (pa, pb) in people.items():
                if pa and pb and abs(a1[0] - pa[0]) > 25 and abs(b0[0] - pb[0]) > 25 and \
                        (a1[0] - pa[0]) * (b0[0] - pb[0]) < 0:
                    out.append(f'DIRECTION: cut at {t:.2f} s ({before} > {after}): {n} is on {who}\'s '
                               f'{"right" if a1[0] > pa[0] else "left"} (screen) before it and on the other side after')
    return out


# ------------------------------------------------------------------------------------------------ rule 17
def _silhouette(film, cam, th, size):
    """A figure's solids drawn as a mask on screen (each capsule as a run of discs)."""
    import audit as A
    m = Image.new('L', size, 0)
    d = ImageDraw.Draw(m)
    for s in th.solids:
        if s.kind not in ('capsule', 'sphere'):
            continue
        pts = np.array([s.a + (s.b - s.a) * u for u in np.linspace(0, 1, 8)])
        pr = A._project(film, cam, pts)
        if pr is None:
            continue
        top = A._project(film, cam, pts + np.array([0.0, s.r, 0.0]))
        for x, y, z, ty in zip(pr[0], pr[1], pr[2], top[1]):
            if z > 0.2:
                r = abs(y - ty)
                d.ellipse((x - r, y - r, x + r, y + r), fill=255)
    return np.asarray(m) > 0


def hide_faults(film, step=3):
    """Rule 17: an effect behind a figure is never drawn over it (robots and creatures too, Prepper note 13)."""
    if not (hasattr(film, 'effect_points') and hasattr(film, 'scene')):
        return []
    switch = getattr(film, 'EFFECT_SWITCH', None)
    if not switch:
        return ['EFFECTS HIDDEN: effect_points(t) but no EFFECT_SWITCH ([(module, function)] that draws the effects)']
    import audit as A
    B = getattr(film, 'B', None)
    out, seen = [], set()
    end = min(film.DUR, getattr(film, 'BLACK_AT', film.DUR))
    draw = getattr(film, 'picture', None) or film.frame_image
    for i in range(0, int(end * film.FPS), step):
        t = i / film.FPS
        pts = film.effect_points(t)
        if not pts:
            continue
        cam = film.cam_for(t)
        figs = [th for th in film.scene(t) if th.kind != 'set' and any(s.part in ('body', 'head') for s in th.solids)]
        cands = []
        for en, p, r in pts:
            pe = A._project(film, cam, np.asarray(p, float)[None])
            if pe is None or pe[2][0] < 0.3:
                continue
            for th in figs:
                pf = A._project(film, cam, np.asarray(th.pos, float)[None])
                if pf is None or pe[2][0] < pf[2][0] + 0.15:
                    continue                              # the effect is in front of this figure: may cover it
                x0, y0, x1, y1 = A._screen_boxes(film, cam, th.lo[None], th.hi[None])[2][0]
                if x0 <= pe[0][0] <= x1 and y0 <= pe[1][0] <= y1 and (th.name, en) not in seen:
                    k = abs(float(A._project(film, cam, np.asarray(p, float)[None] + [0, r, 0])[1][0]) - pe[1][0])
                    cands.append((th, en, (pe[0][0], pe[1][0]), max(6.0, k)))
        if not cands:
            continue
        if B is not None:
            B.SS = 1
        full = np.asarray(draw(t).convert('RGB').resize((1080, 1920))).astype(int)
        saved = []
        for mod, fn in switch:
            m = importlib.import_module(mod) if isinstance(mod, str) else mod
            saved.append((m, fn, getattr(m, fn)))
            setattr(m, fn, lambda *a, **k: None)
        try:
            bare = np.asarray(draw(t).convert('RGB').resize((1080, 1920))).astype(int)
        finally:
            for m, fn, f in saved:
                setattr(m, fn, f)
        fx = np.abs(full - bare).sum(2) > 40
        for th, en, (x, y), r in cands:
            sil = _silhouette(film, cam, th, (1080, 1920))
            disc = np.zeros_like(sil)
            yy, xx = np.ogrid[:1920, :1080]
            disc[(xx - x) ** 2 + (yy - y) ** 2 <= (1.5 * r) ** 2] = True
            n = int((fx & sil & disc).sum())
            if n > 40:
                seen.add((th.name, en))
                out.append(f'EFFECTS HIDDEN: {t:.2f} s: the {en} behind {th.name} is drawn over them ({n} px)')
    return out


# ------------------------------------------------------------------------------------------------ rule 18
def _measure(film, name, t, at, size):
    import audit as A
    p = np.asarray(at(t) if callable(at) else at, float)
    cam = film.cam_for(t)
    pr = A._project(film, cam, np.array([p, p + [0, size, 0]]))
    if pr is None or pr[2][0] < 0.2:
        return None
    x, y = float(pr[0][0]), float(pr[1][0])
    return x, y, abs(float(pr[1][1]) - y)


def readability_faults(film):
    """Rule 18: every prop a joke needs is at least READABLE px on screen (of 1920) wherever it is listed."""
    if not hasattr(film, 'JOKE_PROPS'):
        return ['READABILITY: the film has no JOKE_PROPS ([(name, [times], where, size m)], [] for none): rule 18']
    out = []
    for name, times, at, size in film.JOKE_PROPS:
        for t in times:
            m = _measure(film, name, t, at, size)
            if m is None or not (0 <= m[0] <= 1080 and 0 <= m[1] <= 1920):
                out.append(f'READABILITY: {t:.2f} s: the {name} is not on screen')
            elif m[2] < READABLE:
                out.append(f'READABILITY: {t:.2f} s: the {name} is {m[2]:.0f} px on screen (under {READABLE} of 1920: '
                           f'make it bigger or bring it nearer)')
    return out


def sheet(film, out):
    """Each joke prop at phone size (the whole frame at about a phone's scale), boxed, with its size on screen."""
    B = getattr(film, 'B', None)
    if B is not None:
        B.SS = 1
    tiles = []
    f = ImageFont.truetype(FONT, 18)
    draw = getattr(film, 'frame_image', None) or film.picture
    for name, times, at, size in getattr(film, 'JOKE_PROPS', []):
        for t in times:
            m = _measure(film, name, t, at, size)
            im = draw(t).convert('RGB').resize((1080, 1920))
            k = 390 / 1080                                # a phone shows the frame about 390 points wide
            im = im.resize((390, 693))
            d = ImageDraw.Draw(im)
            if m:
                x, y, h = m[0] * k, m[1] * k, max(6, m[2] * k)
                d.rectangle((x - h, y - h * 1.2, x + h, y + h * 0.3), outline=(255, 0, 0), width=2)
            lab = f'{name} {t:.1f}s: {m[2]:.0f} px' if m else f'{name} {t:.1f}s: off screen'
            ok = m and m[2] >= READABLE
            d.rectangle((0, 0, 390, 26), fill=(20, 120, 40) if ok else (180, 30, 30))
            d.text((6, 3), lab, font=f, fill=(255, 255, 255))
            tiles.append(im)
    if not tiles:
        return None
    cols = min(5, len(tiles))
    img = Image.new('RGB', (390 * cols, 693 * ((len(tiles) + cols - 1) // cols)), (255, 255, 255))
    for i, im in enumerate(tiles):
        img.paste(im, ((i % cols) * 390, (i // cols) * 693))
    img.save(out, quality=86)
    return out


def faults(film):
    """Everything here but the prop test (that runs on pre-flight's drawing pass)."""
    return shape_faults(film) + readability_faults(film) + direction_faults(film) + hide_faults(film)


def main():
    film = importlib.import_module(sys.argv[1])
    import kitchecks
    import figure as F
    kitchecks.install()
    B = getattr(film, 'B', None)
    if B is not None:
        B.SS = 1
    draw = getattr(film, 'picture', None) or film.frame_image
    n0 = len(kitchecks.POSES)
    for i in range(0, int(min(film.DUR, getattr(film, 'BLACK_AT', film.DUR)) * film.FPS), 3):
        F.CONTEXT['where'] = f'{i / film.FPS:.2f}s'
        draw(i / film.FPS)
    fs = turn_faults(kitchecks.POSES[n0:]) + faults(film)
    print('\n'.join(fs) or 'viewchecks: clean')
    if len(sys.argv) > 2:
        print('readability sheet:', sheet(film, sys.argv[2]))


if __name__ == '__main__':
    main()
