#!/usr/bin/env python3
"""The 'Merry Chr' shot's soundtrack: the trailer score at its most distorted (the crescendo, just before the
gasp), and nothing else. (The director: no THUDs - seeing him do it is chilling enough; the music does the
work.)

    python3 merry_chr_audio.py OUT.wav
"""
import os
import sys

import numpy as np

import animation_test_audio as A
from animation_test_audio import SR

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots'))
import h1_merry_chr as SHOT  # noqa: E402

SCORE_FROM = 41.3        # the 'chased by a murderous clown' crescendo at its fastest and loudest (ends before the gasp)


def soundtrack():
    score = A.load(A.SCORE)
    a = int(round(SCORE_FROM * SR))
    st = score[a:a + int(round(SHOT.DURATION * SR))].copy()
    return st


if __name__ == '__main__':
    st = soundtrack()
    A.write_wav(sys.argv[1], st)
    print(f'{sys.argv[1]}: {len(st) / SR:.2f} s')
