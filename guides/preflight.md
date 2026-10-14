# Pre-flight: get it right before the first render

We make these films almost daily. The Patriots 2 needed many full renders because faults were found by eye after
each one. This checklist moves every lesson we learned to the start, where a fix costs minutes. Use it for every
film, with `guides/figure-rig.md` (bodies and movement) and `guides/best-practice.md` (the master file).

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
- A **model sheet** of each new character (front, three-quarter, profile; seated or lying if the script needs it)
  at the series' proportions, alongside the storyboard; approved together.
- The storyboard shows each set from its main camera and each reverse angle, drawn from the same plan.
- Look at the sheet for: legs and feet on everyone; hands on things (keys, rails); faces readable at phone size;
  lettering and badges clear of arms.

- **An action list for every figure:** one sentence each ("hiding under a chair, head under the seat, shaking"), with
  where they are in the frame. Sam reads it with the storyboard; anything he can't picture is redrawn before animating.
- **A composition check per shot:** the busiest actions spread across the frame, none piled in one corner.

## Stage 3: before the first animatic (automatic)
`python3 preflight.py FILM OUT_DIR` runs everything below on every third frame and makes a contact sheet with the
safe area drawn on; fix whatever it reports, then render the animatic.
- Arms: the guard (no limb longer than the rig; hands that can't reach are errors).
- Contacts: fingertips on keys, feet on floors, hips on seats.
- Sets: listed set pieces never overlap; desk items from one plan.
- Captions: at most 2 rows of 42 characters within 700 px; readable speed.
- Shots over 8 s are flagged (keep only the chosen ones, such as an unbroken speech).
- People: footprints never overlap along their paths (except named pairs); feet on the floor even when leaning; nobody
  scaled away from the cast's size.
- **Then review the motion yourself before sending:** a strip of frames across every shot, looking at every corner (a
  frozen figure, a clip, an empty or crowded corner shows only in motion, never in one still).

## Stage 4: recordings
- **Naming:** Sam names each file with its script line number first (`03 people.m4a`, `04 traitors.m4a`; extra
  takes `03b ...`; sounds `S1 choke.m4a`). Without speech recognition here, the name is what identifies a take.
- Run `python3 voices.py FILES --script script.txt` the moment they arrive: it reports **duplicates** (two names,
  one take: it happened twice on The Patriots 2), each file's length, phrases and syllables, and each script
  line's expected length. Ask Sam about any duplicate or any file whose length doesn't fit its line, before
  building.
- Clean and level (mossad_audio.line), play exactly as recorded (volume only), captions follow what was said.
- Silences between phrases may be shortened (never the words) to tighten the film.

## Stage 5: the final render
- One final render, checked against the safe-area guides (title, widest caption, busiest frame).
- Deliver in the chat, save in `animations/`, update `story/status.md`, add new lessons to the master file.

## The lessons this checklist comes from (The Patriots 2)
| Fault found late | Now caught at |
|---|---|
| Legs missing on people at frame edges | figure-rig: legs always drawn (person() refuses otherwise) |
| Arms too long; hands to the knees | figure guard + rig (stage 3) |
| Trolley at knee height | brief: props at working height; rail pose at the waist |
| Fingertips on the desk, not the keys | contact check (stage 3) |
| Mouth moving under the balaclava while typing | figure-rig 6: a heard letter is not spoken |
| Reverse shot showed a different room | brief: one plan per location |
| Desk items changed between shots | brief: desk plan; one plan drawn by every camera |
| A monitor through a curtain | set pieces listed and checked (stage 3) |
| Uniform stripes drawn over arms | figure-rig 5: garment details before the arms |
| Beer can wobbling with no cause | storyboard look: every movement needs a visible cause |
| Women in the boat without headscarves | brief: real groups checked against sources |
| Grey "beads" in young men's hair | brief: hair designed per person on the model sheet |
| Lying patient sliding off the bed; no face profile | model sheet: lying view designed up front |
| Doctor resembling a real politician | model sheet: compared with the series' existing caricatures |
| Mislabelled and duplicate recordings | stage 4: naming rule and voices.py |
| A caption on three rows | stage 3 caption check |
| Lifeboat a different size in the next scene | brief: recurring objects listed; one drawing at a fixed size relative to its people |
| Chair seat floating, stand too thin | figure-rig: seated hips on the seat; under-desk knee space drawn |
| Film much longer than briefed | brief: honest length estimate from the pace |

## Added 8 Oct (Russiadent Evil): general audits, parallel run, picture cache
- `python3 source/preflight.py FILM OUT_DIR` now uses every processor core (the film took 19 minutes on one) and, if the
  film defines `checks()` and `audits()`, runs them: plan checks, then the general body/movement audit
  (`source/filmkit.py`), then the permanent-marks probes. A film without an end time (`BLACK_AT` or `DUR`) is refused.
- **Audit what any body part does, not one fault:** each character alone, as a picture, over time (in pieces, pops,
  stretches, frozen). Allowed fast moves and known separate shapes (a blood pool) are listed in the film's `FAST_OK`.
- After an edit to one action: `python3 -c "import FILM as R; print(R.audits())"` (about 2 minutes), then look at ONE small strip.
- Render: `python3 source/FILM.py final OUT` (caches pictures); `... final OUT --reuse --redo none` for caption/timing notes;
  `... --reuse --redo shot1,shot2` for notes on those shots only. Sound-only notes: rebuild the sound and attach it.

