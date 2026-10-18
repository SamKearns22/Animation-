#!/usr/bin/env python3
"""No beat skipped or doubled where pieces of a song are joined (Sam, 18 Oct: 'it sort of dips'; the old bridge in
Shocking Behaviour had skipped about 1.1 s, two beats, and he found it by ear, twice). A film that builds a song
from several recordings lists the pieces in SPLICE = ((clip, start_s, end_s), ...), in order. At each join this
looks at what the song does next in the OUTGOING recording (if it carries on past the cut), or what came just
before in the INCOMING one, and finds where the incoming piece really starts in the song: the two must line up to
within 40 ms. A join it cannot confirm either way (neither recording overlaps the other) is reported too, to be
checked by ear with a sound-check clip.

    python3 source/musiccheck.py FILM
"""
import importlib
import os
import subprocess
import sys

import numpy as np

SR = 16000
HOP = 160                       # 10 ms frames
WIN = 1.5                       # seconds compared
SEARCH = 1.6                    # how far either way to look for the real match


def _audio(clip, a, b):
    import imageio_ffmpeg
    a = max(0.0, a)
    raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-ss', f'{a:.3f}', '-t', f'{b - a:.3f}',
                          '-i', clip, '-vn', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float64) / 32768


def _spec(x):
    n = 1024
    if len(x) < n:
        return np.zeros((0, n // 2 + 1))
    frames = np.lib.stride_tricks.sliding_window_view(x, n)[::HOP] * np.hanning(n)
    s = np.log1p(np.abs(np.fft.rfft(frames, axis=1))[:, 4:400] * 20)
    s -= s.mean(axis=1, keepdims=True)
    return s


def _find(ref, r0, probe):
    """Where `probe` best matches inside `ref` (which starts r0 s into its recording): (seconds, score 0-1)."""
    R, P = _spec(ref), _spec(probe)
    if len(P) == 0 or len(R) < len(P):
        return None, 0.0
    best, at = -1.0, 0
    pn = P / (np.linalg.norm(P) + 1e-9)
    for i in range(len(R) - len(P) + 1):
        w = R[i:i + len(P)]
        c = float((w * pn).sum() / (np.linalg.norm(w) + 1e-9))
        if c > best:
            best, at = c, i
    return r0 + at * HOP / SR, best


def _length(clip):
    import imageio_ffmpeg
    err = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-i', clip], capture_output=True, text=True).stderr
    for part in err.split('Duration:')[1:2]:
        h, m, s = part.split(',')[0].strip().split(':')
        return int(h) * 3600 + int(m) * 60 + float(s)
    return 0.0


def faults(film):
    splice = getattr(film, 'SPLICE', None)
    if not splice or len(splice) < 2:
        return []
    out = []
    for n, ((ca, a0, a1), (cb, b0, b1)) in enumerate(zip(splice, splice[1:]), 1):
        if not (os.path.exists(ca) and os.path.exists(cb)):
            out.append(f'song join {n}: a recording is missing, so the join cannot be checked')
            continue
        lag, score = None, 0.0
        tail = _length(ca) - a1                          # the outgoing recording carries on: where does B start in it?
        w = min(WIN, tail - 0.05)
        if w >= 0.8:
            r0 = max(0.0, a1 - SEARCH)
            f, score = _find(_audio(ca, r0, a1 + min(tail, w + SEARCH)), r0, _audio(cb, b0, b0 + w))
            lag = None if f is None else f - a1          # + = the song jumps forward (skips) at the join
        w = min(WIN, b0 - 0.05)
        if (lag is None or score < 0.5) and w >= 0.8:  # or the incoming one began earlier: where does A end in it?
            r0 = max(0.0, b0 - w - SEARCH)
            f, score = _find(_audio(cb, r0, b0 + SEARCH), r0, _audio(ca, a1 - w, a1))
            lag = None if f is None else b0 - (f + w)
        if lag is None or score < 0.5:
            out.append(f'song join {n} ({a1:.2f} s into the first recording): cannot be confirmed (the recordings '
                       f'do not overlap there): send Sam a sound-check clip of it')
        elif abs(lag) > 0.04:
            what = 'skips' if lag > 0 else 'repeats'
            out.append(f'song join {n}: the song {what} {abs(lag):.2f} s there (about {abs(lag) / getattr(film, "BEAT", 0.5):.1f} '
                       f'beats): start the next piece {abs(lag):.3f} s {"earlier" if lag > 0 else "later"} in its recording')
    return out


if __name__ == '__main__':
    f = faults(importlib.import_module(sys.argv[1]))
    print('\n'.join(f) if f else 'song joins: continuous')
