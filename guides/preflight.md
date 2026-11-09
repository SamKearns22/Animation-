# Pre-flight: get it right before the first render

Every lesson moved to the start, where a fix costs minutes. Use it for every film, with `guides/figure-rig.md` (bodies
and movement) and the rulebook, `guides/film-quality-rules.md`. (The Patriots 2 table of where each lesson came from
is in git history.)

**Contents:** Stage 1 the brief · Stage 2 the model sheet and storyboard · Stage 3 before the first animatic
(automatic) · Stage 4 recordings · Stage 5 the final render.

## Stage 1: the brief (one message of questions, each with a recommended answer)
- **Timing:** natural pace from Sam's own (3.0-3.6 words a second); estimate the length from the script and say
  plainly if it will run long (The Patriots 2 was briefed at 38 s and came to 60 s).
- **Locations and set dressing:** for every place, the everyday items it would have, generic, with where they sit
  (business meeting: laptops, pens and paper, water glasses, a digital whiteboard, cabinets; ambulance: oxygen
  cylinder, labelled drawers, kit bags, sharps bin, drip bag, blue lights through a frosted window).
- **Recurring objects:** list anything seen in more than one shot (a vehicle, a chair) and its size against its
  people, so it is drawn once and never resized.
- **One plan per location:** the room's layout (walls, window, door, furniture) and a plan of every table or desk,
  so all cameras show the same place. Say which shots are reverse angles.
- **Cast list:** every person, with age, build, skin, hair, clothes, and what they are doing in each shot (every
  background person has a clear action); anyone lying down, seated or walking flagged, so their views are
  designed up front.
- **Real groups and places:** check sources before drawing (official figures, reporting); say what was checked.
- **Props at real size and working height** (desks, counters, trolleys at the user's waist).
- **Audio:** who records which lines; the file naming rule below; whether non-speech sounds (a choke, a gurgle)
  are recorded or made in code.
- **Anything to avoid** (people, symbols, jokes).

## Stage 2: the model sheet and storyboard
- A **model sheet** of each new character (front, side and back, rule 38; seated or lying if the script needs it)
  at the series' proportions, alongside the storyboard; approved together.
- The storyboard shows each set from its main camera and each reverse angle, drawn from the same plan.
- Look at the sheet for: legs and feet on everyone; hands on things (keys, rails); faces readable at phone size;
  lettering and badges clear of arms.

- **An action list for every figure:** one sentence each ("hiding under a chair, head under the seat, shaking"), with
  where they are in the frame. Sam reads it with the storyboard; anything he can't picture is redrawn before animating.
- **A composition check per shot:** the busiest actions spread across the frame, none piled in one corner.

## Stage 3: before the first animatic (automatic)
`python3 source/preflight.py FILM OUT_DIR` (all cores; the full list of what it runs: `guides/satire.md`, "Before every
render"). It runs only the checks for what the film contains (`HAS` in the film: people, rooms, voices, effects,
props; rule 58) and says which it skipped. It draws every 3rd frame (the checks inside the drawing code), checks the
hands on every frame, checks captions (2 rows of 42 characters, 700 px, readable speed) and shot lengths (over 8 s is
flagged), and makes a contact sheet with the safe area. A film needs `BLACK_AT` or `DUR`.
- **The render lock (rule 59):** pre-flight leaves a pass stamp for the code as it is now. The animatic and the final
  refuse to start without it, or after any code change since; faults already named to Sam need `--faults-named`.
  So a failed pre-flight can never be followed by a render in the same command.
- **Hands (rule 41):** `source/handcheck.py` probes everyone `views.person` draws, every frame. Meant exceptions in the
  film's `HANDS_OK` [(who, side, kind, t0, t1, why)]. Alone: `python3 source/handcheck.py FILM [OUT] [--span T0 T1]`.
- **Looks (rule 43):** log each look with `filmkit.eyeline(..., aim=YAW_TO_TARGET, drawn=j2, at=NAME)`; meant looks
  away in `LOOKS_OK`, passed as `check_eyelines(allow=LOOKS_OK)`; `filmkit.look_sheet(picture, records, OUT)`.
- **Poses (rule 42):** pick from `guides/pose-gallery.md`; a new pose goes through `source/posegallery.py` first.
- **In front and behind (rule 57):** the film's `draw_order(t)` (names, back to front); planned swaps in `ORDER_SWAPS`.
- **After an edit to one action:** `python3 source/FILM.py check` (seconds to minutes), then ONE small sheet
  (`python3 source/sheet.py FILM TIMES...`, rule 48).
- **Tests:** `python3 source/kittests.py` after any change to a shared check (a few minutes).
- **Then review the motion yourself before sending:** a strip of frames across every shot, every corner (a frozen
  figure, a clip, an empty or crowded corner shows only in motion).

## Stage 4: recordings
- **Naming:** Sam names each file with its script line number first (`03 people.m4a`, `04 traitors.m4a`; extra
  takes `03b ...`; sounds `S1 choke.m4a`). Without speech recognition here, the name is what identifies a take.
- Run `python3 voices.py FILES --script script.txt` the moment they arrive: it reports **duplicates** (two names,
  one take: it happened twice on The Patriots 2), each file's length, phrases and syllables, and each script
  line's expected length. Ask Sam about any duplicate or any file whose length doesn't fit its line, before
  building. Once the film's `LINES` hold the takes, `python3 voices.py --film FILM` checks each take phrase by
  phrase against the script, the subtitles against the script, and the drawn mouths against the voice (rule 7;
  pre-flight runs it).
- Clean and level (mossad_audio.line), play exactly as recorded (volume only), captions follow what was said.
- Silences between phrases may be shortened (never the words) to tighten the film.

## Stage 5: the final render
- One final render, checked against the safe-area guides (title, widest caption, busiest frame).
- Deliver in the chat, save in `animations/`, update `story/status.md`, propose new lessons to Sam (a rule goes in the rulebook on his yes).
