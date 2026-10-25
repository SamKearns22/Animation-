#!/usr/bin/env python3
"""catalogue: the kit catalogue's thumbnail sheet (guides/kit-catalogue.md; guides/film-quality-rules.md, rule 28):
every set, person, creature, prop and effect already built, drawn small on one sheet, so planning a film starts by
looking at what can be reused instead of reading file names.

Each entry draws itself in its own process (films patch the shared drawing code differently, so they never share
one), from its film's own picture, cast sheet or prop code; an entry that fails is a red tile saying why, never a
crash. When a film's building stage ends, add its new sets, people, props and effects here AND to the catalogue's
tables (one line each below: section, name, how to draw it).

    python3 source/catalogue.py OUT.jpg [SECTION ...]      the sheet (Sets, People, Creatures, Props, Effects)
"""
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
TILE = (300, 420)

# (section, name, file, how to draw it: ('frame', module, t) | ('cast', module) | ('fx', python drawing on img, cam))
ENTRIES = [
    ('Sets', 'London house: living room', 'prepper_set.py', ('frame', 'prepper', 29.0)),
    ('Sets', 'London house: kitchen', 'prepper_set.py', ('frame', 'prepper', 44.2)),
    ('Sets', 'London house: shot 12 (wrecked)', 'prepper_set.py', ('frame', 'prepper', 62.5)),
    ('Sets', 'Trafalgar Square', 'power_crime_set.py', ('frame', 'power_crime', 0.7)),
    ('Sets', 'Casino parlour', 'poker_mon_room.py', ('frame', 'poker_mon', 1.0)),
    ('Sets', 'Round Table (The Traitors)', 'traitors.py', ('frame', 'traitors', 21.0)),
    ('Sets', 'Hangar (Roadster)', 'roadster.py', ('frame', 'roadster', 2.0)),
    ('People', 'Andy, Wes, the robot (Prepper)', 'prepper_cast.py', ('cast', 'prepper')),
    ('People', 'Trump, Putin, Zelensky, Claudia', 'traitors_cast.py', ('cast', 'traitors')),
    ('People', 'Reform HQ five', 'shocking_cast.py', ('cast', 'shocking')),
    ('People', 'Poker players, dealer, Dragonite', 'poker_mon_cast.py', ('cast', 'poker_mon')),
    ('People', 'Old lady, Met officers, crowd', 'power_crime_cast.py', ('frame', 'power_crime', 2.5)),
    ('People', 'Press secretary, reporters', 'press_secretary.py', ('cast', 'press_secretary')),
    ('People', 'Matt Damon, the Roadster', 'roadster.py', ('cast', 'roadster')),
    ('Creatures', 'Chrome Centurion robots', 'prepper_robot.py', ('frame', 'prepper', 60.0)),
    ('Creatures', 'Horse to ride (and donkey, pony), with rider', 'mounts.py', ('frame', 'mounts', 'horse')),
    ('Props', 'Crossbow', 'prepper_fx.py', ('fx', 'X.crossbow3(img, cam, (0, 0.9, 0), 160)')),
    ('Props', 'Minigun with ammo belt', 'prepper_fx.py', ('fx', 'X.minigun3(img, cam, (0, 0.9, 0), 120)')),
    ('Props', 'Machete', 'prepper_fx.py', ('fx', 'X.machete_floor(img, cam, (0, 0.9, 0), 120)')),
    ('Props', 'Tin of beans, 2 L bottle', 'prepper_fx.py', ('fx', 'X.tin(img, cam, (-0.12, 0.9, 0)); '
                                                                     'X.bottle(img, cam, (0.12, 0.9, 0))')),
    ('Props', 'Alexa (whole, on rod legs)', 'prepper_fx.py', ('fx', 'X.alexa(img, cam, (-0.2, 0.9, 0)); '
                                                                     'X.alexa_walker(img, cam, (0.2, 0.75, 0), 0.3)')),
    ('Props', 'Mug on a coaster, steaming', 'prepper_fx.py', ('fx', 'X.coffee(img, cam, (0, 0.9, 0), 1.0)')),
    ('Effects', 'Lumpy flash (yellow, blue)', 'prepper_fx.py', ('fx', 'X.flash(img, cam, (-0.25, 1.2, 0), 0.25, 3); '
                                                                       'X.flash(img, cam, (0.25, 1.2, 0), 0.25, 5, "blue")')),
    ('Effects', 'Sparks, smoke', 'prepper_fx.py', ('fx', 'X.sparks(img, cam, 0.12, 0.0, (-0.2, 1.2, 0), 2); '
                                                           'X.smoke(img, cam, 0.6, 0.0, (0.25, 1.0, 0), 4)')),
    ('Effects', 'Plasma bolt, blade arc', 'prepper_fx.py', ('fx', 'X.plasma(img, cam, (-0.5, 1.4, 0), (0.5, 1.5, 0)); '
                                                                    'X.blade_arc(img, cam, [(-0.4, 0.8, 0), (0, 1.0, 0), (0.4, 0.9, 0)])')),
    ('Effects', 'Flames', 'prepper_fx.py', ('fx', 'X.flames(img, cam, 0.8, 0.0, (0, 0.9, 0), (0, 1, 0), 3)')),
]
SECTIONS = ['Sets', 'People', 'Creatures', 'Props', 'Effects']


def draw_one(k, out):
    """Draw entry k to the file `out` (run in a process of its own)."""
    import importlib
    section, name, path, (kind, *how) = ENTRIES[k]
    if kind == 'frame':
        m = importlib.import_module(how[0])
        if hasattr(m, 'B'):
            m.B.SS = 1
        draw = getattr(m, 'picture', None) or m.frame_image
        draw(how[1]).convert('RGB').save(out)
    elif kind == 'cast':
        m = importlib.import_module(how[0])
        if hasattr(m, 'B'):
            m.B.SS = 1
        m.cast_sheet(out)
    else:
        import burnham as B
        import prepper_fx as X           # noqa: F401  (used by the recipe)
        import sets
        B.SS = 1
        img = B.canvas((236, 232, 224))
        cam = sets.Cam((0.0, 1.15, -1.3), (0.0, 1.0, 0.0), focal=1300)
        exec(how[0], {'X': X, 'img': img, 'cam': cam})
        im = img.convert('RGB')
        from PIL import ImageChops
        box = ImageChops.difference(im, Image.new('RGB', im.size, (236, 232, 224))).getbbox() or (0, 0) + im.size
        w = max(box[2] - box[0], (box[3] - box[1]) * TILE[0] / (TILE[1] - 52)) * 1.15   # trimmed to what is drawn,
        h = w * (TILE[1] - 52) / TILE[0]                                                 # in the tile's shape
        cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
        from PIL import ImageOps
        pad = 2000                                                                       # never past the edge
        im = ImageOps.expand(im, border=pad, fill=(236, 232, 224))
        im.crop((int(cx - w / 2) + pad, int(cy - h / 2) + pad, int(cx + w / 2) + pad, int(cy + h / 2) + pad)).save(out)


def _tile(k, path, err):
    section, name, file, _ = ENTRIES[k]
    tile = Image.new('RGB', TILE, (250, 248, 242))
    d = ImageDraw.Draw(tile)
    f = ImageFont.truetype(FONT, 15)
    if err:
        tile.paste((200, 60, 60), (0, 0, TILE[0], TILE[1] - 52))
        d.text((8, 8), 'could not draw:\n' + '\n'.join(err[i:i + 34] for i in range(0, min(len(err), 238), 34)),
               font=f, fill=(255, 255, 255))
    else:
        im = Image.open(path).convert('RGB')
        im.thumbnail((TILE[0], TILE[1] - 52))
        tile.paste(im, ((TILE[0] - im.width) // 2, 0))
    d.text((6, TILE[1] - 48), name[:34], font=f, fill=(30, 30, 34))
    d.text((6, TILE[1] - 26), file, font=f, fill=(110, 110, 110))
    return tile


def sheet(out, sections=None):
    sections = sections or SECTIONS
    picks = [k for k, e in enumerate(ENTRIES) if e[0] in sections]
    tmp = tempfile.mkdtemp(prefix='catalogue-')

    def run(k):
        path = os.path.join(tmp, f'{k}.png')
        r = subprocess.run([sys.executable, os.path.abspath(__file__), '--one', str(k), path], cwd=HERE,
                           capture_output=True, text=True, timeout=600)
        err = None if r.returncode == 0 and os.path.exists(path) else \
            ((r.stderr.strip().splitlines() or ['failed'])[-1])
        return k, path, err
    with ThreadPoolExecutor(os.cpu_count() or 2) as pool:
        done = dict((k, (p, e)) for k, p, e in pool.map(run, picks))
    rows = []
    fh = ImageFont.truetype(FONT, 26)
    for sec in sections:
        ks = [k for k in picks if ENTRIES[k][0] == sec]
        if not ks:
            continue
        cols = 6
        row = Image.new('RGB', (cols * TILE[0], 44 + ((len(ks) + cols - 1) // cols) * TILE[1]), (230, 226, 218))
        ImageDraw.Draw(row).text((10, 8), sec.upper(), font=fh, fill=(30, 30, 34))
        for i, k in enumerate(ks):
            row.paste(_tile(k, *done[k]), ((i % cols) * TILE[0], 44 + (i // cols) * TILE[1]))
        rows.append(row)
    img = Image.new('RGB', (max(r.width for r in rows), sum(r.height for r in rows)), (230, 226, 218))
    y = 0
    for r in rows:
        img.paste(r, (0, y))
        y += r.height
    img.save(out, quality=84)
    failed = [ENTRIES[k][1] for k in picks if done[k][1]]
    return out, failed


def faults():
    """Each entry's file exists (a catalogue that points at nothing is worse than none)."""
    return [f'catalogue: {name}: {path} not found' for _, name, path, _ in ENTRIES
            if not os.path.exists(os.path.join(HERE, path))]


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--one':
        draw_one(int(a[1]), a[2])
    elif a:
        print('\n'.join(faults()) or 'catalogue: every file found')
        path, failed = sheet(a[0], a[1:] or None)
        print('sheet:', path, '' if not failed else f'({len(failed)} could not draw: {", ".join(failed)})')
    else:
        print(__doc__)
