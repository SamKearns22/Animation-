#!/usr/bin/env python3
"""Check a batch of Sam's recordings before anything is built (lesson of The Patriots 2, where two files carried the
same take under different names, and a file's name did not match what was said in it).

For each file: length, the stretches of speech and the pauses between them, an estimate of the syllables, and its
loudness. Then:
- DUPLICATES: any two files with the same sound (however they are named) are reported;
- with --script: each script line's expected syllables and speaking time, to compare with the measurements.
  Files are identified by their names (numbered by script line, see guides/preflight.md); there is no speech
  recognition here, so when a name and a measurement disagree, ask Sam before building anything.

Usage:
    python3 voices.py FILE.m4a [FILE.m4a ...] [--script script.txt]
    script.txt: one line of dialogue per line, optionally "WHO: words".
"""
import hashlib
import os
import re
import sys

import numpy as np
from scipy.signal import butter, find_peaks, sosfilt

from burnham_film import load, SR
import mossad_audio as MA


def syllables_in(text):
    """A rough count of spoken syllables (vowel groups per word, silent final e, numbers as words)."""
    n = 0
    for w in re.findall(r"[A-Za-z']+", text.lower()):
        w = w.replace("'", '')
        groups = re.findall(r'[aeiouy]+', w)
        k = len(groups)
        if w.endswith('e') and k > 1 and not w.endswith(('le', 'ee')):
            k -= 1
        n += max(1, k)
    return n


def measure(path):
    a = load(path)
    pcm = np.round(a * 32767).astype(np.int16).tobytes()
    st = MA.pauses(a, 0.12)
    x = sosfilt(butter(2, [300, 2500], 'band', fs=SR, output='sos'), a)
    hop = SR // 200
    e = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    e = np.convolve(e, np.hanning(9) / np.hanning(9).sum(), 'same')
    pk, _ = find_peaks(e, distance=18, prominence=e.max() * 0.08)
    env = e[::4] / (e.max() + 1e-9)
    return dict(path=path, dur=len(a) / SR, hash=hashlib.sha1(pcm).hexdigest()[:12], stretches=st,
                syll=int(round(len(pk) * 1.2)), lufs=MA.lufs(a), env=env)   # x1.2: the peak count misses about 1 in 6


def similar(a, b):
    n = min(len(a['env']), len(b['env']))
    if n < 20 or abs(len(a['env']) - len(b['env'])) > 0.05 * n:
        return 0.0
    return float(np.corrcoef(a['env'][:n], b['env'][:n])[0, 1])


def main():
    args = sys.argv[1:]
    script = []
    if '--script' in args:
        k = args.index('--script')
        script = [l.strip() for l in open(args[k + 1]) if l.strip()]
        args = args[:k] + args[k + 2:]
    ms = [measure(p) for p in args]
    for m in ms:
        sts = ', '.join(f'{a:.2f}-{b:.2f}' for a, b in m['stretches'])
        print(f"{os.path.basename(m['path'])}: {m['dur']:.1f} s, ~{m['syll']} syllables, {len(m['stretches'])} phrases "
              f"[{sts}], {m['lufs']:.1f} LUFS")
    print()
    dup = False
    for i, a in enumerate(ms):
        for b in ms[i + 1:]:
            if a['hash'] == b['hash'] or similar(a, b) > 0.97:
                dup = True
                print(f"DUPLICATE: {os.path.basename(a['path'])} and {os.path.basename(b['path'])} are the same take")
    if not dup:
        print('No duplicates.')
    if script:
        # Expected size of each script line, to compare with the measurements above. (Matching files to lines by
        # measurement alone was tried on The Patriots 2 and got 2 of 7 right: without speech recognition the file
        # name, numbered by script line, is what identifies a take; when a name and a measurement disagree, ask Sam.)
        print()
        print('Script lines (expected syllables, and speech at a natural 3-4 syllables a second):')
        for j, l in enumerate(script, 1):
            syl = syllables_in(l.split(':', 1)[-1])
            print(f'  {j}. ~{syl} syllables, {syl / 4.2:.1f}-{syl / 3.0:.1f} s: {l[:70]}')


if __name__ == '__main__':
    main()
