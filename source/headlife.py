#!/usr/bin/env python3
"""headlife: head acting for anyone talking, driven by Sam's own recording (Job K proposal 1, Sam: Y, 10 Nov).

A long talking shot where only the mouth and eyes move reads as an AI "talking photo". Here the head moves pose to
pose: a new tilt at the start of each phrase (and every 1.5-2.3 s inside a long one), reached in three drawings with
a little overshoot and then HELD still (never a sine wave); a short nod on each stressed syllable. The deadpan face
stays; the moves are small (at most 4 degrees).

MAP
  envelope(path, t0, t1)  the voice's loudness per drawing (12 a second), from any sound or video file
  accents(env)            drawings where the voice lands on a stress
  HeadLife(env, t0)       the tilt and nod per drawing; .at_time(t) -> (roll degrees, nod 0..1)
  from_voice(path, ...)   the usual way in

Use: sp['head_life'] = headlife.from_voice(VOICE_WAV, t0=line_start) and views.person tilts and nods the head at
the film's time t (views.Rolled). A pose can also set j['head_roll'] (degrees) and j['nod'] (0..1) by hand.
"""
import subprocess

import numpy as np

FPS = 12


def envelope(path, t0=0.0, t1=None, fps=FPS):
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(t0)] + (['-t', str(t1 - t0)] if t1 is not None else []) + \
          ['-i', path, '-ac', '1', '-ar', '12000', '-f', 's16le', '-']
    x = np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.int16).astype(np.float32) / 32768
    n = 12000 // fps
    return np.array([np.sqrt(np.mean(x[i * n:(i + 1) * n] ** 2)) for i in range(len(x) // n)])


def accents(env, gap=5):
    """Drawing numbers where the voice lands on a stress: the loudest drawing within +-3, well above the speech's
    usual loudness, at least `gap` drawings apart."""
    voiced = env[env > 0.01]
    if not len(voiced):
        return []
    bar = 1.25 * float(np.median(voiced))
    out, last = [], -99
    for i in range(len(env)):
        lo, hi = max(0, i - 3), min(len(env), i + 4)
        if env[i] >= bar and env[i] == env[lo:hi].max() and i - last >= gap:
            out.append(i)
            last = i
    return out


def phrase_starts(env, quiet=3):
    """Drawings where speech starts again after at least `quiet` silent drawings (a quarter of a second)."""
    on = env > max(0.01, 0.25 * float(np.median(env[env > 0.01])) if (env > 0.01).any() else 0.01)
    out, run = [], quiet
    for i, v in enumerate(on):
        if v and run >= quiet:
            out.append(i)
        run = 0 if v else run + 1
    return out


class HeadLife:
    def __init__(self, env, t0=0.0, fps=FPS, seed=3):
        rng = np.random.default_rng(seed)
        n = len(env)
        self.t0, self.fps = t0, fps
        self.roll, self.nod = np.zeros(n), np.zeros(n)
        starts = phrase_starts(env) or [0]
        keys = []
        for k, s in enumerate(starts):              # a new tilt on each phrase, more inside a long one
            end = starts[k + 1] if k + 1 < len(starts) else n
            i = s
            while i < end - 8:
                keys.append(i)
                i += int(rng.integers(18, 28))
        prev, a, tgts = 0.0, 0.0, []
        for _ in keys:
            tgt = prev
            while abs(tgt - prev) < 2.0:
                tgt = float(rng.choice([-4.0, -2.5, -1.0, 1.5, 3.0, 4.0]))
            tgts.append(tgt)
            prev = tgt
        self.roll[:keys[0] if keys else n] = 0.0
        for k, (i0, tgt) in enumerate(zip(keys, tgts)):
            i1 = keys[k + 1] if k + 1 < len(keys) else n
            for j in range(i0, i1):
                w = (0.35, 0.85, 1.08)[j - i0] if j - i0 < 3 else 1.0   # three drawings in, a little past the mark
                self.roll[j] = a + (tgt - a) * w
            a = tgt
        for i0 in accents(env):
            for u, d in enumerate((0.6, 1.0, 0.55, 0.2)):
                if i0 + u < n:
                    self.nod[i0 + u] = max(self.nod[i0 + u], d)

    def at_time(self, t):
        """(roll in degrees, nod 0..1) at the film's time t; held at the ends."""
        i = int(round((t - self.t0) * self.fps))
        i = max(0, min(len(self.roll) - 1, i))
        return float(self.roll[i]), float(self.nod[i])


def from_voice(path, t0=0.0, t1=None, seed=3):
    return HeadLife(envelope(path, t0, t1), t0, seed=seed)
