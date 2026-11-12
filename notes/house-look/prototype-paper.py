"""Ad-vanced Notice two ways, side by side: left smooth (24 fps, every frame drawn), right on twos (each drawing held
2 frames, as posted) with a paper grain on the drawing only (captions go on clean, after). Test only."""
import os, sys, subprocess
from multiprocessing import Process
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC = '/home/user/Animation-/source'
sys.path.insert(0, SRC); os.chdir(SRC)
S = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(S, 'frames'); os.makedirs(FR, exist_ok=True)
FPS = 24
FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 40)


def paper(img, P):
    a = np.asarray(img.convert('RGB'), np.float32) / 255
    b = P[..., None]
    soft = (1 - 2 * b) * a * a + 2 * b * a
    out = a + 0.7 * (soft - a)
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8))


def label(d, x, text):
    w = d.textlength(text, font=FONT)
    d.rectangle([x - w / 2 - 14, 316, x + w / 2 + 14, 380], fill='white')
    d.text((x - w / 2, 322), text, font=FONT, fill='black')


def work(i0, i1):
    import ad_vanced_notice as A
    P = np.asarray(Image.open(os.path.join(S, 'paper.png')).convert('L'), np.float32) / 255
    held = None
    for i in range(i0, i1):
        out = os.path.join(FR, f'{i:05d}.jpg')
        if os.path.exists(out):
            continue
        t = i / FPS
        pic = A.picture(t).convert('RGB')
        if i % 2 == 0 or held is None:
            held = paper(A.picture((i - i % 2) / FPS).convert('RGB') if i % 2 else pic, P)
        left = A.overlay(pic.convert('RGBA'), t).convert('RGB').resize((540, 960), Image.LANCZOS)
        right = A.overlay(held.convert('RGBA'), t).convert('RGB').resize((540, 960), Image.LANCZOS)
        c = Image.new('RGB', (1080, 1920), (32, 32, 32))
        c.paste(left, (0, 400)); c.paste(right, (540, 400))
        d = ImageDraw.Draw(c)
        label(d, 270, 'SMOOTH'); label(d, 810, 'STEPS + PAPER')
        c.save(out, quality=90)


if __name__ == '__main__':
    import ad_vanced_notice as A
    n = int(round(A.DUR * FPS))
    if sys.argv[1:] == ['sound']:
        A.MA.write_wav(os.path.join(S, 'avn.wav'), A.soundtrack())
        sys.exit()
    k = 4
    bounds = [n * j // k for j in range(k + 1)]
    ps = [Process(target=work, args=(bounds[j], bounds[j + 1])) for j in range(k)]
    [p.start() for p in ps]; [p.join() for p in ps]
    print('frames', len(os.listdir(FR)), 'of', n)
