#!/usr/bin/env python3
"""crowdpath: keep a street crowd from passing through each other, trees, posts and walls (every film with a crowd).

Sam, GTA v5 note 13 (23 Nov): "The runners need to run in different directions ... and not clip into the walls or any
other object." A crowd's people each follow a path on the ground (z along the street, x across it). Their paths were
never checked against one another or against what stands on the pavement, so walkers met head-on and walked through
each other and through palm trunks. This moves each faulty person sideways (their x, or their running lane) to the
nearest clear line; when and how far they walk or run is never changed.

MAP
  track ........ a person's ground path (x, z) over the times
  faults ....... one person's clashes against the others and the fixed posts (trunks, hydrants), within the pavement
  clear ........ the fixing pass: everyone at fault tries the nearby lines, nearest first, and keeps the first clear one
  report ....... every clash left (for a check): who, with whom or what, when

Use (a film's crowd):
    import crowdpath as CP
    CP.clear(people, pos_fn, set_line, lines_fn, posts, ts)
      pos_fn(pp, t) -> (x, z); set_line(pp, x) moves pp to the line x; lines_fn(pp) -> the lines to try;
      posts: [(x, z, radius)]; ts: the times to check (0.1 s apart catches a run past a post)
"""
import numpy as np

BODY = 0.25          # a person's half-width on the ground (m): two pass side by side with 0.5 m between their middles
DEPTH = 0.16         # and half their depth front to back: one stands 0.32 m behind another without touching


def track(pp, pos_fn, ts):
    return np.array([pos_fn(pp, t)[:2] for t in ts])


def _clashes(a, others):
    """For path a against every path in others (N, K, 2): the first sample index of each clash, -1 for none."""
    dx = np.abs(others[:, :, 0] - a[None, :, 0])
    dz = others[:, :, 1] - a[None, :, 1]
    near = (dx / (2 * BODY)) ** 2 + (dz / (2 * DEPTH)) ** 2 < 1.0
    cross = (dx[:, 1:] < 2 * BODY) & (dx[:, :-1] < 2 * BODY) & (np.sign(dz[:, 1:]) != np.sign(dz[:, :-1]))
    hit = near[:, :-1] | cross
    return np.where(hit.any(axis=1), hit.argmax(axis=1), -1)


def faults(i, tracks, posts, first=False):
    a = tracks[i]
    out = []
    for (px, pz, r) in posts:
        if abs(px - a[0, 0]) > r + BODY + 4 and np.abs(a[:, 0] - px).min() > r + BODY:
            continue
        d = np.hypot(a[:, 0] - px, a[:, 1] - pz)
        if d.min() < r + BODY:
            out.append(('post', (px, pz), int(d.argmin())))
            if first:
                return out
    ids = [j for j in tracks if j != i]
    if ids:
        k = _clashes(a, np.stack([tracks[j] for j in ids]))
        for j, kk in zip(ids, k):
            if kk >= 0:
                out.append(('person', j, int(kk)))
                if first:
                    return out
    return out


def clear(people, pos_fn, set_line, lines_fn, posts, ts, key=lambda pp: pp['i'], passes=2):
    """Fix every person at fault, in order: the nearest clear line wins; none clear: the one with fewest clashes.
    Two passes: a later move can clear an earlier person's only line."""
    tracks = {key(pp): track(pp, pos_fn, ts) for pp in people}
    moved = 0
    for _ in range(passes):
        for pp in people:
            i = key(pp)
            if not faults(i, tracks, posts, first=True):
                continue
            best = None
            for x in lines_fn(pp) or []:
                old = set_line(pp, x)
                tracks[i] = track(pp, pos_fn, ts)
                n = len(faults(i, tracks, posts))
                if best is None or n < best[0]:
                    best = (n, x)
                set_line(pp, old)
                if n == 0:
                    break
            if best is None:
                tracks[i] = track(pp, pos_fn, ts)
                continue
            set_line(pp, best[1])
            tracks[i] = track(pp, pos_fn, ts)
            moved += 1
    return moved


def report(people, pos_fn, posts, ts, key=lambda pp: pp['i']):
    tracks = {key(pp): track(pp, pos_fn, ts) for pp in people}
    out = []
    for pp in people:
        i = key(pp)
        for f in faults(i, tracks, posts):
            if f[0] == 'person' and f[1] < i:
                continue
            out.append((i,) + f[:2] + (round(float(ts[f[2]]), 2),))
    return out
