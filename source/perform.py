#!/usr/bin/env python3
"""Natural performance, shared (Sam, 18 Oct: the first dance faces were robotic and the moves stiff; fixed in
Shocking Behaviour, now the default for every film). Use these on any pose that comes from key poses on a beat.

    follow(pose_at, m)          the body leads, the hands arrive ARMS_LAG later and the head HEAD_LAG later
                                (overlapping action), so nothing moves as one rigid block
    bounce(m, beat, depth)      a dip in the knees on every beat (added to the pose's 'dip')
    face_cycle(m, beat, faces)  synchronised faces that change every two beats through a varied list, snapping
                                (faces snap; bodies flow), never one face held for the whole dance
    ease_mix(u)                 half eased, half linear: arrives into each key without stopping dead on it
Rules of thumb (Williams; Sam's notes): the whole upper body moves as one piece in a sway (the neck never comes
away); the leading foot steps out with a big sway; arms go big and wide on a pop routine; a held pose still moves a
little (filmkit.shifts); faces vary every two beats with happy, groovy expressions (grin, sing, pout, bliss, smug).
"""
import math

ARMS_LAG = 0.06
HEAD_LAG = 0.09
GROOVY = ['grin', 'sing', 'pout', 'grin', 'bliss', 'smug', 'sing', 'grin', 'pout', 'bliss', 'smug', 'sing']


def follow(pose_at, m, arms=('L', 'R', 'poleL', 'poleR'), head=('head', 'chin')):
    k = dict(pose_at(m))
    a, h = pose_at(m - ARMS_LAG), pose_at(m - HEAD_LAG)
    for f in arms:
        if f in a:
            k[f] = a[f]
    for f in head:
        if f in h:
            k[f] = h[f]
    return k


def bounce(m, beat, depth=7.0):
    return depth * (0.5 - 0.5 * math.cos(2 * math.pi * m / beat))


def face_cycle(m, beat, faces=GROOVY, beats=2):
    return faces[int(max(0.0, m) / (beats * beat)) % len(faces)]


def ease_mix(u):
    e = u * u * (3 - 2 * u)
    return e * 0.5 + u * 0.5
