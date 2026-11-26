#!/usr/bin/env python3
"""kitinputs: the shared kits hand every check what it needs (named-lines change 3, Sam's Y 23 Nov).

Why: 37 of Milburn's 61 pre-flight lines were checks that could not see the film, because the film never handed them
their inputs (who is in each shot, cameras, facings, lists), and Blessed only got a short, real list after its own
code built those inputs (7 check fixes inside one film). Milburn was drawn with the places kit (story/FILM-places.txt)
and the people kit (views.person), which already know where everyone is: this reads it from the drawing itself, so a
new film starts with it and no film code is written for the checks.

How: survey(film) draws the film at SURVEY_FPS with cover.py's tap on (cover.survey_record): every person the people
kit draws (who, screen box, scale, which way they face, depth: from the places view, or from their drawn size), the
places view painted, every piece with words on it, and a small grey copy of the frame. fill(film) then gives the
checks, ONLY where the film has not given its own (the film's always wins), and says each one out loud:
  roster ........ {shot: who is on screen}: the shot cast check (rule 14), in place of the collision audit's roster
  pop_faults .... rule 6 from the drawing: someone appearing or vanishing mid-shot away from the frame's edge
  PLAN .......... the film's plan with: a camera for each shot painted from one places view (its height, horizon,
                  lens: a level camera); the facing of each person seen through a level camera (from their drawn yaw);
                  the film's own SHOT_MARKS (module level) when the plan has none, else who the shot draws
  cam_for(t) .... the camera's movement MEASURED from the frames (the picture's shift and zoom between samples),
                  for the camera-feel check (rule 72)
  EFFECTS ....... [] when the film's HAS says it has no effects (said, not assumed)
  JOKE_PROPS .... every places piece with words on it, measured where drawn (its box on screen, rule 18)
  LINE_SUBJECTS . each person of the film's CAST (people kit) drawn alone, large (the line-work check)
  PROP_SIZES .... each places piece whose kind has a real size (sizes.SIZES), in metres from the places file
  OUTFIT ........ each kit person's top hem (the description's `hem`) as the clothes check reads it
Not given yet (named, so it stays a line): audits (each body alone on every frame: needs the render's drawing pass to
keep each person's own drawing; see the lessons report), and anyone the film draws outside the people kit (Milburn's
tiny figures in shot 2b are drawn by its own set code, so no shared tool can see them).

MAP
  survey 70 | roster and pops 140 | plan 185 | camera 250 | lists 300 | fill and Film 345 | main 410

    python3 source/kitinputs.py FILM          what the kits hand the checks for this film (and what they cannot)
    python3 source/kitinputs.py test          the shared parts on made-up surveys (kittest kit_inputs)
"""
import fnmatch
import importlib
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
SURVEY_FPS = 4.0          # samples a second (each is one drawing of the frame); at least MIN_PER_SHOT a shot
MIN_PER_SHOT = 3
EDGE = 12                 # px: a box this near the frame's edge left or entered by the edge (not a pop)
THUMB = (135, 240)        # the grey copy of each frame the camera is measured on
_CACHE = {}


# ---------------------------------------------------------------------------------------------- survey
def _times(film):
    out = []
    for s in getattr(film, 'SHOTS', []):
        name, a, b = s[0], s[1], s[2]
        n = max(MIN_PER_SHOT, int((b - a) * SURVEY_FPS))
        out += [(str(name), a + (k + 0.5) * (b - a) / n) for k in range(n)]
    return out


def _one(args):
    film_name, shot, t = args
    film = sys.modules.get(film_name) or importlib.import_module(film_name)
    import cover
    try:
        r = cover.survey_record(film, t)
    except Exception as e:                       # a frame that cannot be drawn is said, never skipped in silence
        return dict(t=t, shot=shot, error=f'{type(e).__name__}: {e}'[:200], people=[], texts=[], view=None)
    r['shot'] = shot
    r['thumb'] = np.asarray(r.pop('image').convert('L').resize(THUMB), np.float32)   # the camera is measured on it
    return r


def survey(film, pool=True):
    """[record] in film order, one per sample (see the MAP); cached for the run."""
    key = getattr(film, '__name__', str(film))
    if key in _CACHE:
        return _CACHE[key]
    import cover
    if cover.picture_fn(film) is None:
        _CACHE[key] = []
        return []
    args = [(film.__name__, s, t) for s, t in _times(film)]
    if pool and len(args) > 6:
        from multiprocessing import Pool
        with Pool(os.cpu_count()) as p:
            out = p.map(_one, args, chunksize=4)
    else:
        out = [_one(a) for a in args]
    _CACHE[key] = out
    return out


# ---------------------------------------------------------------------------------------------- roster and pops
def roster(sv):
    out = {}
    for r in sv:
        out.setdefault(r['shot'], set())
        for p in r['people']:
            if p.get('box'):
                out[r['shot']].add(p['who'])
    return out


def _at_edge(box, size=(1080, 1920)):
    return box[0] <= EDGE or box[1] <= EDGE or box[2] >= size[0] - EDGE or box[3] >= size[1] - EDGE


def pop_faults(film, sv):
    """Rule 6 from the drawing: within a shot, someone on screen in one sample and gone in the next (or the other way)
    while away from the frame's edge, unless the film's ALLOWED_POPS names it."""
    allowed = list(getattr(film, 'ALLOWED_POPS', ()))
    out, seen = [], set()
    by_shot = {}
    for r in sv:
        by_shot.setdefault(r['shot'], []).append(r)
    boxes = lambda r: {p['who']: p['box'] for p in r['people'] if p.get('box')}
    for shot, rs in by_shot.items():
        for i, (a, b) in enumerate(zip(rs, rs[1:])):
            pa, pb = boxes(a), boxes(b)
            for who, box, t, verb in [(w, x, a['t'], 'vanishes') for w, x in pa.items() if w not in pb] + \
                                     [(w, x, b['t'], 'appears') for w, x in pb.items() if w not in pa]:
                if _at_edge(box) or (shot, who, verb) in seen:
                    continue
                # Open Wounds chat 32 (pre-flight said a guest "vanishes mid-shot" at 33.88-34.12 s: drawn frame by
                # frame he runs off the left edge at 33.96 s; the samples, 0.24 s apart, caught him 146 px in, then
                # gone): a runner between samples is carried on at the speed the samples show; reaching the edge by
                # the next sample is leaving (or entering) through it, not a pop
                other = boxes(rs[i - 1]).get(who) if verb == 'vanishes' and i > 0 else \
                    boxes(rs[i + 2]).get(who) if verb == 'appears' and i + 2 < len(rs) else None
                if other is not None:
                    t_other = rs[i - 1]['t'] if verb == 'vanishes' else rs[i + 2]['t']
                    t_gap = (b['t'] if verb == 'vanishes' else a['t']) - t
                    k = t_gap / (t - t_other) if t != t_other else 0.0
                    carried = [box[n] + (box[n] - other[n]) * k for n in range(4)]
                    if _at_edge(carried) or carried[2] < 0 or carried[0] > 1080:
                        continue
                if any(fnmatch.fnmatchcase(who, n) and t0 <= t <= t1 for n, t0, t1, *_ in allowed):
                    continue
                seen.add((shot, who, verb))
                out.append(f'pop-in (rule 6, from the drawing): shot {shot}: {who} {verb} mid-shot between '
                           f'{a["t"]:.2f} and {b["t"]:.2f} s, away from the frame\'s edge (gone through a door? '
                           f'ALLOWED_POPS with why)')
    return out


# ---------------------------------------------------------------------------------------------- plan
def shot_views(sv):
    """{shot: (view name, camera, people depths, place)} for shots painted from ONE places view in every sample."""
    seen = {}
    for r in sv:
        seen.setdefault(r['shot'], []).append(r['view'])
    out = {}
    for shot, vs in seen.items():
        names = {v[0] if v else None for v in vs}
        if len(names) == 1 and None not in names:
            out[shot] = vs[0]
    return out


def facing_of(yaw):
    """Plan degrees (0 north, 90 east) for a person drawn at `yaw` through a level camera looking north (the places
    convention: x across, depth away from the lens): views.project puts their front at screen x = sin(yaw), nearer =
    cos(yaw), so they face 180 - yaw."""
    return (180.0 - float(yaw or 0.0)) % 360.0


def plan(film, sv):
    """(the film's PLAN with what the kits add, the lines saying what was added). None if the film has no PLAN."""
    import copy
    src = getattr(film, 'PLAN', None)
    if src is None:
        return None, []
    if isinstance(src, str):
        src = importlib.import_module(src)
    P = copy.deepcopy(src) if isinstance(src, dict) else {k: copy.deepcopy(getattr(src, k)) for k in dir(src)
                                                          if k.isupper()}
    said = []
    cams = P.setdefault('CAMS', {})
    import plan as PLN
    have = PLN.Plan(P)
    for shot, (vname, cam, _, place) in shot_views(sv).items():
        if have.cam_for_shot(shot) is None and cam:
            cams[shot] = dict(up=cam.get('up'), look='level', lens=cam.get('lens'), horizon=cam.get('horizon'),
                              view=vname, kit=True)
            said.append(f'camera for shot {shot}: the places view "{vname}"')
    full = PLN.Plan(P)
    yaws = {}
    for r in sv:
        c = full.cam_for_shot(r['shot'])
        lvl = r['view'] is not None or (c is not None and c.get('look') == 'level')
        for p in r['people']:
            if p.get('box') and p.get('yaw') is not None and lvl:
                yaws.setdefault(p['who'], []).append(p['yaw'])
    for lb, p in (P.get('PEOPLE') or {}).items():
        who = p.get('who', lb)
        if 'facing' not in p and yaws.get(who):
            p['facing'] = facing_of(float(np.median(yaws[who])))
            said.append(f'{lb} faces {p["facing"]:.0f} degrees (drawn yaw {np.median(yaws[who]):.0f} through a level '
                        f'camera)')
    if not P.get('SHOT_MARKS'):
        marks = getattr(film, 'SHOT_MARKS', None)
        if marks is not None:
            P['SHOT_MARKS'] = marks
            said.append('SHOT_MARKS: the film\'s own (outside its PLAN)')
        elif sv and P.get('PEOPLE'):
            people = set(P['PEOPLE'])
            P['SHOT_MARKS'] = {s: sorted(w for w in ws if w in people) for s, ws in roster(sv).items()}
            said.append('SHOT_MARKS: who each shot draws')
    return P, said


# ---------------------------------------------------------------------------------------------- camera
def _shift_zoom(a, b):
    """How the picture moved from a to b: (dx, dy) in thumb px and a zoom, by phase correlation over a few zooms."""
    from PIL import Image
    best = (0.0, 0.0, 1.0, -1.0)
    A = a - a.mean()
    for z in (0.94, 0.97, 1.0, 1.03, 1.06):
        if z == 1.0:
            Bz = b
        else:
            im = Image.fromarray(b).resize((int(THUMB[0] * z), int(THUMB[1] * z)))
            w, h = im.size
            x0, y0 = (w - THUMB[0]) // 2, (h - THUMB[1]) // 2
            if z > 1:
                Bz = np.asarray(im.crop((x0, y0, x0 + THUMB[0], y0 + THUMB[1])), np.float32)
            else:
                pad = Image.new('F', THUMB, float(b.mean()))
                pad.paste(im, (-x0, -y0))
                Bz = np.asarray(pad, np.float32)
        Bm = Bz - Bz.mean()
        F = np.fft.fft2(A) * np.conj(np.fft.fft2(Bm))
        R = np.abs(np.fft.ifft2(F / (np.abs(F) + 1e-6)))
        k = np.unravel_index(np.argmax(R), R.shape)
        if R[k] > best[3]:
            dy = k[0] if k[0] <= R.shape[0] // 2 else k[0] - R.shape[0]
            dx = k[1] if k[1] <= R.shape[1] // 2 else k[1] - R.shape[1]
            best = (float(dx), float(dy), z, float(R[k]))
    return best


class _Cam2:
    """What camfeel reads of a 2D camera: zoom and centre (frame pixels)."""
    def __init__(self, z, cx, cy):
        self.z, self.cx, self.cy = z, cx, cy


def cam_track(film, sv):
    """{shot: [(t, zoom, cx, cy)]}: the camera as the frames show it, each shot starting at (1, 540, 960)."""
    k = 1080.0 / THUMB[0]
    out, by_shot = {}, {}
    for r in sv:
        if r.get('thumb') is not None:
            by_shot.setdefault(r['shot'], []).append((r['t'], r['thumb']))
    for shot, tt in by_shot.items():
        ts, th = [t for t, _ in tt], [x for _, x in tt]
        z, cx, cy = 1.0, 540.0, 960.0
        tr = [(ts[0], z, cx, cy)]
        for i in range(1, len(ts)):
            dx, dy, dz, _ = _shift_zoom(th[i - 1], th[i])
            z = z / dz                       # the content moved by (-dx, -dy): the camera by (dx, dy)
            cx, cy = cx + dx * k / z, cy + dy * k / z
            tr.append((ts[i], z, cx, cy))
        out[shot] = tr
    return out


def cam_for(film, sv):
    tracks = cam_track(film, sv)

    def fn(t):
        shot = next((s[0] for s in getattr(film, 'SHOTS', []) if s[1] <= t < s[2]), None)
        tr = tracks.get(str(shot))
        if not tr:
            return None
        if t <= tr[0][0]:
            return _Cam2(*tr[0][1:])
        for a, b in zip(tr, tr[1:]):
            if a[0] <= t <= b[0]:
                u = (t - a[0]) / (b[0] - a[0])
                return _Cam2(*(x + (y - x) * u for x, y in zip(a[1:], b[1:])))
        return _Cam2(*tr[-1][1:])
    return fn


# ---------------------------------------------------------------------------------------------- lists
class Screen:
    """A JOKE_PROPS `at` measured from the drawing: (x, y, height px) of the piece's box at its nearest sample."""
    def __init__(self, boxes):
        self.boxes = boxes                        # [(t, (x0, y0, x1, y1))]

    def __call__(self, t):
        t0, b = min(self.boxes, key=lambda tb: abs(tb[0] - t))
        return (b[0] + b[2]) / 2, b[3], b[3] - b[1]


def joke_props(sv):
    boxes = {}
    for r in sv:
        for name, box, k in r['texts']:
            if box:
                boxes.setdefault(name, []).append((r['t'], tuple(v * k for v in box)))
    return [(name, [bx[0][0]], Screen(bx), None) for name, bx in boxes.items()]


def _places(film):
    path = os.path.join(ROOT, 'story', f'{getattr(film, "FILM", getattr(film, "NAME", film.__name__))}-places.txt'
                        .replace('_', '-'))
    if not os.path.exists(path):
        return None
    import places as PL
    return PL.parse(open(path).read())


def _span(v):
    a, _, b = str(v).partition(' to ')
    try:
        return abs(float(b) - float(a)) if b else None
    except ValueError:
        return None


def prop_sizes(film):
    import sizes
    d = _places(film)
    if d is None:
        return None
    out, done = [], set()
    for v in d['views'].values():
        for it in v['items']:
            w, h = _span(it['raw'].get('x')), _span(it['raw'].get('z'))
            if it['kind'] in sizes.SIZES and w and h and it['name'] not in done:
                done.add(it['name'])
                out.append((it['name'], it['kind'], w, h, None))
    return out


def outfit(film):
    """Each kit person's top hem as views.person draws it (their `hem`, else the kit's JACKET), standing."""
    import views as V
    cast = getattr(film, 'CAST', None) or {}
    out = {}
    for who, sp in cast.items():
        if isinstance(sp, dict) and 'height' in sp and not sp.get('robe'):
            edge = 'blouse hem' if sp.get('outfit') == 'dress' or sp.get('skirt') else 'jacket hem'
            out[who] = {edge: float(sp.get('bottom', V.JACKET))}
    return out


def line_subjects(film, scale=None):
    """Each kit person alone, at the largest size the film draws them (the survey's scale; 1.26 if never seen)."""
    cast = getattr(film, 'CAST', None) or {}
    scale = scale or {}

    def subjects():
        import views as V
        from people_parts import B
        out = []
        for who, sp in cast.items():
            if not isinstance(sp, dict) or 'height' not in sp:
                continue

            def draw(img, sp=sp, s=scale.get(who, 1.26)):
                V.person(img, B.Cam(1.0, 540, 960), 540, 960 - 500 * s, s, dict(sp), 0.0, 0.0)
            out.append((who, draw))
        return out
    return subjects


# ---------------------------------------------------------------------------------------------- fill and Film
class Film:
    """The film as the checks see it: its own inputs first, the kits' where it has none."""
    def __init__(self, film, extra):
        self._film, self._extra = film, extra

    def __getattr__(self, n):
        if n in self._extra:
            return self._extra[n]
        return getattr(self._film, n)


def alone_audit(film):
    """The general audit (house style) from a film's ALONE = {name: (t0, t1, draw)}: draw(t) paints that one person
    alone on a clear RGBA layer; each is checked over every frame of its span for in pieces, popping, stretching and
    frozen (filmkit.silhouette_audit). So a film never writes its own audits() (Open Wounds chat 19)."""
    def audits():
        import math
        import filmkit
        fps = getattr(film, 'FPS', 12)
        actors = {name: ([i / fps for i in range(math.ceil(t0 * fps), int(t1 * fps))], draw)
                  for name, (t0, t1, draw) in film.ALONE.items()}
        allow = [(k, a, b, why) for n, a, b, why in getattr(film, 'ALLOWED_POPS', ()) for k in actors
                 if k.split(' [')[0] == n]
        return filmkit.silhouette_audit(actors, fps=fps, still_ok=getattr(film, 'STILL_OK', ()), allow=allow)
    return audits


def fill(film, has, survey_pool=True):
    """(Film, lines said, faults): what the kits hand the checks, ONLY where the film gave nothing."""
    import cover
    said, faults, extra = [], [], {}
    people = 'people' in has
    sv = survey(film, survey_pool) if cover.picture_fn(film) is not None else []
    errs = [r for r in sv if r.get('error')]
    if errs:
        faults.append(f'kit inputs: {len(errs)} sample(s) could not be drawn ({errs[0]["error"]} at {errs[0]["t"]:.2f} '
                      's): the survey is short there')
    drawn = any(r['people'] for r in sv)
    if people and drawn and not hasattr(film, 'scene'):
        extra['KIT_ROSTER'] = roster(sv)
        said.append('who is in each shot: from the drawing')
        faults += pop_faults(film, sv)
        said.append('pop-ins (rule 6): from the drawing')
    if not hasattr(film, 'audits') and getattr(film, 'ALONE', None):
        extra['audits'] = alone_audit(film)
        said.append(f'audits: the general audit on each of ALONE ({len(film.ALONE)}), drawn alone')
    if getattr(film, 'PLAN', None) is not None:
        P, s = plan(film, sv)
        if s:
            extra['PLAN'] = P
            said += ['plan: ' + x for x in s]
    if not hasattr(film, 'cam_for') and sv:
        extra['cam_for'] = cam_for(film, sv)
        said.append('cam_for(t): the camera measured from the frames (camera feel, rule 72)')
    if not hasattr(film, 'EFFECTS') and 'effects' not in has:
        extra['EFFECTS'] = []
        said.append('EFFECTS: none (HAS says the film has no effects)')
    if not hasattr(film, 'JOKE_PROPS') and sv:
        extra['JOKE_PROPS'] = joke_props(sv)
        said.append(f'JOKE_PROPS: {len(extra["JOKE_PROPS"])} piece(s) with words, measured where drawn')
    if people and getattr(film, 'CAST', None):
        if not hasattr(film, 'LINE_SUBJECTS'):
            big = {}
            for r in sv:
                for p in r['people']:
                    if p.get('box') and p.get('s'):
                        big[p['who']] = max(big.get(p['who'], 0.0), float(p['s']))
            extra['LINE_SUBJECTS'] = line_subjects(film, big)
            said.append('LINE_SUBJECTS: the cast, each drawn alone by the people kit')
        if not hasattr(film, 'OUTFIT'):
            extra['OUTFIT'] = outfit(film)
            said.append(f'OUTFIT: {len(extra["OUTFIT"])} kit person(s)\' hems')
    if 'props' in has and not hasattr(film, 'PROP_SIZES'):
        ps = prop_sizes(film)
        if ps is not None:
            extra['PROP_SIZES'] = ps
            said.append(f'PROP_SIZES: {len(ps)} places piece(s) with a real size')
    return Film(film, extra), said, faults


def main():
    if sys.argv[1:2] == ['test']:
        sys.exit(0 if _test() else 1)
    film = importlib.import_module(sys.argv[1].replace('-', '_'))
    f, said, faults = fill(film, set(getattr(film, 'HAS', ())))
    print('the kits hand the checks:')
    for x in said:
        print(' -', x)
    for x in faults:
        print('FAULT', x)


def _test():
    rec = lambda t, shot, ppl, view=None: dict(t=t, shot=shot, view=view, texts=[], people=[
        dict(who=w, box=b, yaw=y) for w, b, y in ppl])
    sv = [rec(0.1, '1', [('a', (100, 300, 400, 1900), 0)]), rec(0.6, '1', [('a', (100, 300, 400, 1900), 0)]),
          rec(1.1, '1', []),                                                        # a vanishes in mid-frame: a pop
          rec(2.1, '2', [('b', (0, 300, 200, 1900), 30)]), rec(2.6, '2', [])]       # b leaves by the edge: fine
    film = type('F', (), {'SHOTS': [('1', 0, 2), ('2', 2, 3)], 'ALLOWED_POPS': [], '__name__': 'made_up'})
    pops = pop_faults(film, sv)
    ok = len(pops) == 1 and ' a vanishes' in pops[0]
    ok = ok and roster(sv) == {'1': {'a'}, '2': {'b'}}
    ok = ok and abs(facing_of(0) - 180) < 1e-9 and abs(facing_of(90) - 90) < 1e-9
    a = np.zeros(THUMB[::-1], np.float32)
    a[60:120, 40:80] = 200.0
    b = np.roll(a, 5, axis=1)
    dx, dy, z, _ = _shift_zoom(a, b)
    ok = ok and abs(dx + 5) <= 1 and abs(dy) <= 1 and z == 1.0
    print('PASS' if ok else 'FAIL', f'kit inputs: pops {pops}, shift {dx, dy, z}')
    return ok


if __name__ == '__main__':
    main()
