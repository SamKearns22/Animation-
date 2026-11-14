# Where things stand (project, 14 Nov; no film in progress; the aim: films at 15% of a week)
- **Newest work:** `claude/people-kit-c4c` (also on the main line); face tool: its own chain (stopped).
- **Rules that bite next:** 86 (every tool gets a kittest), 85 (cost watch), 61 (MAP; the page).
- **Done (overnight chat 4c, item 4, Opus medium, ~2.2%; job ~4.6% of 8%, stop 12%):** step 2. Brand in his four looks
  (front and turned) and Walliams redrawn from their lines: 13 finished frames at 0.00%. `people_famous.py` (Brand's
  head made general: card, tune, full beard, curls/knot, deep set, house moods, torso extras), `people_walliams.py`
  (his head as one part, test only). Kittest extended (18 people, 4 frames); every old kittest passes.
- **Next: chat 4d, Opus MEDIUM (building from the clear plan below):** steps 3-5: the press pack as a crowd line,
  turned heads for invented people (one module from blessed_cast's press code), then the morning-report sheets; then
  the places kit chat (item 5, Opus HIGH). Hard stop: 12% for the job.
- **Needs Sam (morning report):** as before (face tool picks, bench picks); nothing new from this chat.
- **Read:** this section; "Item 4" below (steps 3-5 and the chat 4c notes); `notes/overnight-run.md`; `people.py` MAP.
- **Open rule requests:** none.
- **For Claude:** replicate swaps the film's dicts IN PLACE, keeping `KEEP` (look_, mood: film staging). TC.HEADS and
  TORSOS point at `kit_head`/`kit_torso`, which pick per LOOK (Brand's four looks share who='brand'). Turned famous
  heads go through turnhead under 'kit:WHO' (people_famous.install's head_view), so blessed_cast's Person is unused.

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
5. **The morning report:** one sheet per film-frame pair (new beside finished), the cast sheet, the cost; then the
   places kit chat (item 5, Opus high).
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

