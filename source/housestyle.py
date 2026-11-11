#!/usr/bin/env python3
"""The house style is on (Sam, 18 Oct: Shocking Behaviour began without the smoother limbs, and without the
general audit, because it was not started from the template). preflight.py runs this on every satire film: each
thing the template switches on must be on, and each shared check must have what it needs from the film."""
import os
import re
import sys

import figure as F

NEEDS = [   # (what the film defines, why, the kind of thing it is for: rule 58, the film's HAS)
    ('audits', 'the general audit (each body alone: in pieces, popping, stretching, frozen): start from the template',
     'people'),
    ('LINE_SUBJECTS', 'the line-work check (every shape outlined, one weight)', 'people'),
    ('PROP_SIZES', 'the real-size check for props and set pieces', 'props'),
    ('OUTFIT', "the clothes check (skirts from the waist, jackets to the hips)", 'people'),
]


def faults(film, B, has=None):
    out = []
    if not getattr(B, '_limbs', None):
        out.append('house style: the smoother limbs are off (limbs.install(B), as in the template)')
    if 'arm' not in F._GUARDED:
        out.append('house style: the arm checker is off (figure.guard(B), as in the template)')
    for name, why, kind in NEEDS:
        if (has is None or kind in has) and not hasattr(film, name):
            out.append(f'house style: the film has no {name}: {why}')
    moving = any(getattr(film, n, None) for n in ('CONTACTS', 'MOMENTUM', 'PUSHES', 'IN_SHOT')) or \
        getattr(film, 'MOTION_LED', False)
    for name in ('solids', 'layers'):                # people or things moving near each other: the clip check
        if moving and not hasattr(film, name):
            out.append(f'house style: the film has action but no {name}(t): the clip check cannot see it')
    out += eye_faults(film)
    return out


def eye_faults(film):
    """Rule S5 (tool job, 11 Nov): a film's own cast files that draw a pupil must cut it to the eye's outline
    (eyekit, or clip_convex as remakes_cast does); burnham's stock faces already do."""
    out = []
    base = getattr(film, '__name__', '').split('_')[0]
    here = os.path.dirname(os.path.abspath(__file__))
    for name, mod in list(sys.modules.items()):
        path = getattr(mod, '__file__', None) or ''
        if not base or not (name == film.__name__ or name.startswith(base + '_')) or os.path.dirname(path) != here:
            continue
        try:
            src = open(path).read()
        except OSError:
            continue
        if re.search(r'\bpupil', src) and not re.search(r'\beyekit\b|\bclip_convex\b', src):
            out.append(f'rule S5: {name}.py draws pupils without cutting them to the eye (use eyekit.iris_and_pupil '
                       'or eyekit.inside)')
    return out
