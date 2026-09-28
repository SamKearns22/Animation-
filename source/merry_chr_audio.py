#!/usr/bin/env python3
"""The 'Merry Chr' shot's soundtrack: the trailer score at its most distorted (the crescendo, just before the
gasp), with the THUD of his forehead on the wall exactly on each impact frame - dull, close, and the loudest
thing.

    python3 merry_chr_audio.py OUT.wav
"""
import os
import sys

import numpy as np

import animation_test_audio as A
from animation_test_audio import SR, band

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots'))
import h1_merry_chr as SHOT  # noqa: E402

SCORE_FROM = 41.3        # the 'chased by a murderous clown' crescendo at its fastest and loudest (ends before the gasp)


def thud(seed):
    """A head struck against a plastered wall: a heavy, dull body thump, a muffled knock of the wall, a small
    wet smack of the blood on it. No crack, nothing bright."""
    rng = np.random.default_rng(seed)
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f = 95 * np.exp(-t / 0.05) + 55                               # the thump, its pitch falling as it dies
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.07)
    knock = band(rng.standard_normal(n) * np.exp(-t / 0.018), 180, 900)
    knock /= np.abs(knock).max()
    wet = band(rng.standard_normal(n) * np.exp(-t / 0.006), 600, 2500)
    wet /= np.abs(wet).max()
    x = 1.0 * body + 0.55 * knock + 0.12 * wet
    x[:int(0.002 * SR)] *= np.linspace(0, 1, int(0.002 * SR))
    x[-int(0.1 * SR):] *= np.linspace(1, 0, int(0.1 * SR))
    x = np.tanh(x / np.abs(x).max() * 1.8) / np.tanh(1.8)
    return x


def soundtrack():
    score = A.load(A.SCORE)
    a = int(round(SCORE_FROM * SR))
    st = score[a:a + int(round(SHOT.DURATION * SR))].copy()
    peak = np.abs(st).max()
    for k, f in enumerate(SHOT.IMPACTS):
        i = int(round(f / SHOT.FPS * SR))
        # the music ducks under each hit so the THUD is the loudest thing
        m = min(len(st) - i, int(0.35 * SR))
        st[i:i + m] *= 1 - 0.45 * np.exp(-np.arange(m) / SR / 0.12)[:, None]
        c = thud(k)[:len(st) - i] * peak * 1.6
        st[i:i + len(c), 0] += c * (1.0 if k % 2 else 0.96)
        st[i:i + len(c), 1] += c * (0.96 if k % 2 else 1.0)
    return np.tanh(st * 1.1) / np.tanh(1.1) * 0.97


if __name__ == '__main__':
    st = soundtrack()
    A.write_wav(sys.argv[1], st)
    print(f'{sys.argv[1]}: {len(st) / SR:.2f} s')
