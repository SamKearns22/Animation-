#!/usr/bin/env python3
"""Pre-flight: catch problems before the animatic, not after the final render (lesson of The Patriots 2, which
took many renders because faults were found by eye, one round at a time).

Works on any film module that has frame_image(t) and SHOTS [(name, start, end)], plus optionally caption_at(t)
and BLACK_AT / DUR. It:
1. turns on the figure guard (every arm drawn is measured; see figure.py) and runs every module-level check;
2. draws every 3rd frame small and quick, so any check inside the drawing code (overlaps, fingertips on the
   keyboard, feet on the floor, unreachable hands) fires now, with the time of the frame;
3. checks the captions: at most 700 px wide in at most 2 rows of 42 characters, on screen long enough to read
   (about 17 characters a second at most), never empty between pieces of one line;
4. checks shot lengths (over 8 s is flagged, so a long single shot is a choice, not an accident);
5. makes a contact sheet (one frame a second, safe-area guides drawn on) to look at once, instead of renders.

Usage:
    python3 preflight.py patriots2 OUT_DIR            before the animatic: stops at the first fault
    python3 preflight.py patriots2 OUT_DIR --audit    list every fault (for a finished film)
"""
import importlib
import os
import sys
import traceback

from PIL import Image, ImageDraw, ImageFont

import burnham as B
import figure as F

SAFE = (60, 310, 900, 1500)
MAX_SHOT = 8.0


def main():
    name, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    audit = '--audit' in sys.argv              # list every fault instead of stopping at the first
    if audit:
        F._ALLOW.append('audit of a finished film')
    film = importlib.import_module(name)        # module-level checks (set plans, overlaps) run on import
    F.guard(B)
    if hasattr(film, 'checks'):                 # the film's own plan checks (overlaps, outfits...)
        film.checks()
    end = getattr(film, 'BLACK_AT', getattr(film, 'DUR', 0))
    if not end:                                 # a film without an end time would pass having checked nothing
        sys.exit('preflight: the film module needs BLACK_AT or DUR (its length in seconds)')
    fps = getattr(film, 'FPS', 12)
    problems = []
    B.SS = 1
    # 2. every 3rd frame, small: the checks inside the drawing code
    for i in range(0, int(end * fps), 3):
        t = i / fps
        shot = next((s[0] for s in getattr(film, 'SHOTS', []) if s[1] <= t < s[2]), '')
        F.CONTEXT['where'] = f'{shot} {t:.2f}s'
        try:
            film.frame_image(t)
        except Exception as e:
            problems.append(f'{t:6.2f} s: {e}')
            if not isinstance(e, ValueError):
                traceback.print_exc()
    F.CONTEXT['where'] = ''
    # 3. captions
    f = ImageFont.truetype(B.SANS, 50)
    seen = {}
    if hasattr(film, 'caption_at'):
        for i in range(int(end * fps)):
            c = film.caption_at(i / fps)
            if c:
                seen.setdefault(c, []).append(i / fps)
    for c, ts in seen.items():
        rows = B.wrap(c, f, 700)
        wide = max(f.getbbox(r)[2] for r in rows)
        if len(rows) > 2 or wide > 700 or max(len(r) for r in rows) > 42:
            problems.append(f'caption "{c}": {len(rows)} rows, {wide} px wide (max 2 rows, 700 px, 42 characters)')
        dur = len(ts) / fps
        words = len(c.split())
        if dur < 0.8 or words / max(dur, 0.01) * 60 > 220:   # BBC/Netflix aim at 160-180 words a minute (verbatim speech may run faster)
            problems.append(f'caption "{c}": {dur:.1f} s on screen for {words} words (too fast to read)')
    # 4. shot lengths
    for s in getattr(film, 'SHOTS', []):
        if s[2] - s[1] > MAX_SHOT:
            problems.append(f'shot {s[0]} ({s[1]:.1f}-{s[2]:.1f} s) is {s[2] - s[1]:.1f} s long (over {MAX_SHOT:.0f} s: '
                            f'fine only if chosen, e.g. an unbroken speech)')
    # 5. contact sheet with the safe area drawn on
    tiles = []
    logged = len(F.LOG)                         # the sheet's frames repeat ones already checked
    for k in range(int(end)):
        t = k + 0.5
        im = film.frame_image(t).convert('RGB').resize((B.W, B.H))
        d = ImageDraw.Draw(im, 'RGBA')
        for box in ((0, 0, 1080, SAFE[1]), (0, SAFE[3], 1080, 1920), (SAFE[2], 864, 1080, SAFE[3])):
            d.rectangle(box, fill=(255, 0, 0, 60))
        d.rectangle(SAFE, outline=(0, 255, 0, 255), width=5)
        d.text((20, 1840), f'{t:.1f} s', font=ImageFont.truetype(B.SANS, 60), fill=(255, 255, 255))
        tiles.append(im.resize((216, 384)))
    cols = 10
    sheet = Image.new('RGB', (cols * 216, ((len(tiles) + cols - 1) // cols) * 384), (20, 20, 20))
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % cols) * 216, (i // cols) * 384))
    sheet.save(os.path.join(out, f'{name}-preflight.jpg'), quality=85)
    del F.LOG[logged:]
    F.report()
    print(f'{len(problems)} problem(s)')
    for p in problems:
        print(' -', p)
    print('contact sheet:', os.path.join(out, f'{name}-preflight.jpg'))


if __name__ == '__main__':
    main()
