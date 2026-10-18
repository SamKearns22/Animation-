#!/usr/bin/env python3
"""The house style is on (Sam, 18 Oct: Shocking Behaviour began without the smoother limbs, and without the
general audit, because it was not started from the template). preflight.py runs this on every satire film: each
thing the template switches on must be on, and each shared check must have what it needs from the film."""
import figure as F

NEEDS = [   # (what the film defines, why)
    ('audits', 'the general audit (each body alone: in pieces, popping, stretching, frozen): start from the template'),
    ('LINE_SUBJECTS', 'the line-work check (every shape outlined, one weight)'),
    ('PROP_SIZES', 'the real-size check for props and set pieces'),
    ('OUTFIT', "the clothes check (skirts from the waist, jackets to the hips)"),
]


def faults(film, B):
    out = []
    if not getattr(B, '_limbs', None):
        out.append('house style: the smoother limbs are off (limbs.install(B), as in the template)')
    if 'arm' not in F._GUARDED:
        out.append('house style: the arm checker is off (figure.guard(B), as in the template)')
    for name, why in NEEDS:
        if not hasattr(film, name):
            out.append(f'house style: the film has no {name}: {why}')
    moving = any(getattr(film, n, None) for n in ('CONTACTS', 'MOMENTUM', 'PUSHES', 'IN_SHOT')) or \
        getattr(film, 'MOTION_LED', False)
    for name in ('solids', 'layers'):                # people or things moving near each other: the clip check
        if moving and not hasattr(film, name):
            out.append(f'house style: the film has action but no {name}(t): the clip check cannot see it')
    return out
