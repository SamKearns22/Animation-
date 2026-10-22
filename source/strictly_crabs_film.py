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
CAP_TOP = 1310            # tall film: one line on the dance floor below the desk (and the crabs), inside the safe area
SANS = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')

# subtitle chunks: (line number, stretch of speech, words, syllables) - two to five words, the punchline on its own
CHUNKS = [(1, 0, "I can't say I understand", 7), (1, 0, 'the joke, darling,', 4), (1, 1, "but I'm having", 4),
          (1, 1, 'an amazing time.', 5), (2, 0, 'Two hundred and ninety!', 7)]


# ------------------------------------------------------------------------------------------------ titles
SETTLED = (111, 184)     # recording frames where the logo sits still and only the light streaks flow
LOOP0, XF = 135, 24      # each replay restarts at frame 135; 24-frame (0.4 s) crossfade into it
PUSH = 185               # from here the recording's own push-in starts (185-191): kept for the very end, at the cut


def _aligned(frames):
    """Each settled frame nudged (affine, found by matching the logo) so its logo sits exactly on frame PUSH-1's:
    the crossfades then mix only the streaks, never two copies of the lettering."""
    import cv2
    ref = cv2.cvtColor(frames[PUSH - 1], cv2.COLOR_RGB2GRAY).astype(np.float32)
    h, w = ref.shape
    mask = np.zeros((h, w), np.uint8); cv2.circle(mask, (581, 291), 250, 255, -1)
    out = {}
    for k in range(SETTLED[0], PUSH):
        g = cv2.cvtColor(frames[k], cv2.COLOR_RGB2GRAY).astype(np.float32)
        M = np.eye(2, 3, dtype=np.float32)
        try:
            cv2.findTransformECC(ref, g, M, cv2.MOTION_AFFINE,
                                 (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1e-5), mask, 5)
        except cv2.error:
            pass
        out[k] = cv2.warpAffine(frames[k], M, (w, h), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
                                borderMode=cv2.BORDER_REFLECT)
    return out


def title_sequence():
    """The recording at its own 59.94 fps, lengthened so the logo stays on screen until TITLES: after frame 184 the
    settled stretch (logo still, streaks flowing) plays again twice, each replay joined by a 0.4 s crossfade of the
    streaks, then the recording's own last 7 frames (the push-in) land exactly on the cut."""
    fr = sorted(glob.glob(os.path.join(HERE, 'data', 'strictly-crabs', 'titles', 'out', '*.png')))
    B = [np.asarray(Image.open(f).convert('RGB')) for f in fr]
    A = _aligned(B)
    n_ext = round(TITLES * REC_FPS) - len(B)              # frames to add: about 99
    reps = max(1, round(n_ext / (PUSH - LOOP0)))
    passes = [[B[i] for i in range(PUSH)]] + [[A[i] for i in range(LOOP0, PUSH)] for _ in range(reps)]
    for p in passes[:-1]:                                  # each pass's tail fades into the frames just before LOOP0
        for m in range(XF):
            w = 0.5 - 0.5 * np.cos(np.pi * (m + 1) / XF)
            j = len(p) - XF + m
            tail = (A[j] if j in A else p[j]).astype(np.float32)
            p[j] = (tail * (1 - w) + A[LOOP0 - XF + m].astype(np.float32) * w).astype(np.uint8)
    seq = [f for p in passes for f in p] + B[PUSH:]
    # Sam, 21 Oct: the push-in needs one more frame of the expanding logo. The ball was growing about 3.5% a frame
    # (tracked scale 1.02 -> 1.23 over frames 185-191), so three more recording frames (one 24 fps frame) are the last
    # frame zoomed on the ball's centre by the same steady steps. The cut stays at TITLES (the film is anchored to its end).
    import cv2
    for z in (1.035, 1.071, 1.109):
        M = cv2.getRotationMatrix2D((580.0, 279.0), 0, z)
        seq.append(cv2.warpAffine(B[-1], M, (B[-1].shape[1], B[-1].shape[0]), flags=cv2.INTER_CUBIC,
                                  borderMode=cv2.BORDER_REFLECT))
    return seq


def tall_frame(src, s=1.3, ox=530, oy=960, cx=581, cy=291, ea=480, eb=290):
    """TikTok (Sam, 22 Oct): the ident filling a whole 1080x1920 frame, no widescreen rectangle left showing. The ball and
    lettering (an oval, kept exactly as recorded) sit in the middle; everywhere outside it, every ray from the ball's
    centre carries on in the colour where it leaves the oval, so the burst runs on to all four edges. Sharp, no blur."""
    import cv2
    X, Y = np.meshgrid(np.arange(VW, dtype=np.float32), np.arange(VH, dtype=np.float32))
    du, dv = (X - ox) / s, (Y - oy) / s
    e = np.maximum(np.sqrt((du / ea) ** 2 + (dv / eb) ** 2), 1.0)
    return cv2.remap(src, (cx + du / e).astype(np.float32), (cy + dv / e).astype(np.float32), cv2.INTER_CUBIC)


def titles(out_dir, w=1280, h=720):
    """The opening at 24 fps, ending exactly at TITLES on the recording's last frame (then the jump cut)."""
    seq = title_sequence()
    os.makedirs(out_dir, exist_ok=True)
    n = round(TITLES * FPS)
    for k in range(n):
        i = len(seq) - 1 - round((n - 1 - k) * REC_FPS / FPS)    # anchored to the end: the last frame is the last frame
        fr = seq[max(0, i)]
        if h > w:
            fr = tall_frame(fr)
        Image.fromarray(fr).resize((w, h), Image.LANCZOS).save(f'{out_dir}/{k:04d}.png')


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
    for i, row in enumerate(wrap(s, f, 820)):
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
        pic = Image.frombuffer('RGB', (w, h), buf)
        img = pic.resize((VW, VH), Image.LANCZOS) if h > w else compose(pic)
        for a, b, text in subs:
            if a <= t < b:
                caption(img, text, CAP_TOP if h > w else PIC_TOP + PH + 24)
        enc.stdin.write(img.tobytes())
        k += 1
    enc.stdin.close(); enc.wait(); p.wait()
    os.rmdir(tmp)


# ------------------------------------------------------------------------------------------------ join
def dance_parts(a, b, out):
    """The dance with its second shot taken out (Sam, 22 Oct): part A (start to beat 16) then part B (beat 24 on)."""
    subprocess.run([FF, '-v', 'error', '-y', '-i', a, '-i', b, '-filter_complex', '[0:v][1:v]concat=n=2:v=1[v]', '-map', '[v]',
                    '-r', str(FPS), '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', out], check=True)


def join(dance, judges, titles_dir, out):
    import strictly_judges as J
    import mossad_audio as MA
    wav = out + '.wav'
    MA.write_wav(wav, film_sound())
    probe = subprocess.run([FF, '-i', dance], capture_output=True, text=True).stderr
    w, h = probe.split('Video:')[1].split(',')[2].split()[0].split('x')
    fc = (f'[0:v]scale={w}:{h},fps={FPS},setsar=1[a];[1:v]fps={FPS},trim=0:{J.DANCE_LEN},setpts=PTS-STARTPTS,setsar=1[b];'
          f'[2:v]scale={w}:{h},fps={FPS},trim=0:{J.DUR},setpts=PTS-STARTPTS,setsar=1[c];[a][b][c]concat=n=3:v=1,fps={FPS}[v]')
    subprocess.run([FF, '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{titles_dir}/%04d.png', '-i', dance, '-i', judges,
                    '-i', wav, '-filter_complex', fc, '-map', '[v]', '-map', '3:a', '-r', str(FPS), '-c:v', 'libx264', '-crf', '20',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', out], check=True)
    os.remove(wav)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'titles':
        titles(a[1], *(int(x) for x in a[2:4]))
    elif a[0] == 'sound':
        import mossad_audio as MA
        MA.write_wav(a[1], film_sound())
    elif a[0] == 'dance':
        dance_parts(a[1], a[2], a[3])
    elif a[0] == 'join':
        join(*a[1:5])
    elif a[0] == 'vertical':
        vertical(a[1], a[2])
    elif a[0] == 'subs':
        for x, y, s in subtitles():
            print(f'{x:6.2f}-{y:6.2f}  {s}')
