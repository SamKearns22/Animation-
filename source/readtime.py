#!/usr/bin/env python3
"""MAP  readtime (Open Wounds note 22, 26 Nov): is a story action on screen long enough to be seen?

Sam: "The final wolf pounce on Tony, so quick it's barely registered by the viewer." Seen before: note 13, the
worker's pounce. Why nobody saw it: every check looked at single frames (each frame of the leap was a fine drawing);
nothing asked how long the action is on screen, or whether the eye is led to it before it happens. Four frames of a
wolf already in mid-air, from off-screen, read as a blur at phone size.

A film lists its story actions (READ_TIMES: name, seconds the actor is seen before the action, the wind-up's
seconds, the action's seconds); faults() flags any action seen for under SEEN_MIN in all, with a wind-up under
WINDUP_MIN, or the action itself under ACT_MIN (at 12 fps: 6 frames). Pre-flight runs it on every film with READ_TIMES.

    from readtime import faults; faults(film)

On screen (Open Wounds note 28, chat 42: "We have lost the moment where the person leaps from the construction site"):
the site was brought nearer and the runner's leap landed at the frame's edge, out of sight. Nothing asked whether a
story action happens INSIDE the frame after a framing change. A film lists ON_SCREEN rows (name, point(t) -> the
actor's screen x, y, t0, t1): the action's point must be inside the frame, MARGIN px in from its edges, for ACT_MIN
of its seconds (sampled at 12 a second).
"""
SEEN_MIN = 1.0       # s: the actor on screen before the action lands (the eye finds it)
WINDUP_MIN = 0.3     # s: the anticipation (a coil, a draw back): the viewer's cue that it is coming
ACT_MIN = 0.5        # s: the action itself


def check(name, seen, windup, act):
    out = []
    if seen + windup + act < SEEN_MIN:
        out.append(f'{name}: on screen {seen + windup + act:.2f} s in all (under {SEEN_MIN} s): the eye has no time '
                   f'to find it (Sam, note 22, "barely registered")')
    if windup < WINDUP_MIN:
        out.append(f'{name}: wind-up {windup:.2f} s (under {WINDUP_MIN} s): nothing tells the viewer it is coming')
    if act < ACT_MIN:
        out.append(f'{name}: the action {act:.2f} s (under {ACT_MIN} s): a blur at phone size')
    return ['READ TIME: ' + f for f in out]


MARGIN = 40          # px in from the frame's edges: an actor on the very edge is half cut away, not seen


def on_screen(name, point, t0, t1, w=1080, h=1920):
    """A story action inside the frame long enough to be seen (note 28)."""
    n = max(1, int(round((t1 - t0) * 12)))
    inside = 0
    for i in range(n):
        x, y = point(t0 + (i + 0.5) / 12.0)
        inside += MARGIN <= x <= w - MARGIN and MARGIN <= y <= h - MARGIN
    if inside / 12.0 < min(ACT_MIN, t1 - t0):
        return [f'READ TIME: {name}: inside the frame {inside / 12.0:.2f} s of {t1 - t0:.2f} s (under {ACT_MIN} s): '
                f'it happens at or past the frame\'s edge (Sam, note 28, "we have lost the moment")']
    return []


def faults(film):
    out = []
    for row in getattr(film, 'READ_TIMES', None) or []:
        out += check(*row)
    for row in getattr(film, 'ON_SCREEN', None) or []:
        out += on_screen(*row)
    return out
