#!/usr/bin/env python3
"""Blessed (12 Nov, chat 3): the checks the film was never set up for (rule 59: a check the film has not been set up
for is a fault before the first animatic). blessed.py calls install(film) at its end, which sets these on the film:

MAP
  metres ........... LEVELS, _level, where: each painting's level camera (real, or fitted to its marks) and a screen
                     mark (x, ground y, pixels per metre) back to metres (x, d, the floor's height)
  scene ............ scene(t), cam_for(t), project(cam, P), the plan's camera per shot (audit.py: rules 5, 6, 14)
  audits ........... audits(): each body alone over every frame it is on screen (filmkit.silhouette_audit)
  line work ........ LINE_SUBJECTS(): each of the cast alone, large (linecheck.py)
  set feet ......... SET_FEET, SET_CAM, MOVE_SPAN, set_movers(t) (and movers(t), rule 16's form): the three walking shots against their solid things
                     (setcheck.film_faults, rule 13)
"""
import math
import sys
import types

from PIL import Image

import blessed_sets as ST
import burnham as B
from remakes_sets import Level

F = None                                          # the film module (blessed), set by install()

# ---------------------------------------------------------------------------------------------- metres
ROOM = {'tv': 'tvroom', 'cell_cot': 'cell', 'gates2': 'gates'}   # the painting (and plan room) each view stands in
LEVELS = {}


def _base(view):
    return ROOM.get(view, ST.view_cam(view)[0])


def _level(view):
    """The painting's level camera: the real one where the set has it, else one fitted to its first mark (eye 1.6 m,
    a 1000 px lens), so every mark maps back to metres exactly and the floors keep their heights (the jury's tiers)."""
    v = _base(view)
    if v not in LEVELS:
        real = {'court_out': ST.OUT, 'gates': ST.GATE, 'cell': F.CELL,
                # the jury box: its two rows drawn at 430 and 380 px a metre, a box front between them; a jury box's
                # rows stand about 0.9 m apart, so the lens is 0.9 / (1/380 - 1/430) = 2941 px and the back tier
                # stands 0.58 m up (a 1000 px guess put the rows 0.3 m apart: knees through the row in front)
                'court_jury': Level(1.6, 1945 - 1.6 * 430, 0.9 / (1 / 380 - 1 / 430))}
        if v in real:
            LEVELS[v] = real[v]
        else:
            st = ST.STAGE.get(v, {})
            marks = [m for k, m in st.items() if isinstance(m, tuple)] or [q for k, m in st.items() for q in m]
            gy, ppm = (marks[0][1], marks[0][2]) if marks else (1400.0, 300.0)
            LEVELS[v] = Level(1.6, gy - 1.6 * ppm, 1000.0)
    return LEVELS[v]


def where(view, mark):
    """A screen mark on a painting -> (x, d, floor height) in metres."""
    L = _level(view)
    sx, gy, ppm = mark
    d = L.f / ppm
    return (sx - L.cx) / ppm, d, L.h - (gy - L.hz) * d / L.f


# ---------------------------------------------------------------------------------------------- scene
def placed(t):
    """Everyone drawn at t: [(name, view, (x, d, floor), height, seated, facing)], from the same functions the
    drawing uses (so the two never drift)."""
    shot = F.shot_of(t)
    v = F.VIEW[shot]
    st = ST.STAGE.get(_base(v), {})
    H = F.HEIGHTS
    out = []

    def one(name, mark, seated=False, facing=(0.0, -1.0), h=None):
        out.append((name, v, where(v, mark), h or H.get(name, 1.75), seated, facing))

    def pack(L, spots, at):
        for i, (x, d) in enumerate(spots):
            fx, fz = at[0] - x, at[1] - d
            n = math.hypot(fx, fz) or 1.0
            one('press%d' % i, ST._mark(L, x, d), facing=(fx / n, fz / n), h=F.press_sp(i, 0)['height'])

    if shot == 'arrive':
        one('brand', F.arrive(F.brand_sp(t, 'trial'), t)[0])
        pack(ST.OUT, st['press'], (0.45, 3.9))
    elif shot == 'jury':
        for row, marks in ((F.JY.BACK_ROW, st['back']), (F.JY.FRONT_ROW, st['front'])):
            for w, m in zip(row, marks):
                one(w, m, True)
    elif shot in ('oath', 'oath2'):
        one('brand', st['brand'])
        one('judge', st['judge'], True)
    elif shot == 'dock':
        one('brand', st['brand'])
        for g in ('guard1', 'guard2'):
            one(g, st[g], True, h=F.GUARDS[g]['height'])
    elif shot == 'van':
        one('brand', st['brand'], True)
    elif shot == 'escort':
        one('brand', F.escort(F.brand_sp(t, 'prison'), t)[0])
        one('officer', F.escort(dict(F.BC.OFFICER), t, 'officer')[0])
    elif shot == 'cot':                           # sat on the cot's edge (chat 4), facing the lens
        one('brand', F.COT_MARK)                  # note 18: lying flat, drawn standing front-on from above
    elif shot == 'phone':
        one('brand', st['brand'])
    elif shot in ('tvroom', 'push'):
        for w in ('inmate3', 'inmate1', 'brand', 'inmate2'):
            one(w, st[w], True)
    elif shot == 'tv':                            # the newsreader at his desk, inside the TV picture
        out.append(('newsreader', v, (0.0, 3.0, 0.0), H['newsreader'], True, (0.0, -1.0)))
    elif shot == 'gates':
        one('brand', F.gates_wide(F.brand_sp(t, 'trial'), t)[0])
        pack(ST.GATE, st['press'], (0.65, ST.GATE_D - 0.3))
    elif shot == 'gates2':
        one('brand', F.gates_close(F.brand_sp(t, 'trial'), t)[0])
        pack(ST.GATE, ST.STAGE['gates']['press'], (0.6, F.G2_TO))
    return out


def scene(t):
    """Everyone solid, in their painting's metres, laid in its plan room (audit.py: nothing passes through anything,
    nothing pops in, and who is on screen in each shot for SHOT_CAST)."""
    import audit
    things = []
    for name, v, (x, d, base), h, seated, facing in placed(t):
        X = F._PX[_base(v)] + x
        things.append(audit.Thing(name, audit.simple(name, X, d, h, base, seated, facing)))
    return things


def cam_for(t):
    shot = F.shot_of(t)
    return types.SimpleNamespace(view=_base(F.VIEW[shot]), cam=F._cam(F.VIEW[shot], t))


def project(c, P):
    """World points (N x 3: x across the plan, y up, z = depth) -> screen x, y and depth, through the painting's level
    camera and the shot's zoom."""
    import numpy as np
    L = _level(c.view)
    x = P[:, 0] - F._PX[c.view]
    d = np.maximum(P[:, 2], 1e-3)
    sx = L.cx + L.f * x / d
    sy = L.hz - L.f * (P[:, 1] - L.h) / d
    return (sx - c.cam.cx) * c.cam.z + 540, (sy - c.cam.cy) * c.cam.z + 960, P[:, 2]


def plan_cams():
    """Rule 1: a camera in the plan for every shot, in its painting's room, looking in."""
    out = {}
    for s, _, _ in F.SHOTS:
        x = F._PX[_base(F.VIEW[s])]
        out[s] = dict(pos=(x, 1.6, 0.3), look=(x, 1.6, 6.0))
    return out


# ---------------------------------------------------------------------------------------------- audits
_ALONE = [None]


def keep(sp):
    """While one body is audited alone, everyone else is drawn on a scratch picture (their points still come back:
    the officer's grip needs Brand's)."""
    return _ALONE[0] is None or sp.get('who') == _ALONE[0]


def scratch():
    return Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))


def _alone(who):
    def draw(t):
        lay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
        shot = F.shot_of(t)
        if shot == 'tv':
            import newsdesk_set as ND
            import sets as S3
            reader = dict(F.BC.NEWSREADER, head_life=F.HEAD_LIFE['newsreader'], **F.face('newsreader', t, 'neutral'))
            cm = S3.Cam((0.0, 1.16, -0.6), (0.0, 1.10, 4.15), focal=1500)   # the studio's own camera (studio_feed)
            px, pz = ND.PRESENTER_AT
            ND.put_seated(lay, cm, reader, px, pz, 180.0, t)
            return lay
        mid, press = ST.mid, F.press
        ST.mid, F.press = (lambda *a, **k: None), (lambda *a, **k: None)   # the set and the press pack stay out
        _ALONE[0] = who
        try:
            F.draw_people(lay, F._cam(F.VIEW[shot], t), shot, t)
        finally:
            ST.mid, F.press, _ALONE[0] = mid, press, None
        return lay
    return draw


def audits():
    """Each of the cast alone over every frame they are on screen: in pieces, popping, stretching, frozen
    (filmkit.silhouette_audit), and the movement library's own checks."""
    import filmkit
    import moves
    keep_ss = B.SS
    B.SS = 1
    try:
        actors = {}
        for shot, a, b in F.SHOTS:
            for who in F.SHOT_CAST[shot]:
                ts = [i / F.FPS for i in range(math.ceil(a * F.FPS), int(b * F.FPS))]
                if ts:
                    actors[f'{who} [{shot} {a:.1f}]'] = (ts, _alone(who))
        filmkit.EYES.clear()
        out = filmkit.silhouette_audit(actors, fps=F.FPS, still_ok=F.STILL_OK,
                                       allow=[(k, t0, t1, why) for n, t0, t1, why in F.ALLOWED_POPS for k in actors
                                              if k.startswith(n + ' [')])
    finally:
        B.SS = keep_ss
    return out + moves.audit()


# ---------------------------------------------------------------------------------------------- line work
def LINE_SUBJECTS():
    """Each of the cast alone, large, for the line-work check (every shape outlined, one weight)."""
    import views as V

    def one(who):
        def d(im):
            V.person(im, B.Cam(1.0, 540, 960), 540, 400, 1.0, dict(F.CAST[who], full=True, pose='custom'), 0.0, 0.0)
        return d
    return [(who, one(who)) for who in F.CAST]


# ---------------------------------------------------------------------------------------------- set feet (rule 13)
SET_FEET = {   # each walking shot's solid things on the ground: (name, x0, x1, d0, d1, height, layer), metres
    'arrive': [('left planter wall', -14.0, -0.9, 11.0, 11.6, 1.25, 'under'),
               ('right planter wall', 3.9, 14.0, 11.0, 11.6, 1.25, 'under'),
               ('steps', -0.9, 3.9, 9.2, 11.0, 0.7, 'under'),
               ('left rail', -0.65, -0.55, 9.2, 11.0, 1.65, 'under'),
               ('right rail', 3.55, 3.65, 9.2, 11.0, 1.65, 'under'),
               ('lamp post', -3.95, -3.85, 8.45, 8.55, 8.0, 'under'),
               ('left tree', -5.5, -5.3, 12.4, 12.6, 7.5, 'under'),
               ('right tree', 6.5, 6.7, 12.9, 13.1, 7.5, 'under')],
    'escort': [('bed', -1.05, -0.25, 1.39, 3.39, 0.45, 'under'),
               ('toilet', 0.68, 1.02, 2.9, 3.39, 0.45, 'under')],
    'gates': [('gatehouse left of the wicket', -12.0, 0.15, 9.0, 9.6, 8.0, 'under'),
              ('gatehouse right of the wicket', 1.15, 12.0, 9.0, 9.6, 8.0, 'under'),
              ('left bollard', -1.87, -1.63, 8.48, 8.72, 0.9, 'under'),
              ('right bollard', 1.63, 1.87, 8.48, 8.72, 0.9, 'under'),
              ('sign', -3.3, -1.9, 7.35, 7.45, 2.7, 'under')],
}
SET_FEET['gates2'] = SET_FEET['gates']


def set_cams():
    return {'arrive': ST.OUT, 'escort': F.CELL, 'gates': ST.GATE, 'gates2': ST.GATE}


def move_spans():
    return {s: (a, b - 1.0 / F.FPS) for s, a, b in F.SHOTS if s in SET_FEET}


def set_movers(t):
    """Everyone standing in the walking shots: (who, x, d, (body width, height)) in the painting's metres
    (setcheck, rule 13)."""
    return [(n, x, d, (0.5, h)) for n, v, (x, d, base), h, seated, f in placed(t) if not seated]


def movers(t):
    """Everyone on screen as (name, world point at the body's middle) for the screen-direction check across cuts
    (viewchecks.direction_faults, rule 16)."""
    return [(n, (F._PX[_base(v)] + x, base + 0.5 * h, d)) for n, v, (x, d, base), h, seated, f in placed(t)]


# ---------------------------------------------------------------------------------------------- install
def install(film):
    global F
    F = film
    film.scene, film.cam_for, film.project = scene, cam_for, project
    film.audits, film.LINE_SUBJECTS = audits, LINE_SUBJECTS
    film.PLAN['CAMS'] = plan_cams()
    film.SET_FEET, film.SET_CAM, film.MOVE_SPAN = SET_FEET, set_cams(), move_spans()
    film.set_movers, film.movers = set_movers, movers
    film.keep, film.scratch = keep, scratch


if __name__ == '__main__':
    sys.exit('blessed_checks is installed by blessed.py; run python3 source/preflight.py blessed OUT')
