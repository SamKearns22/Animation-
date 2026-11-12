# House look: paper, edges, shadows, on twos (Sam, 12 Nov: Y to all)

## Brief checklist (Sam's words, ticked when built)
- [x] Paper texture on every film, drawings only (never captions, Hook Text, sign-off). Sam, 12 Nov: "looks a bit less AI".
- [x] Jerky steps kept: 12 drawings a second, each held 2 frames in the 24 fps file (already how the satire films are made).
- [x] Strength as tested (grain + soft blotches, 70% soft light); a single setting so it can be changed.
- [x] Per-shape paper edges (thin light top edge) and soft shadows (down and right, where shapes overlap), done on each shape, not from outlines.
- [ ] Then write rule S7 "House look" (replaces old S7, no shorthand merged in) in `guides/film-quality-rules.md`; trim the duplicate in `guides/satire.md` "The look". Check: engine applies it once; pre-flight confirms frames in pairs.

## Where things stand (12 Nov, chat 2 of 8, after Sam's note)
- Rules that bite next: 30 (a repeat note: find why first), 13 (checks in the shared kit), 61 (read the MAP).
- Sam's note 1 (12 Nov): "far more smudged than the test; makes no sense to build something that doesn't match it".
  Why: the test's paper picture was never saved; the build re-made it from the one-line recipe and got the mix
  backwards (blotches 0.09 v 0.04, grain 0.05 v 0.11). Fixed: `house_look.paper` now runs the test's exact ffmpeg
  steps (measured equal). Clip 2 sent (`review/house-look-side-by-side-2.mp4`, not on GitHub).
- Still different from the test, on purpose (brief): edges and shadows are per shape, not traced from outlines.
- Done: `source/house_look.py`, engine, pre-flight `look_faults`, kittest `house_look_once_in_pairs` (passes).
- Switch: `film_engine.HOUSE_LOOK = False` until Sam's Y.
- Next (on Sam's Y): Sonnet, medium: set HOUSE_LOOK = True, write S7 (below), trim `guides/satire.md` "The look"
  ("no gradients or glows" excepts the house look), catalogue row. On N: Opus medium, a new chat with his notes.
- Needs Sam: 1 Y/N clip 2; 2 Y/N the 24-a-second films stay smooth; 3 Y/N S7 wording; 4 Y/N lesson (below).
- Open rule request (lesson, proposed): merged into rule 86 (tools): "A test shown to Sam is saved as made (its files
  and code); the build reuses it and is checked against it, side by side, before it goes to Sam."
- Proposed S7 (replaces the shorthand row; that rule stays in `guides/satire.md` "The look" and its check still runs):
  "House look: every drawing laid on paper (grain and soft blotches, soft light 70%); each shape a thin light top edge
  and a soft shadow down-right onto what it lies on (thin things none); captions, Hook Text and sign-off clean on top;
  12 drawings a second, each held 2 frames of a 24 fps file (a film drawn at 24 says why). Laid once, by the engine."
  Check: `film_engine.look_faults` (pre-flight); kittest `house_look_once_in_pairs`.
- Read: the Final and posting pack is not needed; just this section and `source/film_engine.py` MAP.
- For Claude: side-by-side = `notes/house-look/side-by-side.py T0 T1 OUT` (run from source/). Films not on
  film_engine.render (bayeux, motion-led) don't get the look yet.
