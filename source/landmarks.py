#!/usr/bin/env python3
"""Body landmarks (Sam, 18 Oct: the skirts first started at the knee, not the waist; Jenrick came out a squat
dwarf). Where the waist, hips, knees and ankles are on the people's skeleton (views.py units: y down from the neck
base), drawn as guide lines across a cast sheet, and a check that clothes start and end where real ones do.

A film lists its clothes in OUTFIT = {who: {'jacket hem': y, 'skirt top': y, 'skirt hem': y, 'trouser top': y,
'blouse hem': y}} (person units, as drawn) and real heights in HEIGHTS = {who: metres}; preflight.py runs faults().
    landmarks.draw(d, x, y_neck, s, width)     the guide lines on a cast sheet panel
"""
import views as V

LANDMARKS = {'shoulders': 60.0, 'chest': 200.0, 'waist': 395.0, 'hips': V.HIP_Y, 'crotch': 520.0,
             'knee': V.HIP_Y + 228.0, 'ankle': 890.0, 'sole': 928.0}
RULES = {   # garment edge: (landmark, allowed distance either way, person units)
    'jacket hem': ('hips', (0, 90)),             # suit jackets cover the seat: from the hips to just below
    'cropped jacket hem': ('waist', (-20, 45)),
    'skirt top': ('waist', (-30, 40)),           # a skirt starts at the waist, never lower than the hips
    'skirt hem': ('knee', (-60, 80)),            # knee length: just above to just below the knee
    'trouser top': ('waist', (-30, 55)),
    'blouse hem': ('hips', (-60, 60)),           # untucked; a tucked blouse ends under the skirt top
}
HEIGHTS_OK = 0.06                                # metres: a person's height on screen within this of their real one


def draw(d, x, y_neck, s, width, colour=(220, 60, 60)):
    for name, y in LANDMARKS.items():
        yy = y_neck + y * s
        d.line([(x - width / 2, yy), (x + width / 2, yy)], fill=colour, width=1)
        d.text((x + width / 2 - 70, yy - 14), name, fill=colour)


def faults(film):
    out = []
    for who, edges in getattr(film, 'OUTFIT', {}).items():
        for edge, y in edges.items():
            if edge not in RULES:
                continue
            mark, (lo, hi) = RULES[edge]
            off = y - LANDMARKS[mark]
            if not lo <= off <= hi:
                out.append(f'{who}: the {edge} is at {y:.0f}, {off:+.0f} from the {mark} ({LANDMARKS[mark]:.0f}); it '
                           f'should be {lo:+d} to {hi:+d} from it')
    drawn = getattr(film, 'DRAWN_HEIGHTS', {})
    for who, real in getattr(film, 'HEIGHTS', {}).items():
        if who in drawn and abs(drawn[who] - real) > HEIGHTS_OK:
            out.append(f'{who}: drawn {drawn[who]:.2f} m tall; really about {real:.2f} m')
    return out
