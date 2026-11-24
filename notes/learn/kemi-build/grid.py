"""Draw a labelled pixel grid over a reference photo, enlarged, so measurements can be read off it (Open Wounds chat 6)."""
import sys
from PIL import Image, ImageDraw
src, out, scale, step = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
im = Image.open(src).convert('RGB')
im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
d = ImageDraw.Draw(im)
for x in range(0, int(im.width / scale), step):
    X = int(x * scale); d.line([(X, 0), (X, im.height)], fill=(255, 0, 0) if x % (step * 5) == 0 else (255, 150, 150), width=1)
    if x % (step * 5) == 0: d.text((X + 2, 2), str(x), fill=(255, 0, 0))
for y in range(0, int(im.height / scale), step):
    Y = int(y * scale); d.line([(0, Y), (im.width, Y)], fill=(0, 0, 255) if y % (step * 5) == 0 else (150, 150, 255), width=1)
    if y % (step * 5) == 0: d.text((2, Y + 2), str(y), fill=(0, 0, 255))
im.save(out, quality=90)
