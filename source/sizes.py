#!/usr/bin/env python3
"""Real sizes (Sam, 18 Oct: the paper, pens, lift and doorway came out at the wrong size, out of proportion with
everything round them). Every prop and set piece is drawn at its real size in metres, through the same camera as the
people, never by eye in pixels. This holds the sizes and checks what a film draws against them.

A film lists what it draws in PROP_SIZES = [(name, kind, width, height, px_per_m)]: width and height in metres
(px_per_m None), or in pixels with the scale of that spot (px_per_m = pixels per metre there, e.g. a person's
s / views.M_PER_UNIT), or in pixels with px_per_m 0 when the depth is unknown (then only the shape is judged: a lift
door twice as tall as wide, not stick-thin). Sizes within TOL pass. preflight.py runs it.

    python3 source/sizes.py FILM           check a film's PROP_SIZES
    python3 source/sizes.py list           print the table
"""
import importlib
import sys

TOL = 0.30                       # 30% either way: real things vary; anything further out looks wrong
SIZES = {   # kind: (width m, height m), the face we usually see (UK where it matters). Length for long thin things.
    'person': (0.45, 1.75), 'child': (0.3, 1.2),
    'A4 paper': (0.21, 0.297), 'biro': (0.145, 0.01), 'pencil': (0.175, 0.008), 'mug': (0.085, 0.095),
    'takeaway cup': (0.09, 0.15), 'can': (0.066, 0.115), 'pen pot': (0.08, 0.1), 'desk plant': (0.15, 0.25),
    'phone': (0.072, 0.15), 'laptop open': (0.33, 0.23), 'monitor': (0.55, 0.36), 'keyboard': (0.44, 0.03),
    'lanyard card': (0.054, 0.086), 'playing card': (0.063, 0.088), 'poker chip': (0.039, 0.0033), 'small handbag': (0.25, 0.18), 'briefcase': (0.42, 0.32),
    'desk': (1.4, 0.74), 'desk depth': (0.75, 0.74), 'office chair': (0.6, 1.0), 'meeting table': (2.4, 0.74),
    'door': (0.84, 2.04), 'double doorway': (1.6, 2.1), 'lift door opening': (1.0, 2.1), 'lift surround': (1.4, 2.4),
    'window pane': (1.2, 1.5), 'ceiling height office': (3.0, 2.7), 'light switch': (0.086, 0.086), 'exit sign': (0.36, 0.13),
    'moped': (0.7, 1.15), 'moped side': (1.85, 1.15), 'motorbike side': (2.1, 1.2), 'e-scooter side': (1.1, 1.2),
    'bicycle side': (1.75, 1.05), 'car side': (4.3, 1.5), 'car front': (1.8, 1.5), 'bus side': (10.5, 4.4),
    'lectern': (0.6, 1.2), 'podium flag': (0.9, 1.5), 'tv camera': (0.25, 0.3), 'microphone': (0.05, 0.2),
    # Power Crime Action (20 Oct): Met TSG carrier = Mercedes Sprinter high roof (5.93 x 2.02 x 2.7 m); SIG MCX
    # carbine about 0.75 m with the stock out; a protest placard of the Defend Our Juries kind about 45 x 60 cm (Sam's photos);
    # a hand-waved flag 0.9 x 0.6 m on a 1.2 m pole; Nelson's Column 51.6 m to the top of the statue.
    'police van side': (5.93, 2.7), 'police van back': (2.02, 2.7), 'carbine': (0.75, 0.2),
    'protest placard': (0.45, 0.6), 'hand flag': (0.9, 0.6), "Nelson's Column": (5.0, 51.6),
}


def check(name, kind, w, h, px_per_m=None):
    """A fault, or None, for one thing drawn w x h (metres, or pixels with px_per_m)."""
    if kind not in SIZES:
        return f'{name}: no real size for "{kind}" in sizes.SIZES: add it (look it up) before drawing'
    rw, rh = SIZES[kind]
    if px_per_m == 0:                                    # depth unknown: judge the shape only
        got, want = w / h, rw / rh
        if not (1 - TOL) <= got / want <= 1 + TOL:
            return (f'{name}: drawn {w:.0f} x {h:.0f} px, {got:.2f} wide per tall; a real {kind} is {want:.2f} '
                    f'({rw} x {rh} m): too {"wide" if got > want else "thin"}')
        return None
    if px_per_m:
        w, h = w / px_per_m, h / px_per_m
    for got, want, what in ((w, rw, 'wide'), (h, rh, 'tall')):
        if want and not (1 - TOL) <= got / want <= 1 + TOL:
            return f'{name}: {got:.2f} m {what}; a real {kind} is about {want} m ({got / want:.0%} of it)'
    return None


def faults(film):
    out = []
    for name, kind, w, h, ppm in getattr(film, 'PROP_SIZES', ()):
        f = check(name, kind, w, h, ppm)
        if f:
            out.append(f)
    return out


def scale_ref(d, x, y_floor, px_per_m, colour=(150, 150, 160)):
    """A plain 1.75 m person and a 1 m ruler standing on the floor at x, for a scale sheet: draw any new prop beside
    it at the same px_per_m, so its size is seen against a person before it goes in a shot."""
    h = 1.75 * px_per_m
    hw = 0.22 * px_per_m
    d.ellipse([x - 0.1 * px_per_m, y_floor - h, x + 0.1 * px_per_m, y_floor - h + 0.23 * px_per_m], fill=colour)
    d.rounded_rectangle([x - hw, y_floor - h + 0.25 * px_per_m, x + hw, y_floor], radius=int(0.08 * px_per_m), fill=colour)
    rx = x + hw + 0.15 * px_per_m
    d.line([(rx, y_floor), (rx, y_floor - px_per_m)], fill=(200, 40, 40), width=3)
    for i in range(11):
        yy = y_floor - i * px_per_m / 10
        d.line([(rx - (8 if i % 5 else 16), yy), (rx, yy)], fill=(200, 40, 40), width=2)


if __name__ == '__main__':
    if sys.argv[1] == 'list':
        for k, (w, h) in SIZES.items():
            print(f'{k:24s} {w:6.3f} x {h:6.3f} m')
    else:
        f = faults(importlib.import_module(sys.argv[1]))
        print('\n'.join(f) if f else 'sizes: everything at its real size')
