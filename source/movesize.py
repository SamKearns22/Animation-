#!/usr/bin/env python3
"""MAP  Move size (Open Wounds chat 32, 26 Nov): does a named nod or lean READ on screen?

The fresh-eye review (round 27, May in shot 1) said: "she sits upright and square, never leaning in as she talks" and
"no nod reads". The moves file named both; the acting check only asks that a move EXISTS near its word, never how far
it moves what a viewer sees. Two causes, both invisible to that check: a nod of 1 dropped the head 7 px on a 1920 px
frame (2-3 px on a phone), and 'lean in 0.8' meant 0.8 DEGREES (a body move's amount is in its first channel's units),
not 0.8 of a lean.

This check looks as a viewer: for every head move the moves file names (nod, lean in, bow, chin up, preen, peer,
lean), it draws the film's own frame just before the move and at its peak, and measures how far the person's eyes
moved on screen (views.person notes each eye as drawn,
and the mid-face point after lean, roll and nod: _drawn['head_at']). Under MIN_PX (on the 1080 x 1920 frame) is a fault.

  faults(film, shots=None) -> ['shot 1 may: the nod at 4.12 s moves her head 4 px ...']
  The film records what it draws: module.DRAWN[who] = views.person(...)'s return (Open Wounds does). A film that
  does not is named, not passed.

    python3 source/movesize.py FILM [SHOT ...]
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

MIN_PX = 22.0          # the head's move on the 1080 x 1920 frame: about 5 px on a phone held at arm's length, the
#                        least a stranger sees as a nod without looking for it (round 27: 7 px read as "no nod"; 21 px still hard to see on a sheet)
HEAD_MOVES = {'nod', 'lean in', 'bow', 'chin up', 'preen', 'peer', 'lean', 'nod by'}


def _eyes_at(module, who, t):
    module.picture(t)
    d = (module.DRAWN.get(who) or {}).get('_drawn') or {}
    eyes = d.get('eyes') or []
    if eyes:
        xs = [e['white'][0] for e in eyes]
        ys = [e['white'][1] for e in eyes]
        return sum(xs) / len(xs), sum(ys) / len(ys)
    return d.get('head_at')           # a house face that does not note its eyes: the head's mid-face point


def faults(film_name, shots=None):
    import acting as A
    desc = A.load(film_name)
    film = A.film_side(film_name)
    A.install_gaits(desc)
    module = film['module']
    if not hasattr(module, 'DRAWN'):
        return [f'movesize: {film_name} does not record what it draws (DRAWN); not measured']
    out = []
    for key in desc['shots']:
        b = A.block_for(desc, key)
        if shots and b['shot'] not in shots:
            continue
        who = b.get('who') or key
        start, cut = film['span'](b['shot'])
        clock = A.Clock(film, b, b['shot'], None)
        for m in b['body']:
            if m['move'] not in HEAD_MOVES or m['curve'] == 'except':
                continue
            a = clock(m['a'])
            if m['curve'] == 'ramp':
                peak = a + m['over']
            else:
                peak = a + m['rise'] + 0.02
            before = max(start + 0.01, a - 0.02)
            if not (start <= peak < cut):
                continue
            p0, p1 = _eyes_at(module, who, before), _eyes_at(module, who, peak)
            if p0 is None or p1 is None:
                out.append(f'shot {b["shot"]} {who}: the {m["move"]} at {a:.2f} s: no eyes drawn to measure')
                continue
            px = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
            if px < MIN_PX:
                out.append(f'shot {b["shot"]} {who}: the {m["move"]} at {a:.2f} s moves the head {px:.0f} px '
                           f'(about {px * 390 / 1080:.0f} on a phone): a viewer sees no {m["move"]}; it needs '
                           f'{MIN_PX:.0f} px or more (a body move\'s amount is in its first channel\'s units: '
                           f'acting.BODY)')
    return out


if __name__ == '__main__':
    fs = faults(sys.argv[1], sys.argv[2:] or None)
    print('\n'.join(fs) or 'movesize: every named head move reads')
