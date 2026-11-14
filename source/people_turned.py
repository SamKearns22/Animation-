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
from people_parts import P4, TH, dk, INK, curve, oval

# ---------------------------------------------------------------------------------------------- haircuts from behind
# style: front hair design; hl: hairline; the profile keys say how far down the back the hair reaches. Lifted from
# blessed_cast.PRESS_STYLES; 'knot' and 'none' new (chat 4d: a bun behind; no hair at all, under a wig).
STYLES = {
    'short': dict(hl=-0.1, prof=dict(hair_low=0.4, nape=0.66)),
    'crop': dict(hl=-0.06, prof=dict(hair_low=0.36, nape=0.62, volume=0.015)),
    'bald': dict(hl=None, prof=dict(hair_top=0.3, hair_top_back=0.34, hair_ragged=0.008, hair_low=0.66, nape=0.7)),
    'bob': dict(hl=-0.12, prof=dict(hair_low=0.9, nape=0.95, volume=0.07), long=1.1),
    'pony': dict(hl=-0.14, prof=dict(hair_low=0.44, nape=0.7, volume=0.02), pony=True),
    'curly': dict(hl=-0.08, prof=dict(hair_low=0.5, nape=0.74, volume=0.12), curls=True),
    'long': dict(hl=-0.14, prof=dict(hair_low=0.6, nape=0.8, volume=0.05), long=1.55),
    'side': dict(hl=-0.08, prof=dict(hair_low=0.44, nape=0.7, volume=0.035), parting=True),
    'knot': dict(hl=-0.1, prof=dict(hair_low=0.4, nape=0.66, volume=0.02), knot=True),
    'none': dict(hl=None, prof=dict(), bare=True),
}
TURNED = {'crop': 'crop', 'bald': 'bald', 'side': 'side', 'bob': 'bob', 'long': 'long', 'curly': 'curly',
          'bun': 'knot', 'receding': 'bald', 'none': 'none', 'pony': 'pony', 'short': 'short'}   # kit hair -> from behind
HIDES_EARS = ('bob', 'long', 'curly')       # hair over the ears: none drawn on top of it


# ---------------------------------------------------------------------------------------------- the press pack's pieces
def _layout(sp):
    m = dict(P4.AVG)
    for k, v in sp['kit_face']['m'].items():
        m[k] += v
    return P4.layout(m)


def _cap(L, hl):
    e, c = L['fw'] * 0.5, L['fhw'] * 0.5
    return [(-e - 0.02, 0.36), (-e - 0.03, 0.02), (-e + 0.04, -0.24), (-0.24, -0.4), (0.0, -0.45), (0.24, -0.4),
            (e - 0.04, -0.24), (e + 0.03, 0.02), (e + 0.02, 0.36), (e - 0.03, 0.34), (c + 0.01, 0.12), (c - 0.03, 0.02),
            (c * 0.7, hl), (0.0, hl - 0.012), (-c * 0.7, hl), (-c + 0.03, 0.02), (-c - 0.01, 0.12), (-e + 0.03, 0.34)]


def _profile(style):
    st = STYLES[style]
    return lambda L: TH.fitted(L, -0.42, 1.06, **st['prof'])


def _hair(img, p, f, L, sp, look):
    st, hc, style = STYLES[look['style']], look['hair_c'], look['style']
    if st.get('bare'):
        return
    H = TH.H
    if st.get('long'):
        import people_famous as PF
        PF._turned_long(p, f, hc, st['long'])
    fronts = [] if st['hl'] is None else [f.pts(TH.dense(curve(_cap(L, st['hl']), 2)))]
    prof = TH.PEOPLE[look['key']].build(sp)[1]
    mask = TH.hair(img, p, f, fronts, hc, prof)
    rng = np.random.default_rng(look['strand_seed'])
    yaw = math.degrees(f.th)
    bx = f.hx + (0.0 if yaw >= 170 else -0.18 * H)            # the back of the skull on screen

    def strands(pen):                                          # the hair's fall: strokes down from the crown
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
        x, y = bx, f.top + 0.36 * H
        tail = [(x - 16, y), (x - 26, y + 60), (x - 20, y + 130), (x - 4, y + 168), (x + 12, y + 132), (x + 20, y + 62),
                (x + 16, y)]
        p.poly(curve(tail, 3), hc, INK, 2.2)
        for k in range(3):
            p.line(curve([(x - 6 + 6 * k, y + 14), (x - 10 + 7 * k, y + 80), (x - 4 + 4 * k, y + 140)], 3), dk(hc, 0.72), 1.3)
        p.poly(oval(x, y + 6, 18, 8, 12), (40, 40, 44), INK, 1.6)
    if st.get('knot'):                                         # new: a bun high on the back of the head
        x, y = bx - (0.0 if yaw >= 170 else 0.1 * H), f.top - 0.3 * H
        p.poly(curve(oval(x, y, 26, 22, 18), 2), hc, INK, 2.2)
        for k in range(3):
            p.line(curve([(x - 16 + 12 * k, y - 14), (x - 10 + 12 * k, y), (x - 15 + 12 * k, y + 12)], 3), dk(hc, 0.7), 1.4)
        p.line([(x - 12, y + 22), (x + 12, y + 22)], (40, 40, 44), 3.4)
    _ = style


def _mood(sp, f):
    return dict(lid=0.1, look=0.3, squint=0.0, closed=False, gaze_dy=-0.2), 0.0, 0.0


def _rest(p, f, L, sp, fx, my, lip):
    P4.lips(p, f, L, dict(sp, smile=0.0, mouth='rest'), lip, (fx, my - 6))


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


def _over(img, p, f, L, sp, view):
    if sp['kit_face'].get('glasses') and view in ('three', 'side'):
        PP._glasses(p, f, L, sp['kit_face']['glasses'])


# ---------------------------------------------------------------------------------------------- the Person
def look(sp):
    """This look's turned head: its key and what it is built from (the same look always gets the same Person)."""
    fc = sp['kit_face']
    style = TURNED[fc.get('turned') or fc['hair']]
    hc = tuple(sp.get('hair_c', (40, 32, 28)))
    key = 'kit:%s:%s:%s:%s:%s' % (sp['who'], style, tuple(sp['skin']), hc, sorted(fc['m'].items()))
    return dict(key=key, style=style, hair_c=hc, strand_seed=sp.get('strand_seed', 1),
                ears_hidden=style in HIDES_EARS)


def register(sp, key=None):
    """One turnhead Person per look; key= lets a check key it another way (replicate: the film's way)."""
    lk = look(sp)
    lk['key'] = key or lk['key']
    if lk['key'] not in TH.PEOPLE:
        fc = sp['kit_face']
        face = (lambda pen, f, L, sp2: _marks(pen, f, L, sp)) if (fc.get('stub') or fc.get('beard')
                                                                  or fc.get('freckles')) else None
        TH.register(TH.Person(lk['key'], lambda sp2, _sp=sp: _layout(_sp), -0.42, 0.4, _profile(lk['style']),
                              sp['skin'], fc['iris'], fc['brow'], fc['lip'], _mood,
                              lambda p, f, L, sp2, fx, my, _l=fc['lip']: _rest(p, f, L, sp2, fx, my, _l),
                              lambda img, p, f, L, sp2, _lk=lk: _hair(img, p, f, L, sp2, _lk),
                              face=face, over=_over if fc.get('glasses') else None))
    return lk


ON = True        # replicate turns this off to score a frame without the new turned heads (crowds keep theirs: the film's)
KEYED = {}       # who -> a function(sp) -> key, to key a look another way (replicate keys the press the film's way)


# ---------------------------------------------------------------------------------------------- install
def install():
    """Once: an invented kit face's turned views through its own turnhead Person, at the house's bigger head size (no
    lift: from behind, the neck shows long)."""
    V = PP.AV.MC.V
    if getattr(V.head_view, 'kit_turned', False):
        return
    old = V.head_view

    def head_view(img, p, sp, t, view, hx=0.0, hy=-150.0):
        if (ON or sp.get('kit_crowd')) and sp.get('kit_face') and not sp.get('kit_head') and not sp.get('kit_famous') and view in TH.YAW:
            k = KEYED.get(sp['who'])
            lk = register(sp, k(sp) if k else None)
            with PP._Big():
                return TH.draw(img, p, dict(sp, who=lk['key'], ears_hidden=lk['ears_hidden']), t, view, hx, hy)
        return old(img, p, sp, t, view, hx, hy)
    head_view.kit_turned = head_view.turnhead = True
    V.head_view = head_view
