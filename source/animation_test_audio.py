#!/usr/bin/env python3
"""The animation test's soundtrack, cut from the trailer score (music/horror-trailer-score.m4a).

The picture runs PICTURE seconds and cuts to black on the first frame of the THUD (the cleaver hit in the
score, at horror_trailer_music.CHOP_AT); the sound carries on over the black for TAIL seconds. So the score is
taken from CHOP_AT - PICTURE to CHOP_AT + TAIL. Before the THUD that is only the Deck the Halls refrain; on top
of it go the sounds of her chopping the earlier slices in Shot 1 (a knife through ham into a wooden board -
lighter than the THUD: no bone).

    python3 animation_test_audio.py OUT.wav [START END]     (a part of it, in seconds of the film)
"""
import os
import subprocess
import sys
import wave

import imageio_ffmpeg
import numpy as np

SR = 44100
PICTURE = 6.0                     # Shot 1 (2 s) + Shot 2 (1.5 s) + Shot 3 (2.5 s)
TAIL = 1.5                        # darkness, and the last moments of the noise
CHOPS = (12 / 24, 28 / 24)        # Shot 1's chops land on these frames (see shots/s1_chop.py)
HERE = os.path.dirname(os.path.abspath(__file__))
SCORE = os.path.join(HERE, '..', 'music', 'horror-trailer-score.m4a')


def load(path):
    raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-loglevel', 'error', '-i', path, '-f', 's16le',
                          '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).reshape(-1, 2).astype(np.float64) / 32768


def band(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * ((f > lo) & (f < hi)), len(x))


def kitchen_chop(seed):
    """A cleaver through cooked ham into a wooden board: a soft wet slap, a woody knock, a faint ring."""
    rng = np.random.default_rng(seed)
    n = int(0.5 * SR)
    t = np.arange(n) / SR
    slap = band(rng.standard_normal(n) * np.exp(-t / 0.012), 300, 3500)
    slap /= np.abs(slap).max()
    knock = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.035) + 0.5 * np.sin(2 * np.pi * 410 * t) * np.exp(-t / 0.02)
    tick = band(rng.standard_normal(n) * np.exp(-t / 0.0015), 1500, 9000)
    tick /= np.abs(tick).max()
    ring = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / 0.09) for a, f in ((0.10, 2810), (0.06, 4170), (0.04, 5930)))
    x = 0.55 * slap + 0.9 * knock + 0.35 * tick + ring
    x[-int(0.1 * SR):] *= np.linspace(1, 0, int(0.1 * SR))
    return x / np.abs(x).max()


def soundtrack():
    import horror_trailer_music as H
    score = load(SCORE)
    a = int(round((H.CHOP_AT - PICTURE) * SR))
    st = score[a:a + int(round((PICTURE + TAIL) * SR))].copy()
    music = np.sqrt((st[:int(PICTURE * SR)] ** 2).mean())
    for k, at in enumerate(CHOPS):
        c = kitchen_chop(k) * music * 5.0             # clear over the piano, well under the THUD
        i = int(round(at * SR))
        st[i:i + len(c), 0] += c * (0.95 if k else 1.0)
        st[i:i + len(c), 1] += c * (1.0 if k else 0.95)
    return np.clip(st, -0.999, 0.999)


def write_wav(path, st):
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())


if __name__ == '__main__':
    st = soundtrack()
    if len(sys.argv) > 3:
        st = st[int(float(sys.argv[2]) * SR):int(float(sys.argv[3]) * SR)]
    write_wav(sys.argv[1], st)
    print(f'{sys.argv[1]}: {len(st) / SR:.2f} s')
