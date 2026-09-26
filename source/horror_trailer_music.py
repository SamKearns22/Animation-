#!/usr/bin/env python3
"""Horror trailer score, exactly 55 seconds, built from our Deck the Halls piano.

    0.0 - 10  gentle Deck (the opening phrase, looping)
    10  - 22  increasingly off-putting Deck: the piano sags flat, notes go wrong, a low drone creeps in
    22  - 34  faster, more maddened Deck: stutters, clusters, the tape wobbles, a second piano a tritone down
    34  - 42.5 horrifying crescendo: faster and faster, a third shrieking piano, a rising screech
    42.5 - 43 a horror gasp cuts it all off
    43  - 48  five seconds of silence
    48  - 52.6 'Hark! the herald angels sing, glory to the new-born King!': choir, diva, organ, timpani,
               bells, cymbals, far too fast
    52.6 - 53 the music is stripped away, leaving the diva alone, sliding down into nothing
    53  - 55  two seconds of silence for the post-trailer titles

Usage:
    python3 horror_trailer_music.py OUT.m4a
"""
import os
import subprocess
import sys
import tempfile

import imageio_ffmpeg
import numpy as np

import deck_the_halls as D
from deck_the_halls import SR, A_HARM, A_TUNE, CHORDS, midi, hz, piano_note

rng = np.random.default_rng(13)
TOTAL = 55.0
DECK_END = 42.5
GASP_END = 43.0
HARK_START = 48.0
DENUDE = 52.6
HARK_END = 53.0
LEAD = 0.05


# ---------------------------------------------------------------------------
# Deck the Halls, looping and accelerating
# ---------------------------------------------------------------------------
def bpm_at(t):
    return np.interp(t, [0, 10, 22, 34, 38, 42.5], [100, 104, 128, 185, 240, 330])


_tg = np.arange(0, DECK_END + 3, 0.001)
_beats = np.concatenate([[0], np.cumsum(bpm_at(_tg[:-1]) / 60 * 0.001)])


def b2t(b):
    return float(np.interp(b, _beats, _tg)) + LEAD


def mad(t):
    """0 while the carol is innocent, rising to 1 at the gasp."""
    return np.clip((t - 9) / (DECK_END - 9), 0, 1)


def add_note(L, R, m, t, dur, vel):
    if t < 0 or dur <= 0:
        return
    s = piano_note(m, min(vel, 1.05), dur)
    i = int(t * SR)
    s = s[:max(0, len(L) - i)]
    pan = np.clip((m - 60) / 40, -0.45, 0.45)
    L[i:i + len(s)] += s * (0.5 - pan / 2) * 1.4
    R[i:i + len(s)] += s * (0.5 + pan / 2) * 1.4


def deck():
    n = int((DECK_END + 1) * SR)
    L, R = np.zeros(n), np.zeros(n)
    events = []
    b = 0.0
    while b2t(b) < DECK_END:
        pos = b
        for name, nb in A_TUNE:
            events.append((pos, midi(name), nb, 'tune'))
            pos += nb
        for j, ch in enumerate(A_HARM):
            root, tones = CHORDS[ch]
            events.append((b + 2 * j, midi(root), 1.9, 'bass'))
            for tone in tones:
                events.append((b + 2 * j + 1, midi(tone), 0.9, 'chord'))
        b += 16
    for bb, m0, nb, kind in events:
        t = b2t(bb)
        if t >= DECK_END:
            continue
        k = float(mad(t))
        dur = b2t(bb + nb * 0.94) - t
        m = m0 + (-40 * k ** 1.2 + rng.normal(0, 3 + 28 * k)) / 100  # the whole piano sags out of tune
        base = {'tune': 0.78, 'bass': 0.5, 'chord': 0.3}[kind]
        vel = base * (1 + 0.45 * k) + rng.normal(0, 0.03)
        t += rng.normal(0, 0.004 + 0.018 * k)
        if kind == 'tune':
            if rng.random() < 0.38 * k ** 1.5:
                m += rng.choice([-1, 1])  # a wrong note
            if rng.random() < 0.2 * k ** 2:
                m += rng.choice([-12, 12])  # in the wrong octave
            add_note(L, R, m, t, dur, vel)
            if k > 0.5 and rng.random() < (k - 0.5) * 1.2:  # stutters
                for r in (1, 2):
                    add_note(L, R, m + rng.normal(0, 0.3), t + dur * r / 3, dur / 3, vel * 0.9)
            if t >= 26:  # a second piano, a tritone down, a bar behind
                t2 = b2t(bb + 2)
                if t2 < DECK_END:
                    add_note(L, R, m - 6, t2, dur, vel * 0.75 * min(1, (t - 26) / 8))
            if t >= 34:  # a third, shrieking an octave and a semitone up
                t3 = b2t(bb + 1)
                if t3 < DECK_END:
                    add_note(L, R, m + 13, t3, dur, vel * 0.7 * min(1, (t - 34) / 4))
        else:
            add_note(L, R, m, t, dur, vel)
            if rng.random() < k * 0.9:  # clusters
                add_note(L, R, m + 1, t, dur, vel * 0.8)
            if kind == 'bass' and k > 0.45:
                add_note(L, R, m + 6, t, dur, vel * 0.7)

    # the tape starts to wobble: seasick at first, then lurching
    tt = np.arange(n) / SR
    k = mad(tt)
    depth = 0.004 * k ** 1.4 * SR
    ph = np.cumsum(2 * np.pi * (0.5 + 5 * k ** 2) / SR)
    idx = np.arange(n) - depth * (1 + np.sin(ph))
    L = np.interp(idx, np.arange(n), L)
    R = np.interp(idx, np.arange(n), R)
    L, R = D.reverb(L), D.reverb(R)

    # a low beating drone creeping in, then a rising screech for the crescendo
    amp = np.clip((tt - 11) / 23, 0, 1) ** 1.5 * 0.22 + np.clip((tt - 34) / 8.5, 0, 1) ** 2 * 0.25
    dr = np.zeros(n)
    for f, a in ((87.31, 1), (92.5, 0.8), (174.6, 0.5), (185.0, 0.4), (123.5, 0.35)):
        dr += a * np.sin(2 * np.pi * f * tt * (1 + 0.004 * np.sin(0.4 * tt)))
    dr *= amp
    u = np.clip((tt - 34) / (DECK_END - 34), 0, 1)
    sc = np.zeros(n)
    for det in (-0.02, -0.007, 0.0, 0.009, 0.021):
        f = 200 * 2 ** (3.3 * u + det)
        p = np.cumsum(2 * np.pi * f / SR) + rng.uniform(0, 6.3)
        for h in range(1, 9):
            sc += np.sin(h * p) / h
    sc *= (u ** 2) * 0.09 * (1 + 0.3 * np.sin(2 * np.pi * 11 * tt))

    gain = np.interp(tt, [0, 10, 22, 34, 42.5], [1.0, 1.0, 1.05, 1.12, 1.5])
    L = L * gain + dr + sc
    R = R * gain + dr * 0.95 + sc * 1.05
    cut = int(DECK_END * SR)
    f = int(0.008 * SR)
    for ch in (L, R):
        ch[cut - f:cut] *= np.linspace(1, 0, f)
        ch[cut:] = 0
    return L[:cut], R[:cut]


# ---------------------------------------------------------------------------
# The gasp
# ---------------------------------------------------------------------------
def shaped(x, fn):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * fn(f), len(x))


def formant_gain(f, forms):
    g = np.full_like(f, 0.015, dtype=float)
    for F, bw, a in forms:
        g += a / (1 + ((f - F) / bw) ** 2)
    return g


def gasp():
    dur = GASP_END - DECK_END
    n = int(dur * SR)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    lo = shaped(noise, lambda f: formant_gain(f, [(600, 150, 1), (1050, 180, 0.7), (2500, 400, 0.5), (5000, 1500, 0.3)]))
    hi = shaped(noise, lambda f: formant_gain(f, [(900, 150, 1), (1600, 200, 0.8), (3000, 400, 0.6), (6000, 1500, 0.4)]))
    x = t / dur
    sig = lo * (1 - x) + hi * x
    env = np.minimum(1, t / 0.018) * (0.75 + 0.25 * x ** 0.7)
    tail = int(0.04 * SR)
    env[-tail:] *= np.linspace(1, 0, tail) ** 2
    sig = sig * env
    sig /= np.abs(sig).max()
    return sig * 0.9, sig * 0.9


# ---------------------------------------------------------------------------
# Hark! the herald angels sing
# ---------------------------------------------------------------------------
HB = 60 / 208
BEATS = [1, 1, 1.5, 0.5, 1, 1, 1, 1, 1, 1, 1.5, 0.5, 1, 1, None]
MEL = ['C5', 'F5', 'F5', 'E5', 'F5', 'A5', 'A5', 'G5', 'C6', 'C6', 'C6', 'Bb5', 'A5', 'G5', 'A5']
ALTO = ['A4', 'A4', 'A4', 'G4', 'A4', 'C5', 'C5', 'C5', 'A5', 'A5', 'A5', 'G5', 'F5', 'E5', 'F5']
TENOR = ['F4', 'C4', 'C4', 'C4', 'C4', 'F4', 'F4', 'E4', 'C5', 'C5', 'C5', 'C5', 'C5', 'C5', 'C5']
BASS = ['F3', 'F3', 'F3', 'C3', 'F3', 'F3', 'F3', 'C3', 'F3', 'F3', 'F3', 'C3', 'F3', 'C3', 'F3']
HARM = ['F', 'F', 'F', 'C', 'F', 'F', 'F', 'C', 'F', 'F', 'F', 'C7', 'F', 'C', 'F']
DIVA = MEL[:-1] + ['F6']
FEMALE = [(800, 90, 1.0), (1150, 100, 0.5), (2900, 150, 0.3), (3900, 180, 0.2), (4950, 200, 0.1)]
MALE = [(650, 90, 1.0), (1080, 100, 0.45), (2650, 150, 0.35), (2900, 150, 0.35), (3250, 180, 0.15)]
HN = int((HARK_END - HARK_START + 0.5) * SR)
_starts = [0.02]
for _b in BEATS[:-1]:
    _starts.append(_starts[-1] + _b * HB)
STARTS = np.array(_starts)  # seconds after HARK_START
CUT = DENUDE - HARK_START


def voice(names, forms, vib_cents, detune, dive=False):
    """One operatic singer on 'ah', following the notes, with a wide wobbling vibrato."""
    t = np.arange(HN) / SR
    idx = np.clip(np.searchsorted(STARTS, t, side='right') - 1, 0, len(names) - 1)
    lm = np.array([midi(nm) for nm in names], float)[idx]
    w = int(0.03 * SR)
    lm = np.convolve(np.pad(lm, (w, w), mode='edge'), np.ones(w) / w, 'same')[w:-w]  # glide between notes
    rate = 6.3 + rng.normal(0, 0.3)
    vib = vib_cents / 100 * np.sin(2 * np.pi * rate * t + rng.uniform(0, 6.3)) * np.minimum(1, t / 0.15)
    lm = lm + vib + detune / 100
    if dive:  # after the music is stripped away, the voice slides down into nothing
        u = np.clip((t - CUT) / (HARK_END - DENUDE), 0, 1)
        lm = lm - 40 * u ** 1.6
    f = 440 * 2 ** ((lm - 69) / 12)
    ph = np.cumsum(2 * np.pi * f / SR) + rng.uniform(0, 6.3)
    out = np.zeros(HN)
    K = min(80, int(7000 / f.min()))
    for k in range(1, K + 1):
        fk = k * f
        a = formant_gain(fk, forms) / k * (fk < 9000)
        out += a * np.sin(k * ph)
    # a small dip between syllables
    env = np.ones(HN)
    for s in STARTS[1:]:
        i = int(s * SR)
        d = int(0.035 * SR)
        env[i - d:i + d] *= 1 - 0.55 * np.hanning(2 * d)
    env *= np.minimum(1, t / 0.03)
    out *= env
    return out / (np.sqrt((out ** 2).mean()) + 1e-9)


def bell(m, dur=2.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f0 = hz(m)
    out = np.zeros(n)
    for r, a, tau in ((0.5, 0.5, 2.0), (1, 1, 1.4), (1.19, 0.6, 1.0), (1.5, 0.4, 0.8), (2, 0.7, 0.9),
                      (2.51, 0.3, 0.5), (2.66, 0.3, 0.45), (3.01, 0.25, 0.35), (4.1, 0.15, 0.25)):
        out += a * np.exp(-t / tau) * np.sin(2 * np.pi * f0 * r * t + rng.uniform(0, 6.3))
    return out * np.minimum(1, t / 0.002)


def timp(m, vel):
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    f = hz(m) * (1 + 0.1 * np.exp(-t / 0.03))
    ph = np.cumsum(2 * np.pi * f / SR)
    out = np.exp(-t / 0.7) * np.sin(ph) + 0.5 * np.exp(-t / 0.4) * np.sin(1.5 * ph) \
        + 0.3 * np.exp(-t / 0.3) * np.sin(1.99 * ph)
    k = int(0.02 * SR)
    out[:k] += rng.standard_normal(k) * np.exp(-np.arange(k) / (0.004 * SR)) * 0.6
    return out * vel


def crash(dur=3.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = shaped(rng.standard_normal(n), lambda f: np.clip((f - 2500) / 4000, 0, 1) ** 0.7)
    return x * np.exp(-t / 1.1) / np.abs(x).max()


def hall(x, secs=3.0, tau=0.75):
    L = int(secs * SR)
    tt = np.arange(L) / SR
    ir = rng.standard_normal(L) * np.exp(-tt / tau) * (tt > 0.02)
    ir = np.convolve(ir, np.ones(8) / 8, 'same')
    ir /= np.sqrt((ir ** 2).sum())
    n = len(x) + L
    wet = np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[:len(x)]
    return x * 0.8 + wet * 0.45


def place(buf, s, t, gain=1.0):
    i = int(t * SR)
    s = s[:max(0, len(buf) - i)]
    buf[i:i + len(s)] += s * gain


def hark():
    L, R = np.zeros(HN), np.zeros(HN)
    # choir: four sopranos, three altos, three tenors, three basses, slightly out of tune with each other
    parts = [(MEL, FEMALE, 4, 1.0, 0.35), (ALTO, FEMALE, 3, 0.7, -0.2), (TENOR, MALE, 3, 0.7, 0.15),
             (BASS, MALE, 3, 0.9, -0.35)]
    for names, forms, count, g, pan in parts:
        for c in range(count):
            v = voice(names, forms, 70, rng.normal(0, 12)) * g / count ** 0.5
            p = pan + rng.normal(0, 0.15)
            L += v * (0.5 - p / 2)
            R += v * (0.5 + p / 2)
    L *= 0.09
    R *= 0.09
    # organ: the chords with a deep pedal
    t = np.arange(HN) / SR
    idx = np.clip(np.searchsorted(STARTS, t, side='right') - 1, 0, len(HARM) - 1)
    org = np.zeros(HN)
    for ch in set(HARM):
        root, tones = CHORDS[ch]
        mask = np.array([h == ch for h in HARM])[idx].astype(float)
        mask = np.convolve(mask, np.ones(400) / 400, 'same')
        s = np.zeros(HN)
        for nm in [root] + tones:
            f0 = hz(midi(nm))
            for r, a in ((0.5, 0.6), (1, 1), (2, 0.5), (4, 0.2)):
                s += a * np.sin(2 * np.pi * f0 * r * t)
        org += s * mask
    org *= 0.035 * np.minimum(1, t / 0.05)
    L += org
    R += org
    # piano hammering the tune in octaves, with chords on every beat
    for i, (nm, st) in enumerate(zip(MEL, STARTS)):
        d = (BEATS[i] or 2) * HB
        for sh in (0, -12):
            s = piano_note(midi(nm) + sh, 1.0, d) * 0.35
            place(L, s, st, 0.9)
            place(R, s, st, 1.1)
    nbeats = int(sum(BEATS[:-1])) + 2
    for b in range(nbeats):
        st = 0.02 + b * HB
        if st > CUT:
            break
        ch = HARM[min(np.searchsorted(STARTS, st + 0.001, side='right') - 1, len(HARM) - 1)]
        root, tones = CHORDS[ch]
        for nm in tones:
            s = piano_note(midi(nm), 0.8, HB * 0.8) * 0.2
            place(L, s, st, 1.0)
            place(R, s, st, 1.0)
        # bells pealing on every beat
        bl = bell(midi(['F5', 'C6', 'A5', 'F6', 'C5'][b % 5])) * 0.08
        place(L, bl, st, 1.2 if b % 2 else 0.8)
        place(R, bl, st, 0.8 if b % 2 else 1.2)
        # timpani on every other beat
        if b % 2 == 0 and b < 14:
            tp = timp(midi('F2') if b % 4 == 0 else midi('C2'), 0.5 if b % 8 == 0 else 0.35)
            place(L, tp, st)
            place(R, tp, st)
    # timpani roll on 'King'
    rt = STARTS[-1]
    while rt < CUT:
        tp = timp(midi('F2'), 0.12 + 0.25 * (rt - STARTS[-1]) / (CUT - STARTS[-1]))
        place(L, tp, rt)
        place(R, tp, rt)
        rt += 0.055
    for st, g in ((STARTS[0], 0.35), (STARTS[8], 0.3), (STARTS[-1], 0.35)):
        c = crash() * g
        place(L, c, st)
        place(R, c, st + 0.004)
    # the diva, above everything
    diva = voice(DIVA, FEMALE, 110, 0, dive=True) * 0.1
    before = np.clip((CUT - t) / 0.006, 0, 1)
    L += diva * before * 0.9
    R += diva * before * 1.1
    L, R = hall(L), hall(R)
    # stripped bare: everything goes, except the diva sliding away on her own
    L *= before
    R *= before
    alone = diva * (1 - before) * 1.4
    alone *= np.clip((HARK_END - HARK_START - t) / 0.03, 0, 1)
    end = int((HARK_END - HARK_START) * SR)
    return (L + alone)[:end], (R + alone)[:end]


def main():
    out = sys.argv[1]
    n = int(TOTAL * SR)
    L, R = np.zeros(n), np.zeros(n)

    dl, dr = deck()
    dpk = max(np.abs(dl).max(), np.abs(dr).max())
    L[:len(dl)] += dl / dpk
    R[:len(dr)] += dr / dpk

    gl, gr = gasp()
    place(L, gl, DECK_END)
    place(R, gr, DECK_END)

    hl, hr = hark()
    hpk = max(np.abs(hl).max(), np.abs(hr).max())
    place(L, hl / hpk, HARK_START)
    place(R, hr / hpk, HARK_START)

    # a gentle limiter so the loud parts are loud without crackling
    st = np.stack([L, R], 1)
    st = np.tanh(st * 1.6) / np.tanh(1.6) * 0.95
    st[int(GASP_END * SR):int(HARK_START * SR)] = 0
    st[int(HARK_END * SR):] = 0
    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, 'score.wav')
        import wave
        with wave.open(wav, 'wb') as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((st * 32767).astype(np.int16).tobytes())
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-i', wav,
                        '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)
    print(f'{out}: {os.path.getsize(out) / 1e6:.1f} MB')


if __name__ == '__main__':
    main()
