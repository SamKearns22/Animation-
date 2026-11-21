#!/usr/bin/env python3
"""Grand Theft Autism: the whole film's animatic render (21 Nov, Sam: "Render animatic. Overrule all checks and
preflights. 0.5 s darkness before the logo swipe in. No hook text.").

MAP
  caption_at ... none yet (Sam records the voices, so there is nothing to caption)
  no HOOK ...... no Hook Text (Sam)
  sound() ...... his song under the whole film: from the cut (music/gta-opener-chorus-long.mp3, 9.4 s is all that is
                 saved), full to the end of the opening, down to car-radio level over 0.6 s, a short fade at its end
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

LENGTH = F.LENGTH
DUR = LENGTH
SHOTS = F.SHOTS
SONG = os.path.join(HERE, '..', 'music', 'gta-opener-chorus-long.mp3')
SONG_FROM = 0.1               # seconds into the saved cut: the film's frame 1 (the 0.5 s dark lead-in is its own start)
SONG_LEN = 9.4


def caption_at(t):
    return None


def shot_of(t):
    return next((k for k, (_, a, b) in enumerate(SHOTS, 1) if a <= t < b), len(SHOTS))


def _draw(i):
    t = i / 12
    im = F.frame_image(t).convert('RGB').resize((540, 960), Image.LANCZOS)
    FE.stamp(im, t, shot_of(t))
    return im.tobytes()


def main():
    out = sys.argv[1]
    n = int(round(LENGTH * 12))
    silent = out + '.silent.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '540x960', '-r',
                          '12', '-i', '-', '-r', '24', '-c:v', 'libx264', '-crf', '20', '-preset', 'medium',
                          '-pix_fmt', 'yuv420p', silent], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for k, fr in enumerate(pool.imap(_draw, range(n), chunksize=1)):
            p.stdin.write(fr)
            if k % 24 == 0:
                print(f'drawing {k}/{n}', flush=True)
    p.stdin.close()
    p.wait()
    open_end = F.SHOTS[0][2]                       # the opening's end (7.0 s on the film's clock)
    fade_at = SONG_LEN - 0.6
    vol = (f"volume='if(lt(t,{open_end}),1,if(lt(t,{open_end + 0.6}),1-(1-0.16)*(t-{open_end})/0.6,0.16))':eval=frame,"
           f"afade=t=out:st={fade_at}:d=0.6")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', silent, '-ss', str(SONG_FROM), '-t', str(SONG_LEN), '-i', SONG,
                    '-filter_complex', f'[1:a]{vol},apad=whole_dur={LENGTH}[a]', '-map', '0:v', '-map', '[a]', '-c:v',
                    'copy', '-c:a', 'aac', '-b:a', '160k', '-t', str(LENGTH), out], check=True)
    os.remove(silent)
    print('done', out, round(os.path.getsize(out) / 1e6, 2), 'MB')


if __name__ == '__main__':
    main()
