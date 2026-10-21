"""Strictly Crabs Dancing: join the three parts into the whole film, then the TikTok version.

    python3 strictly_crabs_film.py titles OUT_DIR [W H]     the opening at 24 fps, logo moving until TITLES, as frames
    python3 strictly_crabs_film.py sound OUT.wav            the whole film's sound (song + judges' voices)
    python3 strictly_crabs_film.py join DANCE.mp4 JUDGES.mp4 TITLES_DIR OUT.mp4   clean widescreen film with sound
    python3 strictly_crabs_film.py vertical CLEAN.mp4 OUT.mp4                    1080x1920 with subtitles (no hook)
    python3 strictly_crabs_film.py subs                     print the subtitles with their times, to proofread
    then: python3 finish.py VERT.mp4 animations/strictly-crabs-vertical.mp4 "BBC keeps things fresh 🦀" --y 500 --until 4.85

Sam, 21 Oct: logo keeps moving until 4.85 s, then a jump cut into the crabs (no fade); subtitles; Hook Text; sign-off.
"""
import glob
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FF = '/usr/local/lib/python3.13/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'
FPS = 24
TITLES = 4.85
REC_FPS = 59.94
VW, VH = 1080, 1920
PW, PH = 1080, 608               # the widescreen picture fitted to the width: the crabs reach the frame edges, so no crop
PIC_TOP = 640
SANS = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')

# subtitle chunks: (line number, stretch of speech, words, syllables) - two to five words, the punchline on its own
CHUNKS = [(1, 0, "I don't really understand", 7), (1, 0, 'the joke, darling,', 4), (1, 1, "but I'm having", 4),
          (1, 1, 'an amazing time.', 5), (2, 0, 'Two hundred and ninety!', 7)]


# ------------------------------------------------------------------------------------------------ titles
def titles(out_dir, w=1280, h=720):
    """The recording's frames, retimed to 24 fps; after the recording ends (3.2 s) the last frame keeps pushing in
    slowly towards the logo, so it is still moving at the cut."""
    fr = sorted(glob.glob(os.path.join(HERE, 'data', 'strictly-crabs', 'titles', 'out', '*.png')))
    os.makedirs(out_dir, exist_ok=True)
    end = (len(fr) - 1) / REC_FPS
    last = Image.open(fr[-1]).convert('RGB')
    cx, cy = 585, 300                                    # the ball's middle in the recording
    for k in range(round(TITLES * FPS)):
        t = k / FPS
        if t <= end:
            im = Image.open(fr[min(len(fr) - 1, round(t * REC_FPS))]).convert('RGB')
        else:
            f = (t - end) / (TITLES - end)
            z = 1 + 0.12 * (f * 0.6 + 0.4 * f * f)       # carries on at about the recording's own pace, gently faster
            W, H = last.size
            bw, bh = W / z, H / z
            x0 = min(max(cx - bw / 2, 0), W - bw); y0 = min(max(cy - bh / 2, 0), H - bh)
            im = last.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + bw, y0 + bh))
        im.resize((w, h), Image.LANCZOS).save(f'{out_dir}/{k:04d}.png')


# ------------------------------------------------------------------------------------------------ sound
def film_sound():
    import strictly_judges as J
    MA = J.MA
    total = J.FILM_AT + J.DUR
    n = int(total * MA.SR)
    v = np.zeros(n)
    jv = J.voices()
    s = int(J.FILM_AT * MA.SR)
    v[s:s + len(jv)] += jv[:n - s]
    bed = J.music_bed(0.0, total)[:n]
    mix, _ = MA.master(v + bed, n)
    return mix


# ------------------------------------------------------------------------------------------------ subtitles
def subtitles():
    """[(film start, film end, text)]: each chunk on its first syllable's beat in the recording."""
    import strictly_judges as J
    from press_secretary import _syllable_beats
    out = []
    for ln in J.LINES:
        v = ln['_voice']
        beats = _syllable_beats(v, ln['_stretches'])
        for si, (a0, b0) in enumerate(ln['_stretches']):
            mine = [c for c in CHUNKS if c[0] == ln['n'] and c[1] == si]
            bt = [b for b in beats if a0 - 0.02 <= b <= b0 + 0.02] or [a0]
            total, k = sum(c[3] for c in mine), 0
            for _, _, text, syl in mine:          # each chunk on the beat of its first syllable (scaled to the stretch)
                i = min(len(bt) - 1, round(k / total * len(bt)))
                t0 = a0 if k == 0 else bt[i]
                out.append([J.FILM_AT + ln['start'] + t0 + 0.05, None, text])   # never ahead of the voice
                k += syl
        out[-1][1] = J.FILM_AT + ln['end'] + 0.25
    for a, b in zip(out, out[1:]):
        if a[1] is None:
            a[1] = b[0]
    return [tuple(x) for x in out]


def wrap(s, f, width):
    words, rows = s.split(), ['']
    for wd in words:
        t = (rows[-1] + ' ' + wd).strip()
        if f.getlength(t) <= width or not rows[-1]:
            rows[-1] = t
        else:
            rows.append(wd)
    return rows


def caption(img, s, top):
    f = ImageFont.truetype(SANS, 52)
    d = ImageDraw.Draw(img)
    for i, row in enumerate(wrap(s, f, 700)):
        d.text((540, top + 30 + i * 66), row, font=f, fill=(255, 255, 255), anchor='mm', stroke_width=5,
               stroke_fill=(0, 0, 0))


# ------------------------------------------------------------------------------------------------ vertical
def glow(edge, height, flip):
    row = edge.mean(axis=0, keepdims=True)
    row = np.asarray(Image.fromarray(row.astype(np.uint8)).resize((VW // 8, 1), Image.BILINEAR)
                     .filter(ImageFilter.GaussianBlur(4)).resize((VW, 1), Image.BILINEAR), float)
    base = np.array([8, 3, 14], float)                   # the set's own dark purple
    d = np.linspace(0, 1, height)[:, None, None]
    d = 1 - (1 - d) ** 2
    pad = row * (1 - d) + base * d
    return pad[::-1] if flip else pad


def compose(pic):
    big = np.asarray(pic.resize((PW, PH), Image.LANCZOS), float)
    out = np.empty((VH, VW, 3))
    out[PIC_TOP:PIC_TOP + PH] = big
    out[:PIC_TOP] = glow(big[:24], PIC_TOP, True)
    out[PIC_TOP + PH:] = glow(big[-24:], VH - PIC_TOP - PH, False)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def vertical(src, dst):
    subs = subtitles()
    probe = subprocess.run([FF, '-i', src], capture_output=True, text=True).stderr
    w, h = [int(x) for x in probe.split('Video:')[1].split(',')[2].split()[0].split('x')]
    tmp = dst + '.frames'
    os.makedirs(tmp, exist_ok=True)
    p = subprocess.Popen([FF, '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{VW}x{VH}', '-r', str(FPS),
                            '-i', '-', '-i', src, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '22',
                            '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', dst],
                           stdin=subprocess.PIPE)
    k = 0
    while True:
        buf = p.stdout.read(w * h * 3)
        if len(buf) < w * h * 3:
            break
        t = k / FPS
        img = compose(Image.frombuffer('RGB', (w, h), buf))
        for a, b, text in subs:
            if a <= t < b:
                caption(img, text, PIC_TOP + PH + 24)
        enc.stdin.write(img.tobytes())
        k += 1
    enc.stdin.close(); enc.wait(); p.wait()
    os.rmdir(tmp)


# ------------------------------------------------------------------------------------------------ join
def join(dance, judges, titles_dir, out):
    import strictly_judges as J
    import mossad_audio as MA
    wav = out + '.wav'
    MA.write_wav(wav, film_sound())
    probe = subprocess.run([FF, '-i', dance], capture_output=True, text=True).stderr
    w, h = probe.split('Video:')[1].split(',')[2].split()[0].split('x')
    fc = (f'[0:v]scale={w}:{h},fps={FPS},setsar=1[a];[1:v]fps={FPS},trim=0:24.9,setpts=PTS-STARTPTS,setsar=1[b];'
          f'[2:v]scale={w}:{h},fps={FPS},trim=0:{J.DUR},setpts=PTS-STARTPTS,setsar=1[c];[a][b][c]concat=n=3:v=1[v]')
    subprocess.run([FF, '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{titles_dir}/%04d.png', '-i', dance, '-i', judges,
                    '-i', wav, '-filter_complex', fc, '-map', '[v]', '-map', '3:a', '-c:v', 'libx264', '-crf', '20',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', out], check=True)
    os.remove(wav)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'titles':
        titles(a[1], *(int(x) for x in a[2:4]))
    elif a[0] == 'sound':
        import mossad_audio as MA
        MA.write_wav(a[1], film_sound())
    elif a[0] == 'join':
        join(*a[1:5])
    elif a[0] == 'vertical':
        vertical(a[1], a[2])
    elif a[0] == 'subs':
        for x, y, s in subtitles():
            print(f'{x:6.2f}-{y:6.2f}  {s}')
