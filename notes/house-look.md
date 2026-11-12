# House look: paper, edges, shadows, on twos (Sam, 12 Nov: Y to all)

## Brief checklist (Sam's words, ticked when built)
- [x] Paper texture on every film, drawings only (never captions, Hook Text, sign-off). Sam, 12 Nov: "looks a bit less AI".
- [x] Jerky steps kept: 12 drawings a second, each held 2 frames in the 24 fps file (already how the satire films are made).
- [x] Strength as tested (grain + soft blotches, 70% soft light); a single setting so it can be changed.
- [x] Per-shape paper edges (thin light top edge) and soft shadows (down and right, where shapes overlap), done on each shape, not from outlines.
- [ ] Then write rule S7 "House look" (replaces old S7, no shorthand merged in) in `guides/film-quality-rules.md`; trim the duplicate in `guides/satire.md` "The look". Check: engine applies it once; pre-flight confirms frames in pairs.

## Where things stand (12 Nov, chat 2 of 8, FINISHED)
- Sam said Y to all (12 Nov) and "put it over the sign off": clip 3 matched his test; the paper depth is 0.45.
- Done: `HOUSE_LOOK = True` in `film_engine`; the sign-off is laid on the same paper (`signoff.py`); rule S7 written
  in the rulebook (replaces the old shorthand row; that rule lives on in `guides/satire.md` "The look"); satire.md
  and the kit catalogue updated; rule 86 carries the lesson (keep Sam's test, compare side by side); CLAUDE.md and the
  rulebook's chat row now say chats open the next chat themselves and Sam never types a prompt (his note 5).
- Open rule requests: none. Needs Sam: nothing.
- For Claude: films not on `film_engine.render` (bayeux, trailer, motion-led) don't get the look yet. The old S7
  shorthand check (`viewchecks.shape_faults`) still runs but its rulebook row is gone: name it in the next audit.
