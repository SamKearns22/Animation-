#!/usr/bin/env python3
"""MAP  Milburn's voices and the film's clock (Sam's 16 recordings, 18 Nov): the takes cleaned and matched, then the
timeline that follows from how long each really is.

  VOICES ....... {line n: the cleaned, matched, levelled take (48 kHz)}; lines made of two takes are joined
  LINES_TIMED .. {n: dict(start, end, stretches, env, bleep)} start/end in film seconds, stretches = where the line
                 really speaks (seconds from its start), env = loudness for the mouth
  TIMES ........ every shot cut and beat, from the lines (nothing in the film's timing is typed in any more)
  word_times ... when each word of a line is reached (syllables spread over the real speech)

Map: takes 30 | tone and level 70 | timeline 120 | word times 190
"""
import math
import os

import numpy as np

import mossad_audio as MA
import mouths
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


def _trim(x, name):
    """The take with hum and hiss out, cut to the speech (50 ms before, 80 ms after); also where it started."""
    y = MA.denoise(MA.dehum(x))
    st = MA.pauses(y, 0.12)
    s0 = max(0.0, st[0][0] - 0.05)
    s1 = min(len(y) / SR, st[-1][1] + 0.08)
    return y[int(s0 * SR):int(s1 * SR)].copy(), s0


def _match_tone(lines):
    """Make the takes sound like one session: each line's tone nudged towards the average, at most 4 dB, no echo."""
    from scipy.signal import firwin2, welch, fftconvolve
    specs = []
    for x in lines:
        f, p = welch(x, SR, nperseg=2048)
        specs.append(p + 1e-14)
    target = np.exp(np.mean([np.log(p) for p in specs], axis=0))
    out = []
    for x, p in zip(lines, specs):
        g_db = 10 * np.log10(target / p)
        sm = np.array([np.mean(g_db[(f >= fc / 2 ** (1 / 6)) & (f <= fc * 2 ** (1 / 6))]) if fc > 0 else 0.0 for fc in f])
        sm = np.clip(np.nan_to_num(sm), -4.0, 4.0)
        sm[f < 80] = sm[f > 80][0] if np.any(f > 80) else 0.0
        sm[f > 4000] = np.minimum(sm[f > 4000], 0.0)
        h = firwin2(1025, f / (SR / 2), 10 ** (sm / 20))
        out.append(fftconvolve(x, h, mode='same'))
    return out


def _build():
    raw, fuck_at = {}, None
    for n in ORDER:
        parts = []
        for k, name in enumerate(TAKES[n]):
            x, s0 = _trim(load(os.path.join(HERE, 'audio', f'milburn-{name}.m4a')), name)
            if name == 'you-fucker':
                fuck_at = (FUCK[0] - s0, FUCK[1] - s0)
            if k:
                parts.append(np.zeros(int(GAP.get(n, 0.3) * SR)))
            parts.append(x)
        raw[n] = np.concatenate(parts)
    toned = _match_tone([raw[n] for n in ORDER])
    voices = {}
    for n, y in zip(ORDER, toned):
        y = MA.smooth_tail(y * 10 ** ((LUFS - MA.lufs(y)) / 20))
        k_in, k_out = int(0.01 * SR), int(0.06 * SR)
        y[:k_in] *= np.linspace(0, 1, k_in)
        y[-k_out:] *= 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, k_out))
        voices[n] = y
    return voices, fuck_at


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
    _st = MA.pauses(VOICES[_n], 0.18)
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
