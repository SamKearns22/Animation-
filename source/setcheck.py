#!/usr/bin/env python3
"""Rule 83 (Sam, 8 Nov, Ad-Vanced Notice note 42b: the study's portrait clipped into the mantel clock and nothing caught
it): in a flat painted set, no painted object overlaps another unless the set lists it as meant. A set file gives
SET_BOXES = [(name, (x0, y0, x1, y1))] in any one unit (its wall metres, or screen px) and SET_MEANT = [(a, b, why)];
the film's checks() calls faults(SET_BOXES, SET_MEANT).

Rule 13 (tool job, 11 Nov; first built as Remakes' camp check, rule 56): a figure moving through a set, every frame,
against the set's solid things on the ground. A set lists SET_FEET = [(name, x0, x1, d0, d1, top, layer)]: a thing's
footprint in metres (x across, d away from the camera), its height, and whether the set paints it 'under' the cast
(behind) or 'over' it (in front). The film gives movers(t) -> [(who, x, d, (body_w, body_h))] in the same metres,
SET_CAM (with p(x, d, z) -> screen point and ppm(d) -> pixels per metre at that distance) and MOVE_SPAN = (t0, t1).
moving_faults names: feet inside a solid thing; a figure further away than something painted under the cast yet
overlapping it on screen (he would show in front of what hides him); one nearer than something painted over him.
Pre-flight runs film_faults on every film that has SET_FEET (and says so when a film with people has SET_BOXES but
no SET_FEET).

MAP
  faults ........... rule 83: painted objects overlapping in a flat set
  moving_faults .... rule 13: moving figures against the set's solid things, every frame
  film_faults ...... pre-flight's entry: the film's SET_FEET, movers, SET_CAM, MOVE_SPAN

    python3 source/setcheck.py SETMODULE      (rule 83)
    python3 source/setcheck.py --moving FILM  (rule 13)
"""
import importlib
import sys


def faults(boxes, meant=()):
    ok = {frozenset((a, b)) for a, b, *_ in meant}
    out = []
    for i, (a, A) in enumerate(boxes):
        for b, Bx in boxes[i + 1:]:
            w = min(A[2], Bx[2]) - max(A[0], Bx[0])
            h = min(A[3], Bx[3]) - max(A[1], Bx[1])
            if w > 0 and h > 0 and frozenset((a, b)) not in ok:
                out.append(f'SET OVERLAP (rule 83): {a} and {b} overlap ({w:.3g} x {h:.3g}): move one, or list it in '
                           f'SET_MEANT with why')
    return out


def moving_faults(movers, feet, cam, t0, t1, fps=12, label='', margin=0.15):
    """Every frame from t0 to t1: each mover (who, x, d, (bw, bh)) against each solid thing in feet. Returns faults
    ('LABEL 3.25s: link stands in the barrel')."""
    out = []
    pre = f'{label} ' if label else ''
    for fr in range(int(t0 * fps), int(t1 * fps) + 1):
        t = fr / fps
        for w, x, d, (bw, bh) in movers(t):
            sx, sy = cam.p(x, d)
            k = cam.ppm(d)
            fig = (sx - bw / 2 * k, sy - bh * k, sx + bw / 2 * k, sy)
            for n, x0, x1, d0, d1, z1, layer in feet:
                if x0 - margin < x < x1 + margin and d0 - margin < d < d1 + margin:
                    out.append('%s%.2fs: %s stands in the %s' % (pre, t, w, n))
                    continue
                pts = [cam.p(xx, dd, zz) for xx in (x0, x1) for dd in (d0, d1) for zz in (0, z1)]
                box = (min(q[0] for q in pts), min(q[1] for q in pts), max(q[0] for q in pts), max(q[1] for q in pts))
                over = fig[0] < box[2] and box[0] < fig[2] and fig[1] < box[3] and box[1] < fig[3]
                if over and layer == 'under' and d > d0:
                    out.append('%s%.2fs: %s is behind the %s but drawn over it' % (pre, t, w, n))
                if over and layer == 'over' and d < d0:
                    out.append('%s%.2fs: %s is in front of the %s but drawn under it' % (pre, t, w, n))
    return out


def film_faults(film, fps=None):
    """Pre-flight: rule 13's moving-figure check on any film whose set lists SET_FEET (the film's own, or SET_FEET
    given through the film). A film with people and SET_BOXES but no SET_FEET is named, never skipped quietly."""
    feet = getattr(film, 'SET_FEET', None)
    if feet is None:
        if getattr(film, 'SET_BOXES', None) is not None and 'people' in set(getattr(film, 'HAS', ('people',))):
            return ['rule 13: the film has SET_BOXES but no SET_FEET, movers(t) and SET_CAM, so nothing checks '
                    'figures moving against the set (setcheck.moving_faults)']
        return []
    missing = [n for n in ('movers', 'SET_CAM', 'MOVE_SPAN') if not hasattr(film, n)]
    if missing:
        return [f'rule 13: the film has SET_FEET but no {", ".join(missing)}: the moving-figure check cannot run']
    t0, t1 = film.MOVE_SPAN
    out = moving_faults(film.movers, feet, film.SET_CAM, t0, t1, fps or getattr(film, 'FPS', 12))
    return out[:8] + ([f'... and {len(out) - 8} more'] if len(out) > 8 else [])


if __name__ == '__main__':
    if sys.argv[1] == '--moving':
        f = film_faults(importlib.import_module(sys.argv[2]))
        print('\n'.join(f) if f else 'moving figures: clear of the set')
        sys.exit(0)
    m = importlib.import_module(sys.argv[1])
    f = faults(m.SET_BOXES, getattr(m, 'SET_MEANT', ()))
    print('\n'.join(f) if f else 'set overlaps: none unmeant')
