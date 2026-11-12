"""Side-by-side for Sam: left as the films are now, right with the house look (engine's house_look.apply)."""
import os, sys, subprocess
sys.path.insert(0, '/home/user/Animation-/source'); os.chdir('/home/user/Animation-/source')
import numpy as np
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
T0, T1, OUT = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
FONT = ImageFont.truetype('/home/user/Animation-/source/fonts/DejaVuSans-Bold.ttf', 40)

def lab(d, x, t):
    w = d.textlength(t, font=FONT); d.rectangle([x - w/2 - 14, 316, x + w/2 + 14, 380], fill='white'); d.text((x - w/2, 322), t, font=FONT, fill='black')

def frame(i):
    import ad_vanced_notice as A, house_look as L
    t = i / 12
    p = A.picture(t).convert('RGB')
    a = A.overlay(p.copy().convert('RGBA'), t).convert('RGB').resize((540, 960), Image.LANCZOS)
    b = A.overlay(L.apply(p).convert('RGBA'), t).convert('RGB').resize((540, 960), Image.LANCZOS)
    c = Image.new('RGB', (1080, 1920), (32, 32, 32)); c.paste(a, (0, 400)); c.paste(b, (540, 400))
    d = ImageDraw.Draw(c); lab(d, 270, 'AS NOW'); lab(d, 810, 'HOUSE LOOK')
    return np.asarray(c).tobytes()

if __name__ == '__main__':
    import ad_vanced_notice as A
    wav = OUT + '.wav'; A.MA.write_wav(wav, A.soundtrack())
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    p = subprocess.Popen([ff, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', '12', '-i', '-',
                          '-ss', f'{T0:.3f}', '-i', wav, '-map', '0:v', '-map', '1:a', '-r', '24', '-c:v', 'libx264', '-crf', '24',
                          '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', OUT],
                         stdin=subprocess.PIPE)
    with Pool(4) as pool:
        for fr in pool.imap(frame, range(int(round(T0 * 12)), int(round(T1 * 12))), chunksize=2):
            p.stdin.write(fr)
    p.stdin.close(); p.wait(); os.remove(wav)
    print('done', OUT, round(os.path.getsize(OUT) / 1e6, 2), 'MB')
