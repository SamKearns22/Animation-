# Craft-step2: learn step results (craft chat 7, 17 Nov; changes nothing)
- **Built:** `rough.py board FILM OUT.jpg [--root DIR]` draws every shot in the film's SHOTS through its own picture(t)
  (in its own process, so an older checkout draws with its own kits): start, key beat, end, next shot's first frame;
  app-safe box and thirds drawn over; a plan row per shot from story/FILM-board.txt (missing fields printed "not
  planned"). Kittest `shot_board_every_shot` passes; `rough_of_every_new_thing` still passes. No rule, gate or
  preflight changed.
- **Drawn from:** Remakes at 3a820183 (the film file, 14 shots, before animatic 1's notes); Blessed at fcf09cda (moves
  built, before notes 4-46; only cast notes 1-3 came before). Times: Remakes 1 min 49 s, Blessed 1 min 22 s.
- **Count** (a fresh helper that did not draw them, the 23 census notes for these films; table in
  `learn/judge.md` here, 1 min 40 s): shown 15, flagged 2 (11, Remakes 63), not shown 6 (17a pop-in, 30
  Walliams not yet in the plan, Remakes 47 duration, 61 reverse added later, 71 change of mind, 75 banner from a later
  version). Blessed 10 of 13, Remakes 5 of 10. Step 1 forecast for these two films: 11 (still+plan 10, plus Remakes 47);
  the board also showed 18, 32, 33, 37, 46 (the next-shot frame showed the gates jump) and missed 47.
- **Limit (named):** the helper knew each note before looking, so 15 is the most the board could have shown, not what
  Sam would have spotted unprompted. EPR (13 notes, 10 moving-only) was not drawn; across all 36 the reach stays about
  half.
- **F8 [found in building, named]:** the board uses the film's own drawing, so it cannot exist before the film file;
  the gate's "sent after the film's code was first committed" cannot be met. Changed in the wording for Sam: the board
  is drawn once people are placed, and must be delivered before the first move is built.
- **Chat cost:** about 0.7% of a week at the count (estimate was 0.5%; most is reading, not drawing).
- **The helper's gaps (for the build after Sam's yes):** cast against the brief per row; camera height and direction
  marked; measured subject size, off-centre and empty share; a continuity strip for repeated props.
- **Rule-11 wording sent to Sam (17 Nov), Q1:** "Before any movement is built, every shot in the film is drawn on one
  board by the film's own drawing: its real camera, its cast at their marks and true heights, at the start, the key
  moment and the end, with the next shot's first frame beside it, and the app's button area and the thirds marked.
  Under each shot is a row: camera height and distance and why, how tall the lead is on screen, where the eye goes and
  where it goes in the next shot, what must match across the cut, and that shot's open choices as numbered questions. A
  quick rough of every new person, place and move still goes on one sheet before it is built. Each is sent once: notes
  on it are acted on, never sent again. A sheet counts as sent only once it has reached you." Rule 10 gains: "these are
  written in the board's row (rule 11)." Check column (to build): preflight reads the board record: refuses if a shot
  is missing from a delivered board, a shot has nobody in its cast, or the board was delivered after the first move was
  built; `rough.py board FILM OUT.jpg`.
- **Q2 sent:** board notes counted apart from "at most 3" (pick N, counted apart).
