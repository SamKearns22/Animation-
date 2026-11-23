#!/usr/bin/env python3
"""MAP: story post for Grand Theft Autism (Sam, 23 Nov): the 'delighted' last shot (her line "My safe food is
nitroglycerin", then the snap round to Lucia with the big grin), redrawn full size from the film's own drawing code
so there are NO subtitles (the posted final has them burned in), with the film's own sound for those seconds, and
Sam's Hook Text on a diagonal, on the whole time.
    python3 source/gta_delight_story.py animations/grand-theft-autism-story.mp4
  T0, T1 ...... the last shot on the film's clock (gta_film); its sound is the film's own mix (G.mix, Sam's recordings
                in sounds/grand-theft-autism) cut at the same seconds, so the lips stay in sync
  TEXT/TILT/Y . the Hook Text (hook_text.card, TikTok white boxes), tilted, in the sky above the car"""
import os
import subprocess
import sys
import tempfile
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ['ARM_FOLD_NAMED'] = '1'
os.environ['NAMED_FAULTS_FILE'] = '/tmp/gta_named_faults.txt'
import grand_theft_autism as G    # noqa: E402  (sets the film's render switches exactly as the final had them)
from hook_text import card, FF    # noqa: E402

T0, T1 = G.F.SHOTS[-1][1], G.LENGTH      # the whole last shot: her line, the snap to Lucia, the grin held
TEXT = 'When Rockstar remembers to represent your people in their masterpiece:'
TILT, Y = 6.0, 420


def _draw(i):
    """One drawing with the body check on (humancheck, rule 89): (pixels, its faults)."""
    import humancheck as HC
    HC.frame_begin()
    px = G.F.frame_image(T0 + i / 12).convert('RGB').resize((1080, 1920)).tobytes()
    return px, HC.frame_end(T0 + i / 12)


def main(out):
    tmp = tempfile.mkdtemp()
    black = os.path.join(tmp, 'black.mp4')                  # the whole film's sound, mixed as the final was
    subprocess.run([FF, '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=black:s=64x64:r=24:d={G.LENGTH}',
                    '-c:v', 'libx264', black], check=True)
    sound = os.path.join(tmp, 'sound.mp4')
    G.mix(black, sound)
    silent = os.path.join(tmp, 'pic.mp4')
    n = int(round((T1 - T0) * 12))
    p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', '12',
                          '-i', '-', '-r', '24', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', silent],
                         stdin=subprocess.PIPE)
    import humancheck as HC
    w = HC.Writer(f'story {T0}-{T1}')
    with Pool(os.cpu_count()) as pool:
        for k, (fr, faults) in enumerate(pool.imap(_draw, range(n))):
            p.stdin.write(fr)
            w.frame(T0 + k / 12, faults)
    p.stdin.close()
    p.wait()
    png = os.path.join(tmp, 'hook.png')
    card(1080, 1920, TEXT, Y, png, centre=True, tilt=TILT)
    dur = n / 12
    subprocess.run([FF, '-v', 'error', '-y', '-i', silent, '-ss', f'{T0:.3f}', '-t', f'{dur:.3f}', '-i', sound,
                    '-i', png, '-filter_complex',
                    f'[0:v][2:v]overlay=0:0,format=yuv420p[v];[1:a]afade=t=out:st={dur - 0.3:.2f}:d=0.3[a]',
                    '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '20', '-preset', 'slow',
                    '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)
    notes = os.path.join(HERE, '..', 'notes', 'archive', 'grand-theft-autism-notes.md')
    w.finish(out, notes=open(notes).read() if os.path.exists(notes) else '')
    print('wrote', out, f'{os.path.getsize(out) / 1e6:.1f} MB', f'{dur:.2f} s')


if __name__ == '__main__':
    main(sys.argv[1])
