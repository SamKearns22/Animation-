# Where the project stands (handover for a new session)

Read this first in any new session, after CLAUDE.md.

## Done
- **Animation test (6 s + 1.5 s black):** Shots 1-3 of `story/animation-test.md`, rendered and assembled
  with the trailer score (THUD on the cut to black). Recipes: `source/shots/s1_chop.py`, `s2_daughter.py`,
  `s3_closeup.py`. Sound: `source/animation_test_audio.py`. Joining drawings into video: `source/assemble.py`.
  Finished video: `animations/yuletide-animation-test.mp4`.
- **Look book** (`lookbook/`), **tone guide** (`guides/tone.md`), **premise and title cards**
  (`story/yuletide.md`).
- **Horror still 'Merry Chr' (spare room)** - latest mock-up (director's final verdict pending), reframed from the dark landing (level
  shift lens, doorcase border, low winter light, contrast kept for the present and the wall). Floor things are
  placed so none sits inside another; clothes drape over what is under them; checks cover this and the
  wall openings. Brief and
  notes: `story/horror-merry-chr.md`. Recipe `source/shots/h1_merry_chr.py`; set `source/spare_room.py`;
  present, blood writing, wreckage, dresser things and the broken fairy lights `source/merry_chr.py`; the
  kneeling man `source/man.py`. Still: `animations/yuletide-merry-chr-still.jpg`. The shot tool now builds
  frames on other sets (`set=` in a recipe) and has a quick `animatic` mode.
- **'Merry Chr' animated (3 s):** `animations/yuletide-merry-chr.mp4` (1.5 MB), second version. He slams his
  forehead into the r every 0.9 s like a machine, with force: pulled back ~8 cm mostly from his back, a
  2-frame strike on ones, his back crumpling into it on impact (his head snaps back against the wall), his
  shoulders thrown forward, a 3 cm bounce, dead arms swinging. The r is 45% bigger and bolder in a dense ring of
  spatter; runs and spatter down the side of the mattress and the bed rail; a normal-sized satin bow (two big loops, two small, a knot, tails) centred on a
  ribbon tied round its middle; stains soaked up ragged from below; 'To Mum x' faint on the card; drops on the floor and low on the wall from the
  en-suite, and blood on its mirror; the fairy lights on both walls flash brokenly, their glow with them.
  Director's decisions: the blood does NOT grow (he strikes the same spot), no THUD sounds (the score alone:
  `source/merry_chr_audio.py`, 41.3-44.3 s). Tools added: `shot.py animatic_sequence`, resumable
  `shot.py sequence`, a check that clothes never reach the edge of their grid (that was the 'hole' in his
  shirt).
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
- The container can restart during long renders: `shot.py sequence` now resumes (just run it again).
- Next (director): lock a full trailer shot list timed to the finished score
  (`music/horror-trailer-score.m4a`) before building more.

## Working within the budget (director's Claude plan)
- The plan is charged for Claude's work, not render time. Keep sessions short: one piece of work per
  session, then a fresh session.
- Always make a quick animatic (quarter size, no drawing pass) before a full render; look at few images.
- Render in the background and report once at the end.
