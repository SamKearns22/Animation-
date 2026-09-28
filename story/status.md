# Where the project stands (handover for a new session)

Read this first in any new session, after CLAUDE.md.

## Done
- **Animation test (6 s + 1.5 s black):** Shots 1-3 of `story/animation-test.md`, rendered and assembled
  with the trailer score (THUD on the cut to black). Recipes: `source/shots/s1_chop.py`, `s2_daughter.py`,
  `s3_closeup.py`. Sound: `source/animation_test_audio.py`. Joining drawings into video: `source/assemble.py`.
  Finished video: `animations/yuletide-animation-test.mp4`.
- **Look book** (`lookbook/`), **tone guide** (`guides/tone.md`), **premise and title cards**
  (`story/yuletide.md`).
- **Hair simulation** (`hair.Sim`, switched on by `hair_t` in the mother's spec): works, not yet used in a
  finished shot.

## Open
- **FIRST: the mother's right wrist is bent unnaturally in almost every chop** (director's note). Measured
  over every drawing: Shot 1 bends 30-45 deg up/down all the time and sits at the 25 deg sideways limit in
  14 of 32 drawings (every impact and the rest after); Shot 2 35-50 deg; Shot 3 50 deg at the start, fine
  (10 deg) only in the raised hold, where the blade was allowed to tip and turn with her arm
  (`raised_cleaver` in `s3_closeup.py`). A natural chop keeps the wrist within about 20 deg (more only when
  cocked back at the top of a lift) and never at its sideways limit.
  Cause: every recipe fixes the cleaver's angle and the hand's grip on the handle, so the wrist takes up
  all the difference. Fix: in every frame, turn the cleaver (tilt about its edge, pitch, turn about the
  vertical) to suit her forearm so the wrist stays near straight, keeping the edge square across the ham at
  each impact so the slices stay clean; tighten `checks.py` to about 30 deg up/down and 15 deg sideways for
  the chopping hand. Then re-render Shots 1-3 (animatic first) and rebuild
  `animations/yuletide-animation-test.mp4`.
- The girl's neckline reads as a square neck (after trimming her head piece so her shoulder skin no longer
  shows through her top and hair); a round crew collar band would be nicer.
- A check in `checks.py` for skin poking through clothes (a first attempt could not tell it from the
  throat above a collar).
- Speeding up the hair grid build (~90 s per drawing).
- The parting at the mother's crown reads as a squared-off patch, and a faint bright line runs along her
  hairline, when the camera looks down on her hair.
- Next (director): lock a full trailer shot list timed to the finished score
  (`music/horror-trailer-score.m4a`) before building more.

## Working within the budget (director's Claude plan)
- The plan is charged for Claude's work, not render time. Keep sessions short: one piece of work per
  session, then a fresh session.
- Always make a quick animatic (quarter size, no drawing pass) before a full render; look at few images.
- Render in the background and report once at the end.
