# Where the project stands (handover for a new session)

Read this first in any new session, after CLAUDE.md.

## In progress: "Hope Again" (TikTok parody, `prompts/king-of-the-north.md`)
- Conference speech that turns into the "King in the North" scene, 11 shots, 43 s, Listening & Learning look,
  made vertical. Pictures: `source/burnham.py` (cast, armour, shots, storyboard sheet). Timeline, sound and
  render: `source/burnham_film.py` (`animatic OUT.mp4` about 8 min at half size; `final OUT.mp4`).
- Sam's recordings: `source/audio/burnham-line.m4a` (the speech), `source/audio/king-shouts.m4a` (four shouts:
  1st lowest = old knight, 2nd highest = young woman, 3rd = Miliband, 4th = Sikh knight). Crowd, swords,
  drums and horn are made in code; no show music.
- Director's decisions: title HOPE AGAIN; the only emblem is Manchester's bee; knights keep conference
  lanyards; standing ovation in waves (one, a few, all); Miliband stays seated then stands and bellows;
  all five ministers (Streeting, Rayner, Miliband, Mahmood, Healey) in varied armour in the front-on sword shot;
  ends on a slow push-in on Burnham's face with war drums, hard cut to black. Captions must be accurate.
- Notes applied after animatic 1: voices play exactly as recorded (gain only, no echo, no pitch change);
  captions follow Sam's actual words ("they were the ones who gave it away...", "KING OF THE NORTH!");
  clapping only (no crowd murmur); ending music made in code (original, ominous and regal: D minor strings, brass, low choir, timpani; replaced the battle sounds);
  Andy gestures (points, air quotes, wagging finger, hand on hip); knights each salute differently;
  the king is royal (crown, dark fur, gold chain, gilded breastplate); title centred on the frame.
- Status: animatic 2 sent 30 Sep 2026, awaiting notes. Then: final render,
  `animations/king-in-the-north-vertical.mp4` (under 25 MB), safe-area check, post text.

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
