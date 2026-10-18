#!/usr/bin/env python3
"""Side by side with the reference, before Sam sees it (Sam, 18 Oct: the scooters took three goes, Farage several).
Puts a reference photo and our drawing next to each other at the same height on one sheet, with faint guide lines
across both every 5% of the height (bolder every 25%), so heights (hairline, brows, eyes, nose, mouth, chin; a
scooter's seat and handlebars) can be compared straight across. Optional crops pick the matching part of each.

    python3 source/compare.py REF.jpg OURS.png OUT.jpg [--ref-crop x0,y0,x1,y1] [--ours-crop x0,y0,x1,y1] [--h 900]

Then write down, before sending anything: what the reference shows (how many, colours, positions, which way they
face, brands, proportions as measured on the guides) and, for each, whether ours matches. Fix every mismatch first.
"""
import sys

from PIL import Image, ImageDraw


def sheet(ref, ours, out, ref_crop=None, ours_crop=None, h=900):
    a = Image.open(ref).convert('RGB')
    b = Image.open(ours).convert('RGBA')
    bg = Image.new('RGBA', b.size, (255, 255, 255, 255))
    bg.alpha_composite(b)
    b = bg.convert('RGB')
    if ref_crop:
        a = a.crop(ref_crop)
    if ours_crop:
        b = b.crop(ours_crop)
    a = a.resize((max(1, int(a.width * h / a.height)), h))
    b = b.resize((max(1, int(b.width * h / b.height)), h))
    im = Image.new('RGB', (a.width + b.width + 20, h), (255, 255, 255))
    im.paste(a, (0, 0))
    im.paste(b, (a.width + 20, 0))
    d = ImageDraw.Draw(im, 'RGBA')
    for i in range(1, 20):
        y = h * i / 20
        d.line([(0, y), (im.width, y)], fill=(255, 0, 80, 150 if i % 5 == 0 else 60), width=2 if i % 5 == 0 else 1)
        d.text((a.width + 2, y - 12), f'{i * 5}', fill=(255, 0, 80, 200))
    im.save(out, quality=88)
    return out


if __name__ == '__main__':
    args = sys.argv[1:]
    opts = {}
    for flag in ('--ref-crop', '--ours-crop', '--h'):
        if flag in args:
            i = args.index(flag)
            opts[flag] = args[i + 1]
            del args[i:i + 2]
    crop = lambda s: tuple(int(v) for v in s.split(',')) if s else None
    print(sheet(*args[:3], ref_crop=crop(opts.get('--ref-crop')), ours_crop=crop(opts.get('--ours-crop')),
                h=int(opts.get('--h', 900))))
