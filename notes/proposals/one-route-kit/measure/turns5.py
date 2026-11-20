"""Kit people at five real turns (DEGREES: refcast.py passed radians, so all its five turns were the front) and one
arms-up pose; one PNG per tile. Run from source/: python3 ../notes/proposals/one-route-kit/measure/turns5.py OUT"""
import sys, os
sys.path.insert(0, os.getcwd())
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
import people as PK, people_parts as PP
from PIL import Image
B, V = PP.B, PP.V
from satire_style import install_circle_hands
install_circle_hands(B)
cam = B.Cam(1.0, 540, 960)
for film in ['grand-theft-autism', 'milburn']:
    cast = PK.install(dict(PK.load(film)))
    for w, sp in cast.items():
        s = 0.5 * sp['height'] / 1.75
        for yaw in (0, 45, 90, 135, 180, 'up'):
            tile = Image.new('RGBA', (2160, 3840), (232, 228, 222, 255))
            j = None
            if yaw == 'up':
                j = V.standing(sp)
                V.arm_to(j, 'R', (230, -120, 40)); V.arm_to(j, 'L', (-260, 140, 30))
            V.person(tile, cam, 540, 840 - 928 * s, s, dict(sp), 0.0, 0 if yaw == 'up' else yaw, j)
            tile = tile.resize((1080, 1920), Image.LANCZOS).crop((290, 60, 790, 880)).convert('RGB')
            tile.save(f'{out}/{film}-{w}-{yaw}.png')
    print(film, len(cast), flush=True)
