#!/usr/bin/env python3
"""Horror trailer score (about 60.9 seconds), built from our Deck the Halls piano.

    0     - 15    gentle Deck: the phrase twice, clean...
    15    - 18.05 ...until the tune sags, drags and goes wrong; it cuts off before its last note
    18.05         the knife comes down, in place of the final "la"
    18.05 - 23.25 silence, broken only by the knife; the girl asks "Why would she do that?", then a second of nothing
    23.25 - 28    the distortion starts: the odd note off-key, late or too loud; tiny crackles and static
    28    - 35    faster, more maddened; four of its notes are human screams (28.7, 30.6, 33.8, 37.75 s),
                  cut off dead, each from a different mouth and each more desperate than the last
    35    - 44.6  the crescendo: 'being chased by a murderous clown' - still clearly the tune; its last loop
                  plays right to the end
    44.6  - 45.1  a horror gasp
    45.1  - 46.1  one second of silence
    46.1  - 51.4  someone breathing in the dark
    51.4  - 52.9  the ambush: something horrible, a sudden swarm of intense buzzing, cut dead
    52.9  - 58.5  straight into 'HARK! THE HE-RALD AN-GELS SING!' as an orchestral climax
    58.5  - 58.9  the orchestra is stripped away, leaving the diva alone, sliding down into nothing
    58.9  - 60.9  two seconds of silence for the post-trailer titles

Usage:
    python3 horror_trailer_music.py OUT.m4a
"""
import os
import subprocess
import sys
import tempfile
import wave

import imageio_ffmpeg
import numpy as np

import deck_the_halls as D
from deck_the_halls import SR, A_HARM, A_TUNE, CHORDS, midi, hz, piano_note

rng = np.random.default_rng(13)


def reseed(*key):
    """Give each part of the score its own fixed dice, so changing one part never reshuffles another."""
    global rng
    seed = [13] + [int(round(k * 1000)) % (2 ** 32) for k in key]
    rng = np.random.default_rng(seed)
    D.rng = np.random.default_rng(seed + [1])
LEAD = 0.05
CLEAN_BEATS = 32                      # two gentle loops of the phrase at a steady 100 bpm
PAUSE_AT = LEAD + CLEAN_BEATS * 0.6   # 19.25 s: where the third loop would begin; the music picks up from here after the pause
MUSIC_CUT = LEAD + (CLEAN_BEATS - 2) * 0.6  # 18.05 s: the last note never plays - the music cuts off early
SHOCK_GAP = 0.06                            # a sliver of dead air so the hit lands like a slap
CHOP_AT = MUSIC_CUT                         # 18.05 s: the knife lands in place of the final "la"
OMEN_FROM = LEAD + (CLEAN_BEATS - 7) * 0.6  # 15.05 s: the tune starts to go wrong just before the knife
PAUSE = 4.0                           # the silence for "Why would she do that?"
RAMP_END = 38.0                       # the tempo keeps climbing until here (music time)


def bpm_at(t):
    return np.interp(t, [0, PAUSE_AT, 23.5, 28.5, 33.5, RAMP_END, RAMP_END + 3.5],
                     [100, 100, 115, 150, 200, 280, 330])  # and on, faster still, for the extra loop


_tg = np.arange(0, RAMP_END + 8, 0.001)
_beats = np.concatenate([[0], np.cumsum(bpm_at(_tg[:-1]) / 60 * 0.001)])


def b2t(b):
    return float(np.interp(b, _beats, _tg)) + LEAD


# the Deck ends exactly as its last complete loop finishes, final 'la' and all, and the gasp comes straight after
LAST_BEAT = int(np.interp(RAMP_END - LEAD, _tg, _beats) // 16) * 16 + 16  # plus one more full loop
MUSIC_END = b2t(LAST_BEAT)            # length of the Deck music itself (music time), about 40.3 s
DECK_END = MUSIC_END + PAUSE          # about 44.3 in the finished track
GASP_END = DECK_END + 0.5
BREATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio', 'breathing.m4a')
BREATH_SPAN = (0.30, 5.60)            # the breathing, trimmed from the recording
BREATH_AT = GASP_END + 1.0            # one second of silence after the gasp, then the breathing
AMBUSH = 1.5                          # the discordant buzzing ambush
AMBUSH1_AT = BREATH_AT + BREATH_SPAN[1] - BREATH_SPAN[0]  # it falls on the breather as the breathing ends
HARK_START = AMBUSH1_AT + AMBUSH      # and the Hark comes straight in after it
DENUDE = HARK_START + 5.6
HARK_END = DENUDE + 0.4
TOTAL = HARK_END + 2.0                # ends on two seconds of silence for the titles
SCREAM_WINDOW = (28.0, DECK_END - 0.7)
DIALOGUE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio', 'why-would-she-do-that.m4a')
DIALOGUE_SPAN = (2.82, 4.10)          # where the words are in the recording
DIALOGUE_AT = PAUSE_AT + 1.6            # ends about 22.1 s, leaving a second of silence before the music


def real(t):
    """Music time -> time in the finished track (the pause pushes everything after it back)."""
    return t if t < PAUSE_AT else t + PAUSE


# ---------------------------------------------------------------------------
# Shared sound-shaping helpers
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


FEMALE = [(800, 90, 1.0), (1150, 100, 0.5), (2900, 150, 0.3), (3900, 180, 0.2), (4950, 200, 0.1)]
MALE = [(650, 90, 1.0), (1080, 100, 0.45), (2650, 150, 0.35), (2900, 150, 0.35), (3250, 180, 0.15)]


def additive(f, spectrum, fmax=9000):
    """A tone following the frequency curve f, its harmonics weighted by spectrum(fk, k)."""
    ph = np.cumsum(2 * np.pi * f / SR) + rng.uniform(0, 6.3)
    out = np.zeros(len(f))
    for k in range(1, min(90, int(fmax / f.min())) + 1):
        fk = k * f
        out += spectrum(fk, k) * (fk < fmax) * np.sin(k * ph)
    return out


# ---------------------------------------------------------------------------
# Deck the Halls, looping and accelerating (all in 'music time')
# ---------------------------------------------------------------------------
def mad(t):
    """0 while the carol is innocent, rising to 1 at the gasp."""
    return np.clip((t - PAUSE_AT) / (MUSIC_END - PAUSE_AT), 0, 1)


def add_note(L, R, m, t, dur, vel):
    if t < 0 or dur <= 0:
        return
    s = piano_note(m, min(vel, 1.05), dur)
    i = int(t * SR)
    s = s[:max(0, len(L) - i)]
    pan = np.clip((m - 60) / 40, -0.45, 0.45)
    L[i:i + len(s)] += s * (0.5 - pan / 2) * 1.4
    R[i:i + len(s)] += s * (0.5 + pan / 2) * 1.4


def calliope(L, R, m, t, dur, vel):
    """A wheezy, out-of-tune fairground organ doubling the tune."""
    n = int((dur + 0.05) * SR)
    tt = np.arange(n) / SR
    f = hz(m + rng.normal(0, 0.15)) * (1 + 0.006 * np.sin(2 * np.pi * 7 * tt))
    s = additive(f, lambda fk, k: [0, 1, 0.45, 0.3, 0.12, 0.08, 0.05][k] if k < 7 else 0.0)
    s += shaped(rng.standard_normal(n), lambda fr: np.exp(-((fr - hz(m) * 2) / 600) ** 2)) * 0.04
    env = np.minimum(1, tt / 0.012) * np.clip((dur + 0.05 - tt) / 0.05, 0, 1)
    s *= env * vel * (1 + 0.25 * np.sin(2 * np.pi * 7 * tt))
    i = int(t * SR)
    s = s[:max(0, len(L) - i)]
    L[i:i + len(s)] += s * 0.55
    R[i:i + len(s)] += s * 0.45


# the open 'AAAH' of a scream; each mouth scales it by the size of its vocal tract
SCREAM_AH = [(1000, 180, 1.0), (1650, 220, 0.75), (2900, 300, 0.6), (3900, 380, 0.35), (5000, 600, 0.15)]
# (who, octave shift, tract size, breathiness, roughness, strain, voice cracks, loudness)
MOUTHS = [
    ('woman',            12, 1.00, 0.10, 0.15, 1.5, 0, 1.00),
    ('man',               0, 0.84, 0.14, 0.30, 2.0, 0, 1.00),
    ('young woman',      12, 1.08, 0.12, 0.30, 2.5, 1, 1.08),
    ('big man',           0, 0.78, 0.20, 0.55, 3.0, 0, 1.12),
    ('hoarse woman',     12, 0.95, 0.30, 0.55, 3.5, 1, 1.18),
    ('man, high, in pain', 12, 0.86, 0.22, 0.65, 4.0, 2, 1.24),
    ('older woman',       0, 0.94, 0.35, 0.85, 5.0, 2, 1.30),
    ('everyone at once',  None, 0, 0, 0, 0, 0, 1.38),
]
# who screams on each of the six chosen notes (None = that note stays an ordinary piano note)
SCREAMERS = [MOUTHS[0], MOUTHS[1], None, MOUTHS[4], None, MOUTHS[7]]


def smooth_noise(n, width):
    w = max(1, int(width * SR))
    x = np.convolve(rng.standard_normal(n + w), np.ones(w) / w, 'same')[:n]
    return x / (x.std() + 1e-9)


def scream(m, dur, mouth):
    """A human scream on the note's pitch, cut off dead at the end of the note."""
    who, octv, tract, breath, rough, strain, cracks, _ = mouth
    if octv is None:  # the last one: several of them together
        s = sum(scream(m, dur, mo) * g for mo, g in ((MOUTHS[2], 1), (MOUTHS[3], 0.8), (MOUTHS[5], 0.9), (MOUTHS[6], 0.8)))
        return s / np.abs(s).max()
    n = int(dur * SR)
    t = np.arange(n) / SR
    base = m + octv
    while 440 * 2 ** ((base - 69) / 12) > 1150:
        base -= 12
    # the pitch hauls itself up into the note, wanders a little, never a regular wobble
    lm = base - 4 * np.exp(-t / 0.05) + 0.25 * smooth_noise(n, 0.08) + 0.12 * smooth_noise(n, 0.012) * (1 + rough)
    for _ in range(cracks):  # the voice cracks upward for a moment
        c0 = rng.uniform(0.25, 0.75) * dur
        lm += rng.choice([4, 5, 7]) * np.exp(-((t - c0) / 0.035) ** 2)
    f = 440 * 2 ** ((lm - 69) / 12)
    forms = [(F * tract, bw * tract, a) for F, bw, a in SCREAM_AH]
    spec = lambda fk, k: formant_gain(fk, forms) / k ** 0.5
    s = additive(f, spec)
    s /= np.abs(s).max()
    if rough:  # a torn, rattling edge on the voice
        sub = additive(f / 2, spec)
        s += sub / np.abs(sub).max() * rough * 0.35 * (0.5 + 0.5 * np.clip(smooth_noise(n, 0.02), -1, 1))
    s *= 1 + rough * 0.35 * smooth_noise(n, 0.006)  # uneven, shuddering loudness
    s = np.tanh(s * strain) / np.tanh(strain)  # the throat straining
    air = shaped(rng.standard_normal(n), lambda fr: formant_gain(fr, forms) * (fr > 400))
    s += air / np.abs(air).max() * breath
    env = np.minimum(1, t / 0.02) * (0.9 + 0.1 * t / dur)
    k = int(0.003 * SR)
    env[-k:] *= np.linspace(1, 0, k)
    s *= env
    return s / np.abs(s).max()


def deck():
    n = int((MUSIC_END + 1) * SR)
    bufs = {'A': (np.zeros(n), np.zeros(n)), 'B': (np.zeros(n), np.zeros(n))}  # before / after the stop
    events = []
    b = 0.0
    while b2t(b) < MUSIC_END:
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

    # choose the two notes that become screams: long ones, well apart
    lo, hi = SCREAM_WINDOW
    cands = [e for e in events if e[3] == 'tune' and e[2] >= 1.0 and lo <= real(b2t(e[0])) < hi]
    picks = []
    for e in cands:
        if not picks or b2t(e[0]) - b2t(picks[-1][0]) > 1.5:
            picks.append(e)
    picks = picks[:len(SCREAMERS)]
    print('screams at', [round(real(b2t(e[0])), 2) for e, who in zip(picks, SCREAMERS) if who])
    screams = []

    for ev in events:
        bb, m0, nb, kind = ev
        reseed(1, bb, m0, {'tune': 1, 'bass': 2, 'chord': 3}[kind])
        t = b2t(bb)
        if t >= MUSIC_END:
            continue
        after = t >= PAUSE_AT - 0.001
        if MUSIC_CUT - 0.001 <= t < PAUSE_AT - 0.001:
            continue  # the final note of the second loop, and its chords, are gone
        omen = float(np.clip((t - OMEN_FROM) / (MUSIC_CUT - OMEN_FROM), 0, 1)) if not after else 0.0
        L, R = bufs['B' if after else 'A']
        k = float(mad(t))
        dur = b2t(bb + nb * 0.94) - t
        m = m0 + (-20 * k + rng.normal(0, 2 + 8 * k)) / 100  # a slight sag, a little honky-tonk
        base = {'tune': 0.78, 'bass': 0.5, 'chord': 0.3}[kind]
        vel = base * (1 + 0.4 * k) + rng.normal(0, 0.03)
        t += rng.normal(0, 0.003 + 0.006 * k)
        if after:
            t = max(t, PAUSE_AT)
        if omen:  # the omen: the tune sags flat and drags, and one note goes wrong
            m -= 0.7 * omen ** 1.3
            t += 0.03 * omen
            if kind == 'tune' and bb == CLEAN_BEATS - 3:
                m -= 1
                t += 0.07
            if kind != 'tune' and omen > 0.5:
                add_note(L, R, m + 1, t, dur, vel * 0.6)
        if kind == 'tune':
            if after and rng.random() < 0.05 + 0.1 * k:  # the occasional note off-key...
                m += rng.choice([-1, 1]) * rng.choice([0.5, 1.0])
            elif after and rng.random() < 0.05 + 0.1 * k:  # ...or late...
                t += rng.uniform(0.04, 0.09 + 0.05 * k)
            elif after and rng.random() < 0.06 + 0.1 * k:  # ...or too loud
                vel = min(1.05, vel * 1.5)
            if ev in picks and SCREAMERS[picks.index(ev)]:
                screams.append((t, m, dur, SCREAMERS[picks.index(ev)]))
                add_note(L, R, m, t, dur, vel * 0.35)
                continue
            add_note(L, R, m, t, dur, vel)
            if k > 0.3:  # honky-tonk: a second string badly out of tune
                add_note(L, R, m + 0.22, t, dur, vel * 0.45 * min(1, (k - 0.3) / 0.3))
            if k > 0.55:  # the tune in octaves, hammered
                add_note(L, R, m - 12, t, dur, vel * 0.7 * min(1, (k - 0.55) / 0.2))
            if t > PAUSE_AT + 3:  # the fairground organ joins in
                calliope(L, R, m + 12, t, dur, vel * 0.32 * min(1, (t - PAUSE_AT - 3) / 12) ** 1.3)
        else:
            add_note(L, R, m, t, dur, vel)
            if kind == 'bass' and k > 0.6 and rng.random() < 0.5:
                add_note(L, R, m + 1, t, dur, vel * 0.5)

    tt = np.arange(n) / SR
    k = mad(tt)
    depth = 0.0012 * k ** 1.5 * SR  # a gently warped tape
    ph = np.cumsum(2 * np.pi * (0.4 + 2.5 * k ** 2) / SR)
    idx = np.arange(n) - depth * (1 + np.sin(ph))
    omen = np.clip((tt - OMEN_FROM) / (MUSIC_CUT - OMEN_FROM), 0, 1) * (tt < PAUSE_AT)
    idx -= np.cumsum(0.05 * omen ** 2) + 0.0025 * SR * omen * (1 + np.sin(2 * np.pi * 1.3 * tt))  # the tape slows and warps
    out = {}
    for key, (L, R) in bufs.items():
        reseed(9, ord(key))
        L = np.interp(idx, np.arange(n), L)
        R = np.interp(idx, np.arange(n), R)
        out[key] = [D.reverb(L), D.reverb(R)]
    whole = out['A'][0] + out['B'][0]
    P = max(np.abs(whole[:int(22 * SR)]).max(), np.abs(whole[int(22 * SR):]).max() / 1.5)

    # the screams go on dry and cut off dead
    for si, (st, m, dur, mouth) in enumerate(screams):
        reseed(2, round(st, 2))
        s = scream(m, dur, mouth) * P * mouth[-1]
        i = int(st * SR)
        out['B'][0][i:i + len(s)] += s * 0.95
        out['B'][1][i:i + len(s)] += s * 1.05

    reseed(3)
    # the bed: a low drone creeping in, tiny crackles and static, and a rising whine at the end
    bed = np.zeros(n)
    amp = np.clip((tt - PAUSE_AT) / 16, 0, 1) ** 1.5 * 0.08 + np.clip((tt - (MUSIC_END - 8)) / 8, 0, 1) ** 2 * 0.08
    for f, a in ((87.31, 1), (92.5, 0.7), (174.6, 0.5), (185.0, 0.35)):
        bed += a * np.sin(2 * np.pi * f * tt * (1 + 0.004 * np.sin(0.4 * tt)))
    bed *= amp * P
    rate = np.interp(tt, [0, PAUSE_AT - 0.01, PAUSE_AT, 25, 32, MUSIC_END], [0, 0, 0.6, 3, 9, 25])  # crackles per second
    hits = np.nonzero(rng.random(n) < rate / SR)[0]
    click = np.exp(-np.arange(60) / 8.0) * np.sign(rng.standard_normal(60))
    for i in hits:
        a = rng.uniform(0.03, 0.12) * P * (1 + 1.5 * k[i])
        seg = click[:n - i] * a
        bed[i:i + len(seg)] += seg
    t_s = PAUSE_AT + 1.0
    while t_s < MUSIC_END - 0.3:
        kk = float(mad(t_s))
        ln = rng.uniform(0.03, 0.12 + 0.1 * kk)
        m_ = int(ln * SR)
        i = int(t_s * SR)
        c = rng.uniform(1500, 6000)
        burst = shaped(rng.standard_normal(m_), lambda fr: np.exp(-((fr - c) / 1500) ** 2))
        burst *= np.hanning(m_) * (rng.random(m_) < 0.6) * P * rng.uniform(0.05, 0.12) * (1 + kk)
        bed[i:i + m_] += burst / (np.abs(burst).max() + 1e-9) * P * 0.07 * (1 + kk)
        t_s += rng.exponential(2.5 - 1.8 * kk)
    u = np.clip((tt - (MUSIC_END - 6.5)) / 6.5, 0, 1)
    for det in (-0.02, 0.0, 0.021):
        f = 220 * 2 ** (3.0 * u + det)
        bed += additive(f, lambda fk, kk: 1.0 / kk) * (u ** 2.5) * 0.03 * P

    gain = np.interp(tt, [0, PAUSE_AT, 25, 32, MUSIC_END], [1.0, 1.0, 1.05, 1.12, 1.5])
    for key in out:
        out[key] = [ch * gain + bed for ch in out[key]]

    # stitch: stop dead at 12 s, two seconds of nothing, then carry on
    cut = int(PAUSE_AT * SR)
    f = int(0.006 * SR)
    res = []
    for c in (0, 1):
        a = out['A'][c][:cut].copy()
        mc = int((MUSIC_CUT - SHOCK_GAP) * SR)
        a[mc - f:mc] *= np.linspace(1, 0, f)
        a[mc:] = 0
        bpart = out['B'][c][cut:int(MUSIC_END * SR)].copy()
        if len(bpart) > f:
            bpart[-f:] *= np.linspace(1, 0, f)
        res.append(np.concatenate([a, np.zeros(int(PAUSE * SR)), bpart]))
    return res


# ---------------------------------------------------------------------------
# The knife: through the fingers and into the chopping board
# ---------------------------------------------------------------------------
def chop():
    """A cleaver hitting meat and bone, hard, then burying itself in the board."""
    reseed(6)
    n = int(1.2 * SR)
    t = np.arange(n) / SR

    def burst(t0, length, lo, hi, decay):
        x = np.zeros(n)
        i0, k = int(t0 * SR), int(length * SR)
        seg = rng.standard_normal(k) * np.exp(-np.arange(k) / (decay * SR))
        x[i0:i0 + k] = seg
        return shaped(x, lambda f: ((f > lo) & (f < hi)) * 1.0)

    # the smack of the blade into flesh: a hard, bright slap
    smack = burst(0.0, 0.05, 700, 6000, 0.008)
    smack /= np.abs(smack).max()
    # a heavy punch in the gut, pitch dropping like a kick drum, and a cinematic sub-boom under it
    punch = np.sin(np.cumsum(2 * np.pi * (55 + 180 * np.exp(-t / 0.018)) / SR)) * np.exp(-t / 0.11)
    boom = np.sin(np.cumsum(2 * np.pi * (38 + 25 * np.exp(-t / 0.06)) / SR)) * np.exp(-t / 0.45)
    # bone splintering
    crack = np.zeros(n)
    for c in (0.006, 0.009, 0.014, 0.022, 0.035):
        crack += burst(c, 0.005, 2500, 12000, 0.0007) * rng.uniform(0.5, 1)
    crack /= np.abs(crack).max()
    # the blade burying into the wooden board a split second later: a dead, woody 'chunk' and a short metal ring
    chunk = np.zeros(n)
    i0 = int(0.012 * SR)
    tt = t[:n - i0]
    chunk[i0:] = (np.sin(2 * np.pi * 180 * tt) * np.exp(-tt / 0.03) + 0.6 * np.sin(2 * np.pi * 420 * tt) * np.exp(-tt / 0.02)
                  + 0.2 * sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.07) for f in (2750, 4130, 5870)))
    # a wet squelch
    wet = burst(0.004, 0.25, 250, 1800, 0.05)
    wet *= 0.6 + 0.4 * np.clip(np.convolve(rng.standard_normal(n), np.ones(150) / 150, 'same') * 8, -1, 1)
    wet /= np.abs(wet).max()
    snap = burst(0.0, 0.006, 150, 12000, 0.0012)  # the instant of contact
    snap /= np.abs(snap).max()
    body = shaped(burst(0.0, 0.12, 60, 400, 0.03), lambda f: 1.0)  # the dead weight of the blow
    body /= np.abs(body).max()
    x = 1.2 * snap + 1.0 * smack + 1.2 * punch + 0.35 * boom + 0.6 * body + 0.6 * crack + 0.7 * chunk + 0.4 * wet
    x = np.tanh(x * 1.2) / np.tanh(1.2)  # hard, but keeping the crack of the attack
    x = x * 0.85 + D.reverb(x)[:n] * 0.25
    x[-int(0.3 * SR):] *= np.linspace(1, 0, int(0.3 * SR))
    return x / np.abs(x).max() * 0.97


def denoise(x, noise, frame=2048, hop=512, strength=2.0, floor=0.08):
    """Take the phone's background hiss out: learn what the hiss sounds like from a stretch with nobody
    speaking, then turn down that sound everywhere, frame by frame."""
    win = np.hanning(frame)
    pad = np.concatenate([np.zeros(frame), x, np.zeros(frame)])
    starts = np.arange(0, len(pad) - frame, hop)
    X = np.array([np.fft.rfft(pad[i:i + frame] * win) for i in starts])
    nz = np.concatenate([np.zeros(frame), noise, np.zeros(frame)])
    N = np.median(np.abs(np.array([np.fft.rfft(nz[i:i + frame] * win)
                                   for i in range(frame, len(nz) - 2 * frame, hop)])), axis=0)
    mag = np.abs(X) + 1e-12
    g = np.clip(1 - strength * N / mag, floor, 1)
    g = np.convolve(np.pad(g, ((1, 1), (0, 0)), mode='edge').ravel(), [1], 'same').reshape(len(g) + 2, -1)
    g = (g[:-2] + g[1:-1] + g[2:]) / 3  # smooth over time so it doesn't warble
    out = np.zeros(len(pad))
    norm = np.zeros(len(pad))
    for k, i in enumerate(starts):
        out[i:i + frame] += np.fft.irfft(X[k] * g[k], frame) * win
        norm[i:i + frame] += win ** 2
    return (out / np.maximum(norm, 1e-6))[frame:frame + len(x)]


def recording(path, span, level, noise=None, tone=None):
    """A voice recording: hiss removed, trimmed, low rumble removed, tone shaped, level set."""
    raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-i', path, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16) / 32768
    if noise:
        x = denoise(x, x[int(noise[0] * SR):int(noise[1] * SR)])
    a, b = (int(v * SR) for v in span)
    x = x[a:b].copy()
    x = shaped(x, lambda f: np.clip((f - 60) / 60, 0, 1) * (tone(f) if tone else 1))
    k = int(0.03 * SR)
    x[:k] *= np.linspace(0, 1, k)
    x[-k:] *= np.linspace(1, 0, k)
    return x / np.abs(x).max() * level


def warm(f, db=2.5, at=250, width=180):
    return 10 ** (db * np.exp(-((f - at) / width) ** 2) / 20)


def dialogue():
    """'Why would she do that?' - cleaned, warmed, and put outdoors on a snowy bench."""
    v = recording(DIALOGUE, DIALOGUE_SPAN, 0.7, noise=(0.3, 2.6),
                  tone=lambda f: warm(f) / (1 + (f / 9000) ** 2))  # a touch fuller, a touch softer on top
    # outdoors: no room, just a faint far-off slap of sound off the hospital wall
    echo = np.zeros(len(v) + int(0.09 * SR))
    echo[int(0.09 * SR):] = shaped(v, lambda f: 1 / (1 + (f / 2500) ** 2)) * 0.07
    echo[:len(v)] += v
    return echo


def snow_air(length):
    """The hush of snowy open air: soft, muffled, barely there."""
    reseed(10)
    n = int(length * SR)
    t = np.arange(n) / SR
    air = shaped(rng.standard_normal(n), lambda f: (f > 40) / (1 + (f / 500) ** 2))
    air = air / np.abs(air).max() * (0.8 + 0.2 * np.sin(2 * np.pi * 0.3 * t))
    fade = int(0.35 * SR)
    air[:fade] *= np.linspace(0, 1, fade)
    air[-fade:] *= np.linspace(1, 0, fade)
    return air * 0.012


def breathing():
    """Someone breathing in the dark - cleaned, and brought in close: fuller low end, a cramped little space."""
    v = recording(BREATH, BREATH_SPAN, 0.55, noise=(1.7, 2.0), tone=lambda f: warm(f, 3.5, 200, 150))
    close = np.zeros(len(v) + int(0.012 * SR))
    close[:len(v)] += v
    close[int(0.009 * SR):int(0.009 * SR) + len(v)] += shaped(v, lambda f: 1 / (1 + (f / 3000) ** 2)) * 0.22
    return close / np.abs(close).max() * 0.55


# ---------------------------------------------------------------------------
# The gasp
# ---------------------------------------------------------------------------
def gasp():
    reseed(4)
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
# HARK! THE HE-RALD AN-GELS SING! - an orchestral climax
# ---------------------------------------------------------------------------
HB = 60 / 90
#        Hark   the   he-   rald  an-   gels  SING
BEATS = [1.0, 1.0, 2.0, 0.5, 0.5, 1.15, None]  # DAH DAH DAHHH, DA DA DAH DAHHH
MEL = ['C5', 'F5', 'F5', 'E5', 'F5', 'A5', 'A5']
ALTO = ['A4', 'A4', 'A4', 'G4', 'A4', 'C5', 'C5']
TENOR = ['F4', 'C4', 'C4', 'C4', 'C4', 'F4', 'F4']
BASS = ['F3', 'F3', 'F3', 'C3', 'F3', 'F3', 'F3']
LOW = ['F2', 'F2', 'F2', 'C2', 'F2', 'F2', 'F2']
HARM = ['F', 'F', 'F', 'C', 'F', 'F', 'F']
DIVA = MEL[:-1] + ['F6']
HN = int((HARK_END - HARK_START + 0.5) * SR)
_starts = [0.02]
for _b in BEATS[:-1]:
    _starts.append(_starts[-1] + _b * HB)
STARTS = np.array(_starts)  # seconds after HARK_START
CUT = DENUDE - HARK_START
HT = np.arange(HN) / SR
_IDX = np.clip(np.searchsorted(STARTS, HT, side='right') - 1, 0, len(MEL) - 1)


def pitch_curve(names, vib_cents, rate, detune, glide=0.03):
    lm = np.array([midi(nm) for nm in names], float)[_IDX]
    w = int(glide * SR)
    lm = np.convolve(np.pad(lm, (w, w), mode='edge'), np.ones(w) / w, 'same')[w:-w]
    vib = vib_cents / 100 * np.sin(2 * np.pi * rate * HT + rng.uniform(0, 6.3)) * np.minimum(1, HT / 0.15)
    return lm + vib + detune / 100


def hits_env(attack=0.02, dip=0.7, swell_last=True):
    """Every syllable struck like a conductor's downbeat: a punch, a slight settle, a gap before the next."""
    env = np.zeros(HN)
    for i, s in enumerate(STARTS):
        e = STARTS[i + 1] if i + 1 < len(STARTS) else CUT + 0.3
        a, b_ = int(s * SR), int(e * SR)
        tt = np.arange(b_ - a) / SR
        seg = np.minimum(1, tt / attack) * (0.8 + 0.2 * np.exp(-tt / 0.12))
        if i == len(STARTS) - 1 and swell_last:
            seg *= 1 + 0.4 * np.clip(tt / 1.0, 0, 1)  # the final note swells
        gap = int(0.04 * SR)
        if i + 1 < len(STARTS):
            seg[-gap:] *= 1 - dip * np.linspace(0, 1, gap)
        env[a:b_] = seg[:len(env[a:b_])]
    return env


def section(names, count, spectrum, vib, rate, spread, env, pan):
    L, R = np.zeros(HN), np.zeros(HN)
    for _ in range(count):
        lm = pitch_curve(names, vib, rate + rng.normal(0, 0.3), rng.normal(0, spread))
        f = 440 * 2 ** ((lm - 69) / 12)
        s = additive(f, spectrum)
        s = s / (np.sqrt((s ** 2).mean()) + 1e-9) * env / count ** 0.5
        p = np.clip(pan + rng.normal(0, 0.12), -0.9, 0.9)
        L += s * (0.5 - p / 2)
        R += s * (0.5 + p / 2)
    return L, R


def brass_spectrum(env):
    cut = 1200 + 3000 * np.clip(env, 0, 1.4)  # louder = brighter, the brass 'blaze'
    return lambda fk, k: (1.0 / k ** 0.6) / (1 + (fk / cut) ** 4)


def strings_spectrum(fk, k):
    return formant_gain(fk, [(500, 250, 0.6), (1400, 500, 0.5), (3000, 900, 0.3)]) / k ** 0.9


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
    n = int(2.0 * SR)
    t = np.arange(n) / SR
    f = hz(m) * (1 + 0.1 * np.exp(-t / 0.03))
    ph = np.cumsum(2 * np.pi * f / SR)
    out = np.exp(-t / 0.9) * np.sin(ph) + 0.5 * np.exp(-t / 0.5) * np.sin(1.5 * ph) \
        + 0.3 * np.exp(-t / 0.35) * np.sin(1.99 * ph)
    k = int(0.025 * SR)
    out[:k] += rng.standard_normal(k) * np.exp(-np.arange(k) / (0.005 * SR)) * 0.8
    return out * vel


def bass_drum(vel):
    n = int(1.5 * SR)
    t = np.arange(n) / SR
    f = 45 * (1 + 1.2 * np.exp(-t / 0.04))
    return np.exp(-t / 0.5) * np.sin(np.cumsum(2 * np.pi * f / SR)) * vel


def tam_tam(dur=4.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for f0 in rng.uniform(60, 900, 40):
        out += np.sin(2 * np.pi * f0 * t + rng.uniform(0, 6.3)) / (1 + f0 / 200)
    swell = np.minimum(1, t / 0.25)
    out = out * swell * np.exp(-t / 1.8) + shaped(rng.standard_normal(n), lambda f: (f > 300) * np.exp(-f / 5000)) * np.exp(-t / 0.6) * 0.15
    return out / np.abs(out).max()


def crash(dur=3.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = shaped(rng.standard_normal(n), lambda f: np.clip((f - 2500) / 4000, 0, 1) ** 0.7)
    return x * np.exp(-t / 1.3) / np.abs(x).max()


def hall(x, secs=2.0, tau=0.45):
    L = int(secs * SR)
    tt = np.arange(L) / SR
    ir = rng.standard_normal(L) * np.exp(-tt / tau) * (tt > 0.025)
    ir = np.convolve(ir, np.ones(8) / 8, 'same')
    ir /= np.sqrt((ir ** 2).sum())
    n = len(x) + L
    wet = np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[:len(x)]
    return x * 0.9 + wet * 0.18  # kept fairly dry, so it hits as directly as the Deck


def place(buf, s, t, gain=1.0):
    i = int(t * SR)
    s = s[:max(0, len(buf) - i)]
    buf[i:i + len(s)] += s * gain


def hark():
    reseed(5)
    L, R = np.zeros(HN), np.zeros(HN)
    env = hits_env()
    soft = hits_env(attack=0.05, dip=0.5)

    def mix(pair, g):
        L[:] += pair[0] * g
        R[:] += pair[1] * g

    # brass: trumpets on the tune, horns in the middle, trombones and tuba underneath
    mix(section(MEL, 5, lambda fk, k: brass_spectrum(env * 1.2)(fk, k), 12, 5.5, 5, env, 0.2), 0.27)
    mix(section([nm[:-1] + str(int(nm[-1]) - 1) for nm in MEL], 2, brass_spectrum(env), 8, 5.0, 5, env, 0.1), 0.12)
    mix(section(ALTO, 4, brass_spectrum(env * 0.8), 8, 5.0, 6, env, -0.3), 0.13)
    mix(section(TENOR, 3, brass_spectrum(env * 0.8), 6, 5.0, 6, env, -0.4), 0.12)
    mix(section(BASS, 4, brass_spectrum(env), 0, 5.0, 5, env, 0.35), 0.21)
    mix(section(LOW, 3, brass_spectrum(env * 0.8), 0, 5.0, 4, env, 0.0), 0.2)
    # strings: violins up high, sawing away, cellos and basses on the bottom
    mix(section([nm[:-1] + str(int(nm[-1]) + 1) for nm in MEL], 8, strings_spectrum, 25, 6.0, 8, soft, -0.35), 0.09)
    mix(section(MEL, 6, strings_spectrum, 22, 6.0, 8, soft, -0.2), 0.08)
    mix(section(LOW, 4, strings_spectrum, 15, 5.5, 6, soft, 0.3), 0.1)
    # choir on 'ah', with operatic vibrato
    for names, forms, count, g, pan in ((MEL, FEMALE, 5, 0.1, 0.3), (ALTO, FEMALE, 4, 0.07, -0.2),
                                        (TENOR, MALE, 4, 0.07, 0.15), (BASS, MALE, 4, 0.08, -0.35)):
        mix(section(names, count, lambda fk, k, fo=forms: formant_gain(fk, fo) / k, 60, 6.0, 12, soft, pan), g)
    # organ pedal and chords
    org = np.zeros(HN)
    for nm in ('F1', 'F2', 'C3', 'F3', 'A3', 'C4'):
        f0 = hz(midi(nm))
        for r, a in ((1, 1), (2, 0.5), (4, 0.2)):
            org += a * np.sin(2 * np.pi * f0 * r * HT)
    org *= 0.02 * np.minimum(1, HT / 0.05) * np.clip((CUT - HT) / 0.01, 0, 1)
    L += org
    R += org
    # piano hammering the tune in octaves
    for i, (nm, st) in enumerate(zip(MEL, STARTS)):
        d = (BEATS[i] or 2) * HB
        for sh in (0, -12, -24):
            s = piano_note(midi(nm) + sh, 1.0, d) * 0.3  # our piano, up front
            place(L, s, st, 0.9)
            place(R, s, st, 1.1)
    # percussion: a timpani and bass-drum blow on every syllable, cymbals and bells on the big ones
    for i, st in enumerate(STARTS):
        big = i in (0, 2, 6)
        tp = timp(midi('F2') if HARM[i] == 'F' else midi('C2'), 0.7 if big else 0.5)
        tp += timp(midi('C2') if HARM[i] == 'F' else midi('G1'), 0.35)  # a second pair of timpani
        bd = bass_drum(0.9 if big else 0.55)
        for buf in (L, R):
            place(buf, tp, st)
            place(buf, bd, st)
        bl = bell(midi(['F5', 'C6', 'A5', 'F5', 'C6', 'A5', 'F6'][i])) * 0.05
        place(L, bl, st, 1.2 if i % 2 else 0.8)
        place(R, bl, st, 0.8 if i % 2 else 1.2)
        if big or i == 5:
            c = crash() * (0.35 if i < 6 else 0.45)
            place(L, c, st)
            place(R, c, st + 0.004)
    gong = tam_tam() * 0.5  # a great gong under SING
    place(L, gong, STARTS[-1])
    place(R, gong, STARTS[-1] + 0.006)
    rt = STARTS[-1] + 0.1  # a thundering timpani roll under the final note
    while rt < CUT:
        tp = timp(midi('F2'), 0.1 + 0.3 * (rt - STARTS[-1]) / (CUT - STARTS[-1]))
        place(L, tp, rt)
        place(R, tp, rt + 0.01)
        rt += 0.05
    # the diva, above everything, leaping to a top F on SING
    lm = pitch_curve(DIVA, 110, 6.3, 0, glide=0.05)
    u = np.clip((HT - CUT) / (HARK_END - DENUDE), 0, 1)
    lm = lm - 40 * u ** 1.6  # after the orchestra is stripped away, she slides down into nothing
    diva = additive(440 * 2 ** ((lm - 69) / 12), lambda fk, k: formant_gain(fk, FEMALE) / k)
    diva = diva / np.sqrt((diva ** 2).mean()) * soft * 0.1
    before = np.clip((CUT - HT) / 0.006, 0, 1)
    L += diva * before * 0.9
    R += diva * before * 1.1
    L, R = hall(L), hall(R)
    L *= before
    R *= before
    alone = diva * (1 - before) * 1.4
    alone *= np.clip((HARK_END - HARK_START - HT) / 0.03, 0, 1)
    end = int((HARK_END - HARK_START) * SR)
    return (L + alone)[:end], (R + alone)[:end]


def ambush():
    """Something horrible comes upon you: a whoosh, a hit, and a swarm of furious buzzing all around, cut dead."""
    reseed(8)
    n = int(AMBUSH * SR)
    t = np.arange(n) / SR
    hit = 0.12  # a split-second rush of air, then it is on you
    L, R = np.zeros(n), np.zeros(n)
    for _ in range(70):  # the swarm: dozens of wings, each droning on its own pitch, swooping past
        f0 = rng.uniform(110, 420)
        swoop = np.convolve(rng.standard_normal(n + 4000), np.ones(4000) / 4000, 'same')[:n] * 40
        f = f0 * (1 + 0.06 * swoop + 0.02 * np.sin(2 * np.pi * rng.uniform(3, 9) * t))
        ph = np.cumsum(2 * np.pi * f / SR) + rng.uniform(0, 6.3)
        wing = np.tanh(6 * np.sin(ph)) * (0.6 + 0.4 * np.sin(2 * np.pi * rng.uniform(5, 20) * t + rng.uniform(0, 6.3)))
        pan = np.clip(rng.uniform(-1, 1) + 0.6 * np.sin(2 * np.pi * rng.uniform(0.5, 2) * t), -1, 1)
        g = rng.uniform(0.4, 1.0)
        L += wing * g * (0.5 - pan / 2)
        R += wing * g * (0.5 + pan / 2)
    hum = np.tanh(4 * np.sin(np.cumsum(2 * np.pi * (58 + 3 * np.sin(2 * np.pi * 0.7 * t)) / SR)))  # a dirty electric drone
    env = np.clip((t - hit) / 0.02, 0, 1) * (0.85 + 0.15 * np.clip((t - hit) / (AMBUSH - hit), 0, 1))
    whoosh = shaped(rng.standard_normal(n), lambda f: np.exp(-((f - 1800) / 1500) ** 2)) * np.clip(t / hit, 0, 1) ** 3 * (t < hit)
    whoosh /= np.abs(whoosh).max()
    boom = np.sin(np.cumsum(2 * np.pi * (40 + 120 * np.exp(-np.clip(t - hit, 0, None) / 0.03)) / SR)) \
        * np.exp(-np.clip(t - hit, 0, None) / 0.3) * (t >= hit)
    out = []
    for ch in (L, R):
        ch = shaped(ch, lambda f: np.clip((f - 90) / 60, 0, 1))
        ch = ch / np.abs(ch).max() * env + hum * env * 0.35 + whoosh * 0.6 + boom * 0.9
        ch = np.tanh(ch * 2.5) / np.tanh(2.5)
        ch[-int(0.004 * SR):] *= np.linspace(1, 0, int(0.004 * SR))
        out.append(ch * 0.65)
    return out


def swoop(length=0.28):
    """The blade sweeping down: a rush of air that climbs and tightens into the moment of impact."""
    reseed(7)
    n = int(length * SR)
    t = np.arange(n) / SR
    u = t / length
    noise = rng.standard_normal(n)
    bands = [shaped(noise, lambda f, c=c: np.exp(-((f - c) / (0.5 * c)) ** 2)) for c in (350, 900, 2200)]
    bands = [b / np.abs(b).max() for b in bands]
    x = bands[0] * np.clip(1 - 2 * u, 0, 1) + bands[1] * (1 - np.abs(2 * u - 1)) + bands[2] * np.clip(2 * u - 1, 0, 1)
    return x * u ** 2.5


# ---------------------------------------------------------------------------
# Mastering
# ---------------------------------------------------------------------------
def widen(L, R, amount=0.6):
    """Spread things around the listener on headphones; keep the deep bass in the middle, where it hits hardest."""
    M, S = (L + R) / 2, (L - R) / 2
    S = shaped(S, lambda f: np.clip((f - 120) / 180, 0, 1) * (1 + amount * np.clip((f - 300) / 300, 0, 1)))
    return M + S, M - S


def phone_bass(L, R, mix=0.6):
    """Let a phone speaker 'hear' the deep bass: add the bass's higher echoes (harmonics), which a small speaker
    can play and the ear fills back in as the missing low note."""
    M = (L + R) / 2
    low = shaped(M, lambda f: 1 / (1 + (f / 110) ** 4))
    pk = np.abs(low).max() + 1e-9
    h = np.abs(low / pk) + 0.5 * np.tanh(3 * low / pk)  # even and odd harmonics
    h = shaped(h, lambda f: np.clip((f - 110) / 60, 0, 1) / (1 + (f / 450) ** 4))
    h *= np.sqrt((low ** 2).mean()) / (np.sqrt((h ** 2).mean()) + 1e-12) * mix
    return L + h, R + h


def loudness(st):
    """Integrated loudness in LUFS, measured the way TikTok, Instagram and YouTube measure it."""
    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, 'm.wav')
        write_wav(wav, st * 0.25)
        err = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-i', wav, '-af', 'ebur128',
                              '-f', 'null', '-'], capture_output=True, text=True).stderr
    line = [l for l in err.split('Summary:')[1].splitlines() if l.strip().startswith('I:')][0]
    return float(line.split()[1]) + 20 * np.log10(4)


def true_peak_limit(st, ceiling_db=-1.5):
    """Hold every peak, including the ones hiding between samples, under the ceiling, easing the volume down
    smoothly around each one."""
    thr = 10 ** (ceiling_db / 20)
    n = len(st)
    up = 4
    peak = np.zeros(n)
    for c in range(2):
        X = np.fft.rfft(st[:, c])
        Y = np.zeros(n * up // 2 + 1, complex)
        Y[:len(X)] = X
        y = np.fft.irfft(Y, n * up) * up
        peak = np.maximum(peak, np.abs(y[:n * up]).reshape(n, up).max(1))
    need = np.minimum(1, thr / np.maximum(peak, 1e-12))
    g = need.copy()
    s = 1
    while s < int(0.004 * SR):  # spread each dip 4 ms either side (a look-ahead)
        g = np.minimum(g, np.minimum(np.roll(g, s), np.roll(g, -s)))
        s *= 2
    k = int(0.002 * SR)
    c = np.cumsum(np.concatenate([[0], g]))
    sm = (c[k:] - c[:-k]) / k
    g = np.minimum(g, np.concatenate([np.full(k // 2, sm[0]), sm, np.full(n - len(sm) - k // 2, sm[-1])]))
    return st * g[:, None]


def write_wav(path, st):
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(st, -1, 1) * 32767).astype(np.int16).tobytes())


TARGET_LUFS = -14.0  # the level the big video apps play everything at


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
    # level the Hark to match the Deck's climax: trim the sub-rumble, squash the drum peaks so the body of
    # the sound comes forward, then match its loudness to the last few seconds of the Deck
    hl, hr = (shaped(x, lambda f: np.clip((f - 35) / 45, 0, 1)) for x in (hl, hr))
    hpk = max(np.abs(hl).max(), np.abs(hr).max())
    hl, hr = (np.tanh(x / hpk * 3.0) for x in (hl, hr))
    rms = lambda a: np.sqrt((a ** 2).mean())
    ref = rms(L[int((DECK_END - 4) * SR):int(DECK_END * SR)])
    g = ref / rms(hl[:int((CUT - 0.1) * SR)])
    place(L, hl * g, HARK_START)
    place(R, hr * g, HARK_START)

    # a gentle limiter so the loud parts are loud without crackling
    st = np.stack([L, R], 1)
    st = np.tanh(st * 1.6) / np.tanh(1.6) * 0.95
    for a, b in ((MUSIC_CUT - SHOCK_GAP, PAUSE_AT + PAUSE), (GASP_END, HARK_START), (HARK_END, TOTAL)):
        st[int(a * SR):int(b * SR)] = 0  # true silence
    w = swoop()  # the axe sweeps down...
    i = int(CHOP_AT * SR) - len(w)
    st[i:i + len(w), 0] += w * 0.45
    st[i:i + len(w), 1] += w * 0.45
    c = chop()  # ...and bites  # the knife comes down the instant the music dies: a jump-scare hit
    c = np.tanh(c / np.abs(c).max() * 2.2) / np.tanh(2.2) * 0.99  # loud and heavy, with the crack still on top
    i = int(CHOP_AT * SR)
    st[i:i + len(c), 0] += c * 0.97
    st[i:i + len(c), 1] += c
    for at in (AMBUSH1_AT,):  # ...then it is upon them
        al, ar = ambush()
        i = int(at * SR)
        st[i:i + len(al), 0] = al[:n - i]
        st[i:i + len(ar), 1] = ar[:n - i]
    # the music and effects: spread wider, bass made audible on phone speakers
    L, R = widen(st[:, 0], st[:, 1])
    L, R = phone_bass(L, R)
    st = np.stack([L, R], 1)
    # the voices, cleaned and placed
    v = dialogue()
    i = int(DIALOGUE_AT * SR)
    st[i:i + len(v), 0] += v
    st[i:i + len(v), 1] += v
    air = snow_air(len(v) / SR + 0.7)
    i = int((DIALOGUE_AT - 0.35) * SR)
    st[i:i + len(air), 0] += air
    st[i:i + len(air), 1] += air[::-1]  # a slightly different hush in each ear
    v = breathing()  # someone breathing in the dark...
    i = int(BREATH_AT * SR)
    st[i:i + len(v), 0] += v
    st[i:i + len(v), 1] += v
    # master to the video apps' standard loudness, with every peak held safely under -1.5 dB
    for _ in range(3):
        st *= 10 ** ((TARGET_LUFS - loudness(st)) / 20)
        st = true_peak_limit(st)
    print(f'loudness {loudness(st):.1f} LUFS')
    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, 'score.wav')
        write_wav(wav, st)
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-i', wav,
                        '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', out], check=True)
    print(f'{out}: {os.path.getsize(out) / 1e6:.1f} MB')


if __name__ == '__main__':
    main()
