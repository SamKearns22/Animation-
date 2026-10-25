#!/usr/bin/env python3
"""benchmark: the reference benchmark sheet (guides/film-quality-rules.md, rule 3), before Sam sees any place.

Why: places drawn from memory came out wrong (the lion had a hole; Trafalgar Square was missing its kerbs and traffic).
Rule 3: list the 8-10 things that make a place recognisable, put our first picture beside Sam's reference on one sheet
and tick each; build whatever is missing before Sam sees it; no references yet: stop and ask.

A film gives BENCHMARK, one entry per place:
  dict(place='kitchen', refs=['kitchen-1.jpg', ...], at=17.0,                 refs: in references/<NAME>/ (or a path
       items=[('island with a dark slate-like top', 'island_parts'),           from the repo's top); at: the film
              ('herringbone wood floor', 'left out: the brief asks for tiles'), time of our picture of it
              ('brass globe pendants', ''), ...])
  Each item: (what makes the place recognisable, how ours has it). Blank = not done yet: a fault. Anything written
  ("done: ...", "left out: why") counts as decided, so the sheet says why something is missing.

    python3 source/benchmark.py FILM OUT.jpg       the sheet (our frame, the references, the ticked list per place)
Pre-flight runs faults(film): no BENCHMARK, a place without references, fewer than 8 items, or an item left blank.
"""
import importlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
FONT = os.path.join(HERE, 'fonts', 'DejaVuSans-Bold.ttf')
FEWEST, MOST = 8, 10


def _ref_path(film, r):
    for p in (os.path.join(ROOT, 'references', getattr(film, 'NAME', ''), r), os.path.join(ROOT, r), r):
        if os.path.exists(p):
            return p
    return None


def faults(film):
    """Rule 3's faults as lines (empty when every place is benchmarked and every item decided)."""
    bm = getattr(film, 'BENCHMARK', None)
    if bm is None:
        return ['benchmark (rule 3): the film has no BENCHMARK (8-10 things per place, our picture beside the '
                'references; source/benchmark.py)']
    out = []
    for e in bm:
        p = e.get('place', '?')
        refs = e.get('refs', [])
        if not refs:
            out.append(f'benchmark: {p} has no references: stop and ask Sam for some (rule 3: never from memory)')
        for r in refs:
            if _ref_path(film, r) is None:
                out.append(f'benchmark: {p}: reference {r} not found (references/{getattr(film, "NAME", "")}/)')
        items = e.get('items', [])
        if len(items) < FEWEST:
            out.append(f'benchmark: {p} lists {len(items)} thing(s) that make it recognisable (rule 3: 8-10)')
        blank = [w for w, how in items if not (how or '').strip()]
        if blank:
            out.append(f'benchmark: {p}: not built yet: ' + '; '.join(blank))
    return out


def sheet(film, out):
    """One sheet: a row per place with our frame, up to three references and the list, each item ticked or crossed."""
    B = getattr(film, 'B', None)
    if B is not None:
        B.SS = 1
    rows = []
    f, fs = ImageFont.truetype(FONT, 26), ImageFont.truetype(FONT, 20)
    for e in film.BENCHMARK:
        h = 640
        tiles = []
        draw = getattr(film, 'picture', None) or film.frame_image   # without captions
        ours = draw(e.get('at', 0.0)).convert('RGB')
        ours.thumbnail((h, h))
        tiles.append(('ours', ours))
        for r in e.get('refs', [])[:3]:
            p = _ref_path(film, r)
            if p:
                im = Image.open(p).convert('RGB')
                im.thumbnail((h, h))
                tiles.append((os.path.basename(r), im))
        wide = sum(im.width for _, im in tiles) + 20 * len(tiles) + 780
        row = Image.new('RGB', (wide, h + 60), (250, 248, 242))
        d = ImageDraw.Draw(row)
        x = 10
        for lab, im in tiles:
            row.paste(im, (x, 50))
            d.text((x, 14), lab, font=fs, fill=(30, 30, 34))
            x += im.width + 20
        d.text((x, 10), e.get('place', '?').upper(), font=f, fill=(30, 30, 34))
        for i, (what, how) in enumerate(e.get('items', [])):
            done = bool((how or '').strip())
            y = 56 + i * 56
            d.text((x, y), ('[x] ' if done else '[ ] ') + what[:58], font=fs,
                   fill=(30, 110, 40) if done else (190, 30, 30))
            d.text((x + 40, y + 24), (how or 'NOT BUILT YET')[:64], font=fs, fill=(110, 110, 110))
        rows.append(row)
    W = max(r.width for r in rows)
    img = Image.new('RGB', (W, sum(r.height for r in rows)), (250, 248, 242))
    y = 0
    for r in rows:
        img.paste(r, (0, y))
        y += r.height
    img.save(out, quality=86)
    return out


def main():
    film = importlib.import_module(sys.argv[1])
    for x in faults(film):
        print(x)
    if len(sys.argv) > 2 and getattr(film, 'BENCHMARK', None):
        print('sheet:', sheet(film, sys.argv[2]))


if __name__ == '__main__':
    main()
