# Where the project stands (handover for a new session)

Read this first in any new session, after CLAUDE.md.

## Done
- **Animation test (6 s + 1.5 s black):** Shots 1-3 of `story/animation-test.md`, rendered and assembled
  with the trailer score (THUD on the cut to black). Recipes: `source/shots/s1_chop.py`, `s2_daughter.py`,
  `s3_closeup.py`. Sound: `source/animation_test_audio.py`. Joining drawings into video: `source/assemble.py`.
  Finished video: `animations/yuletide-animation-test.mp4`.
- **Look book** (`lookbook/`), **tone guide** (`guides/tone.md`), **premise and title cards**
  (`story/yuletide.md`).
- **Horror still 'Merry Chr' (spare room)** - mock-up drawn, awaiting the director's verdict. Brief and
  notes: `story/horror-merry-chr.md`. Recipe `source/shots/h1_merry_chr.py`; set `source/spare_room.py`;
  present, blood writing, wreckage, dresser things and the broken fairy lights `source/merry_chr.py`; the
  kneeling man `source/man.py`. Still: `animations/yuletide-merry-chr-still.jpg`. The shot tool now builds
  frames on other sets (`set=` in a recipe) and has a quick `animatic` mode.
- **Hair simulation** (`hair.Sim`, switched on by `hair_t` in the mother's spec): works, not yet used in a
  finished shot.

## Open
- The girl's neckline reads as a square neck (after trimming her head piece so her shoulder skin no longer
  shows through her top and hair); a round crew collar band would be nicer.
- A check in `checks.py` for skin poking through clothes (a first attempt could not tell it from the
  throat above a collar).
- Speeding up the hair grid build (~90 s per drawing).
- The parting at the mother's crown reads as a squared-off patch, and a faint bright line runs along her
  hairline, when the camera looks down on her hair.
- 'Merry Chr' next: animate it - the head strikes on the THUDs (the blotch growing with each), the fairy
  lights flashing brokenly (`merry_chr.bulb_lit(i, t)` already gives each bulb's state at time t).
- Next (director): lock a full trailer shot list timed to the finished score
  (`music/horror-trailer-score.m4a`) before building more.

## Working within the budget (director's Claude plan)
- The plan is charged for Claude's work, not render time. Keep sessions short: one piece of work per
  session, then a fresh session.
- Always make a quick animatic (quarter size, no drawing pass) before a full render; look at few images.
- Render in the background and report once at the end.
