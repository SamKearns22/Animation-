# Where the project stands (handover for a new session)

Read this first in any new session, after CLAUDE.md.

## Done
- **Animation test (6 s + 1.5 s black):** Shots 1-3 of `story/animation-test.md`, rendered and assembled
  with the trailer score (THUD on the cut to black). Recipes: `source/shots/s1_chop.py`, `s2_daughter.py`,
  `s3_closeup.py`. Sound: `source/animation_test_audio.py`. Joining drawings into video: `source/assemble.py`.
  The finished MP4 goes into `animations/` once the director approves it.
- **Look book** (`lookbook/`), **tone guide** (`guides/tone.md`), **premise and title cards**
  (`story/yuletide.md`).
- **Hair simulation** (`hair.Sim`, switched on by `hair_t` in the mother's spec): works, not yet used in a
  finished shot.

## Open
- Shot 2 re-rendered after trimming the girl's head piece (her shoulder skin showed through her top and
  hair). Her neckline now reads as a square neck; a round crew collar band would be nicer.
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
