#!/usr/bin/env python3
"""Mossad: cleaning and levelling Sam's recordings (source/audio/mossad-*.m4a).

Each recording is cleaned gently, then every line is set to the same loudness:
- hum: a gentle high-pass below the voice (75 Hz), plus a notch on any mains hum found (50 Hz and its harmonics);
- hiss and room noise: spectral noise reduction learnt from the file's own quiet parts, limited to about 10 dB
  and smoothed over time and pitch, so the voice never sounds underwater or watery;
- loudness: measured the broadcast way (ITU-R BS.1770, K-weighted, gated), every line set to the same level.
Nothing else: no echo, no pitch change, no compression. The voices play as recorded.

Usage:
    python3 mossad_audio.py report        loudness, noise and pauses of each file, before and after
    python3 mossad_audio.py wavs OUT_DIR  cleaned, levelled copies to listen to
"""
import math
import os
import sys
import wave

import numpy as np
from scipy.signal import butter, iirnotch, istft, resample_poly, sosfilt, sosfiltfilt, stft, tf2sos

from burnham_film import load, SR

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ['mossad-customer-1', 'mossad-cashier-1', 'mossad-customer-2', 'mossad-cashier-2', 'mossad-cashier-3',
         'mossad-cashier-4', 'mossad-customer2-1']
LINE_LUFS = -20.0   # every line the same; the whole film is mastered to -14 LUFS afterwards
MAX_CUT_DB = 10.0   # the most the noise reduction may turn anything down


def lufs(x):
    """Integrated loudness (ITU-R BS.1770-4, mono), in LUFS."""
    # K-weighting: a high shelf (+4 dB above about 1.5 kHz) and a high-pass at about 38 Hz (the standard's
    # coefficients, re-derived for 48 kHz).
    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]
    y = sosfilt(np.vstack([tf2sos(b1, a1), tf2sos(b2, a2)]), x)
    blk, hop = int(0.4 * SR), int(0.1 * SR)
    z = np.array([np.mean(y[i:i + blk] ** 2) for i in range(0, max(1, len(y) - blk + 1), hop)])
    L = -0.691 + 10 * np.log10(z + 1e-12)
    z = z[L > -70]
    rel = -0.691 + 10 * np.log10(np.mean(z) + 1e-12) - 10
    z = z[-0.691 + 10 * np.log10(z + 1e-12) > rel]
    return -0.691 + 10 * np.log10(np.mean(z) + 1e-12)


def true_peak_db(x):
    """The highest peak, measured between the samples too (4x oversampled), in dBTP."""
    return 20 * np.log10(np.abs(resample_poly(x, 4, 1)).max() + 1e-12)


def dehum(x):
    x = sosfiltfilt(butter(2, 75, 'high', fs=SR, output='sos'), x)
    spec = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    f = np.fft.rfftfreq(len(x), 1 / SR)
    for h in (50, 100, 150):  # notch only a hum that is really there (a narrow peak well above its neighbours)
        band = (f > h - 15) & (f < h + 15)
        pk = (f > h - 1.5) & (f < h + 1.5)
        if spec[pk].max() > 4 * np.median(spec[band]):
            b, a = iirnotch(h, 30, SR)
            x = sosfiltfilt(tf2sos(b, a), x)
    return x


def denoise(x):
    """Gentle spectral noise reduction, learnt from the quietest tenth of the recording."""
    nper = 2048
    f, t, X = stft(x, SR, nperseg=nper, noverlap=nper * 3 // 4)
    mag = np.abs(X)
    energy = mag.sum(axis=0)
    quiet = energy <= np.percentile(energy, 10)
    noise = np.median(mag[:, quiet], axis=1, keepdims=True)
    floor = 10 ** (-MAX_CUT_DB / 20)
    g = np.clip(1 - (1.5 * noise / (mag + 1e-12)) ** 2, 0, 1) ** 0.5
    g = np.maximum(g, floor)
    # smooth the gains across time and pitch so nothing warbles ("musical noise")
    from scipy.ndimage import uniform_filter
    g = uniform_filter(g, size=(5, 5), mode='nearest')
    _, y = istft(X * g, SR, nperseg=nper, noverlap=nper * 3 // 4)
    return y[:len(x)]


def edges(x):
    """A short fade at the very start and end of a recording so it never clicks."""
    k = int(0.01 * SR)
    x = x.copy()
    x[:k] *= np.linspace(0, 1, k)
    x[-k:] *= np.linspace(1, 0, k)
    return x

# ------------------------------------------------------------------------------------------------- mastering (Cry Minister, 8 Oct)
# Phone recordings are quiet with sharp peaks (about 20 dB above their average). Turning them up to -14 LUFS and then
# limiting every loud word by up to 8 dB within milliseconds sounded like crackle on a phone (Cry Minister, note 32).
# So: even the loud stretches out gently, master at -16 LUFS, and never limit more than 3 dB.
MASTER_LUFS = -16.0
MAX_LIMIT_DB = 3.0


def gentle_level(x, ratio=3.0, above=4.0):
    """Even out loud and soft words the way a studio does: the volume eases down only on stretches more than `above` dB
    louder than the line's average (by half the excess), easing in over 30 ms and back over 300 ms, so it follows
    syllables, never the voice's own waves. The film's sound used to be turned up 7 dB and then squashed by up to 8 dB
    within milliseconds on every loud word: on a phone that is crackle (Sam's note 32, twice)."""
    blk = int(0.001 * SR)
    nb = -(-len(x) // blk)
    p = (np.pad(x, (0, nb * blk - len(x))) ** 2).reshape(nb, blk).mean(1)
    from scipy.ndimage import uniform_filter1d
    lv = 10 * np.log10(uniform_filter1d(p, 30) + 1e-12)              # level over 30 ms, in dB
    ref = 10 * np.log10(np.mean(p[lv > lv.max() - 40]) + 1e-12)       # the speech's average level
    want = -np.maximum(0.0, lv - (ref + above)) * (1 - 1 / ratio)     # gain wanted, dB
    g, att, rel = np.zeros(nb), 1 - math.exp(-1 / 30), 1 - math.exp(-1 / 300)
    for i in range(1, nb):
        k = att if want[i] < g[i - 1] else rel
        g[i] = g[i - 1] + (want[i] - g[i - 1]) * k
    gs = np.interp(np.arange(len(x)), np.arange(nb) * blk + blk / 2, 10 ** (g / 20))
    return x * gs




def smooth_limit(x, ceiling_db):
    """A last guard on the few bursts left over (at most 3 dB of them): the volume eases down over 10 ms just ahead of
    a peak and recovers over about 150 ms."""
    from scipy.ndimage import minimum_filter1d, uniform_filter1d
    c, blk = 10 ** (ceiling_db / 20), int(0.001 * SR)
    nb = -(-len(x) // blk)
    a = np.abs(np.pad(x, (0, nb * blk - len(x)))).reshape(nb, blk).max(1)
    need = minimum_filter1d(np.minimum(1.0, c / np.maximum(a, 1e-9)), 21)    # 10 ms either side
    g, rel = need.copy(), 1 - math.exp(-1 / 150)
    for i in range(1, nb):
        g[i] = min(need[i], g[i - 1] + (1 - g[i - 1]) * rel)
    g = np.minimum(need, uniform_filter1d(g, 5))
    g = np.minimum(g, uniform_filter1d(g, 5))
    gs = np.interp(np.arange(len(x)), np.arange(nb) * blk + blk / 2, g)
    return np.clip(x * gs, -c, c)




def master(mix, end=None, lufs_target=MASTER_LUFS):
    """The whole film's sound: levelled gently, set to -16 LUFS (or quieter if the loudest burst would need more than
    3 dB of limiting), then the few bursts left eased under -1 dB. Returns (mastered, the gain applied before limiting)."""
    end = len(mix) if end is None else end
    x = gentle_level(mix)
    if np.abs(x).max() < 1e-9:
        return x, 1.0
    g = min(10 ** ((lufs_target - lufs(x[:end])) / 20), 10 ** ((MAX_LIMIT_DB - 1.0) / 20) / np.abs(x).max())
    return smooth_limit(x * g, -1.0), g


def limit_check(mix, end=None):
    """Faults for the plan checks: limiting deeper than 3 dB anywhere (it sounds like crackle on a phone)."""
    x = gentle_level(mix)
    out, g = master(mix, end)
    d = limit_db(x * g, out)
    return [f'the sound is limited by {d:.1f} dB somewhere (most allowed {MAX_LIMIT_DB:.0f}): master quieter'] \
        if d > MAX_LIMIT_DB + 0.3 else []


def limit_db(before, after):
    """How hard the limiting pressed anywhere (dB): the most that `after` sits below `before` over 10 ms."""
    w = int(0.01 * SR)
    n = min(len(before), len(after)) // w
    a = np.sqrt((before[:n * w].reshape(n, w) ** 2).mean(1)) + 1e-9
    b = np.sqrt((after[:n * w].reshape(n, w) ** 2).mean(1)) + 1e-9
    loud = a > a.max() * 0.05
    return float(np.max(20 * np.log10(a[loud] / b[loud]))) if loud.any() else 0.0


def smooth_tail(y):
    """After the last voiced sound of a piece, the hiss of its final "s" or "k" only ever dies away: in several takes
    (Cry Minister lines 1, 12, 13, 15) the phone's own voice clean-up chopped that hiss into bursts about 12 a second, which the
    film's extra volume turned into crackle (Sam's note 38; they are in the recordings too). After the brightest moment
    of the tail (the real consonant) the bursts and thumps are pressed down to a falling envelope; nothing is ever
    turned up."""
    w = int(0.01 * SR)
    n = len(y) // w
    if n < 4:
        return y
    fr = y[:n * w].reshape(n, w)
    lv = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)
    zc = np.abs(np.diff(np.sign(fr), axis=1)).mean(1) / 2 * SR
    v = (zc < 3500) & (lv > lv.max() - 25)
    run = np.convolve(v.astype(int), np.ones(5, int), 'valid') == 5          # real voice: 50 ms of it in a row
    voiced = np.where(run)[0]                                                 # (a thump is shorter)
    if not len(voiced):
        return y
    t0 = (voiced[-1] + 5) * w                                          # the unvoiced tail starts here
    if len(y) - t0 < 2 * w:
        return y
    from scipy.ndimage import uniform_filter1d
    tail = y[t0:]
    env = np.sqrt(uniform_filter1d(tail ** 2, int(0.005 * SR)) + 1e-12)     # 5 ms: shows the bursts
    slow = np.sqrt(uniform_filter1d(tail ** 2, int(0.02 * SR)) + 1e-12)     # 20 ms
    from scipy.signal import butter, sosfilt
    hiss = sosfilt(butter(4, 3000, 'high', fs=SR, output='sos'), tail)
    hs = uniform_filter1d(hiss ** 2, int(0.02 * SR))
    first = hs[:int(0.2 * SR)]
    pk = int(np.argmax(first >= 0.7 * first.max()))                        # the real "s", "z" or "k" (its first strong
                                                                             # moment) is kept whole,
    fall = np.concatenate([env[:pk], np.minimum.accumulate(slow[pk:])])     # then the hiss never rises again
    g = np.minimum(1.0, fall / env)
    g = uniform_filter1d(g, int(0.003 * SR))                                 # no clicks from the gain itself
    out = y.copy()
    out[t0:] = tail * g
    return out


CACHE = {}


def line(name):
    """A recording, cleaned and set to the shared line loudness."""
    if name not in CACHE:
        x = load(os.path.join(HERE, 'audio', name + '.m4a'))
        x = edges(smooth_tail(denoise(dehum(x))))
        CACHE[name] = x * 10 ** ((LINE_LUFS - lufs(x)) / 20)
    return CACHE[name]


def noise_floor_db(x):
    hop = SR // 50
    rms = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    return 20 * np.log10(np.percentile(rms, 10) + 1e-12)


def pauses(x, min_gap=0.12):
    """Where the speech starts and stops: (start, end) of each stretch of talk, in seconds."""
    hop = SR // 100
    rms = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    on = rms > max(np.percentile(rms, 95) * 0.06, 1e-4)
    runs, start = [], None
    for i, v in enumerate(on):
        if v and start is None:
            start = i
        if not v and start is not None:
            runs.append([start, i])
            start = None
    if start is not None:
        runs.append([start, len(on)])
    merged = []
    for a, b in runs:
        if merged and (a - merged[-1][1]) / 100 < min_gap:
            merged[-1][1] = b
        else:
            merged.append([a, b])
    return [(a / 100, b / 100) for a, b in merged if b - a >= 4]


def write_wav(path, x):
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def main():
    if sys.argv[1] == 'report':
        for name in FILES:
            raw = load(os.path.join(HERE, 'audio', name + '.m4a'))
            x = line(name)
            print(f'{name}: {len(raw) / SR:.2f} s | before {lufs(raw):.1f} LUFS, noise {noise_floor_db(raw):.0f} dB | '
                  f'after {lufs(x):.1f} LUFS, noise {noise_floor_db(x):.0f} dB, peak {true_peak_db(x):.1f} dBTP')
            print('   talk:', ' '.join(f'{a:.2f}-{b:.2f}' for a, b in pauses(x)))
    elif sys.argv[1] == 'wavs':
        os.makedirs(sys.argv[2], exist_ok=True)
        for name in FILES:
            write_wav(os.path.join(sys.argv[2], name + '.wav'), line(name))


if __name__ == '__main__':
    main()
