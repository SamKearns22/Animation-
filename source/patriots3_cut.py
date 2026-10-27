#!/usr/bin/env python3
"""Cut Sam's one-take test recording (audio/patriots3-test-all.m4a) into the film's lines (placeholders).
Each cut is levelled to -25 LUFS, long pauses inside it shortened to 0.25 s, and sped up (never over 1.5x) to fit its
slot in the film's timing. Real recordings replace these files; delete this when they do."""
import subprocess, wave
import numpy as np, imageio_ffmpeg
import voices as V, mossad_audio as MA

SR = V.SR
# name: (from s, to s in the test take, slot s the line must fit in the film)
CUTS = {'patriot-1': (2.35, 3.85, 1.6), 'patriot-2': (6.1, 12.5, 5.0), 'loader-1': (13.4, 14.7, 1.3),
        'patriot-3': (15.8, 21.4, 4.0), 'loader-2': (22.0, 24.4, 1.7), 'heil': (24.7, 25.8, 1.0),
        'patriot-4': (26.0, 32.0, 4.6), 'patriot-5': (33.0, 41.9, 6.0), 'patriot-6': (42.95, 45.6, 2.0)}
FF = imageio_ffmpeg.get_ffmpeg_exe()


def tighten(x, gap=0.25):
    """Shorten every silence longer than `gap` to `gap` (keeps 30 ms of fade each side)."""
    ph = V.phrases(x)
    out = [x[:int(ph[0][0] * SR)][-int(0.05 * SR):]] if ph else []
    for i, (s, e) in enumerate(ph):
        out.append(x[int(s * SR):int(e * SR)])
        if i + 1 < len(ph):
            out.append(np.zeros(int(min(gap, ph[i + 1][0] - e) * SR)))
    return np.concatenate(out + [np.zeros(int(0.05 * SR))])


def main():
    a = V.load('audio/patriots3-test-all.m4a')
    for k, (s, e, slot) in CUTS.items():
        x = tighten(a[int(s * SR):int(e * SR)])
        x = x * 10 ** ((-25.2 - MA.lufs(x)) / 20)
        f = int(0.03 * SR)
        x[:f] *= np.linspace(0, 1, f)
        x[-f:] *= np.linspace(1, 0, f)
        x *= min(1.0, 0.95 / np.abs(x).max())
        rate = min(1.5, max(1.0, len(x) / SR / slot))
        w = f'/tmp/{k}.wav'
        with wave.open(w, 'wb') as o:
            o.setnchannels(1), o.setsampwidth(2), o.setframerate(SR)
            o.writeframes((x * 32767).astype(np.int16).tobytes())
        subprocess.run([FF, '-y', '-loglevel', 'error', '-i', w, '-filter:a', f'atempo={rate:.3f}', '-c:a', 'aac',
                        '-b:a', '96k', f'audio/patriots3-{k}.m4a'], check=True)
        print(f'{k}: {len(x) / SR:.2f} s -> {len(x) / SR / rate:.2f} s (x{rate:.2f}, slot {slot})')


if __name__ == '__main__':
    main()
