#!/usr/bin/env python3
"""Hope Again: the timeline, the sound and the render.

Pictures come from burnham.py. Sound: Sam's recordings (audio/burnham-line.m4a, audio/king-shouts.m4a),
with a hall echo; applause, sword clatter and the war drums and horn are made here from scratch.

Usage:
    python3 burnham_film.py animatic OUT.mp4     half size (540 x 960), quick, to check timing
    python3 burnham_film.py final OUT.mp4        full size (1080 x 1920)
    python3 burnham_film.py sound OUT.wav        the soundtrack only
"""
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image

import burnham as B

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 12
SR = 48000
SHOUT = 'THE KING IN THE NORTH!'

# Where things are in Sam's recordings (seconds, measured from the files)
LINE_FILE = os.path.join(HERE, 'audio', 'burnham-line.m4a')
SHOUT_FILE = os.path.join(HERE, 'audio', 'king-shouts.m4a')
SHOUTS = {  # recorded order -> who says it (the highest voice is the young woman)
    'elder': (1.17, 3.05), 'young': (4.89, 6.35), 'miliband': (7.84, 9.91), 'sikh': (11.28, 13.54)}
CAPTIONS = [  # the speech, split at his own pauses (seconds from the start of the film)
    (0.81, 6.10, "The British Right talk about 'taking back control'."),
    (6.98, 8.90, "Never let them forget,"),
    (9.25, 14.0, "they are the ones that gave it away in the first place."),
]

# The shots: (name, length in seconds). The first shot's length is set by the speech.
SHOTS = [('stage', 14.2), ('hall', 3.0), ('frontrow', 2.5), ('elder', 2.3), ('sikh', 2.6), ('young', 1.9),
         ('miliband', 3.2), ('king', 4.0), ('swords_back', 2.5), ('swords_front', 3.0), ('closeup', 4.0)]
SHOUT_AT = {'elder': 0.2, 'sikh': 0.2, 'young': 0.2, 'miliband': 1.0}  # when each shout starts in its shot
STARTS = np.cumsum([0] + [d for _, d in SHOTS])
DUR = float(STARTS[-1])
CHANT_AT = [STARTS[8] + 0.2, STARTS[9] + 0.5]  # the hall chants twice


def shout_len(who):
    a, b = SHOUTS[who]
    return b - a


def load(path):
    """Any sound file -> mono floats at 48 kHz."""
    import imageio_ffmpeg
    raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(SR),
                          '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def level_track():
    """How loud his voice is at each frame (0-1), to move his mouth."""
    a = load(LINE_FILE)
    n = int(14.2 * FPS)
    lv = np.array([np.sqrt(np.mean(a[int(i / FPS * SR):int((i + 1) / FPS * SR)] ** 2) + 1e-12) for i in range(n)])
    return np.clip(lv / np.percentile(lv, 97), 0, 1)


LEVELS = None


def mouth_for(i):
    global LEVELS
    if LEVELS is None:
        LEVELS = level_track()
    v = LEVELS[i] if i < len(LEVELS) else 0
    if v < 0.12:
        return 'line'
    if v < 0.3:
        return 'small'
    return ['mid', 'open'][i % 2] if v > 0.55 else ['small', 'mid'][i % 2]


def frame_image(i):
    t = i / FPS
    k = int(np.searchsorted(STARTS, t, side='right') - 1)
    k = min(k, len(SHOTS) - 1)
    name, dur = SHOTS[k]
    u = t - STARTS[k]
    blink = (t % 3.7) < 0.12
    if name == 'stage':
        img = B.shot_stage(u, with_title=False, cap=None, mouth=mouth_for(i), push=u / dur, blink=blink)
        for a, b, text in CAPTIONS:
            if a <= u < b:
                B.caption(img, text)
        if u < 4.0:
            B.title(img, alpha=1.0 if u < 3.0 else 1.0 - (u - 3.0))
    elif name == 'hall':
        img = B.shot_hall(u)
    elif name == 'frontrow':
        img = B.shot_front_row(u)
    elif name in ('elder', 'sikh', 'young'):
        a = SHOUT_AT[name]
        img = B.shot_knight(u, ['elder', 'sikh', 'young'].index(name), window=(a - 0.05, a + shout_len(name)))
    elif name == 'miliband':
        a = SHOUT_AT[name]
        img = B.shot_miliband(u, window=(a - 0.05, a + shout_len(name) + 0.2))
    elif name == 'king':
        img = B.shot_king(u, blink=blink)
    elif name in ('swords_back', 'swords_front'):
        chanting = any(c - 0.05 <= t <= c + 2.3 for c in CHANT_AT)
        img = B.shot_hall(u, furs=True, chant=chanting) if name == 'swords_back' else B.shot_front_swords(u, chant=chanting)
    else:
        img = B.shot_king(u, zoom=u / dur)
    return img


def render_frame(args):
    i, size = args
    img = frame_image(i).convert('RGB').resize(size, Image.LANCZOS)
    return np.asarray(img).tobytes()


# ------------------------------------------------------------------------------------------------ sound

rng = np.random.default_rng(1)


def place(mix, snd, at, gain=1.0):
    s = int(at * SR)
    if s >= len(mix):
        return
    e = min(len(mix), s + len(snd))
    mix[s:e] += snd[:e - s] * gain


def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    from scipy.signal import lfilter
    return lfilter([1 - a], [1, -a], x)


def bandnoise(n, lo, hi):
    X = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    y = np.fft.irfft(X, n)
    return y / (np.abs(y).max() + 1e-9)


def reverb(x, secs=1.8, wet=0.3, pre=0.02):
    """A big hall: the dry sound plus a long, dark, decaying tail."""
    n = int(secs * SR)
    t = np.arange(n) / SR
    ir = rng.standard_normal(n) * np.exp(-6.9 * t / secs)
    ir = np.convolve(ir, np.ones(24) / 24, 'same')  # darker
    ir[:int(pre * SR)] = 0
    ir /= np.sqrt(np.sum(ir ** 2))
    L = len(x) + n
    y = np.fft.irfft(np.fft.rfft(x, L) * np.fft.rfft(ir, L), L)[:len(x) + n]
    out = np.zeros(len(x) + n)
    out[:len(x)] = x
    return out * (1 - wet) + y * wet * 2.2


def clap():
    n = int(0.03 * SR)
    b = bandnoise(n * 4, 900, 3200)[:n]
    env = np.exp(-np.arange(n) / (0.006 * SR))
    return b * env


def applause(dur, density):
    """density(t) -> how many people are clapping at time t (each about 4.5 claps a second)."""
    n = int(dur * SR)
    out = np.zeros(n + SR)
    bank = [clap() for _ in range(24)]
    t = 0.0
    step = 0.004
    while t < dur:
        k = density(t) * 4.5 * step
        for _ in range(rng.poisson(k)):
            c = bank[rng.integers(len(bank))] * rng.uniform(0.3, 1.0)
            place(out, c, t + rng.uniform(0, step))
        t += step
    return out[:n]


def murmur(dur, lo=150, hi=1800):
    y = bandnoise(int(dur * SR), lo, hi)
    wob = 0.75 + 0.25 * np.sin(np.arange(len(y)) / SR * 2 * np.pi * 0.7 + 1.0)
    return y * wob


def clink():
    n = int(0.5 * SR)
    t = np.arange(n) / SR
    fs = np.array([2100, 3380, 5270, 7900]) * rng.uniform(0.9, 1.1)
    y = sum(np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * np.exp(-t * (6 + 3 * j)) / (j + 1) for j, f in enumerate(fs))
    y += bandnoise(n, 2000, 9000) * np.exp(-t * 60) * 0.6
    return y * 0.4


def drum(pitch=58):
    n = int(1.2 * SR)
    t = np.arange(n) / SR
    f = pitch + (pitch * 1.3) * np.exp(-t * 30)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    y += bandnoise(n, 60, 900) * np.exp(-t * 25) * 0.5
    return y


def horn(dur, notes=(73.4, 110.0), swell=2.5):
    """A low brass drone (a root and its fifth) that swells in: stirring, but our own."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for j, f0 in enumerate(notes):
        f = f0 * (1 + 0.004 * np.sin(2 * np.pi * 5 * t + j))
        ph = 2 * np.pi * np.cumsum(f) / SR
        saw = sum(np.sin(k * ph) / k for k in range(1, 14))
        y += saw * (0.7 if j else 1.0)
    y = onepole_lp(onepole_lp(y, 900), 1400)
    env = np.clip(t / swell, 0, 1) ** 1.5
    return y * env / (np.abs(y).max() + 1e-9)


def pitch_shift(x, semis):
    """Speed a sound up or down (shifting its pitch) - enough to turn four voices into a crowd."""
    r = 2 ** (semis / 12)
    idx = np.arange(0, len(x) - 1, r)
    return np.interp(idx, np.arange(len(x)), x)


def normal(x, peak=1.0):
    return x / (np.abs(x).max() + 1e-9) * peak


def soundtrack():
    n = int((DUR + 0.5) * SR)
    mix = np.zeros(n + 4 * SR)
    # his speech, with the hall's echo, from the first frame
    line = normal(load(LINE_FILE)[:int(14.2 * SR)], 0.9)
    place(mix, reverb(line, 1.6, 0.22), 0.0, 1.0)
    # a hushed hall under the speech
    place(mix, murmur(14.2), 0.0, 0.015)
    # the ovation: one person, then a few, then everyone (shot 2), the front row (shot 3), clapping on under
    # the knights, fading as the king turns
    t_ov = STARTS[1]
    w1, w2, w3 = [t_ov + w for w in B.WAVES_HALL]

    def dens(t):
        T = t_ov + t
        d = 1.0 if T > w1 else 0
        d += 12 * np.clip((T - w2) / 0.5, 0, 1) + 180 * np.clip((T - w3) / 0.8, 0, 1)
        if T > STARTS[7]:  # the king soaks it up: still applauding, a little softer
            d *= 0.7
        return d
    ap_dur = STARTS[8] - t_ov
    place(mix, reverb(normal(applause(ap_dur, dens)), 1.4, 0.25), t_ov, 1.0)
    rise = np.clip((np.arange(int(ap_dur * SR)) / SR - (w3 - t_ov)) / 1.0, 0, 1)
    place(mix, reverb(murmur(ap_dur, 250, 2500) * rise, 1.4, 0.3), t_ov, 0.12)
    # the shouts
    shouts = load(SHOUT_FILE)
    for who, shot in (('elder', 3), ('sikh', 4), ('young', 5), ('miliband', 6)):
        a, b = SHOUTS[who]
        s = normal(shouts[int((a - 0.05) * SR):int((b + 0.1) * SR)], 0.95)
        place(mix, reverb(s, 1.6, 0.25), STARTS[shot] + SHOUT_AT[who] - 0.05, 1.0)
    # the chant: all four shouts, doubled and redoubled into a hall of voices
    for c in CHANT_AT:
        crowd = np.zeros(int(3.5 * SR))
        for rep in range(4):
            for who in SHOUTS:
                a, b = SHOUTS[who]
                s = normal(shouts[int((a - 0.03) * SR):int((b + 0.05) * SR)])
                s = pitch_shift(s, rng.uniform(-2.5, 1.5) - (3 if rep % 2 else 0))
                place(crowd, s, rng.uniform(0, 0.12), rng.uniform(0.4, 0.8))
        place(mix, reverb(normal(crowd), 2.0, 0.45), c, 0.8)
    # swords: clatter through both sword shots and into the close-up, fading
    for k in range(40):
        t = STARTS[8] + rng.uniform(0, STARTS[10] - STARTS[8] + 1.5)
        place(mix, clink(), t, rng.uniform(0.05, 0.16))
    place(mix, reverb(murmur(STARTS[10] - STARTS[8] + 2.0, 200, 2200), 1.5, 0.3), STARTS[8], 0.08)
    place(mix, reverb(normal(applause(STARTS[10] - STARTS[8], lambda t: 90)), 1.2, 0.25), STARTS[8], 0.12)
    # the close-up: war drums and a swelling horn, the hall falling away; hard cut at the end
    t0 = STARTS[10]
    place(mix, horn(DUR - t0 + 0.4, swell=3.2), t0 - 0.3, 0.22)
    for j, beat in enumerate([0.0, 0.85, 1.7, 2.1, 2.55, 3.4, 3.8]):
        place(mix, drum(56 if j % 3 else 50), t0 + beat, 0.35 + 0.08 * j)
    mix = mix[:int(DUR * SR)]
    # soften the very last hundredth of a second so the cut does not click
    mix[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
    return normal(mix, 0.89)


def write_wav(path, x):
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def render(out, size, crf):
    import imageio_ffmpeg
    from multiprocessing import Pool
    wav = out + '.wav'
    write_wav(wav, soundtrack())
    n = int(round(DUR * FPS))
    p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{size[0]}x{size[1]}', '-r', str(FPS), '-i', '-', '-i', wav, '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-crf', str(crf), '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                          '-b:a', '128k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for f, fr in enumerate(pool.imap(render_frame, [(i, size) for i in range(n)], chunksize=2)):
            p.stdin.write(fr)
            if f % 48 == 0:
                print(f'frame {f}/{n}', flush=True)
    p.stdin.close()
    p.wait()
    os.remove(wav)
    print(f'done: {out} ({os.path.getsize(out) / 1e6:.1f} MB)', flush=True)


def main():
    mode, out = sys.argv[1], sys.argv[2]
    if mode == 'animatic':
        B.SS = 1
        render(out, (540, 960), 26)
    elif mode == 'final':
        render(out, (1080, 1920), 20)
    elif mode == 'sound':
        write_wav(out, soundtrack())


if __name__ == '__main__':
    main()
