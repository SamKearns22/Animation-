"""R7 chat 8 (Sam's pick, option 2): blind judges for the WHOLE solid person. May only (the one test person), four
views in mode 'whole' beside the same four in mode 'legs' (chat 6/7's solid legs under the flat torso, the best before),
shuffled and numbered: outlines (headless, black: woman/man) and look (colour: the whole person).
    python3 notes/learn/seated/judge_whole.py TAG      -> judge/outlines-TAG.jpg, judge/look-TAG.jpg, judge/key-TAG.json"""
import json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import judge_r7 as JR
from PIL import Image, ImageDraw, ImageFont


def sheet(outline, seed, path, who='may'):
    tiles = []
    keep = JR.cast[who].get('shirt')
    if outline:                                 # a white top would read as the white page in the black outline (chat 8)
        JR.cast[who]['shirt'] = (160, 160, 160)
    for mode in ('whole', 'legs'):
        os.environ['SEAT_SOLID'] = mode
        tiles += [((who, n, mode), JR.figure(who, y, p, outline)) for y, p, n in JR.VIEWS]
    JR.cast[who]['shirt'] = keep
    random.Random(seed).shuffle(tiles)
    f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
    rows = [tiles[:4], tiles[4:]]
    W = max(sum(t.width + 30 for _, t in r) for r in rows) + 30
    h = tiles[0][1].height
    page = Image.new('RGB', (W, 2 * (h + 60) + 20), 'white'); d = ImageDraw.Draw(page)
    for r, row in enumerate(rows):
        x, y = 30, 40 + r * (h + 60)
        for i, (key, t) in enumerate(row):
            page.paste(t, (x, y)); d.text((x, y - 32), str(r * 4 + i + 1), fill='black', font=f); x += t.width + 30
    page.save(path, quality=90)
    return {str(i + 1): list(k) for i, (k, _) in enumerate(tiles)}


if __name__ == '__main__':
    tag = sys.argv[1]
    J = os.path.join(JR.HERE, 'judge')
    key = {'outlines': sheet(True, 811, os.path.join(J, f'outlines-{tag}.jpg')),
           'look': sheet(False, 1311, os.path.join(J, f'look-{tag}.jpg'))}
    json.dump(key, open(os.path.join(J, f'key-{tag}.json'), 'w'), indent=1)
    print(f'written: judge/outlines-{tag}.jpg, judge/look-{tag}.jpg, judge/key-{tag}.json')
