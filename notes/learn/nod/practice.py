"""Kind: practice. The nod as a pitch (Open Wounds chat 39, Sam's note 26: "It's not a nod, it's a head-bob").
Grey heads (the film's cast, drawn as the film does, shown in grey), front / three-quarter / side; top row the old
kit's bob (the whole head slid down and up), bottom row the new nod (views.Pitched). Two nods at the film's 12 fps,
each down in 0.25 s, up in 0.3 s. python3 notes/learn/nod/practice.py OUT.mp4 [WHO] [--still OUT.jpg]"""
import math
import os
import subprocess
import sys
import tempfile
sys.path.insert(0, 'source')
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import castsheet as CS

out = sys.argv[1]
who = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else 'may'
still = sys.argv[sys.argv.index('--still') + 1] if '--still' in sys.argv else None
cast, PP = CS._setup('brexit-is-done', [who])
B, V = PP.B, PP.V
FPS, AMP = 12, 3.0                                # 3 nod units: 13.5 degrees at the bottom


def nod_at(t):
    """Two nods: 0.25 s down (eased), 0.3 s up (eased), 0.35 s apart."""
    for t0 in (0.3, 1.2):
        u = t - t0
        if 0 <= u < 0.25:
            return AMP * 0.5 * (1 - math.cos(math.pi * u / 0.25))
        if 0.25 <= u < 0.55:
            return AMP * 0.5 * (1 + math.cos(math.pi * (u - 0.25) / 0.3))
    return 0.0


class Life:
    def __init__(self):
        self.n = 0.0

    def at_time(self, t):
        return 0.0, self.n


class Bob:                                        # the old kit's nod, for the top row: the head slid down
    def __init__(self, L, deg, c, hw, hh, view):
        self.L, self.cam, self.s, self.flip = L, L.cam, L.s, getattr(L, 'flip', 1)
        self.dy = deg / V.NOD_DEG * 5.0

    def P(self, x, y):
        return self.L.P(x, y + self.dy)

    def S(self, v):
        return self.L.S(v)


NEW = V.Pitched
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)


def frame(t):
    page = Image.new('RGB', (1080, 1080), 'white')
    d = ImageDraw.Draw(page)
    for row, (name, cls) in enumerate((('old: a bob', Bob), ('new: a nod', NEW))):
        V.Pitched = cls
        for col, yaw in enumerate((0, 45, 90)):
            sp = dict(cast[who])
            life = Life()
            life.n = nod_at(t)
            sp['head_life'] = life
            tile = Image.new('RGBA', (1080, 1920), (255, 255, 255, 255))
            s = 0.5 * sp['height'] / 1.75
            y0 = 840 - 928 * s
            V.person(tile, B.Cam(2.0, 540, 470), 540, y0, s, sp, t, yaw, None)
            hy = int((y0 - 470) * 2.0 + 960)      # the neck top on the tile
            crop = tile.convert('L').crop((540 - 250, hy - 380, 540 + 250, hy + 120)).resize((340, 340))
            page.paste(crop.convert('RGB'), (20 + col * 350, 60 + row * 510))
        d.text((24, 16 + row * 510), name, fill='black', font=f)
    V.Pitched = NEW
    return page


if still:                                         # the bottom of a nod beside rest, for a sheet
    a, b = frame(0.0), frame(0.55)
    sh = Image.new('RGB', (2160, 1080), 'white')
    sh.paste(a, (0, 0)); sh.paste(b, (1080, 0))
    sh.save(still, quality=88)
with tempfile.TemporaryDirectory() as tmp:
    for i in range(int(2.1 * FPS)):
        frame(i / FPS).save(os.path.join(tmp, f'{i:04d}.png'))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(tmp, '%04d.png'),
                    '-vf', 'fps=24', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', out], check=True)
print(out, os.path.getsize(out) // 1024, 'KB')
