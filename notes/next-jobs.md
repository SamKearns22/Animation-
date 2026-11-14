# Where things stand (project, 14 Nov; no film in progress; the aim: films at 15% of a week)
- **Newest work:** `claude/overnight-c9-moves` (also on the main line). Item 7 closed (chat 9).
- **Rules that bite next:** 74 (the acting list: each block lands on its word), 86 (every tool gets a kittest), 85.
- **Done (chat 9, Sonnet, ~0.6%):** item 7 closed: replicate on all shots 0.000% (30 frames), sheet `notes/morning/moves-kit-replicate.jpg`, report entry with cost line. Total ~5.4% (stop 9%). Found: kittest `round_page` fails (page 16.4% of code, bar 15%), not from the moves kit.
- **Next: chat 10, Opus medium:** ranking item 1, the rough command (0.5%, stop 0.75%); test on Blessed; per `notes/overnight-run.md`.
- **Needs Sam:** morning report picks (people kit 1-3; places kit 1-2; moves: list words + kit Y/N).
- **Read:** this file's "Item 7" section; `acting.py` MAP only.
- **Open rule requests:** none.
- **For Claude:** blessed.py has `person(shot, who, t)` (pure move, frames 0 diff), `van_seat`, `_handset`; kit hooks
  `gates2_head`, `guard_eyes`; check_list reads `notes/archive/blessed-handovers.md`. kittests: page.py excluded
  from "films using the kit" (it was failing since chat 7).

## Item 7, moves from the acting list (ranking item 7; overnight run; 6%, stop 9%)
Design (chat 7, 14 Nov): a film's moves are plain lines in `story/FILM-moves.txt` (language in `acting.py` MAP), one
block per shot, each one acting-list row (`## SHOT: WHO, line N, lands on "WORD"`, `row:` the row's words). Lines:
`face:` (mood, shades, gaze steps, later moods), `walk:` (gait, from/to metres on a ground, over, phase, settle, still,
chest, sway), `L:`/`R:`/`both:` hand keys (`PLACE at T`, `PLACE from T to T`, `rest at T`; a second line for a hand
lies over the first from its first key), `body:` moves (bump `from A to B, rise, fall`; ramp `from A over D`; `except`)
on channels lean, nod, roll, dip, bob, head_dy (+ filmkit.shifts idle life), `holds L|R: PROP between A and B`. Times:
"word", a T beat, end, cut, start, landed, min(), +/-; bare numbers are seconds into the shot. Library in the kit:
12 hand places (heart, point, wide, sweep, messiah, arms out, hair, hair back, oath hand, oath mid, bible, clasp low),
13 body moves (lean in, bow, chin up, dip, slump, start, tilt, nod, preen, bask...); a film adds `gait`, `place`,
`body` lines. The film side (`FILMS['blessed']`): its timeline, word_at, grounds, props, which functions the kit
stands in for. Pose-level replication (joints compared) is the fast test; frames prove the drawing.
1. **Done (chat 7):** core + Brand's arrive, oath, oath2, dock, gates, gates2 (exact).
2. **Done (chat 8):** the rest of Blessed: `stance: seated` (van with VAN_YAW; dock guards; the judge: shifts + the
   peer bumps on "Almighty God"/"blessed", mood sceptic), the jury (JY.draw: leave as code unless short), escort (Brand
   and the officer walking, the officer's grip: `holds` a grip prop; eye channels look, head_dx, gaze, lid, blink off),
   `stance: lying` for the cot (cot_pose via lying.py), phone (handset prop, cord), tvroom (dead still: STILL_OK) and
   push (the face change: moods by beat), gates2's background (Walliams' phases: drag, startled, plead, flail, grab,
   gone; guard1's head turn on line 7). Where a move is one-off and the library has nothing, it stays code and the
   block names it (`code: wal_pose`), per the ranking row.
3. **Next (chat 9):** `acting.py replicate blessed` over all shots (~6 min) + kittest extended; catalogue row text; report.
4. **Half done (chat 8: check_list, 2 drifts found):** cost per film in the report (Blessed's moves stage was ~1.5% by the ranking list; target ~0.5%), and the
   check against the notes' acting-list table itself (each row has a block), not only the block's own `lands on`.

## Item 5, places from a description (ranking item 5; overnight run; Opus high; 8%, stop 12%)
Design (chat 5, 14 Nov): a place is plain lines in `story/FILM-places.txt` (language in `places.py` MAP): `# place:`
with its colours, then `## view: NAME` per camera (`camera: up, horizon, lens`: a level camera, Blessed's `Level`;
`people: who depth` sets the layers), then one line per piece, back to front: `KIND: x A to B, z C to D, depth E,
params (name)`. Pieces are lifted unchanged in look into `places_parts.py`, each drawn in its own units (px at its
REF px per metre from its front face's top-left, through `B.Local`), so any level camera draws it at true size (trim
scales with distance). Looks hold Blessed's exact trims (door 'court' / 'jury room', chair 'witness view' / 'close',
panelled fronts x5) each with the ref it was drawn at. Layers: back (behind all the view's people), mid, front
(nearer than all) from depth; overall lights `layer front`. Boxes for rule 83 come from the pieces (bands and pieces
wider than 80% of the frame are not things); overlaps between pieces 0.2 m apart in depth are meant. Points are
snapped to 1e-6 px (float noise moved a whole row). Honest scope: level cameras at any height, distance and lens;
a turned (yawed) camera is not supported by these painted fronts (Blessed has none).
1. **Done:** core, courtroom pieces (panels, block, row, carpet, royal arms, clock, door, chair back, bench,
   microphone, witness box, book, window, panelled, notepad, water jug, papers, gavel block, gavel, glass screen);
   court_box 0.00%.
2. **Done (5b, 5c):** court_bench, court_jury, court_dock, court_out, gates (5b); van, cell, cot_top, phone, tvroom, tv (5c, `places_rooms.py`). Was: court_bench, court_jury, court_dock (pieces exist; cameras: horizon so the wall's foot is z 0 at depth
   6; dock: brand 2.5, guards 3.75), then court_out and gates (already in metres: `OUT`, `GATE` Levels; lift facade,
   entrance, sign band, planted wall, steps, rails, tree, lamp post, pavement, sky; gatehouse pieces), cell, cot_top,
   van (room walls run from the back wall's corners to the canvas corners (-300, -400)/(1380, 2400): a `room` piece
   with that mode), phone (booth, notices, signs), tvroom (pool table, chairs, `tv flicker` light), tv (`studio_feed`
   stays newsdesk_set's; a `tv` piece showing a feed).
3-5. **Done (5d):** replicate 0.004% worst (13 paintings, 12 frames); set_boxes: 36 of 40 hand boxes have their
   piece, 4 hand boxes were stale; 94 kit boxes; kittest, catalogue, page, sheet, report (1,491 lines -> 226).

## Item 4, people from a description (ranking item 4; overnight run; Opus high design, medium build; 8%, stop 12%)
Design (chat 4, 14 Nov): a person is a block of plain lines in `story/FILM-people.txt` (language in `people.py` MAP);
the kit turns it into the engine's person (views.person) and hangs LIFTED parts on it (`people_parts.py`, copied
unchanged in look from `blessed_cast.py`; the face card rides in the person, `kit_face`, not in a table by name).
No film imports the kit until Sam approves (kittest refuses one). The pass mark is `people.py replicate FILM`: the
finished frames beside the same frames with the kit's people swapped in; 0.05% of pixels is the bar.
1. **Done:** invented people (front face, 10 haircuts, stubble, boxed beard, glasses, freckles, outfits, wig, robe,
   officer kit): Blessed's 16 at 0.00%. Page lines. Sheet `people.py sheet blessed OUT.jpg`.
2. **Done (chat 4c): Brand (4 looks) and Walliams:** famous faces as `head: measured CARD` (the likeness card's measures,
   P4.MEASURED/PUSH/TUNE from lines `push 1.6`, `tune eyes_apart 2.0, ...`), `beard: full` (moustache, cheek, chin
   colours: brand_beard lifted, colours from lines), `hair: long curls` with `knot` (brand_hair, bun, turned hair
   lifted), `moods:` lines (a mood = brow, frown, lid, squint, mouth, smile), looks as `like: brand` + outfit lines,
   torso extras (open shirt and crucifix, scarf, tracksuit zip). Walliams: his own head file is one part
   (`blessed_walliams`) or lifted the same way; pick by size. Frames: arrive 2.0, oath 5.6, dock 16, phone 33,
   tvroom 38, gates2 55. Bar 0.05%.
3. **The press pack:** a crowd line (`crowd: press, 10, styles ..., seed`) using the lifted turned press heads.
4. **Turned heads for invented people (rule: drawn in every view):** the press pack's turnhead route for any front
   face, so a kit person turns (the sheet's side and back now use the engine's plain heads: curly reads long from
   behind, the wig is front only). Check: the sheet at 0/45/90/135/180.
   **Chat 4c notes for steps 3-4:** `blessed.press_sp(i, seed)` is looked up at draw time: replicate can swap it for a
   kit wrapper that keeps the film's staging (`kit`, `yaw`, `eye`) and takes the look from the crowd line. The film
   registers one turnhead Person per 'press%d' with the FIRST journalist's skin (skins differ per i and seed): key the
   kit's by who AND skin; if that differs from the film, it is a film fault fixed (report it). Lift PRESS_STYLES,
   _press_layout/_cap/_profile/_hair/_mood/_rest from blessed_cast (no lift: from behind the neck shows long; Big
   only; blessed_cast's _th_draw_big passes 'kit:' names through). Colour lists in a crowd line: items split by ';'.
   Kit hair to turned style: crop crop, bald bald, side side, bob bob, long long, curly curly, bun (new: a knot),
   receding bald, none (new: no hair). Turned invented people in Blessed frames may now differ from the film's plain
   turned heads: report which frames, as an improvement, not a fail.
5. **Done (chat 4d): the morning report:** `notes/morning/people-kit-replicate.jpg` (13 frame pairs), `-cast.jpg`
   (everyone at five turns, the press pack's first 8), `-changes.jpg` (the three frames that change, close up).
**Chat 4d results:** steps 3-4 done. The crowd language: `crowd: press`, then `FACT (3i+s): a; b; c` (member i takes
item 3i+s), `when hair ...: FACTS`, `when job ...: FACTS`, `taller`, `seed: 600 + i`, `hair seed`, `hair colour`,
`brows: darker hair 0.8`, `trousers: darker jacket 0.6`. All 31 journalists' looks equal the film's. Keyed the film's
way the press matches 0.00% everywhere; keyed per look (the kit's way) gates 50 s differs 0.53%: the film's journalists
9+ wore the first same-haircut journalist's hair colour (a film fault, fixed). Turned invented heads: escort 24 s
(the officer, 0.62%) and tvroom 38 s (inmate 2 tipped down, 0.27%); both bigger than the film's plain heads (they
match the person's own front head now). The judge's wig is still front only (turned: bald, as the film was);
Walliams' turned head is still the engine's (test only).
Cost per film once approved: a new invented person ~10 lines (was ~60-120 lines of face table and code); Blessed's
cast code 1,661 lines -> about 200 lines of descriptions plus Brand's own parts.

## Job Q, the handover check (Sam: Y, 13 Nov; Opus medium, ~1.5%; beside the face tool)
Why: Blessed's handovers dropped things (notes 8-11 sat unread when chat 5 broke before writing them and chat 6 read
only the notes file; Walliams' face, open in note 47, fell out of two handovers; chat 5 read "don't stop for any Y" as
a cost override). Closest: CLAUDE.md "Fresh chats and the handover", rule 30, `ledger.py`; nothing checks a handover.
One tool, two moments (Statement 1: quality, fewer notes and faults, cost; kittested; about $0.10 a chat to run):
- **End of a chat, before it hands over:** list every message Sam sent in that chat (`list_events kinds=["user"]`,
  filtered); flag any with no fix or reply, any open note the handover does not carry, any "clip sent" with no file.
- **Start of the next chat:** read Sam's messages in the chat before, to catch one that broke before handing over.
Saves about 2-4% on any film where a chat breaks or drops a note. Lost: nothing. Reads: `guides/job-packs.md` "A tool job".

## Logged 13 Nov (Sam: log for now; not started). The one aim: films at 15% of a week, or as close as honestly possible
- **Job O, true weekly figure (Sonnet, ~0.5%).** Sam: Blessed spent 80% of a week; our ledger counted 50.92% (WEEK_USD
  290). Set `WEEK_USD` in `.claude/hooks/costwatch.py` so Blessed's recorded dollars read 80% (first check the ledger
  has every Blessed chat: 11 Nov rows are estimates); restate every film's ledger and every quoted % with it.
  **DONE 13 Nov (chat 1 of 8, Sonnet):** found Blessed's record missed two chats (chat 5 of 8, $5.08, and chat 6 of 8,
  $2.11: added to `app-costs.tsv`) and carried five duplicate transcript-estimate rows for chats the app already
  showed (dropped by `ledger.py app`). Real Blessed = $100.79 from the app + $36.05 estimated (six 11 Nov chats
  the app cannot show, kept) = $136.84. `WEEK_USD` 290 -> **171** so that reads 80.02%. Every film's estimate rows were
  rescaled x290/171 and app rows recomputed: Blessed 80.02%, Remakes 51.54%, Protest Tiers 14.44%, Link trial 1.9%.
  Film estimates and stage plans (Blessed 19%, Remakes 14.5%) are NOT rescaled: they were guesses on the old ruler;
  Job N redoes them. Rule 85's 3%/5% chat limits are unchanged in % (now $5.13/$8.55, tighter than before): Sam to say
  if he wants them kept in dollars ($8.7/$14.5 = 5.1%/8.5%). Kittest `estimate_forecast_and_alarm` passes.
- **Job N, honest fit at planning (Opus high, ~1-2%).** Widen rule 24: before any building, the plan states whether the
  script fits 15% (from KNOWN vs NEW and real past costs on the true ruler); if not, why (people, places, likeness
  faces), and which tool improvements would bring it closer (never trimming the joke or reusing
  old content: CLAUDE.md, Sam 13 Nov). Blessed (7 people, 8 places, one
  likeness face) is the test case: the plan should have said "about 25-35%, here is why, and these tools would close the gap".
- **Job P, the ranking job: DONE 13 Nov (chat 2 of 8, Opus high): `notes/ranking-list.md`.** Order: 1 roughs of
  every new thing (rule 11), 2 likeness in one sitting, 3 critique test bench and Sonnet critic, 4 people from a
  description (tested on Protest Tiers' cast), 5 places, 6 rounds read a page, 7 moves; N at the next new film's plan.
  All built ~29%; a Blessed-sized film then ~20-26%, a typical one ~15-18%. Sam's numbered message sent. The entry as logged:
- **Job P (as logged, Opus high, ~2-3%).** One chat; output one ranked list of jobs to bring
  films toward 15%, from the real record (every note, every fault caught or missed, every chat's cost, stage cost vs
  plan, on the true weekly figure, Job O). Headings: catch faults before Sam sees them; better tools that work less hard;
  making new people, places and moves faster and surer; reading less. Each job: build cost, saving per film (measured),
  films to pay back, "Lost:" line. Ends with what a Blessed-sized film would cost if all were done. Never: trimming the
  joke or repeating old content (CLAUDE.md). **Headline item: describe, don't code.** Blessed needed ~5,500 lines of its
  own code (cast 1,144, sets 1,491, film 2,050, others); a new person, place or common move should be a short description
  the engine draws from tested parts (figure kit, likeness, set painter joined up). Price it honestly, what it would have
  saved on Blessed and the last 10 films, and a staged plan, people first.
  **Also on the list (Sam: Y, 13 Nov):** (a) a rough of every new person, place and move sent to Sam before its build
  (widens rule 11 from 3-4 key shots to every new thing); (b) test Sonnet as the critique helper (rule 89, now Opus,
  ~a quarter of a build chat) against past films' faults; switch only if it catches as much. (Parallel build chats
  dropped: already how we work.)

