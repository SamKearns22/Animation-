#!/usr/bin/env python3
"""Hope Again: the timeline, the sound and the render.

Pictures come from burnham.py. Sound: Sam's recordings (audio/burnham-line.m4a, audio/king-shouts.m4a),
with a hall echo; applause, sword clatter and the war drums and horn are made here from scratch.

Usage:
    python3 burnham_film.py animatic OUT.mp4     half size (540 x 960), quick, to check timing
    python3 burnham_film.py final OUT.mp4        full size (1080 x 1920)
    python3 burnham_film.py sound OUT.wav        the soundtrack only
"""
import math
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
SHOUT = 'KING OF THE NORTH!'

# Where things are in Sam's recordings (seconds, measured from the files)
LINE_FILE = os.path.join(HERE, 'audio', 'burnham-line.m4a')
SHOUT_FILE = os.path.join(HERE, 'audio', 'king-shouts.m4a')
SHOUTS = {  # recorded order -> who says it (the highest voice is the young woman)
    'elder': (1.17, 3.05), 'young': (4.89, 6.35), 'miliband': (7.84, 9.91), 'sikh': (11.28, 13.54)}
CAPTIONS = [  # the speech, split at his own pauses (seconds from the start of the film)
    (0.81, 6.10, "The British Right talk about 'taking back control'."),
    (6.98, 8.90, "Never let them forget,"),
    (9.25, 14.0, "they were the ones who gave it away in the first place."),
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


# ---------------------------------------------------------------------------------------------- gestures
# Arm positions in each person's own units (+x is to our right). Each entry: elbow, wrist, hand shape.
HIP_R = ((250, 230), (150, 420), 'fist')
ANDY = [  # (time in the shot, arms): accusing, sarcastic, confident
    (0.0, {'L': ((-160, 270), (-150, 470), 'fist'), 'R': ((160, 270), (150, 470), 'fist')}),
    (0.75, {'L': ((-343, 24), (-536, -28), 'point'), 'R': HIP_R}),                     # "The British Right"
    (2.75, {'L': ((-300, 200), (-470, 240), 'palm'), 'R': HIP_R}),                     # "talk about"
    (3.9, {'L': ((-320, -40), (-250, -230), 'quote'), 'R': ((320, -40), (250, -230), 'quote')}),  # air quotes
    (6.95, {'L': ((-310, 150), (-300, -50), 'point_up'), 'R': HIP_R}),                 # "Never let them forget"
    (9.2, {'L': ((-340, 110), (-535, 70), 'point'), 'R': HIP_R}),                      # "they were the ones..."
    (12.0, {'L': ((-335, 20), (-520, -60), 'point'), 'R': HIP_R}),
    (13.6, {'L': ((-280, 220), (-470, 260), 'palm'), 'R': ((280, 220), (470, 260), 'palm')}),  # arms open
]
ANDY_LOOK = [(0.0, 0.0), (0.75, -0.6), (3.9, 0.0), (6.95, -0.4), (9.2, -0.7), (13.6, 0.0)]

REST = {'L': ((-160, 270), (-150, 470), 'fist'), 'R': ((160, 270), (150, 470), 'fist')}
SALUTES = {  # each knight's own gesture of allegiance
    'elder': {'R': ((250, -120), (210, -320), 'sword', -1.45), 'L': ((-190, 250), (-40, 160), 'fist')},
    'sikh': {'R': ((330, 20), (320, -180), 'fist'), 'L': ((-250, 230), (-150, 420), 'fist')},
    'young': {'R': ((200, -150), (230, -350), 'sword', -1.62), 'L': ((-300, 40), (-300, -140), 'fist')},
    'miliband': {'R': ((230, -140), (260, -330), 'fist'), 'L': ((-190, 250), (-60, 170), 'fist')},
}


def lerp(a, b, u):
    return tuple(a[k] + (b[k] - a[k]) * u for k in range(len(a)))


def keyed(keys, t, blend=0.3):
    """Hold each pose until just before the next, then move smoothly into it."""
    i = max(j for j, (kt, _) in enumerate(keys) if kt <= t) if t >= keys[0][0] else 0
    cur = keys[i][1]
    if i + 1 < len(keys) and t > keys[i + 1][0] - blend:
        nxt = keys[i + 1][1]
        u = B.smooth((t - (keys[i + 1][0] - blend)) / blend)
        if not isinstance(cur, dict):
            return cur + (nxt - cur) * u
        out = {}
        for side in ('L', 'R'):
            a, b = cur[side], nxt[side]
            g = [lerp(a[0], b[0], u), lerp(a[1], b[1], u), a[2] if u < 0.5 else b[2]]
            if len(a) > 3 or len(b) > 3:
                ea = a[3] if len(a) > 3 else -1.57
                eb = b[3] if len(b) > 3 else -1.57
                g.append(ea + (eb - ea) * u)
            out[side] = tuple(g)
        return out
    return cur


def andy_arms(u):
    arms = keyed(ANDY, u, 0.28)
    if 6.95 <= u < 9.0:  # the raised finger wags
        el, wr, sh = arms['L'][:3]
        arms = dict(arms, L=(el, (wr[0] + 14 * math.sin(u * 10), wr[1]), sh))
    return arms


def salute(name, u, start):
    """At rest until the shout, then up into their salute, pumping while they shout."""
    arms = keyed([(0.0, REST), (start, SALUTES[name])], u, 0.3)
    if u > start:
        pump = -16 * abs(math.sin((u - start) * 5.5))
        el, wr = arms['R'][0], arms['R'][1]
        arms = dict(arms, R=(el, (wr[0], wr[1] + pump)) + tuple(arms['R'][2:]))
    return arms


def frame_image(i):
    t = i / FPS
    k = int(np.searchsorted(STARTS, t, side='right') - 1)
    k = min(k, len(SHOTS) - 1)
    name, dur = SHOTS[k]
    u = t - STARTS[k]
    blink = (t % 3.7) < 0.12
    if name == 'stage':
        img = B.shot_stage(u, with_title=False, cap=None, mouth=mouth_for(i), push=u / dur, blink=blink,
                           arms=andy_arms(u), look=keyed(ANDY_LOOK, u, 0.3))
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
        img = B.shot_knight(u, ['elder', 'sikh', 'young'].index(name), window=(a - 0.05, a + shout_len(name)),
                            arms=salute(name, u, a))
    elif name == 'miliband':
        a = SHOUT_AT[name]
        img = B.shot_miliband(u, window=(a - 0.05, a + shout_len(name) + 0.2), arms=salute(name, u, a))
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


def clink(low=False):
    """Steel on steel."""
    n = int(0.7 * SR)
    t = np.arange(n) / SR
    base = [620, 1130, 1790, 2470] if low else [2100, 3380, 5270, 7900]
    fs = np.array(base) * rng.uniform(0.9, 1.1)
    y = sum(np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * np.exp(-t * (5 + 3 * j)) / (j + 1) for j, f in enumerate(fs))
    y += bandnoise(n, 1500, 9000) * np.exp(-t * 60) * 0.7
    return y * 0.4


def drum(pitch=58):
    n = int(1.2 * SR)
    t = np.arange(n) / SR
    f = pitch + (pitch * 1.3) * np.exp(-t * 30)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    y += bandnoise(n, 60, 900) * np.exp(-t * 25) * 0.5
    return y


def resonate(x, f, q):
    from scipy.signal import iirpeak, lfilter
    b, a = iirpeak(f, q, fs=SR)
    return lfilter(b, a, x)


def battle_horn(dur, f0, scoop=True):
    """A war horn: a brassy note that scoops up to pitch and grows brighter as it swells."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    env = np.clip(t / 0.25, 0, 1) * np.clip((dur - t) / 0.3, 0, 1)
    f = f0 * (1 - (0.06 * np.exp(-t * 9) if scoop else 0)) * (1 + 0.005 * np.sin(2 * np.pi * 5.5 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    bright = 0.5 + 0.8 * env
    y = sum(np.sin(k * ph) * (1 / k) ** (1.6 - 0.9 * bright) for k in range(1, 18))
    y = resonate(y, 520, 1.2) + 0.6 * resonate(y, 1150, 1.5) + 0.3 * y
    y += bandnoise(n, 400, 3000) * 0.04
    return normal(np.tanh(1.8 * normal(y)) * env)


def hooves(dur, horses=30, approach=True):
    """A cavalry charge: many horses at the gallop, thudding into mud, coming closer."""
    n = int(dur * SR)
    out = np.zeros(n + SR)
    fall_n = int(0.12 * SR)
    ft = np.arange(fall_n) / SR
    for h in range(horses):
        stride = rng.uniform(0.40, 0.48)
        t = rng.uniform(0, stride)
        loud = rng.uniform(0.4, 1.0)
        while t < dur:
            for off in (0.0, 0.09, 0.2):
                f = rng.uniform(70, 110)
                thud = np.sin(2 * np.pi * f * ft) * np.exp(-ft * 38) + bandnoise(fall_n, 100, 700) * np.exp(-ft * 55) * 0.6
                thud += bandnoise(fall_n, 800, 3500) * np.exp(-ft * 120) * 0.25  # the mud
                g = loud * ((0.35 + 0.65 * (t / dur)) if approach else 1.0)
                place(out, thud, t + off, g)
            t += stride
    rumble = bandnoise(n, 25, 180) * np.linspace(0.3, 1.0, n)
    return normal(out[:n] + rumble * 0.6)


def arrows(n_arrows=40, spread=0.35):
    """A volley: each arrow a falling whistle, then the thunk of it landing."""
    L = int(2.0 * SR)
    out = np.zeros(L)
    for _ in range(n_arrows):
        d = rng.uniform(0.5, 0.8)
        m = int(d * SR)
        t = np.arange(m) / SR
        f = 3200 - 1600 * (t / d) + rng.uniform(-300, 300)
        carrier = np.sin(2 * np.pi * np.cumsum(f) / SR)
        noise = onepole_lp(rng.standard_normal(m), 500)
        env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
        w = normal(noise * carrier * env)
        start = rng.uniform(0, spread)
        place(out, w, start, rng.uniform(0.3, 0.8))
        k = int(0.05 * SR)
        tk = np.arange(k) / SR
        thunk = np.sin(2 * np.pi * rng.uniform(250, 420) * tk) * np.exp(-tk * 90) + bandnoise(k, 1000, 5000) * np.exp(-tk * 200) * 0.4
        place(out, thunk, start + d, rng.uniform(0.3, 0.7))
    return normal(out)


def yell(dur):
    """A man screaming in the fight: a strained voice through the formants of 'aah', rough at the edges."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    f0 = rng.uniform(170, 290)
    contour = f0 * (1 + 0.25 * np.sin(np.pi * np.clip(t / dur, 0, 1)) - 0.15 * (t / dur))
    contour *= 1 + 0.02 * np.sin(2 * np.pi * rng.uniform(5, 8) * t) + 0.01 * onepole_lp(rng.standard_normal(n), 30) * 10
    ph = 2 * np.pi * np.cumsum(contour) / SR
    src = sum(np.sin(k * ph) / k for k in range(1, 30)) + 0.25 * rng.standard_normal(n)
    v = rng.choice([(750, 1200, 2600), (650, 1080, 2500), (800, 1300, 2700), (550, 1700, 2600)])
    y = resonate(src, v[0], 3) + 0.7 * resonate(src, v[1], 4) + 0.35 * resonate(src, v[2], 5)
    env = np.clip(t / 0.06, 0, 1) * np.clip((dur - t) / 0.25, 0, 1)
    return normal(np.tanh(3 * normal(y)) * env)


def battle(dur):
    """The war beneath the close-up: horns, the charge, arrows, steel and men screaming in the mud."""
    n = int(dur * SR)
    bus = np.zeros(n + 3 * SR)
    place(bus, battle_horn(2.2, 146.8), 0.0, 0.55)
    place(bus, battle_horn(1.4, 220.0), 0.15, 0.3)
    place(bus, battle_horn(1.9, 196.0), 2.0, 0.5)
    place(bus, battle_horn(1.9, 293.7), 2.1, 0.3)
    place(bus, hooves(dur, 34), 0.0, 0.55)
    place(bus, arrows(45), 0.9, 0.35)
    for k in range(26):
        at = rng.uniform(0.2, dur - 0.3) * (0.5 + 0.5 * rng.random())
        place(bus, yell(rng.uniform(0.6, 1.4)), at, rng.uniform(0.12, 0.3))
    for k in range(18):
        place(bus, clink(low=rng.random() < 0.6), rng.uniform(0.3, dur), rng.uniform(0.25, 0.5))
    for j, beat in enumerate([0.0, 0.85, 1.7, 2.1, 2.55, 3.0, 3.4, 3.8]):
        place(bus, drum(56 if j % 3 else 50), beat, 0.5 + 0.06 * j)
    bus = reverb(bus[:n], 1.2, 0.2)[:n]
    return normal(bus)


def normal(x, peak=1.0):
    return x / (np.abs(x).max() + 1e-9) * peak


def soundtrack():
    """Voices exactly as recorded (only turned up or down); clapping; swords; the battle at the end."""
    n = int((DUR + 0.5) * SR)
    mix = np.zeros(n + 4 * SR)
    line = load(LINE_FILE)[:int(14.2 * SR)]
    voice_gain = 0.85 / np.abs(line).max()
    place(mix, line, 0.0, voice_gain)
    # the ovation: one person, then a few, then everyone; clapping on under the knights and the king
    t_ov = STARTS[1]
    w1, w2, w3 = [t_ov + w for w in B.WAVES_HALL]

    def dens(t):
        T = t_ov + t
        d = 1.0 if T > w1 else 0
        d += 12 * np.clip((T - w2) / 0.5, 0, 1) + 180 * np.clip((T - w3) / 0.8, 0, 1)
        if T > STARTS[7]:
            d *= 0.7
        return d
    ap_dur = STARTS[10] - t_ov
    place(mix, reverb(normal(applause(ap_dur, dens)), 1.2, 0.2)[:int(ap_dur * SR)], t_ov, 0.45)
    # the shouts, each exactly as recorded
    shouts = load(SHOUT_FILE)
    sg = 0.85 / np.abs(shouts).max()
    for who, shot in (('elder', 3), ('sikh', 4), ('young', 5), ('miliband', 6)):
        a, b = SHOUTS[who]
        place(mix, shouts[int((a - 0.05) * SR):int((b + 0.1) * SR)], STARTS[shot] + SHOUT_AT[who] - 0.05, sg)
    # the chant: all four recordings together, each doubled a moment later, unaltered
    for c in CHANT_AT:
        for who in SHOUTS:
            a, b = SHOUTS[who]
            s = shouts[int((a - 0.03) * SR):int((b + 0.05) * SR)]
            place(mix, s, c + rng.uniform(0, 0.08), sg * 0.55)
            place(mix, s, c + rng.uniform(0.15, 0.28), sg * 0.35)
    # swords through both sword shots
    for k in range(40):
        place(mix, clink(), STARTS[8] + rng.uniform(0, STARTS[10] - STARTS[8]), rng.uniform(0.08, 0.2))
    # the close-up: the battle, hard cut at the end
    place(mix, battle(DUR - STARTS[10]), STARTS[10], 0.8)
    mix = mix[:int(DUR * SR)]
    mix[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
    pk = np.abs(mix).max()
    return mix / max(1.0, pk / 0.95)


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
