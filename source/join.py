"""MAP: one ffmpeg join tool, always at 24 frames a second (R8 A8, Sam's Y, 27 Nov; rulebook S4 "ffmpeg joins always
at fps=24", checked by hand until now). A join at a lower rate than a piece drops that piece's frames (Ad-Vanced
Notice, 19 Oct: DLC joined at 12 halved its smoothness); at 24 nothing is lost (a 12 a second piece shows each
drawing twice, the same picture). Every piece is fitted to the first piece's size, its sound evened to 48 kHz (a
silent piece gets silence), then joined end to end.

  join(parts, out, crf=20, size=None)   -> out; size (w, h) defaults to the first piece's
  frames(path), rate(path)              counted frames; the frame rate as written
  python3 source/join.py OUT.mp4 A.mp4 B.mp4 ...
"""
import os
import re
import subprocess
import sys

import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 24


def _probe(path):
    return subprocess.run([FF, '-i', path], capture_output=True, text=True).stderr


def rate(path):
    m = re.search(r'(\d+(?:\.\d+)?) fps', _probe(path))
    return float(m.group(1)) if m else None


def size(path):
    m = re.search(r'Video:.*?, (\d{2,5})x(\d{2,5})', _probe(path))
    return (int(m.group(1)), int(m.group(2))) if m else None


def has_sound(path):
    return 'Audio:' in _probe(path)


def duration(path):
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', _probe(path))
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0.0


def frames(path):
    pr = FF.replace('ffmpeg', 'ffprobe')
    pr = pr if os.path.exists(pr) else 'ffprobe'
    out = subprocess.run([pr, '-v', 'error', '-select_streams', 'v', '-count_frames', '-show_entries',
                          'stream=nb_read_frames', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout
    if out.strip():
        return int(out.strip())
    o = subprocess.run([FF, '-i', path, '-map', '0:v', '-f', 'null', '-'], capture_output=True, text=True).stderr
    m = re.findall(r'frame=\s*(\d+)', o)
    return int(m[-1]) if m else 0


def join(parts, out, crf=20, size_=None, preset='slow'):
    """Join the pieces end to end at 24 a second (see MAP). Returns out."""
    w, h = size_ or size(parts[0])
    args, chains, pairs = [FF, '-y', '-loglevel', 'error'], [], ''
    n = len(parts)
    for i, p in enumerate(parts):
        args += ['-i', p]
    k = n
    for i, p in enumerate(parts):
        chains.append(f'[{i}:v]scale={w}:{h},setsar=1,fps={FPS},format=yuv420p[v{i}]')
        if has_sound(p):
            chains.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}]')
        else:
            args += ['-f', 'lavfi', '-t', f'{duration(p):.3f}', '-i', 'anullsrc=r=48000:cl=stereo']
            chains.append(f'[{k}:a]aresample=48000[a{i}]')
            k += 1
        pairs += f'[v{i}][a{i}]'
    chains.append(f'{pairs}concat=n={n}:v=1:a=1[v][s]')
    args += ['-filter_complex', ';'.join(chains), '-map', '[v]', '-map', '[s]', '-r', str(FPS), '-c:v', 'libx264',
             '-crf', str(crf), '-preset', preset, '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out]
    subprocess.run(args, check=True)
    return out


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    join(sys.argv[2:], sys.argv[1])
    print(f'{sys.argv[1]}: {frames(sys.argv[1])} frames at {rate(sys.argv[1]):g} a second')
