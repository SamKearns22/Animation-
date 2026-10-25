#!/usr/bin/env python3
"""Pre-flight: catch problems before the animatic, not after the final render (lesson of The Patriots 2, which
took many renders because faults were found by eye, one round at a time).

Works on any film module that has frame_image(t) and SHOTS [(name, start, end)], plus optionally caption_at(t)
and BLACK_AT / DUR. It:
1. turns on the figure guard (every arm drawn is measured; see figure.py) and runs every module-level check,
   then the shared checks (housestyle: the template's style on; audit: collisions and pop-ins, from the film's
   scene(t), a FAULT if the film has none; clipcheck: solids, drawing order, teleports,
   contacts; hookcheck: the Hook Text clear of signs; musiccheck: song joins; linecheck: outlines; sizes: real
   sizes; landmarks: clothes against the body), each only if the film defines what it needs;
2. draws every 3rd frame small and quick, so any check inside the drawing code (overlaps, fingertips on the
   keyboard, feet on the floor, unreachable hands) fires now, with the time of the frame;
3. checks the captions: at most 700 px wide in at most 2 rows of 42 characters, on screen long enough to read
   (about 17 characters a second at most), never empty between pieces of one line;
4. checks shot lengths (over 8 s is flagged, so a long single shot is a choice, not an accident);
5. makes a contact sheet (one frame a second, safe-area guides drawn on) to look at once, instead of renders.
Before any of it, it REFUSES to run (rule 14) while the film's brief checklist (notes/NAME.md, "The brief as a
checklist") has a blank "done?" row, or before the composition sheet has been sent (a line "Composition sheet sent:
DATE, FILE" in the notes, rule 11); and it fails a film whose shot is missing anyone the brief puts in it (SHOT_CAST,
against the audit's roster). It prints a short summary; the full list goes to OUT_DIR/NAME-preflight.txt (rule 19).
The shared kit's checks (kitchecks.py, rule 13) run here on every film: facing on the drawing pass, marks, sounds,
and (inside the audit) hands on what they touch, props held, resting hands clear. So do viewchecks.py's (rules 15-18,
20): effect shapes, readability, direction across a cut, effects hidden behind figures, and on the drawing pass every
held prop turned through every view.

Usage:
    python3 preflight.py patriots2 OUT_DIR            before the animatic: stops at the first fault
    python3 preflight.py patriots2 OUT_DIR --audit    list every fault (for a finished film)
"""
import fnmatch
import importlib
import os
import re
import sys
import traceback

from PIL import Image, ImageDraw, ImageFont

import burnham as B
import figure as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAFE = (60, 310, 900, 1500)
MAX_SHOT = 8.0


_FILM = None
_FPS = 12


_TURNED = set()                 # (per worker) the people and props already turned through every view


def _check_frame(i):
    import kitchecks
    import viewchecks
    film = _FILM
    t = i / _FPS
    shot = next((s[0] for s in getattr(film, 'SHOTS', []) if s[1] <= t < s[2]), '')
    F.CONTEXT['where'] = f'{shot} {t:.2f}s'
    n0, d0, p0 = len(F.LOG), len(kitchecks.DRAWN), len(kitchecks.POSES)
    err = None
    try:
        film.frame_image(t)
    except Exception as e:
        err = (str(e), isinstance(e, ValueError), traceback.format_exc())
    turned = viewchecks.turn_faults(kitchecks.POSES[p0:], _TURNED)   # rule 20: every held prop through every view
    del kitchecks.POSES[p0:]
    return t, err, list(F.LOG[n0:]), list(kitchecks.DRAWN[d0:]), turned


def notes_path(film, name):
    return getattr(film, 'NOTES', None) or os.path.join(ROOT, 'notes', f'{getattr(film, "NAME", name)}.md')


def gates(film, name):
    """Rule 14: what stops pre-flight before it starts: a blank row in the brief checklist, no record of the
    composition sheet being sent. Returns the reasons (empty: go)."""
    path = notes_path(film, name)
    if not os.path.exists(path):
        return [f'no notes file ({os.path.relpath(path, ROOT)}): the brief checklist lives there (notes/_template.md)']
    text = open(path).read()
    out = []
    m = re.search(r'^## The brief as a checklist.*?$(.*?)(?=^## |\Z)', text, re.M | re.S)
    if not m:
        out.append('the notes file has no "The brief as a checklist" section (notes/_template.md)')
    else:
        rows = [ln for ln in m.group(1).splitlines() if ln.strip().startswith('|')]
        blank, filled = [], 0
        for ln in rows[2:]:                                 # past the header and the |---| line
            cells = [c.strip() for c in ln.strip().strip('|').split('|')]
            if len(cells) < 3 or not cells[1]:
                continue
            filled += 1
            if not cells[-1]:
                blank.append(f'{cells[0]} ({cells[1][:50]})')
        if not filled:
            out.append('the brief checklist is empty: copy every detail of the brief in, then tick each against the film')
        elif blank:
            out.append(f'the brief checklist has {len(blank)} blank "done?" row(s): ' + '; '.join(blank[:8]) +
                       (' ...' if len(blank) > 8 else '') + ' (tick each against the film, or say why not)')
    if not re.search(r'^\s*[-*]?\s*\**Composition sheet sent\**:\**[ \t]*[^\s(*]', text, re.M | re.I):   # not the (...)
        out.append('no record of the composition sheet being sent (rule 11): send Sam the 3-4 key shots, then add '
                   '"Composition sheet sent: DATE, FILE" to the notes file')
    return out


def cast_faults(film, roster):
    """Rule 14 / CLAUDE.md (25 Oct): every shot has everyone the brief puts in it, on screen at some point (SHOT_CAST:
    {shot: [name or pattern]}, against the audit's roster of who is on screen)."""
    want = getattr(film, 'SHOT_CAST', None)
    if want is None:
        return ['SHOT_CAST missing: list who the brief puts in each shot ({shot: [names]}); pre-flight checks each is '
                'on screen there (CLAUDE.md: no animatic while a shot is missing anyone)']
    out = []
    for shot, names in want.items():
        seen = roster.get(shot, set())
        for n in names:
            if not any(fnmatch.fnmatchcase(x, n) for x in seen):
                out.append(f'shot {shot}: {n} is never on screen (the brief puts them in it; SHOT_CAST)')
    return out


def _sheet_tile(k):
    t = k + 0.5
    im = _FILM.frame_image(t).convert('RGB').resize((B.W, B.H))
    d = ImageDraw.Draw(im, 'RGBA')
    for box in ((0, 0, 1080, SAFE[1]), (0, SAFE[3], 1080, 1920), (SAFE[2], 864, 1080, SAFE[3])):
        d.rectangle(box, fill=(255, 0, 0, 60))
    d.rectangle(SAFE, outline=(0, 255, 0, 255), width=5)
    d.text((20, 1840), f'{t:.1f} s', font=ImageFont.truetype(B.SANS, 60), fill=(255, 255, 255))
    return im.resize((216, 384))


def main():
    name, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    audit = '--audit' in sys.argv              # list every fault instead of stopping at the first
    if audit:
        F._ALLOW.append('audit of a finished film')
    film = importlib.import_module(name)        # module-level checks (set plans, overlaps) run on import
    every_film = not (name == 'quick' or getattr(film, 'QUICK', False))   # film-quality-rules: not quick videos
    stop = gates(film, name) if every_film else []   # rule 14: refuse while the brief or the sheet is not done
    if stop and not audit:
        print('pre-flight REFUSES to run (guides/film-quality-rules.md, rule 14):')
        for x in stop:
            print(' -', x)
        sys.exit(2)
    F.guard(B)
    import kitchecks
    kitchecks.install()                         # every views.py person drawn is logged for the facing check
    if hasattr(film, 'checks'):                 # the film's own plan checks (overlaps, outfits...)
        film.checks()
    shared = ['gate: ' + x for x in stop]       # the shared checks every film gets (Sam, 18 Oct: catch it before I do)
    B.SS = 1
    import audit as collisions, clipcheck, hookcheck, linecheck, musiccheck, sizes, landmarks, housestyle
    import plan, benchmark, sets
    shared += housestyle.faults(film, B)        # the template's house style is on, and each check has its inputs
    if every_film:
        shared += plan.faults(film)             # rule 1: one plan of the world in metres, joined up, a camera per shot
        shared += benchmark.faults(film)        # rule 3: each place benchmarked against its references, all decided
    shared += sets.solids_faults(film)          # rule 12: what the set's solids need (door angles, reasons)
    if getattr(film, 'PLAN', None) is not None and hasattr(film, 'cam_for'):
        shared += sets.portal_faults(film)      # rule 2: every opening shows the space beyond, never a flat colour
    roster = None
    if hasattr(film, 'scene'):
        shared += collisions.check(film)        # rules 5, 6, 12, 13: nothing passes through anything; nothing pops in;
        roster = collisions.LAST_ROSTER         # hands on what they touch, props held, resting hands clear
    if any(hasattr(film, a) for a in ('solids', 'layers', 'IN_SHOT')):
        shared += clipcheck.run(film)           # nothing passes through anything; nothing teleports; drawing order
    if not any(hasattr(film, a) for a in ('scene', 'solids')):   # never skipped in silence (Sam, 21 Oct: Power Crime
        shared.append('the collision and pop-in tests did not run: the film has no scene(t) (audit.py; '   # never ran
                      'guides/film-quality-rules.md rules 5 and 6)')                                      # them)
    if every_film:
        shared += cast_faults(film, roster or {})   # rule 14: no shot missing anyone the brief puts in it
    if hasattr(film, 'LINES'):                  # rule 7: script v recordings v subtitles, and the mouths drawn
        import voices
        shared += voices.check(film)
    if every_film:
        import viewchecks                       # rules 15-18: effect shapes, readability, direction across a cut,
        shared += viewchecks.faults(film)       # effects hidden behind figures (rule 20 runs on the drawing pass)
    shared += kitchecks.marks(film)             # rule 13: marks on real surfaces
    shared += kitchecks.sounds(film)            # rule 13: a sound tied to a thing only with it in frame, once a hit
    shared += hookcheck.faults(film)            # the Hook Text clear of the signs and readouts listed
    shared += musiccheck.faults(film)           # no beat skipped or doubled where pieces of a song are joined
    shared += linecheck.faults(film)            # every shape outlined, one line weight (the cast)
    shared += sizes.faults(film)                # props and set pieces at their real size
    shared += landmarks.faults(film)            # clothes start and end where real ones do
    print('shared checks:', 'clean' if not shared else f'{len(shared)} fault(s)')
    end = getattr(film, 'BLACK_AT', getattr(film, 'DUR', 0))
    if not end:                                 # a film without an end time would pass having checked nothing
        sys.exit('preflight: the film module needs BLACK_AT or DUR (its length in seconds)')
    fps = getattr(film, 'FPS', 12)
    problems = list(shared)
    B.SS = 1
    # 2. every 3rd frame, small: the checks inside the drawing code (all processor cores)
    global _FILM, _FPS
    _FILM, _FPS = film, fps
    drawn = []
    from multiprocessing import Pool
    with Pool(os.cpu_count()) as pool:
        for t, err, log, dr, turned in pool.imap(_check_frame, range(0, int(end * fps), 3), chunksize=4):
            F.LOG.extend(log)
            drawn += dr
            problems += [x for x in turned if x not in problems]
            if err:
                problems.append(f'{t:6.2f} s: {err[0]}')
                if not err[1]:
                    print(err[2])
    F.CONTEXT['where'] = ''
    problems += kitchecks.facing(drawn)         # rule 13: heads never turned past the body; nothing held over a back
    if hasattr(film, 'audits'):               # the film's general body / movement / marks audit (filmkit.py)
        problems += film.audits()
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
    logged = len(F.LOG)                         # the sheet's frames repeat ones already checked
    with Pool(os.cpu_count()) as pool:
        tiles = pool.map(_sheet_tile, range(int(end)))
    cols = 10
    sheet = Image.new('RGB', (cols * 216, ((len(tiles) + cols - 1) // cols) * 384), (20, 20, 20))
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % cols) * 216, (i // cols) * 384))
    sheet.save(os.path.join(out, f'{name}-preflight.jpg'), quality=85)
    del F.LOG[logged:]
    import contextlib
    import io
    import report                               # rule 19: a short summary; every fault in the file
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):       # the figure guard's log (what it allowed, how often): the file only
        F.report()
    log = buf.getvalue().splitlines()
    report.summarise(f'pre-flight ({name})', problems, os.path.join(out, f'{name}-preflight.txt'),
                     notes=(['The figure guard (allowed drawings, how often):'] + log) if log else ())
    if log:
        print(f'(the figure guard logged {len(log)} kind(s) of allowed drawing: in the file)')
    print('contact sheet:', os.path.join(out, f'{name}-preflight.jpg'))
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
