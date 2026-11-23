#!/usr/bin/env python3
"""audiokit: the voice-cleaning steps every film shares (hum, hiss, loudness, speech stretches, soft tails), copied
word for word from Mossad's audio file (mossad_audio.py, a finished film: freeze.py forbids new work loading it) so
the shared tools (takes.py) use a kit file. mossad_audio keeps its own copy for the finished films; the two give
identical sound (kittest takes_cleaned_and_registered compares Milburn's takes)."""
import numpy as np
from scipy.signal import butter, iirnotch, istft, resample_poly, sosfilt, sosfiltfilt, stft, tf2sos

SR = 48000
MAX_CUT_DB = 10.0


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

