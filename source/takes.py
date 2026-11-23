#!/usr/bin/env python3
"""takes: Sam's recordings cleaned the way the film plays them, one means shared by the film and its voice check
(named-lines change 3, Sam's Y 23 Nov). Milburn's chat 18 cleaned its takes inside its own code, and the shared voice
check kept reading the raw files: 60 false script and mouth lines, removed only by handing the cleaned takes over in
milburn.py, so the next film would start without the fix. Now the cleaning lives here: a film that plays cleaned
takes makes them with clean(), every take is registered under the audio name its LINES use, and voices.py reads that
registered take, the one Sam hears. A film that plays the shared loader (mossad_audio.line, the template's way) needs
nothing. The voice check says so when it would read a raw file the film does not play (voices.prepared).

MAP
  clean(prefix, takes, gap, lufs) ... {line n: take}: each file hum and hiss out, cut to the speech (50 ms before, 80 ms
                                      after), the files of one line joined with silence, the session's tone matched
                                      (at most 4 dB), levelled, faded; also each file's cut point (a swear's time in
                                      the file minus it gives its time in the take). Each take is REGISTERED
  PLAYED ............................ {audio name: take} for everything clean() made in this process; the audio name is
                                      prefix + the line's file names joined by '+' ('milburn-you-fucker+squid-games')
  STRETCHES ......................... {audio name: [(start, end)]}: where each registered take speaks (pauses over
                                      MIN_GAP split it), the same stretches the film times its mouths and words by
  played(audio) ..................... the registered take for a line's audio name, or None
  plays_shared_loader(paths) ........ True when the film's code plays mossad_audio.line (raw files, cleaned the shared
                                      way: the voice check reads the same)

    python3 source/takes.py test      the cleaner and the register on a made-up take
"""
import os
import re

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
PLAYED = {}
STRETCHES = {}         # {audio name: [(start, end)] where the take speaks}: the film's mouths, words and captions use
MIN_GAP = 0.18         # these, so the voice check does too (a pause shorter than this does not split the speech)


def _trim(x):
    import voiceclean as MA
    y = MA.denoise(MA.dehum(x))
    st = MA.pauses(y, 0.12)
    if not st:
        return y.copy(), 0.0
    s0 = max(0.0, st[0][0] - 0.05)
    s1 = min(len(y) / SR, st[-1][1] + 0.08)
    return y[int(s0 * SR):int(s1 * SR)].copy(), s0


def match_tone(lines):
    """The takes made to sound like one session: each nudged towards the average tone, at most 4 dB, no echo."""
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


def audio_name(prefix, files):
    return prefix + '+'.join(files)


def clean(prefix, takes, gap=None, lufs=-20.0, load=None, min_gap=MIN_GAP):
    """takes: {line n: [file names without the prefix]} (source/audio/PREFIX+NAME.m4a). Returns ({n: take},
    {(n, file name): seconds cut from the file's start})."""
    import voiceclean as MA
    if load is None:
        load = MA.load
    gap = gap or {}
    order = sorted(takes)
    raw, cut = {}, {}
    for n in order:
        parts = []
        for k, name in enumerate(takes[n]):
            x, s0 = _trim(load(os.path.join(HERE, 'audio', f'{prefix}{name}.m4a')))
            cut[(n, name)] = s0
            if k:
                parts.append(np.zeros(int(gap.get(n, 0.3) * SR)))
            parts.append(x)
        raw[n] = np.concatenate(parts)
    toned = match_tone([raw[n] for n in order]) if len(order) > 1 else [raw[n] for n in order]
    voices = {}
    for n, y in zip(order, toned):
        y = MA.smooth_tail(y * 10 ** ((lufs - MA.lufs(y)) / 20))
        k_in, k_out = int(0.01 * SR), int(0.06 * SR)
        y[:k_in] *= np.linspace(0, 1, k_in)
        y[-k_out:] *= 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, k_out))
        voices[n] = y
        PLAYED[audio_name(prefix, takes[n])] = y
        STRETCHES[audio_name(prefix, takes[n])] = MA.pauses(y, min_gap)
    return voices, cut


def played(audio):
    return PLAYED.get(audio) if audio else None


def stretches(audio):
    return STRETCHES.get(audio) if audio else None


def plays_shared_loader(paths):
    """Does the film's code play its recordings through mossad_audio.line (the shared loader the voice check reads)?"""
    for p in paths:
        try:
            src = open(p).read()
        except OSError:
            continue
        names = set(re.findall(r'import\s+mossad_audio\s+as\s+(\w+)', src)) | {'mossad_audio'}
        if any(re.search(rf'\b{re.escape(a)}\.line\(', src) for a in names) or \
                re.search(r'from\s+mossad_audio\s+import\s+[^\n]*\bline\b', src):
            return True
    return False


def _test():
    t = np.arange(int(1.2 * SR)) / SR
    tone = np.where((t > 0.3) & (t < 0.9), 0.3 * np.sin(2 * np.pi * 180 * t), 0.0) + 0.001 * np.random.randn(len(t))
    v, cut = clean('test-', {1: ['a'], 2: ['a', 'a']}, gap={2: 0.25}, load=lambda path: tone.copy())
    ok = played('test-a') is v[1] and played('test-a+a') is v[2] and abs(cut[(1, 'a')] - 0.25) < 0.08
    ok = ok and len(v[2]) > len(v[1]) + 0.2 * SR
    print('PASS' if ok else 'FAIL', 'takes: cleaned, cut at', round(cut[(1, 'a')], 2), 's, registered', sorted(PLAYED))
    return ok


if __name__ == '__main__':
    import sys
    sys.exit(0 if _test() else 1)
