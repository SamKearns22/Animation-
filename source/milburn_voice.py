#!/usr/bin/env python3
"""MAP  Milburn's voices and the film's clock (Sam's 16 recordings, 18 Nov): the takes cleaned and matched, then the
timeline that follows from how long each really is.

  VOICES ....... {line n: the cleaned, matched, levelled take (48 kHz)}; lines made of two takes are joined
  LINES_TIMED .. {n: dict(start, end, stretches, env, bleep)} start/end in film seconds, stretches = where the line
                 really speaks (seconds from its start), env = loudness for the mouth
  TIMES ........ every shot cut and beat, from the lines (nothing in the film's timing is typed in any more)
  word_times ... when each word of a line is reached (syllables spread over the real speech)

Map: takes 30 | cleaning (takes.clean, shared) 36 | timeline 75 | word times 160
"""
import math
import os

import numpy as np

import mossad_audio as MA
import mouths
import takes as T
from burnham_film import load

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
LUFS = -20.0

# which of Sam's files make each line (in order); `gap`: seconds of silence between two takes of one line
TAKES = {1: ['report'], 2: ['unique-opportunity'], 3: ['the-zone'], 4: ['slash-battle-royale'],
         5: ['long-in-the-making'], 6: ['where-this-one-goes'], 7: ['continue'], 8: ['unit'], 9: ['erstwhile'],
         10: ['you-fucker', 'squid-games'], 11: ['feel-that-way'], 12: ['live-tv'],
         13: ['multifaceted', 'blood-dome'], 14: ['backbenchers']}
GAP = {10: 0.3, 13: 0.35}
FUCK = (1.45, 1.77)            # "fuck" in the you-fucker take (seconds in the file, from the sound; rule 26)
ORDER = sorted(TAKES)


def _build():
    """The takes cleaned the shared way (takes.clean: Milburn's chat 18 cleaning, now one means for every film and
    registered for the voice check); the swear's time moved by where its file was cut."""
    voices, cut = T.clean('milburn-', TAKES, GAP, LUFS)
    s0 = cut[(10, 'you-fucker')]
    return voices, (FUCK[0] - s0, FUCK[1] - s0)


VOICES, _FUCK = _build()
DUR_OF = {n: len(v) / SR for n, v in VOICES.items()}


def bleeped(n):
    """The sound of line n: where Sam swears, a 1 kHz tone goes over the word (rule 26)."""
    v = VOICES[n].copy()
    if n == 10:
        b0, b1 = (int(t * SR) for t in _FUCK)
        k = np.arange(b1 - b0)
        ramp = np.minimum(1, np.minimum(k, len(k) - k) / (0.006 * SR))
        v[b0:b1] = 0.18 * np.sin(2 * math.pi * 1000 * k / SR) * ramp
    return v


# ================================================================================================= timeline
def _timeline():
    """Film seconds for every line, shot cut and beat. Gaps between lines are the old film's (dead air already
    cut, note 11); the gunfire gap after "unit" is the forest's; each cut sits just before the line it brings in."""
    gap = {2: 0.6, 3: 1.0, 4: 0.3, 5: 0.5, 6: 0.6, 7: 0.6, 8: 1.1, 9: 2.5, 10: 0.3, 11: 0.7, 12: 0.8, 13: 1.6,
           14: 1.2}
    s, e = {}, {}
    t = 0.3
    for n in ORDER:
        if n > 1:
            t = e[n - 1] + gap[n]
        s[n], e[n] = t, t + DUR_OF[n]
        t = e[n]
    return s, e


START, END = _timeline()

LINES_TIMED = {}
for _n in ORDER:
    _st = T.STRETCHES['milburn-' + '+'.join(TAKES[_n])]    # where the take speaks (takes.clean, shared)
    LINES_TIMED[_n] = dict(start=START[_n], end=END[_n], stretches=_st,
                           env=mouths.loudness_open(VOICES[_n], SR), bleep=_FUCK if _n == 10 else None)


# the forest's clock: T0 (the shot starts), T_GUN, T_FLAME, T_STARS, T1 (the shot ends)
FOREST = (START[8] - 0.5, END[8] + 0.3, END[8] + 1.1, END[8] + 1.8, END[9] + 0.1)


def word_times(n, text):
    """[(word, film seconds it is reached)] for line n: the words' syllables spread over where the line speaks."""
    words = text.split()
    stretches = LINES_TIMED[n]['stretches']
    syl = [mouths._syllables(w) for w in words]
    per = sum(b - a for a, b in stretches) / max(1, sum(syl))
    out, k = [], 0
    for a, b in stretches:
        t, budget, need, k0 = a, b - a, 0.0, k
        while k < len(words) and (need + syl[k] * per <= budget * 1.25 or k == k0):
            need += syl[k] * per
            k += 1
        scale = budget / max(need, 1e-6)
        for j in range(k0, k):
            out.append((words[j], START[n] + t))
            t += syl[j] * per * scale
    while len(out) < len(words):
        out.append((words[len(out)], END[n]))
    return out


def _after(n, text, find):
    """When line n reaches the first word of `find` (a snippet of its text)."""
    i = text.index(find)
    k = len(text[:i].split())
    return word_times(n, text)[k][1]


def shots_and_beats(texts):
    """(SHOTS, T, forest times, DUR) from the lines. texts: {n: the line's text}."""
    wa = lambda n, f: _after(n, texts[n], f)       # noqa: E731
    S, E = START, END
    cut = dict(a2=S[2] - 0.2, b2=wa(2, 'unique') - 0.1, s3=S[3] - 0.4, a4=S[4] - 0.1, b4=S[5] - 0.4,
               c4=S[6] - 0.2, s6=S[8] - 0.5, a7=S[10] - 0.2, b7=S[11] - 0.3, c7=S[12] - 0.3, d7=E[12] + 0.4,
               e7=E[13] + 0.4)
    dur = E[14] + 0.8
    shots = [('1', 0.0, cut['a2']), ('2a', cut['a2'], cut['b2']), ('2b', cut['b2'], cut['s3']),
             ('3', cut['s3'], cut['a4']), ('4a', cut['a4'], cut['b4']), ('4b', cut['b4'], cut['c4']),
             ('4c', cut['c4'], cut['s6']), ('6', cut['s6'], cut['a7']), ('7a', cut['a7'], cut['b7']),
             ('7b', cut['b7'], cut['c7']), ('7c', cut['c7'], cut['d7']), ('7d', cut['d7'], cut['e7']),
             ('7e', cut['e7'], dur)]
    gun = E[8] + 0.3
    beats = {'simple': wa(1, 'simple') + 0.1, 'light_on_them': wa(2, 'training') - 0.3, 'locks': E[2] + 0.4,
             'gunfire': gun, 'flame': gun + 0.8, 'stars': gun + 1.5, 'glance': S[13] - 1.0, 'gape': E[13] + 0.5}
    return shots, beats, FOREST, dur
