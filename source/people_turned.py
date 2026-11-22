#!/usr/bin/env python3
"""MAP  Turned heads for the people kit's invented people (ranking item 4, overnight chat 4d, 14 Nov). Rule: a person
is drawn the same in every view. Any kit person with an invented front face (sp['kit_face']) turns through turnhead:
their own face card's layout carried round the head, their own iris, brow and lip colours, their haircut from behind
(the press pack's turned haircuts, LIFTED unchanged in look from blessed_cast.py: Blessed note 4, 'the journalists are
blob people'), stubble, a boxed beard, freckles and glasses held round the head. Before this, a kit person seen from
the side or behind fell back to the engine's plain generic head (curly read as long, the face card was lost).
One turnhead Person per look (who, skin, hair, face), under the key 'kit:...', built when a shot first needs it.
No film imports this until Sam approves the kit.

Map: haircuts from behind 21 | the press pack's pieces (lifted) 41 | face marks held round 113 | the Person 143
     (look 144, register 154, ON/KEYED 170) | install 174
"""
import math

import numpy as np

import people_parts as PP
from people_parts import FA, TH, dk, INK, curve, oval

# ---------------------------------------------------------------------------------------------- haircuts from behind
# style: front hair design; hl: hairline; the profile keys say how far down the back the hair reaches. Lifted from
# blessed_cast.PRESS_STYLES; 'knot' and 'none' new (chat 4d: a bun behind; no hair at all, under a wig).
STYLES = {
    'short': dict(hl=-0.1, prof=dict(hair_low=0.4, nape=0.66)),
    'crop': dict(hl=-0.06, prof=dict(hair_low=0.36, nape=0.62, volume=0.015)),
    'bald': dict(hl=None, prof=dict(hair_top=0.4, hair_top_back=0.44, hair_ragged=0.008, hair_low=0.66, nape=0.86)),   # chat 8 (Protest Tiers): the fringe
    # of hair runs down to the neck: ending above it read as a dark band like a blindfold
    'bob': dict(hl=-0.12, prof=dict(hair_low=0.9, nape=0.95, volume=0.07), long=1.1),
    'pony': dict(hl=-0.14, prof=dict(hair_low=0.44, nape=0.7, volume=0.02), pony=True),
    'curly': dict(hl=-0.08, prof=dict(hair_low=0.5, nape=0.74, volume=0.12), curls=True),
    'long': dict(hl=-0.14, prof=dict(hair_low=0.6, nape=0.8, volume=0.05), long=1.55),
    'side': dict(hl=-0.08, prof=dict(hair_low=0.44, nape=0.7, volume=0.035), parting=True),
    'knot': dict(hl=-0.1, prof=dict(hair_low=0.4, nape=0.66, volume=0.02), knot=True),
    'none': dict(hl=None, prof=dict(), bare=True),
    'wig': dict(hl=-0.2, prof=dict(hair_low=0.7, nape=0.82, volume=0.16), curls=True, rolls=True),   # chat 15:
}   # the judge's white bench wig turned (the front's extra 'wig': rolled curls over the crown, a roll over each ear)
TURNED = {'crop': 'crop', 'bald': 'bald', 'side': 'side', 'bob': 'bob', 'long': 'long', 'curly': 'curly',
          'bun': 'knot', 'receding': 'bald', 'none': 'none', 'pony': 'pony', 'short': 'short',
          'shag': 'long'}   # shag (Milburn note 3) turns as long hair: front only so far   # kit hair -> from behind
HIDES_EARS = ('bob', 'long', 'curly', 'wig', 'shag')       # hair over the ears: none drawn on top of it


# ---------------------------------------------------------------------------------------------- the press pack's pieces
def _layout(sp):
    m = dict(FA.AVG)
    for k, v in sp['kit_face']['m'].items():
        m[k] += v
    return FA.layout(m)


def _cap(L, hl):
    e, c = L['fw'] * 0.5, L['fhw'] * 0.5
    return [(-e - 0.02, 0.36), (-e - 0.03, 0.02), (-e + 0.04, -0.24), (-0.24, -0.4), (0.0, -0.45), (0.24, -0.4),
            (e - 0.04, -0.24), (e + 0.03, 0.02), (e + 0.02, 0.36), (e - 0.03, 0.34), (c + 0.01, 0.12), (c - 0.03, 0.02),
            (c * 0.7, hl), (0.0, hl - 0.012), (-c * 0.7, hl), (-c + 0.03, 0.02), (-c - 0.01, 0.12), (-e + 0.03, 0.34)]


def _crown(style):
    """The skull's crown: the hair's outer size (-0.42), or a bare skull's own lower dome (people_parts.TRUE_SKULL,
    Sam 16 Nov: bald heads 'massive and strange-looking'; turned with the front face's dome)."""
    return PP.SKULL_CROWN if PP.TRUE_SKULL and style == 'bald' else -0.42


def _profile(style):
    st = STYLES[style]
    return lambda L: TH.fitted(L, _crown(style), CHIN_V, **st['prof'])


LIFT = True     # turned heads lifted as the front is (GTA chat 10); kittest people_from_a_description sets it
#                 off (with CHIN_V 1.06) to compare with Blessed, drawn before the fix
CHIN_V = 1.0    # the turned chin where the front's is (faces.outline_uv ends at 1.0); was turnhead's 1.06 (a bearded
#                 template's), so every turned kit jaw hung 11 units lower over the neck (Sam, GTA chat 10)


def _shine(p, f, skin):
    """A bare skull's gentle shine, on the dome where it faces us most (the visible arc's middle)."""
    v = PP.SKULL_CROWN * 0.72
    lo, hi = f.visible(v)
    x, z = f.ring((lo + hi) / 2, v)
    X, _ = f.view(float(x), float(z))
    p.poly(oval(f.cx + X * TH.H, f.top + v * TH.H, 15, 7, 16, -0.3), PP.B.lt(skin, 1.18), None)


def _hair(img, p, f, L, sp, look):
    st, hc, style = STYLES[look['style']], look['hair_c'], look['style']
    if st.get('bare'):
        return
    if _crown(style) != -0.42:
        _shine(p, f, sp['skin'])
    H = TH.H
    fc = sp['kit_face']
    own = sp.get('_faithful') and fc['hair'] in OWN_FRONT       # one source: the front's own hairline
    if st.get('long'):
        import people_famous as PF
        PF._turned_long(p, f, hc, st['long'], wavy=not (own and fc['hair'] in STRAIGHT))
    cap = _cap(L, st['hl']) if st['hl'] is not None else None
    if own:
        cap = OWN_FRONT[fc['hair']](L, fc)
    fronts = [] if cap is None else [f.pts(TH.dense(curve(cap, 2)))]
    prof = TH.PEOPLE[look['key']].build(sp)[1]
    mask = TH.hair(img, p, f, fronts, hc, prof)
    rng = np.random.default_rng(look['strand_seed'])
    yaw = math.degrees(f.th)
    bx = f.hx + (0.0 if yaw >= 170 else -0.18 * H)            # the back of the skull on screen

    def strands(pen):                                          # the hair's fall: strokes down from the crown
        if own and fc['hair'] == 'crop':                       # a crop's own texture, not long strands
            PP.crop_front(pen, f, L, hc, fill=False)
            return
        for k in range(14 if not st.get('curls') else 0):
            u = rng.uniform(-0.42, 0.42)
            x0, y0 = bx + u * H * 0.8, f.top - 0.36 * H + abs(u) * 0.2 * H
            pen.line(curve([(x0, y0), (x0 + u * 18, y0 + 0.25 * H), (x0 + u * 30, y0 + 0.55 * H)], 3), dk(hc, 0.72), 1.4)
        if st.get('curls'):                                    # curls: little loops all over
            for k in range(40):
                x, y = bx + rng.uniform(-0.5, 0.5) * H, f.top + rng.uniform(-0.45, 0.65) * H
                pen.line(oval(x, y, 9, 7, 10, 0.3, math.pi * 1.6), dk(hc, 0.66), 1.4)
        if st.get('parting'):
            pen.line(curve([(bx - 0.12 * H, f.top - 0.42 * H), (bx - 0.14 * H, f.top - 0.2 * H)], 3), dk(hc, 0.55), 1.6)
    TH.clipped(img, p, mask, strands)
    if st.get('pony'):                                         # a ponytail from the back of the head, a band round it
        x, y = bx, f.top + (0.36 if not fc.get('pony_high') else -0.12) * H   # GTA: a high ponytail (Lucia)
        k = 1.0 if not fc.get('pony_high') else 1.7                     # a high tail falls past the nape
        fk = 1.35 if fc.get('pony_high') else 1.0                      # chat 9: Lucia's tail fuller (Sam)
        tail = [(x - 16, y), (x - 26 * k ** 0.5 * fk, y + 60 * k), (x - 20 * fk, y + 130 * k), (x - 4, y + 168 * k),
                (x + 12 * fk, y + 132 * k), (x + 20 * k ** 0.5 * fk, y + 62 * k), (x + 16, y)]
        p.poly(curve(tail, 3), hc, INK, 2.2)
        for j in range(3):
            p.line(curve([(x - 6 + 6 * j, y + 14), (x - 10 + 7 * j, y + 80 * k), (x - 4 + 4 * j, y + 140 * k)], 3),
                   dk(hc, 0.72), 1.3)
        p.poly(oval(x, y + 6, 18, 8, 12), (40, 40, 44), INK, 1.6)
    if st.get('rolls'):                                        # the wig's rolls over each ear (chat 15)
        for deg in (-91, 91):
            x, z = f.ring(deg, 0.42)
            X, Z = f.view(float(x), float(z))
            if Z < -0.05:
                continue
            ex = f.cx + X * H + math.copysign(8, X)
            for k in range(3):
                p.ell(ex, f.top + (0.3 + 0.08 * k) * H, 12, 9, hc, INK, 1.8)
    if st.get('knot') and fc.get('hair_messy'):                # chat 9 (her): the big messy curly bun on the crown,
        x, y = bx - (0.0 if yaw >= 170 else 0.04 * H), f.top - 0.4 * H   # sat on the crown, never above it
        rng = np.random.default_rng(31)                                  # (Sam, chat 9: "floats off her head")
        lumps = [(0, 0, 0.11), (-0.07, 0.03, 0.08), (0.07, 0.02, 0.08), (-0.03, -0.07, 0.07), (0.04, -0.07, 0.07),
                 (0, 0.07, 0.09)]
        for dx, dy, r in lumps:
            p.poly(oval(x + dx * H, y + dy * H, r * H + 2.4, r * H * 0.92 + 2.4, 18), INK, None)
        for dx, dy, r in lumps:
            p.poly(oval(x + dx * H, y + dy * H, r * H, r * H * 0.92, 18), hc, None)
        for _ in range(16):
            p.line(oval(x + rng.uniform(-0.12, 0.12) * H, y + rng.uniform(-0.12, 0.08) * H, 7, 6, 10, 0.3, math.pi * 1.6),
                   dk(hc, 0.66), 1.3)
    elif st.get('knot'):                                       # new: a bun high on the back of the head
        x, y = bx - (0.0 if yaw >= 170 else 0.1 * H), f.top - 0.3 * H
        p.poly(curve(oval(x, y, 26, 22, 18), 2), hc, INK, 2.2)
        for k in range(3):
            p.line(curve([(x - 16 + 12 * k, y - 14), (x - 10 + 12 * k, y), (x - 15 + 12 * k, y + 12)], 3), dk(hc, 0.7), 1.4)
        p.line([(x - 12, y + 22), (x + 12, y + 22)], (40, 40, 44), 3.4)
    if own and math.degrees(f.th) < 120:                       # the front's fringe, streaks and layers, on the head
        _own_front(p, f, L, fc, hc, sp['skin'])
    if sp.get('_faithful') and fc.get('piercings') and math.degrees(f.th) < 120:
        PP.piercings(p, f, L, fc, sp.get('brow_up', 0.0), sp.get('frown', 0.0), seen=seen(f, 0.3))
    _ = style


STRAIGHT = ('long', 'shag')                                    # turned long hair hangs straight, as from the front
OWN_FRONT = {                                                  # kit hair -> its front hairline (the cap, design units)
    'crop': lambda L, fc: PP.crop_cap(L),
    'long': lambda L, fc: PP._press_cap(L, -0.08),
    'shag': lambda L, fc: [(-L['fw'] * 0.5 - 0.03, 0.5), (-L['fw'] * 0.5 - 0.04, 0.05), (-0.26, -0.47), (0.0, -0.52),
                           (0.26, -0.47), (L['fw'] * 0.5 + 0.04, 0.05), (L['fw'] * 0.5 + 0.03, 0.5),
                           (L['fhw'] * 0.5, 0.06), (0.0, L['brow_y'] - 0.06), (-L['fhw'] * 0.5, 0.06)],
}


def _own_front(p, f, L, fc, hc, skin):
    """The front head's own hair-over-the-face piece drawn on the turned head (shag: fringe, roots, the blue chunk,
    temple layers; long: the cap and its strands), then the shag's near peekaboo panel down the side."""
    if fc['hair'] == 'crop':
        return
    PP._hair_front(p, f, L, fc, hc, skin)
    sc = fc.get('hair_streak')
    if fc['hair'] == 'shag' and sc:                            # the near peekaboo panel: blue strands down the curtain
        H, yaw = TH.H, math.degrees(f.th)
        ex, ey = f.at(-L['fw'] * 0.5 - 0.02, 0.2)
        for k in range(3):
            x = ex - (0.05 + 0.035 * k) * H * (1.0 if yaw < 60 else 1.6)
            p.line(curve([(x, ey), (x - 0.02 * H, ey + 0.5 * H), (x - 0.01 * H, ey + 1.0 * H)], 3), sc, 7 - k)


def _mood(sp, f):
    """The eyes and brows from the person's own face channels (one source: the front's lid4, look, squint, blink,
    brow_up and frown; before 18 Nov a turned kit head ignored them and kept one fixed look)."""
    if not sp.get('_faithful'):
        return dict(lid=0.1, look=0.3, squint=0.0, closed=False, gaze_dy=-0.2), 0.0, 0.0
    return (dict(lid=sp.get('lid4', 0.1), look=0.3 + sp.get('look', 0.0), squint=sp.get('squint', 0.0),
                 closed=bool(sp.get('blink')), gaze_dy=sp.get('gaze_dy', -0.2)),
            sp.get('brow_up', 0.0), sp.get('frown', 0.0))


def _rest(p, f, L, sp, fx, my, lip):
    FA.lips(p, f, L, dict(sp, smile=0.0, mouth='rest'), lip, (fx, my - 6))


# ---------------------------------------------------------------------------------------------- face marks held round
def _marks(pen, f, L, sp):
    """Stubble, a boxed beard, freckles (people_parts' front-face pieces) on the turned face, kept inside the head."""
    fc, skin = sp['kit_face'], sp['skin']
    e = L['fw'] * 0.5
    jaw = [(-e, 0.5), (-L['jw'] * 0.5, 0.82), (-0.08, 0.98), (0.0, 1.0), (0.08, 0.98), (L['jw'] * 0.5, 0.82), (e, 0.5),
           (e * 0.7, 0.62), (L['mw'] * 0.75, L['lip17'] + 0.04), (0.0, L['lip17'] + 0.03),
           (-L['mw'] * 0.75, L['lip17'] + 0.04), (-e * 0.7, 0.62)]
    if fc.get('stub'):
        pen.poly(curve(f.pts(jaw), 3), dk(skin, fc['stub']), None)
    if fc.get('beard'):
        b = fc['beard']
        pen.poly(curve(f.pts(jaw), 3), b, INK, 1.6)
        pen.poly(curve(f.pts([(-L['mw'] * 0.72, L['lip13'] + 0.02), (-L['mw'] * 0.6, L['lip0'] - 0.01),
                              (0.0, L['nose_y'] + 0.012), (L['mw'] * 0.6, L['lip0'] - 0.01),
                              (L['mw'] * 0.72, L['lip13'] + 0.02), (L['mw'] * 0.5, L['lip0'] + 0.006),
                              (0.0, L['lip0'] - 0.002), (-L['mw'] * 0.5, L['lip0'] + 0.006)]), 3), b, INK, 1.4)
    if fc.get('freckles'):
        rng = np.random.default_rng(31)
        for _ in range(22):
            sgn = 1 if rng.random() < 0.5 else -1
            u, v = sgn * rng.uniform(L['nw'] * 0.4, L['ecx'] + 0.04), rng.uniform(L['eye_y'] + 0.08, L['nose_y'])
            pen.poly(oval(*f(u, v), 2.0, 2.0, 6), dk(skin, 0.74), None)
    if sp2_faithful(sp):                                       # one source: the front's own detail and moustache
        PP.face_detail(pen, f, L, fc, skin, seen=seen(f))
        if fc.get('pencil'):
            PP.pencil(pen, f, L, fc)


def sp2_faithful(sp):
    return bool(sp.get('_faithful'))


def seen(f, k=0.18):
    """A mark at front-design (u, v) shows only where that part of the head faces us (TurnFace.k), so a far-side
    mark is left out rather than squashed onto the head's edge."""
    return lambda u, v: f.k(u, v) > k


def _over(img, p, f, L, sp, view):
    if sp['kit_face'].get('glasses') and view in ('three', 'side'):
        PP._glasses(p, f, L, sp['kit_face']['glasses'])


# ---------------------------------------------------------------------------------------------- the Person
def look(sp):
    """This look's turned head: its key and what it is built from (the same look always gets the same Person)."""
    fc = sp['kit_face']
    style = 'wig' if 'wig' in sp.get('kit_extras', ()) else TURNED[fc.get('turned') or fc['hair']]
    hc = tuple(sp.get('hair_c', (40, 32, 28)))
    key = 'kit:%s:%s:%s:%s:%s' % (sp['who'], style, tuple(sp['skin']), hc, sorted(fc['m'].items()))
    return dict(key=key, style=style, hair_c=hc, strand_seed=sp.get('strand_seed', 1),
                ears_hidden=style in HIDES_EARS, faithful=FAITHFUL)


def register(sp, key=None):
    """One turnhead Person per look; key= lets a check key it another way (replicate: the film's way)."""
    lk = look(sp)
    lk['key'] = key or lk['key']
    if lk['key'] not in TH.PEOPLE:
        fc = sp['kit_face']
        face = (lambda pen, f, L, sp2: _marks(pen, f, L, sp2)) if (fc.get('stub') or fc.get('beard')
                                                                   or fc.get('freckles') or lk['faithful']) else None
        TH.register(TH.Person(lk['key'], lambda sp2, _sp=sp: _layout(_sp), _crown(lk['style']), 0.4, _profile(lk['style']),
                              sp['skin'], fc['iris'], fc['brow'], fc['lip'], _mood,
                              lambda p, f, L, sp2, fx, my, _l=fc['lip']: _rest(p, f, L, sp2, fx, my, _l),
                              lambda img, p, f, L, sp2, _lk=lk: _hair(img, p, f, L, sp2, _lk),
                              face=face, over=_over if fc.get('glasses') else None))
    return lk


FAITHFUL = True  # one source (18 Nov): the front's own parts on the turned head; keyed looks (old films' replicas) off
ON = True        # replicate turns this off to score a frame without the new turned heads (crowds keep theirs: the film's)
KEYED = {}       # who -> a function(sp) -> key, to key a look another way (replicate keys the press the film's way)


# ---------------------------------------------------------------------------------------------- install
def install():
    """Once: an invented kit face's turned views through its own turnhead Person, at the house's bigger head size (no
    lift: from behind, the neck shows long)."""
    V = PP.V
    if 'kit_turned' in V.TURNED_HEADS:
        return

    def head_view(img, p, sp, t, view, hx=0.0, hy=-150.0):
        if (ON or sp.get('kit_crowd')) and sp.get('kit_face') and not sp.get('kit_head') and not sp.get('kit_famous') and view in TH.YAW:
            k = KEYED.get(sp['who'])
            lk = register(sp, k(sp) if k else None)
            faithful = lk['faithful'] and not k
            with PP._Big():                     # lifted as the front is (Sam, GTA chat 10: "the three-quarter turns
                # still have the weird slumped necks"): drawn 15% bigger without the front's lift, every turned head
                # grew downwards, eyes 21 and chin 33 units lower than front on, over the neck
                return TH.draw(img, p, dict(sp, who=lk['key'], ears_hidden=lk['ears_hidden'], _faithful=faithful), t,
                               view, hx, PP._lift(hy) if LIFT else hy)
        return V.NOT_MINE
    V.TURNED_HEADS['kit_turned'] = head_view     # one list of turned heads in views.py, newest tried first


# ---------------------------------------------------------------------------------------------- the lost-parts check
PARTS = ('pencil', 'piercings', 'hair_streak', 'beard', 'stub', 'freckles', 'glasses')   # face-card parts to carry


def _head_png(sp, yaw):
    from PIL import Image
    V = PP.V
    B = PP.B
    img = Image.new('RGBA', (360, 420), (255, 255, 255, 255))
    B.SS = 1
    for k in [k for k in TH.PEOPLE if k.startswith('kit:')]:      # the look is keyed by its parts' absence too
        del TH.PEOPLE[k]
    V.person(img, B.Cam(1.0, 540, 960), 180, 330, 0.9, dict(sp), 0.0, yaw)
    return np.asarray(img.convert('L'), dtype=np.int16)


def lost_parts(cast, views):
    """One source, enforced (proposal three-quarter-people, 18 Nov): every face-card part a kit person has must change
    the picture of their turned head in each turned view a film draws (three-quarter, side). Drawn with and without
    each part: identical means the turn lost it (the fault Sam found: the moustache, piercings and streaks gone).
    `views`: {who: set of views}. Returns fault lines."""
    out = []
    yaws = {'three': 45, 'side': 90}
    for who, vs in sorted(views.items()):
        sp = cast.get(who)
        if not sp or not sp.get('kit_face') or sp.get('kit_famous') or sp.get('kit_head'):
            continue
        fc = sp['kit_face']
        for view in sorted(v for v in vs if v in yaws):
            full = _head_png(sp, yaws[view])
            for part in PARTS:
                if not fc.get(part):
                    continue
                if part == 'piercings' and view == 'side' and set(fc['piercings']) <= {'brow', 'nose'}:
                    continue                                   # both on the far side from the side: hidden, as meant
                less = dict(sp, kit_face={k: v for k, v in fc.items() if k != part})
                if part == 'hair_streak':
                    less['hair_streak'] = None
                if (np.abs(_head_png(less, yaws[view]) - full) > 24).sum() < 12:
                    out.append(f'LOST PART: {who} turned {view} draws no {part} (the front has it): carry it round '
                               '(people_turned: the front\'s own part code on the turned head)')
    for k in [k for k in TH.PEOPLE if k.startswith('kit:')]:
        del TH.PEOPLE[k]
    return out
