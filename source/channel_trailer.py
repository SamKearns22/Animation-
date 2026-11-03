#!/usr/bin/env python3
"""MAP: channel trailer story post (Sam, 3 Nov): nine best bits, cut on the beat of the DLC rock track (126 bpm,
four beats a moment, six for the last), "WELCOME, / NEW FOLLOWERS" in cranberry two-thirds down, no subtitles.
Moments come from the posted finals where they have no subtitles; Patriots 2, the D-Day beach (Patriots 3) and Mossad are re-drawn from their
own code with captions off (Mossad's blast carries on past the film's cut to black).
    python3 source/channel_trailer.py animations/channel-trailer-story.mp4"""
import os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np                          # noqa: E402
from PIL import Image                       # noqa: E402
import burnham as B                         # noqa: E402
from hook_text import FF                    # noqa: E402

A = os.path.join(HERE, '..', 'animations')
BEAT = 60 / 126.05
PHASE = 0.18                                # first downbeat in the track
# (source, start s, beats): a file in animations/, or 'patriots2' / 'mossad' drawn clean
CUTS = [('halo-no-no-vertical.mp4', 4.2, 4),           # roadsters heading for the Halo
        ('bayeux-season-pass-vertical.mp4', 5.1, 4),   # DLC ghost pistol
        ('patriots2', 26.4, 4),                        # the Patriot typing 'traitors'
        ('patriots3', 1.5, 4),                         # D-Day: the beach combat (Sam), drawn clean
        ('power-crime-action-vertical.mp4', 14.6, 4),  # thrown into the van
        ('prepper-minister-vertical.mp4', 56.5, 4),    # the showstopper
        ('netan-yahoo-vertical.mp4', 24.6, 4),         # Darth Maul attacks
        ('flying-whales-vertical.mp4', 10.8, 5),       # whales destroy the Jackdaw
        ('mossad', 28.9, 5)]                           # ends on the Mossad blast (Sam); before its second flare
LINES, CAP, TOP = ['WELCOME,', 'NEW FOLLOWERS'], 92, 1180   # two-thirds down (centre ~1280)
FPS = 24


def drawn(name, t0, dur, out):
    import figure
    mod = __import__(name)
    if name == 'mossad':
        mod.BLACK_AT = 99
    p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920',
                          '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', out],
                         stdin=subprocess.PIPE)
    with figure.allow('posted film, drawn as posted'):
        for i in range(int(round(dur * FPS))):
            B.SS = 2
            t = t0 + i / FPS
            im = (mod.picture(t) if name == 'patriots3' else mod.frame_image(t, captions=False, title=False)).convert('RGB')
            p.stdin.write(np.asarray(im.resize((1080, 1920), Image.LANCZOS)).tobytes())
    p.stdin.close()
    p.wait()


def overlay(path):
    B.SS = 1
    img = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    B.title_lines(img, LINES, cap=CAP, top=TOP)
    img.save(path)


if __name__ == '__main__':
    out = sys.argv[1]
    tmp = tempfile.mkdtemp()
    parts = []
    for k, (src, t0, beats) in enumerate(CUTS):
        dur = beats * BEAT
        seg = os.path.join(tmp, f'{k}.mp4')
        if src.endswith('.mp4'):
            subprocess.run([FF, '-v', 'error', '-y', '-ss', str(t0), '-i', os.path.join(A, src), '-t', f'{dur:.4f}',
                            '-an', '-vf', f'scale=1080:1920,fps={FPS}', '-c:v', 'libx264', '-crf', '16', seg], check=True)
        else:
            drawn(src, t0, dur, seg)
        parts.append(seg)
        print('cut', k, src, flush=True)
    lst = os.path.join(tmp, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    png = os.path.join(tmp, 'text.png')
    overlay(png)
    total = sum(b for _, _, b in CUTS) * BEAT
    subprocess.run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-i', png,
                    '-ss', str(PHASE), '-i', os.path.join(HERE, 'audio', 'bayeux-rock.mp3'),
                    '-filter_complex', f'[0:v][1:v]overlay=0:0,format=yuv420p[v];'
                    f'[2:a]atrim=0:{total:.3f},afade=t=out:st={total - 0.6:.3f}:d=0.6[a]',
                    '-map', '[v]', '-map', '[a]', '-t', f'{total:.3f}', '-c:v', 'libx264', '-crf', '22',
                    '-preset', 'slow', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)
    print('wrote', out, f'{total:.1f} s')
