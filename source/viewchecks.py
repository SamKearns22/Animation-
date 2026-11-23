#!/usr/bin/env python3
"""viewchecks: the checks of what the camera shows (guides/film-quality-rules.md rules S7, 16-18 and 20), for any film.

Why: Prepper Minister's notes 11-16, 20, 45 and 48 (props across a back, star flashes), 13 (effects drawn over people),
57 (the plasma swapped sides of Wes across a cut) and 2, 27, 41, 46 (props too small to read on a phone) were all things
a computer can find. Each is tested on the result:

  props turned (rule 20)   every person drawn holding something (views.py, logged by kitchecks) is redrawn alone at
                           every 30 degrees: from behind nothing held is drawn over the back; from the side the prop
                           stays on the side they face (a prop at a fixed screen angle ends up behind them)
  effect shapes (rule S7)  EFFECTS = [(name, kind, draw(img))]: each effect drawn alone; a 'burst' must be a lumpy,
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
    for k in ('held', 'own_fists', 'quad', 'qz', 'along', 'rear_under'):
        if hasattr(d, k):
            setattr(blank, k, getattr(d, k))
    return blank


def turn_faults(poses, tested=None):
    """Redraw each logged person-with-a-prop alone at every 30 degrees. poses: kitchecks.POSES entries (where, name,
    sp, joints, t). Returns faults; `tested` (a set) skips a person and prop already turned."""
    import body as B
    import views as V
    tested = set() if tested is None else tested
    out = []
    cam = B.Cam(1.0, 540, 960)
    s, X, Y = 0.8, 540, 700
    keep = B.SS
    B.SS = 1
    for where, name, sp, j, t in poses:
        key = _prop_key(name, j, where)
        held = any(getattr(d, 'held', False) or getattr(d, 'own_fists', False) for d in j.get('props', [])) or \
            bool(j.get('grip'))
        if key in tested or not held:                     # only things held (a drawn hand or leg is not)
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
            if math.cos(math.radians(yaw)) < -0.8:        # from behind: nothing held across the back (the torso,
                torso = np.zeros_like(prop)               # shoulders to hips; past its sides a held thing may show)
                torso[int(Y - 10 * s):int(Y + 440 * s), int(X - 110 * s):int(X + 110 * s)] = True
                body = (Bm[..., 3] > 0) & torso
                if body.sum() and (prop & body).sum() > max(300, 0.01 * body.sum()):
                    out.append(f'PROP TURN: {where}: {name} seen from behind ({yaw} degrees): what they hold is drawn '
                               f'across their back')
                    break
    B.SS = keep
    return out


# ------------------------------------------------------------------------------------------------ rule S7
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
    """Rule S7: each listed effect drawn alone and its shape tested (the off-style list in guides/satire.md)."""
    if not hasattr(film, 'EFFECTS'):
        return ['EFFECT SHAPES: the film has no EFFECTS list ([(name, kind, draw(img))], [] for none): rule S7']
    import body as B
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
def _silhouette(film, cam, th, size, grow=1.0):
    """A figure's solids drawn as a mask on screen (each capsule as a run of discs, `grow` times their size)."""
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
                r = abs(y - ty) * grow + (grow - 1.0) * 8
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
        figs = list(film.scene(t))                    # rule 17 (Sam, 20 Nov): anything against anything, sets included
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


def layer_faults(shot, length, fps=12, step=2, allowed=(), label=''):
    """Rule 17 for any picture painted in layers (practice clips, flat-painted shots): every standing thing is listed by
    the shot as (name, distance, draw) through shot(t, record=list). Each thing is drawn alone on a clear sheet; where
    two things overlap, the finished picture must show the NEARER one. allowed = [(name_a, name_b, reason)], names
    matched by their start (a hand on a held gun, people inside a car, see-through glass or smoke). A shot that lists
    nothing is a fault itself: the check cannot see it."""
    out, seen = [], set()
    ok = [(a, b) for a, b, _ in allowed]

    def okay(n1, n2):
        return any((n1.startswith(a) and n2.startswith(b)) or (n1.startswith(b) and n2.startswith(a)) for a, b in ok)
    for i in range(0, int(round(length * fps)), step):
        t = i / fps
        rec = []
        full = np.asarray(shot(t, record=rec).convert('RGB')).astype(np.int32)
        if not rec:
            return [f'LAYERS UNLISTED: {label} lists no things, so nothing in it can be checked (rule 17)']
        alone = []
        front = np.full(full.shape[:2], np.inf)       # the nearest thing covering each pixel, solid or see-through
        for e in rec:
            name, d, fn = e[:3]
            if fn is None:                           # a solid or a camera listed for solid_faults: nothing drawn
                continue
            sheet = Image.new('RGBA', (full.shape[1], full.shape[0]), (0, 0, 0, 0))
            fn(sheet)
            bb = sheet.getchannel('A').point(lambda v: 255 if v > 200 else 0).getbbox()
            if bb:                                   # kept as a crop with its box: only overlaps are compared
                a = np.asarray(sheet.crop(bb)).astype(np.int32)
                alone.append((name, d, bb, a[..., 3] > 200, a[..., :3]))
                vb = sheet.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox()
                veil = np.asarray(sheet.getchannel('A').crop(vb)) > 40
                fy, fx = slice(vb[1], vb[3]), slice(vb[0], vb[2])
                front[fy, fx] = np.where(veil, np.minimum(front[fy, fx], d), front[fy, fx])
        best = np.full(full.shape[:2], 1 << 20, np.int32)   # each pixel credited to the thing it matches best
        owner = np.full(full.shape[:2], -1, np.int16)
        for k, (_, _, (x0, y0, x1, y1), m, c) in enumerate(alone):
            e = np.abs(full[y0:y1, x0:x1] - c).sum(2).astype(np.int32)
            e[~m] = 1 << 20
            bsub, osub = best[y0:y1, x0:x1], owner[y0:y1, x0:x1]
            take = e < bsub
            bsub[take], osub[take] = e[take], k
        for ka in range(len(alone)):
            for kb in range(len(alone)):
                na, da, ba, ma, ca = alone[ka]
                nb, db, bbx, mb, cb = alone[kb]
                if not da < db or (na, nb) in seen or okay(na, nb):
                    continue
                x0, y0 = max(ba[0], bbx[0]), max(ba[1], bbx[1])
                x1, y1 = min(ba[2], bbx[2]), min(ba[3], bbx[3])
                if x1 - x0 < 4 or y1 - y0 < 4:
                    continue                          # their boxes never meet
                sa = (slice(y0 - ba[1], y1 - ba[1]), slice(x0 - ba[0], x1 - ba[0]))
                sb = (slice(y0 - bbx[1], y1 - bbx[1]), slice(x0 - bbx[0], x1 - bbx[0]))
                both = (ma[sa] & mb[sb] & (np.abs(ca[sa].astype(int) - cb[sb]).sum(2) > 60)   # the two look different
                        & (front[y0:y1, x0:x1] >= da))         # and nothing nearer (glass included) is in front of both
                o = owner[y0:y1, x0:x1][both]
                wrong, n = int((o == kb).sum()), int(((o == kb) | (o == ka)).sum())
                if wrong > max(4e-5 * full.shape[0] * full.shape[1], 0.3 * n):   # a speck of matching paint is not a fault
                    seen.add((na, nb))
                    out.append(f'LAYERS: {label} {t:.2f} s: {nb} (farther) is drawn over {na} (nearer), {wrong} px')
    return out


def _bone_in(base, only):
    """A bone sample belongs to the parts a face rubs out when both its joints do."""
    return any(nm == base and a in only and b in only for a, b, nm in BONES)


def _in_poly(x, y, poly):
    inside = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            inside = not inside
    return inside


BONES = (('shL', 'elL', 'upper arm L'), ('elL', 'wrL', 'forearm L'), ('shR', 'elR', 'upper arm R'),
         ('elR', 'wrR', 'forearm R'), ('hipL', 'kneeL', 'thigh L'), ('kneeL', 'footL', 'shin L'),
         ('hipR', 'kneeR', 'thigh R'), ('kneeR', 'footR', 'shin R'), ('neck', 'chest', 'chest'),
         ('chest', 'waist', 'belly'),
         # rule 17, GTA v7 note 2 (Sam 21 Nov, the see-through bonnet at 0.67 s): the vest between the waist and the
         # hips showed over the bonnet, and no sample lay there (waist above the bonnet line, hips hidden below it)
         ('waist', 'hips', 'lower belly'), ('hips', 'hipL', 'pelvis L'), ('hips', 'hipR', 'pelvis R'),
         ('neck', 'shL', 'collar L'), ('neck', 'shR', 'collar R'))


def bone_samples(pts3):
    """The body's joints plus points along every bone (thirds), so a limb half through a door is seen, not only its
    ends (humancheck, proposal big-body-moves: a sausage arm cut from its shoulder passed the joints-only test)."""
    d = dict(pts3)
    out = list(pts3)
    for a, b, nm in BONES:
        if a in d and b in d:
            pa, pb = np.asarray(d[a], float), np.asarray(d[b], float)
            out += [(f'{nm} ({k}/3)', tuple(pa + (pb - pa) * k / 3)) for k in (1, 2)]
    return out


def _hidden_by(cam, q, solids, skip, step=0.03):
    """The first listed solid the line from the lens to body point q passes through before it gets there (None)."""
    cp = np.asarray(cam.pos, float)
    qq = np.asarray(q, float)
    L = float(np.linalg.norm(qq - cp))
    n = int(L / step)
    for k in range(1, n - 2):                      # stop 6-9 cm short of the point: its own surface is not a cover
        p = tuple(cp + (qq - cp) * (k * step / L))
        for sn, test in solids:
            hit = test(p)
            if hit and hit not in skip and sn not in skip and not any(g in hit for g in ('glass', 'screen')):
                return hit                         # glass tints what is behind it, never hides it
    return None


OUTLINE_GRID = 10      # pixels (of 1080) between the outline spots tested
OUTLINE_MIN = 4        # patch spots behind one solid that make a fault (a patch about 30 x 30 px)


def _unproject(cam, X, Y, z):
    """The world point at camera depth z that the frame point (X, Y) (1080 x 1920 pixels) shows (sets.Cam)."""
    x, y = X - 540 - cam.shake[0], Y - 960 - cam.shake[1]
    if getattr(cam, 'roll', 0.0):
        c, s_ = math.cos(-cam.roll), math.sin(-cam.roll)
        x, y = x * c - y * s_, x * s_ + y * c
    a, b = x * z / cam.focal, -y * z / cam.focal
    return tuple(cam.pos[i] + cam.f[i] * z + cam.r[i] * a + cam.u[i] * b for i in range(3))


def outline_shows(cam, shown, sc, samples, solids, skip):
    """Rule 17, the drawn outline (GTA v7 note 2, Sam 21 Nov, "see through the bonnet to Jason", a repeat of v4 note 3):
    the bone points passed, because the vest's edge showed over the bonnet between them. So every spot of the person
    as drawn (shown: the pixels that change when the person is hidden) is tested on a grid: its depth is the nearest
    body point's on screen, and the line from the lens to it must not pass through a solid first.
    -> [(solid, spots, (X, Y) of the first)]"""
    if not all(hasattr(cam, k) for k in ('f', 'r', 'u', 'focal', 'shake')):
        return []
    pts = [(cam.project(q)[0], cam.depth(q)) for _, q in samples if cam.depth(q) > 0.05]
    if not pts:
        return []
    P = np.array([p for p, _ in pts], float)
    D = np.array([d for _, d in pts], float)
    g = max(1, int(OUTLINE_GRID * sc))
    ys, xs = np.nonzero(shown[::g, ::g])
    grid = {}
    for yy, xx in zip(ys, xs):
        X, Y = xx * g / sc, yy * g / sc
        k = int(np.argmin(((P - (X, Y)) ** 2).sum(1)))
        q = _unproject(cam, X, Y, float(D[k]))
        hit = _hidden_by(cam, q, solids, skip, step=0.05)
        if hit:
            grid[(int(yy), int(xx))] = hit
    hits = {}                                   # only spots inside a patch count: a hit neighbour across AND down
    for (yy, xx), hit in sorted(grid.items()):  # (a line of hair grazing a rail's edge is one row: v7 0.00 s)
        if hit in (grid.get((yy, xx - 1)), grid.get((yy, xx + 1))) and hit in (grid.get((yy - 1, xx)), grid.get((yy + 1, xx))):
            h = hits.setdefault(hit, [0, (int(xx * g / sc), int(yy * g / sc))])
            h[0] += 1
    return [(hit, n, at) for hit, (n, at) in hits.items() if n >= OUTLINE_MIN]


def solid_faults(shot, length, fps=12, step=1, label='', frames=None):
    """Rule 17's other half: what layer_faults cannot see (Grand Theft Autism shot 4, chat 11: a body drawn through a
    car door, a chest floating over an erased waist, people sunk into the pavement, all passed twice by layer_faults).
    Every person, every frame. The shot lists, as a 4th item of a record entry, an info dict:
      solid ......... fn(world point) -> the solid's name or None (a car's panels, a shop wall, the ground): listed
                      on an entry whose draw is None
      cam ........... the frame's camera (one entry is enough)
      pts3 .......... [(part, world point)] a person's body (hips, knees, feet, shoulders, elbows, hands, gun)
      may_touch ..... names of solids this person may be inside (their own seat's car cabin is not a solid anyway)
      erase ......... [(name, world polygon[, parts])] faces the shot rubs this person out behind: every body point inside a
                      face's picture must be BEHIND that face (else a waist rubbed out in front of a door)
      ground_px ..... (X, Y) canvas pixels of the ground point under the feet; height_px, the standing height in
                      canvas pixels (None when crouched): drawn alone, the lowest painted row near the feet must be
                      within 3% of their height of Y (sunk or floating) and a standing person at least 85% as tall
    Faults are grouped per person and kind: first time, how many frames."""
    found = {}

    def note(who, kind, t, text):
        k = (who, kind)
        if k not in found:
            found[k] = [t, 0, text]
        found[k][1] += 1
    idx = frames if frames is not None else range(0, int(round(length * fps)), step)
    for i in idx:
        t = i / fps
        rec = []
        full = shot(t, record=rec)
        W, H = full.size
        infos = [(e[0], e[2], e[3]) for e in rec if len(e) > 3 and e[3]]
        solids = [(n, inf['solid']) for n, _, inf in infos if 'solid' in inf]
        cam = next((inf['cam'] for _, _, inf in infos if 'cam' in inf), None)
        for who, fn, inf in infos:
            samples = bone_samples(inf.get('pts3', []))
            for part, q in samples:
                for sn, test in solids:
                    hit = test(q)
                    if hit and hit not in inf.get('may_touch', ()) and sn not in inf.get('may_touch', ()):
                        note(who, 'solid ' + hit, t, f'{who}: {part} is inside {hit} (a body through a solid)')
                        break
            if cam is not None and inf.get('erase'):
                for er in inf['erase']:
                    fname, poly = er[:2]
                    only = er[2] if len(er) > 2 else None   # the body parts this face rubs out (a split drawing)
                    pp = cam.clip(poly) if hasattr(cam, 'clip') else [cam.project(q)[0] for q in poly]
                    if len(pp) < 3:
                        continue
                    a, b, c = (np.asarray(poly[k], float) for k in range(3))
                    nrm = np.cross(b - a, c - a)
                    cp = np.asarray(cam.pos, float)
                    for part, q in samples:
                        base = part.split(' (')[0]
                        if cam.depth(q) < 0.05 or (only is not None and part not in only and
                                                   not _bone_in(base, only)):
                            continue
                        (X, Y), _ = cam.project(q)
                        if not _in_poly(X, Y, pp):
                            continue
                        den = float(nrm @ (np.asarray(q, float) - cp))
                        if abs(den) < 1e-9:
                            continue
                        u = float(nrm @ (a - cp)) / den        # where the face cuts the ray: 1 = at the point
                        if u > 1.02:
                            note(who, 'erase ' + fname, t, f'{who}: {part} is rubbed out by {fname} but is in front of it')
                            break
            if cam is not None and inf.get('toggle'):       # a part behind a solid must not show (knees through a
                inf['toggle'](False)                         # bonnet, legs in a door frame: GTA notes 2, 3, 4, 11)
                try:
                    bare = np.asarray(shot(t).convert('RGB'), np.int16)
                finally:
                    inf['toggle'](True)
                diff = np.abs(np.asarray(full.convert('RGB'), np.int16) - bare).sum(2) > 40
                sc = W / 1080.0
                for part, q in samples:
                    if cam.depth(q) < 0.05:
                        continue
                    hit = _hidden_by(cam, q, solids, set(inf.get('may_touch', ())) | set(inf.get('see_through', ())))
                    if not hit:
                        continue
                    (X, Y), _ = cam.project(q)
                    X, Y = int(X * sc), int(Y * sc)
                    if 2 <= X < W - 2 and 2 <= Y < H - 2 and diff[Y - 2:Y + 3, X - 2:X + 3].mean() > 0.5:
                        note(who, 'shows ' + hit, t, f'{who}: {part} shows through {hit} (it is behind it)')
                for hit, n, (X, Y) in outline_shows(cam, diff, sc, samples, solids,
                                                    set(inf.get('may_touch', ())) | set(inf.get('see_through', ()))):
                    note(who, 'shows ' + hit, t, f'{who}: the drawn body shows through {hit} at ({X}, {Y}) '
                                                 f'({n} spots of its outline are behind it)')
            if inf.get('ground_px') and fn is not None:
                gx, gy = inf['ground_px']
                sc = W / 1080.0                          # ground_px is in 1080 x 1920 pixels
                gx, gy = gx * sc, gy * sc
                if not (0 <= gx < W and 0 <= gy < H):
                    continue
                sheet = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                fn(sheet)
                al = np.asarray(sheet.getchannel('A')) > 128
                hp = (inf.get('height_px') or 0) * sc
                band = max(6, int(0.18 * (hp or 200 * sc)))
                x0, x1 = max(0, int(gx - band)), min(W, int(gx + band))
                rows = np.nonzero(al[:, x0:x1].any(1))[0]
                if not len(rows):
                    continue
                low, top = rows.max(), np.nonzero(al.any(1))[0].min()
                tall = low - top
                lim = max(2.5 * sc, 0.03 * (hp or tall))   # 2.5 px of 1920 is a speck
                if low >= H - 2:
                    continue                             # the feet are below the frame
                if low > gy + lim:
                    note(who, 'sunk', t, f'{who}: feet {(low - gy) / sc:.0f} px below the ground (sunk into it)')
                elif low < gy - lim and not inf.get('airborne'):
                    note(who, 'floating', t, f'{who}: feet {(gy - low) / sc:.0f} px above the ground (floating)')
                if hp and top > 1 and tall < 0.85 * hp:
                    note(who, 'small', t, f'{who}: drawn {tall / sc:.0f} px tall where the camera makes them {hp / sc:.0f}')
    out = []
    for (who, kind), (t0, n, text) in sorted(found.items(), key=lambda e: e[1][0]):
        out.append(f'BODY: {label} {t0:.2f} s: {text} ({n} frame{"s" if n > 1 else ""})')
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
