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

The EARLY check (Open Wounds chat 35, Sam's Y, 26 Nov: "check each move in the acting list the moment it is
written"): early(film) measures only the head moves that are new or changed since the last early check (each one's
words are kept in notes/ledger/FILM/movesize-seen.json once it reads), so a too-small move is caught the moment it is
written, not ten rounds later at pre-flight. It runs in the quick check (preflight.py NAME OUT --text) and alone:

    python3 source/movesize.py FILM --new

and each acting-list row whose words make a move small ('small nods', 'a curt nod', 'a slight lean') gets its own
line: small means the smallest move a stranger still sees (MIN_PX), and curt means quick, never too small to see
(the four moves Sam passed, 26 Nov, were written 'small' and 'curt' and drawn at 3 to 15 px).
"""
import json
import math
import os
import re
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


def faults(film_name, shots=None, only=None):
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
            if only is not None and _sig(b['shot'], who, m) not in only:
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


# ------------------------------------------------------------------------------------------------ early
SMALL = re.compile(r"\b(small|slight|little|tiny|curt|subtle|faint|brief)\b[^;|.]{0,20}?\b(nods?|lean(?: in)?|bows?|"
                   r"chin up|preens?|peers?)\b", re.I)


def _sig(shot, who, m):
    """One head move's words, as the moves file gives them: changed words, a new move."""
    return json.dumps([str(shot), who, m['move'], m.get('amount'), m.get('a'), m.get('rise'), m.get('fall'),
                       m.get('over'), m.get('with')], sort_keys=True, default=str)


def _seen_path(film_name):
    return os.path.join(os.path.dirname(HERE), 'notes', 'ledger', film_name, 'movesize-seen.json')


def wording(film_name):
    """One line per acting-list row whose words make a head move small or curt."""
    import acting as A
    desc = A.load(film_name)
    out = []
    for key in desc['shots']:
        b = A.block_for(desc, key)
        for mt in SMALL.finditer(b.get('row') or ''):
            out.append(f'MOVE SIZE (wording): shot {b["shot"]} {b.get("who") or key}: the acting list says '
                       f'"{mt.group(0)}": small still means a move a stranger sees ({MIN_PX:.0f} px or more on the '
                       f'1080 x 1920 frame), and curt means quick, not tiny: draw it at that size and keep its timing')
    return out


def early(film_name, seen=None, save=True):
    """The head moves new or changed since the last early check, measured now; then the 'small/curt' lines.
    seen: the moves already measured as reading (default: the film's movesize-seen.json)."""
    import acting as A
    path = _seen_path(film_name)
    if seen is None:
        try:
            with open(path) as f:
                seen = set(json.load(f))
        except (OSError, ValueError):
            seen = set()
    desc = A.load(film_name)
    now = set()
    for key in desc['shots']:
        b = A.block_for(desc, key)
        for m in b['body']:
            if m['move'] in HEAD_MOVES and m['curve'] != 'except':
                now.add(_sig(b['shot'], b.get('who') or key, m))
    new = now - set(seen)
    out = faults(film_name, only=new) if new else []
    if save:                                     # a move that read is not measured again until its words change
        ok = (set(seen) & now) | {s_ for s_ in new if not any(
            f' {json.loads(s_)[1]}: the {json.loads(s_)[2]} ' in x for x in out)}
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(sorted(ok), f, indent=0)
    return out, len(new)


if __name__ == '__main__':
    if '--new' in sys.argv:
        fs, n = early(sys.argv[1])
        print(f'movesize (early): {n} new or changed head move(s) measured')
        print('\n'.join('info: ' + w for w in wording(sys.argv[1])))
        print('\n'.join(fs) or 'movesize: every new head move reads')
    else:
        fs = faults(sys.argv[1], sys.argv[2:] or None)
        print('\n'.join(fs) or 'movesize: every named head move reads')
