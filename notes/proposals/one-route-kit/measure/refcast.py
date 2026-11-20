"""Draw every kit person (each people file) at five turns into PNGs in OUT; print a hash per film."""
import sys, os, hashlib
sys.path.insert(0, os.getcwd())
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
import people as PK
import people_parts as PP
from PIL import Image
B, V = PP.B, PP.V
from satire_style import install_circle_hands
install_circle_hands(B)
B.SS = 1
cam = B.Cam(1.0, 540, 960)
for film in ['grand-theft-autism', 'milburn', 'blessed', 'facetool', 'protest-tiers']:
    cast = dict(PK.load(film))
    for w, cd in PK.crowds(film).items():
        for i in range(3):
            cast[f'{w}{i}'] = PK.crowd_person(cd, i)
    cast = PK.install(cast)
    h = hashlib.md5()
    for w, sp in cast.items():
        s = 0.5 * sp['height'] / 1.75
        for yaw in (0, 0.5, 1.0, 1.5, 3.14):
            tile = Image.new('RGBA', (1080, 1920), (232, 228, 222, 255))
            V.person(tile, cam, 540, 840 - 928 * s, s, dict(sp), 0.0, yaw)
            tile = tile.crop((290, 60, 790, 880)).convert('RGB')
            tile.save(f'{out}/{film}-{w}-{yaw}.png'); h.update(tile.tobytes())
    print(film, len(cast), h.hexdigest()[:10], flush=True)
