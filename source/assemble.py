#!/usr/bin/env python3
"""Turn a shot's drawings into video: each drawing is held until the next one's time (so drawings on twos
fill two frames, drawings on ones fill one), at 24 frames a second.

    python3 assemble.py OUT.mp4 FPS DIR [DIR ...] [--black SECONDS] [--audio WAV]

Each DIR is a shot's sequence folder (draw_NNNN.png and log.json from shot.py sequence); the shots are
joined in order. --black adds that much black at the end (the cut to black); --audio lays a soundtrack
under the whole thing.
"""
import json
import os
import subprocess
import sys

import imageio_ffmpeg
import numpy as np
from PIL import Image


def shot_frames(d, fps, duration=None):
    log = json.load(open(os.path.join(d, 'log.json')))
    times = [e['t'] for e in log]
    if duration is None:
        duration = times[-1] + (times[-1] - times[-2] if len(times) > 1 else 1 / fps)
    n = int(round(duration * fps))
    out = []
    for f in range(n):
        k = max(i for i, t in enumerate(times) if t <= f / fps + 1e-6)
        out.append(os.path.join(d, f'draw_{k:04d}.png'))
    return out


def main(a):
    out, fps = a[0], int(a[1])
    black, audio, dirs = 0.0, None, []
    i = 2
    while i < len(a):
        if a[i] == '--black':
            black = float(a[i + 1]); i += 2
        elif a[i] == '--audio':
            audio = a[i + 1]; i += 2
        else:
            dirs.append(a[i]); i += 1
    frames = []
    for d in dirs:
        dur = None
        spec = os.path.join(d, 'duration.txt')
        if os.path.exists(spec):
            dur = float(open(spec).read())
        frames += shot_frames(d, fps, dur)
    W, H = Image.open(frames[0]).size
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
           '-s', f'{W}x{H}', '-r', str(fps), '-i', '-']
    if audio:
        cmd += ['-i', audio, '-c:a', 'aac', '-b:a', '192k']
    cmd += ['-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
            '-shortest' if audio else '-an', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    last = None
    for f in frames:
        if f != last:
            img = np.asarray(Image.open(f).convert('RGB')).tobytes()
            last = f
        p.stdin.write(img)
    blank = np.zeros((H, W, 3), np.uint8).tobytes()
    for _ in range(int(round(black * fps))):
        p.stdin.write(blank)
    p.stdin.close()
    p.wait()
    print(f'{out}: {(len(frames) + int(round(black * fps))) / fps:.2f} s, {os.path.getsize(out) / 1e6:.1f} MB')


if __name__ == '__main__':
    main(sys.argv[1:])
