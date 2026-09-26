#!/usr/bin/env python3
"""Deck the Halls, solo piano: an original arrangement of the traditional (public domain) carol,
played on a synthesised piano, so the recording is ours to use anywhere.

Right hand: the tune. Left hand: bass note on beats 1 and 3, a soft chord on 2 and 4.
Key of F major, about 108 beats per minute.

Usage:
    python3 deck_the_halls.py OUT_DIR
Writes deck-the-halls-piano.wav (two verses with an ending) and deck-the-halls-piano-loop.wav
(one verse that loops seamlessly) and deck-the-halls-piano-phrase-loop.wav (just the opening
phrase, looped).
"""
import math
import os
import sys
import wave

import numpy as np

SR = 44100
BPM = 108
BEAT = 60.0 / BPM
rng = np.random.default_rng(7)

NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


def midi(name):
    """'Bb4' -> MIDI number."""
    n = NOTE[name[0]]
    rest = name[1:]
    if rest.startswith('b'):
        n -= 1
        rest = rest[1:]
    elif rest.startswith('#'):
        n += 1
        rest = rest[1:]
    return 12 * (int(rest) + 1) + n


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# ---------------------------------------------------------------------------
# The music: (note, beats) for the tune; one chord per half bar for the left hand
# ---------------------------------------------------------------------------
Q, E, DQ, H = 1.0, 0.5, 1.5, 2.0
A_TUNE = [  # Deck the halls with boughs of holly / Fa la la la la, la la la la
    ('C5', DQ), ('Bb4', E), ('A4', Q), ('G4', Q),
    ('F4', Q), ('G4', Q), ('A4', Q), ('F4', Q),
    ('G4', E), ('A4', E), ('Bb4', E), ('G4', E), ('A4', DQ), ('G4', E),
    ('F4', Q), ('E4', Q), ('F4', H),
]
B_TUNE = [  # Don we now our gay apparel / Fa la la, la la la, la la la
    ('G4', DQ), ('A4', E), ('Bb4', Q), ('G4', Q),
    ('A4', DQ), ('Bb4', E), ('C5', Q), ('G4', Q),
    ('A4', E), ('B4', E), ('C5', Q), ('D5', E), ('E5', E), ('F5', Q),
    ('E5', Q), ('D5', Q), ('C5', H),
]
A2_TUNE = [  # Troll the ancient Yuletide carol / Fa la la la la, la la la la
    ('C5', DQ), ('Bb4', E), ('A4', Q), ('G4', Q),
    ('F4', Q), ('G4', Q), ('A4', Q), ('F4', Q),
    ('D5', E), ('D5', E), ('D5', E), ('D5', E), ('C5', DQ), ('Bb4', E),
    ('A4', Q), ('G4', Q), ('F4', H),
]
CHORDS = {  # root, chord tones for the left hand
    'F': ('F2', ['A3', 'C4', 'F4']), 'C': ('C3', ['G3', 'Bb3', 'E4']), 'Bb': ('Bb2', ['D4', 'F4', 'Bb3']),
    'G': ('G2', ['B3', 'D4', 'G3']), 'Dm': ('D3', ['A3', 'D4', 'F4']), 'C7': ('C3', ['E4', 'G3', 'Bb3']),
}
A_HARM = ['F', 'F', 'F', 'C', 'C', 'F', 'C', 'F']
B_HARM = ['C', 'C7', 'F', 'C', 'G', 'Dm', 'G', 'C7']
A2_HARM = ['F', 'F', 'F', 'C', 'Bb', 'F', 'C', 'F']


def verse():
    tune = A_TUNE + A_TUNE + B_TUNE + A2_TUNE
    harm = A_HARM + A_HARM + B_HARM + A2_HARM
    return tune, harm


# ---------------------------------------------------------------------------
# The piano: stretched partials, each dying away at its own rate, a felt-hammer thump, three
# slightly detuned strings per note, and a damper that stops the note when it is released
# ---------------------------------------------------------------------------
def piano_note(m, vel, dur):
    f0 = hz(m)
    ring = min(6.0, 4.5 * (261.6 / f0) ** 0.55)  # low notes ring longer
    length = dur + 0.35
    n = int(length * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    B = 0.00035 * (f0 / 261.6) ** 0.5  # inharmonicity: upper partials slightly sharp
    bright = 0.55 + 0.45 * vel
    for k in range(1, 15):
        fk = f0 * k * math.sqrt(1 + B * k * k)
        if fk > SR / 2 - 2000:
            break
        amp = (1.0 / k ** 1.25) * (bright ** (k - 1))
        tau = ring / (1 + 0.45 * (k - 1))
        env = 0.65 * np.exp(-t / (tau * 0.22)) + 0.35 * np.exp(-t / tau)
        for cents in (-0.9, 0.0, 1.1):  # three strings, beating gently
            ph = rng.uniform(0, 2 * math.pi)
            out += amp * env * np.sin(2 * math.pi * fk * (2 ** (cents / 1200)) * t + ph) / 3
    # hammer thump: a short soft noise burst, darker for quiet notes
    k = int(0.012 * SR)
    thump = rng.standard_normal(k) * np.exp(-np.arange(k) / (0.003 * SR))
    thump = np.convolve(thump, np.ones(12) / 12, 'same') * 0.05 * vel
    out[:k] += thump
    # attack and damper
    a = int(0.004 * SR)
    out[:a] *= np.linspace(0, 1, a)
    off = int(dur * SR)
    if off < n:
        rel = np.exp(-np.arange(n - off) / (0.09 * SR))
        out[off:] *= rel
    return out * vel


class Roll:
    def __init__(self, seconds):
        self.L = np.zeros(int(seconds * SR) + SR * 4)
        self.R = np.zeros_like(self.L)

    def add(self, name, start, dur, vel):
        m = midi(name)
        s = piano_note(m, vel, dur)
        i = max(0, int((start + rng.normal(0, 0.006)) * SR))  # a human touch on the timing
        pan = np.clip((m - 60) / 40, -0.45, 0.45)
        self.L[i:i + len(s)] += s * (0.5 - pan / 2) * 1.4
        self.R[i:i + len(s)] += s * (0.5 + pan / 2) * 1.4


def perform(tune, harm, roll, t0, final_slow=False):
    t = t0
    total = sum(b for _, b in tune)
    for i, (name, beats) in enumerate(tune):
        stretch = 1.0
        pos = (t - t0) / BEAT
        if final_slow and pos > total - 4:  # an easing-off in the last bar
            stretch = 1.0 + 0.35 * (pos - (total - 4)) / 4
        dur = beats * BEAT * stretch
        accent = 0.82 if pos % 2 < 0.01 else 0.72
        roll.add(name, t, dur * 0.94, accent + rng.normal(0, 0.03))
        t += dur
    # left hand: two chords per bar, bass on the beat, chord on the off-beat
    for j, ch in enumerate(harm):
        root, tones = CHORDS[ch]
        bt = t0 + j * 2 * BEAT
        roll.add(root, bt, 1.9 * BEAT, 0.5 + rng.normal(0, 0.02))
        for tone in tones:
            roll.add(tone, bt + BEAT, 0.9 * BEAT, 0.3 + rng.normal(0, 0.02))
    return t


def reverb(x):
    """A small warm room around the piano."""
    L = int(1.6 * SR)
    tt = np.arange(L) / SR
    ir = rng.standard_normal(L) * np.exp(-tt / 0.38) * (tt > 0.012)
    ir = np.convolve(ir, np.ones(20) / 20, 'same')
    ir /= np.sqrt((ir ** 2).sum())
    n = len(x) + L
    wet = np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[:len(x)]
    return x * 0.88 + wet * 0.2


def write(path, L, R):
    st = np.stack([L, R], 1)
    st = st / np.abs(st).max() * 0.89
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    tune, harm = verse()
    vlen = sum(b for _, b in tune) * BEAT

    # full piece: two verses, the second one gently easing off, then a final chord
    roll = Roll(vlen * 2 + 6)
    perform(tune, harm, roll, 0.3)
    end = perform(tune, harm, roll, 0.3 + vlen, final_slow=True)
    for name in ('F2', 'C3', 'A3', 'C4', 'F4', 'A4', 'C5', 'F5'):
        roll.add(name, end + 0.05, 3.2, 0.55)
    L, R = reverb(roll.L), reverb(roll.R)
    stop = int((end + 4.0) * SR)
    fade = np.linspace(1, 0, int(1.2 * SR))
    L, R = L[:stop], R[:stop]
    L[-len(fade):] *= fade
    R[-len(fade):] *= fade
    write(os.path.join(out, 'deck-the-halls-piano.wav'), L, R)

    # loop: one verse, with the tail of the verse folded back onto the start so it joins seamlessly
    roll = Roll(vlen + 6)
    perform(tune, harm, roll, 0.0)
    L, R = reverb(roll.L), reverb(roll.R)
    n = int(vlen * SR)
    for ch in (L, R):
        tail = ch[n:n + 3 * SR].copy()
        ch[:len(tail)] += tail
    write(os.path.join(out, 'deck-the-halls-piano-loop.wav'), L[:n], R[:n])
    # the opening phrase alone ('Deck the halls with boughs of holly, fa la la la la, la la la la'), looped
    plen = sum(b for _, b in A_TUNE) * BEAT
    roll = Roll(plen + 6)
    perform(A_TUNE, A_HARM, roll, 0.0)
    L, R = reverb(roll.L), reverb(roll.R)
    n = int(plen * SR)
    for ch in (L, R):
        tail = ch[n:n + 3 * SR].copy()
        ch[:len(tail)] += tail
    write(os.path.join(out, 'deck-the-halls-piano-phrase-loop.wav'), L[:n], R[:n])
    print(f'verse {vlen:.1f}s, full piece {(end + 4.0):.1f}s, phrase {plen:.1f}s')


if __name__ == '__main__':
    main()
