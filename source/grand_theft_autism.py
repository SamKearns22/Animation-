#!/usr/bin/env python3
"""Grand Theft Autism: the whole film's animatic render (21 Nov, Sam: "Render animatic. Overrule all checks and
preflights. 0.5 s darkness before the logo swipe in. No hook text.").

MAP
  caption_at ... none yet (Sam records the voices, so there is nothing to caption)
  no HOOK ...... no Hook Text (Sam)
  sound() ...... his song under the whole film: from the cut (music/monde-de-mer-full.mp3), full to the end of the opening, down to car-radio level over 0.6 s, a short fade at its end
  render ....... python3 source/grand_theft_autism.py OUT.mp4   (540 x 960, 12 drawings a second, each held 2 frames)
"""
import os
import subprocess
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gta_film as F          # noqa: E402
import film_engine as FE      # noqa: E402
from PIL import Image         # noqa: E402

# Sam, 21 Nov: all checks overruled. The drawing code's own figure checks warn (named in the faults file) instead of
# stopping a frame.
os.environ['ARM_FOLD_NAMED'] = '1'
os.environ['NAMED_FAULTS_FILE'] = '/tmp/gta_named_faults.txt'
import figure as _fig         # noqa: E402
_fig._ALLOW.append("Sam's order, 21 Nov: checks overruled")

LENGTH = F.LENGTH
DUR = LENGTH
SHOTS = F.SHOTS
SONG = os.path.join(HERE, '..', 'music', 'monde-de-mer-full.mp3')
SONG_FROM = 36.48             # his whole song (21 Nov): 0.5 s before the chorus's first hit (36.98) = film frame 1
SONG_LEN = LENGTH


# what is said, on the film's clock (the recordings' speech starts; shot 5-8 times are the mouths' starts)
CAPS = [(7.30, 10.24, "This is actually a really difficult sensory experience."),
        (12.10, 12.95, "It's very loud."),
        (23.55, 24.75, "Yeah, I didn't like that."),
        (25.75, 27.99, "You want to tell me why we brought her again?"),
        (28.25, 28.81, "I told you."),
        (29.25, 31.74, "Her hyperfixation is homemade explosives."),
        (32.17, 33.84, "This job wouldn't have worked without her."),
        (35.30, 37.10, "My safe food is nitroglycerin.")]


def caption_at(t):
    return next((c for a, b, c in CAPS if a <= t < b), None)


def shot_of(t):
    return next((k for k, (_, a, b) in enumerate(SHOTS, 1) if a <= t < b), len(SHOTS))


def _draw(i):
    t = i / 12
    im = F.frame_image(t).convert('RGB').resize((540, 960), Image.LANCZOS)
    FE.stamp(im, t, shot_of(t))
    return im.tobytes()


def main():
    out = sys.argv[1]
    t0 = float(sys.argv[sys.argv.index('--from') + 1]) if '--from' in sys.argv else 0.0
    if '--remux' in sys.argv:                      # new sound on an existing picture (no redraw)
        silent = sys.argv[sys.argv.index('--remux') + 1]
        return mix(silent, out)
    n = int(round(LENGTH * 12))
    silent = out + '.silent.mp4'
    if t0 > 0:
        os.replace(out, out + '.old.mp4')
        silent_new = silent
        silent = out + '.new.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '540x960', '-r',
                          '12', '-i', '-', '-r', '24', '-c:v', 'libx264', '-crf', '20', '-preset', 'medium',
                          '-pix_fmt', 'yuv420p', silent], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for k, fr in enumerate(pool.imap(_draw, range(int(round(t0 * 12)), n), chunksize=1)):
            p.stdin.write(fr)
            if k % 24 == 0:
                print(f'drawing {k}/{n}', flush=True)
    p.stdin.close()
    p.wait()
    if t0 > 0:                                     # the first t0 seconds of the old picture, then the new drawings
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-t', f'{t0:.3f}', '-i', out + '.old.mp4', '-i', silent,
                        '-filter_complex', '[0:v][1:v]concat=n=2:v=1:a=0[v]', '-map', '[v]', '-r', '24', '-c:v', 'libx264',
                        '-crf', '20', '-preset', 'medium', '-pix_fmt', 'yuv420p', silent_new], check=True)
        os.remove(silent)
        silent = silent_new
    mix(silent, out)


UP = '/root/.claude/uploads/77034bac-879c-5e0d-ae1f-2f0f01232e9c/'
VOICES = [  # (file, speech starts in file, speech ends, film time it starts)
    ('Autistic_1.m4a', 0.93, 3.87, 7.30), ('Autistic_2.m4a', 0.80, 1.65, 12.10),
    ('Autistic_3.m4a', 0.80, 2.00, 23.55), ('Lucia.m4a', 0.87, 3.11, 25.75),
    ('Jason.m4a', 1.40, 6.99, 28.25), ('Autistic_4.m4a', 0.79, 2.59, 35.30)]


GAIN_DB = {'Autistic_1.m4a': 7.5, 'Autistic_2.m4a': 13.8, 'Autistic_3.m4a': 10.9, 'Autistic_4.m4a': 7.9,
           'Lucia.m4a': 2.0, 'Jason.m4a': 0.0}      # Sam 21 Nov: her voice was barely audible; all brought to one level


def _find(key):
    import glob
    return glob.glob(UP + '*' + key + '*')[0]


def mix(silent, out):
    """The song (radio level after the opening), the voices, the sound effects Sam named: siren, pistol, glass at
    double speed, swerve and crash."""
    end = F.SHOTS[0][2]
    ins, parts, k = ['-i', silent], [], 1
    song = (f"volume='if(lt(t,{end}),1,if(lt(t,{end + 0.6}),1-(1-0.16)*(t-{end})/0.6,0.16))':eval=frame,"
            f"afade=t=out:st={LENGTH - 0.6}:d=0.6")
    ins += ['-ss', str(SONG_FROM), '-t', str(LENGTH), '-i', SONG]
    parts.append(f'[1:a]{song}[m]')
    labels = ['[m]']
    ev = []   # (file key, in-start, length, film time, volume, speed)
    for f, a, b, at in VOICES:
        ev.append((f.split('.')[0] + '.m4a', a - 0.04, b - a + 0.08, at - 0.04, 10 ** (GAIN_DB.get(f, 0) / 20), 1.0))
    for ts in (1.95, 2.30, 2.62, 2.92):
        ev.append(('pistol', 0.0, 0.7, 14.1 + ts, 0.8, 1.0))
    ev.append(('glass-breaking', 0.0, 3.12, 14.1 + 2.30, 0.8, 2.0))        # double speed, Sam
    ev.append(('car-crash', 0.0, 5.09, 14.1 + 5.504 - 0.5, 0.9, 1.0))
    for n, (key, a, ln, at, vol, sp) in enumerate(ev):
        ins += ['-ss', f'{a:.3f}', '-t', f'{ln:.3f}', '-i', _find(key)]
        k += 1
        ms = int(at * 1000)
        parts.append(f'[{k}:a]atempo={sp},volume={vol},adelay={ms}|{ms}[e{n}]')
        labels.append(f'[e{n}]')
    ins += ['-stream_loop', '-1', '-i', _find('police-siren')]
    k += 1
    sir = int(F.SHOTS[1][1] * 1000)
    parts.append(f'[{k}:a]atrim=0:{LENGTH - F.SHOTS[1][1]:.2f},volume=0.07,afade=t=in:d=1.0,adelay={sir}|{sir}[sir]')
    labels.append('[sir]')
    parts.append(''.join(labels) + f'amix=inputs={len(labels)}:duration=longest:normalize=0,alimiter=limit=0.95,apad=whole_dur={LENGTH}[a]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(parts), '-map', '0:v', '-map', '[a]',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-t', str(LENGTH), out], check=True)
    if silent.endswith('.silent.mp4'):
        os.remove(silent)
    print('done', out, round(os.path.getsize(out) / 1e6, 2), 'MB')


if __name__ == '__main__':
    main()
