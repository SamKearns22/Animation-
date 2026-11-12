# House look: paper, edges, shadows, on twos (Sam, 12 Nov: Y to all)

## Brief checklist (Sam's words, ticked when built)
- [x] Paper texture on every film, drawings only (never captions, Hook Text, sign-off). Sam, 12 Nov: "looks a bit less AI".
- [x] Jerky steps kept: 12 drawings a second, each held 2 frames in the 24 fps file (already how the satire films are made).
- [x] Strength as tested (grain + soft blotches, 70% soft light); a single setting so it can be changed.
- [x] Per-shape paper edges (thin light top edge) and soft shadows (down and right, where shapes overlap), done on each shape, not from outlines.
- [ ] Then write rule S7 "House look" (replaces old S7, no shorthand merged in) in `guides/film-quality-rules.md`; trim the duplicate in `guides/satire.md` "The look". Check: engine applies it once; pre-flight confirms frames in pairs.

## Where things stand (12 Nov, chat 2 of 8)
- Rules that bite next: 13 (checks live in the shared kit), 30 (a repeat note: find why first), 61 (read the MAP).
- Done: built and tested. `source/house_look.py` (paper, light top edges, soft shadows, per flat-colour shape; one
  LOOK setting); `film_engine.render` lays it once per drawing before captions and writes 12-a-second films as 24 fps
  with pairs; pre-flight's `look_faults`; kittest `house_look_once_in_pairs` (all kittests pass). Shadow flicker on
  the checked shirt found and fixed (near-equal shapes fade, never flip). Side-by-side clip sent (10-22 s, 2 MB).
- Switch: `film_engine.HOUSE_LOOK = False` until Sam's Y, so no render changes look by surprise.
- Next (on Sam's Y): Sonnet, medium. Set HOUSE_LOOK = True; write S7 (wording below); trim `guides/satire.md` "The
  look" ("no gradients or glows" now excepts the house look's shadows); kit catalogue row. On N: Opus medium, his notes.
- Needs Sam: Y/N on the side-by-side; Y/N Flying Whales and Elder Swindon stay smooth (SMOOTH_WHY added).
- Proposed S7 (replaces the shorthand row; that rule stays in `guides/satire.md` "The look" and its check still runs):
  "House look: every drawing laid on paper (grain and soft blotches, soft light 70%); each shape a thin light top edge
  and a soft shadow down-right onto what it lies on (thin things none); captions, Hook Text and sign-off clean on top;
  12 drawings a second, each held 2 frames of a 24 fps file (a film drawn at 24 says why). Laid once, by the engine."
  Check: `film_engine.look_faults` (pre-flight); kittest `house_look_once_in_pairs`.
- Read: the Final and posting pack is not needed; just this section and `source/film_engine.py` MAP.
- For Claude: side-by-side = `notes/house-look/side-by-side.py T0 T1 OUT` (run from source/). Films not on
  film_engine.render (bayeux, motion-led) don't get the look yet.
