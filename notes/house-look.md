# House look: paper, edges, shadows, on twos (Sam, 12 Nov: Y to all)

## Brief checklist (Sam's words, ticked when built)
- [ ] Paper texture on every film, drawings only (never captions, Hook Text, sign-off). Sam, 12 Nov: "looks a bit less AI".
- [ ] Jerky steps kept: 12 drawings a second, each held 2 frames in the 24 fps file (already how the satire films are made).
- [ ] Strength as tested (grain + soft blotches, 70% soft light); a single setting so it can be changed.
- [ ] Per-shape paper edges (thin light top edge) and soft shadows (down and right, where shapes overlap), done on each shape, not from outlines.
- [ ] Then write rule S7 "House look" (replaces old S7, no shorthand merged in) in `guides/film-quality-rules.md`; trim the duplicate in `guides/satire.md` "The look". Check: engine applies it once; pre-flight confirms frames in pairs.

## Where things stand (12 Nov)
- Rules that bite next: 13 (checks live in the shared kit), 48 (one labelled sheet), 61 (read the MAP).
- Done: three tests sent to Sam on Remakes and Ad-vanced Notice (paper, steps, edges + shadows). Prototypes in
  `notes/house-look/` (`prototype-paper.py`, `prototype-edges.py`; the paper picture is made by the ffmpeg lines in `prototype-paper.py`'s header notes below).
- Next: NEW chat, Opus, high effort (building anything new). Type: "Build the house look: paper, edges, shadows (S7)".
  Test film: Ad-vanced Notice. Put the paper and edges in `film_engine.render` so every film gets them once; edges per shape
  (the prototype fakes them from outlines and puts a faint shadow on wires and poles). Send Sam a side-by-side clip; he says Y/N before the rule is written.
- Needs Sam: nothing yet.
- Read: the pack for building tools in `guides/job-packs.md`; `notes/house-look.md`; `source/film_engine.py` render.
- Open rule requests: S7 House look (above), written only after the build passes its checks.
- For Claude: paper picture = fixed grain (noise 90, blur 0.9, contrast 2.2) averaged with soft blotches (135x240 noise, blur 4, contrast 4, scaled up), soft light at 70%.
