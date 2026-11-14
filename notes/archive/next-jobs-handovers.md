# Where things stand (archived 14 Nov, chat 7) (project, 14 Nov; no film in progress; the aim: films at 15% of a week)
- **Newest work:** `claude/places-kit-c5d` (also on the main line).
- **Rules that bite next:** 86 (every tool gets a kittest), 74 (the acting list), 85 (cost watch).
- **Done (chat 5d, Opus medium, ~1%; item 5 DONE at ~7.1% of 8%):** full replicate: 13 paintings and 12 frames
  within 0.004% (3 min 7 s); set_boxes vs the hand list: every hand box has a piece except 4 stale ones (phone railing,
  phone notices, tvroom cue rack: the painting changed after Sam's note 20); the kit found the Samaritans notice over
  the second hood (morning report). Kittest `places_from_a_description`, MAPs, catalogue row and tile, page lines,
  sheet `notes/morning/places-kit-replicate.jpg`, morning report entry.
- **Next: moves from the acting list (ranking item 7), Opus HIGH (design), new chat**, per `notes/overnight-run.md`
  (estimate 6%, stop 9%; tested on Blessed).
- **Needs Sam:** start the moves chat (chat 5d could not: sessions stop at 8 chats in a row, a system limit);
  morning report picks (people kit 1-3; places kit 1-2).
- **Read:** `notes/overnight-run.md` in full; `notes/ranking-list.md` row 7; CLAUDE.md "Reading little".
- **Open rule requests:** none.
- **For Claude:** places.py: `on NAME` (generic word: a meant overlap), a piece past both picture edges is a band (was
  80% width: dropped the bench and witness box), repeats numbered in set_boxes, `## view: NAME (spoken name)` for the
  page, `picture(view)` for the catalogue. page.py lists places pieces by line (Blessed page 13% of code).

# Where things stand (project, 14 Nov; no film in progress; the aim: films at 15% of a week)
- **Newest work:** `claude/places-kit-c5c` (also on the main line).
- **Rules that bite next:** 86 (every tool gets a kittest), 85 (cost watch), 61 (MAP; the page).
- **Done (chat 5c, Opus high, ~1.9%; job ~6.1% of 8%, stop 12%):** step 2 finished: van, cell (+cell_cot), cot_top,
  phone, tvroom, tv all 0.000% (paintings, quick check) from a new `places_rooms.py` (27 indoor pieces: room, lines,
  brick marks, stroke, studs, oval, wash, glow, flicker; van, cell, cot, phone and association pieces; wall tv with a
  feed). All 13 views are now described (12 views + cell_cot's camera; 162 piece lines). Handed over on amber.
- **Next: chat 5d, Opus MEDIUM (building from a clear plan), same job:** steps 3-5 below (full replicate with
  frames, set_boxes vs SET_BOXES, kittest, MAPs, catalogue row, page lines, sheet, morning report entry), then open
  the moves chat (ranking item 7, Opus high) per `notes/overnight-run.md`.
- **Needs Sam (morning report):** people kit picks 1-3 (unchanged).
- **Read:** `notes/overnight-run.md` in full; this file's item 5 section only; MAPs of `places.py`,
  `places_parts.py`, `places_outside.py`, `places_rooms.py`.
- **Open rule requests:** none.
- **For Claude:** replicate now patches `ST.tv` (the film's back() calls it directly) and painters take `feed`; the
  MAPs of places.py / places_parts.py do not yet name places_rooms (step 4). Quick check: a scratch script that
  installs the description and compares `ST.painting(v, 0.7)` (~10 s for six views); the full replicate with frames
  takes ~3 min (run it in the background). Points are px -> metres as before (`x = (X-540)/ppm`,
  `z = up - (Y-horizon)/ppm`, every ppm 2^a*5^b, pieces' REF = the ppm they stand at, so k = 1).

# Where things stand (archived 9 Nov) (project, 7 Nov; the last film is finished)

## Where things stand (replaced by Job J, 10 Nov) (project, 10 Nov; no film in progress)

- **Rules that bite next:** 89 (critique before every send: now `critique.py`, and pre-flight refuses an animatic without
  a clean last pass or `--faults-named`), 30 (each fault note names its checklist line), 56 (`critique.py where`).
- **Job H (chat 2, the build, done 10 Nov, Opus high, about 1.9%; Job H in all about 3.4% of the 5% cap): FINISHED.**
  Harvest: about 70 of Sam's non-body fault notes from ten films filed into the checklist (now 37 lines: new P13
  clothes, O5 props resting, O6 effects, S5 set detail, S6 same set every shot, M5 hits show; P9 merged into P7).
  `source/critique.py` (pack, record, false, where, before, status) with 3 kittests (pass); pre-flight prints the
  critique line and refuses the animatic without a clean last pass. Calibration, two fresh helpers on Elder Swindon
  stills plus two old faults put back: both caught the mirrored label and the hand off its phone, no false alarm on
  the clean panels, and the before/after note judged right. Both also flagged, on Elder Swindon's current frames: the
  scroll lost in glare (9 s), the drool reading as a straw (3.5 s), the dog a brown lump and his raised arm reading
  awake (16.5 s), the roundabout an even wheel (25 s): for that film's next round. The first real trial is the next film.
- **Job G (chat 4 done, 10 Nov, steps 4-6, Opus high, about 1.3%, stopped on amber):** lying checks: a neck shows,
  no arm held up in the air, each arm on its own side (Sam's lying notes); the kit's lying arms laid flat (elbows bent up
  into the air: Elder Swindon 6's cause); pre-flight now stops a pose seen from an "avoid" view or with no gallery row,
  and checks every lying body; 12 everyday kit poses added to the gallery (hands on hips, pockets, shrug...). Rules
  that bite: 42, 41. **Next for G:** nothing; Job G is finished once Sam numbers the step 6 proposal.
- **Job I (chat 2 done, 10 Nov, Opus medium):** the driver's check now shows on every side standing (three-quarter
  front and back were plain red) and lying; the neck of every lying person now turns with the head and stops at the
  collar (the 'ball' from behind showed a loose block: the back-of-head drawing's own neck ran a fixed length past the
  collar). Trio sheet looked at (fine); `lying.py check` OK; Elder Swindon's close man redrawn and looked at (fine;
  his shoe soles have a slightly doubled outline). Sheet `notes/sheets/job-i-driver-sheet.jpg` (sent).
  **Round 1 of Sam's notes DONE (10 Nov, same chat, stopped on amber):** (a) each leg one shape with one outline
  (`_limb_piece`); a leg in front of the body has its thigh drawn under the shirt hem first; (b) heads a tenth smaller
  lying, smaller again beside a squashed trunk, at the head's own depth; no shine on a bald crown; (c) no floor
  shadow under lying people (floor only; shirt shading kept, my pick on Q1); (d) face-up-away can't be drawn by the
  rig: pre-flight now flags it (`lying_flat.face_up_away`, posecheck 'lying: face up away'); sheet shows 'head left'.
  Soles now the shoe's own colour, darker. One fresh critique pass run (found 7; 3 fixed above).
  **Next for I (chat 3, Opus medium):** Sam's look at the new sheet. Named, not fixed: the slumped shirt reads as a
  wide box and the arm across it is lost (check on check); the turned goatee reads as a spike (the standing rig's own
  side view); from behind the hair ring can read as a blindfold and the neck as a block; handcheck can't see lying
  bodies; second critique pass not run yet. Rules that bite: 41, 30, 89.
  For Claude: `lying_flat._head` returns (HeadCam, view), `_neck` draws before the trunk (`neck_off` skips the
  trunk's neck in burnham.torso / views.torso_view); `neck_to` stops views' back-head neck; `lying_flat.py sheet OUT
  man ball`. Driver's three/three_back check: ad_vanced_notice_cast.torso_view.
- **Job K, the "AI ick" fixes (chat 1 done 10 Nov, Opus high, about 2%):** Sam: 1 Y, 2 Y, 4 Y, 6 dropped, 8 N, 3 dropped,
  7 N; 5 waits for an example. **Next for K (overnight build, Opus, high effort, about 2.5%, cap 3%):** "Job K build:
  read notes/next-jobs.md, the Job K line, then notes/job-k-ai-tells.md 'Sam's answers' and Build plan K." Example
  for 5 first (sent), then 2, 1, 4; one sheet or clip each, sent to Sam. Rules that bite: 86, 48, 79. For Claude:
  `source/ai_tells_lab.py` (cel(), HeadLife). Open rule requests: none.
- **Needs Sam:** nothing for H. K: Y/N on proposals 1-8 (above).
- **Read:** `source/critique.py`'s map (top of file) the first time a film runs a critique; `guides/critique-checklist.md`.
- **Open rule requests:** none from H. Job G step 6: rules 41, 42, 81 merged into 41 (Sam: Y, 10 Nov; written).
- **For Claude:** packs in `source/data/critique/FILM/rR-pN` (git-ignored; the spec sits beside the pack, never in it);
  results in the ledger (`critique` in FILM.json, both answers in the round file). Job G's own notes: Job G section.

- **Rules that bite next:** 78 (resting arms show weight, never sink), 79 (full-size looks before "looks right"), 74 (acting list: shot and why, meaning questions first, no limit).
- **Done (7 Nov):** the touch check prints COULD NOT TEST when it finds no hand or object (`audit.py`, `kitchecks.py`); rules 74, 78, 79 written; two tips in `guides/figure-rig.md` s.4; reference photo `references/body-weight/leaning-on-table-forearm-forward.jpg`. Hook Text rule dropped. All on the main line.
- **Next job A, sitting kit: part 1 BUILT 8 Nov** (`source/sitting.py`, notes `notes/sitting-kit.md`); sheet and moves video sent to Sam. Part 2 after his look: Opus, high effort, new chat. Type: "Build the sitting kit, part 2, from notes/sitting-kit.md".
- **Job B, rule 78 check: BUILT 8 Nov** (`kitchecks.rests`, run by pre-flight; films list resting arms in `RESTS`; tested on the sitting kit's desk and armchair poses and planted faults).
- **Needs Sam:** a look at the sitting kit's sheet and moves video.
- **Read:** `guides/figure-rig.md` s.2 body, s.3 limbs, s.4 contacts, s.6 movement; `guides/pose-gallery.md`; `source/kitchecks.py` (touches, resting); rule 78 and 32 and L1 in the rulebook.
- **Open rule requests:** none (rule 80 written 7 Nov). New rules from A or B are proposed to Sam first.
- **For Claude:** existing seat support is only `check_seated` (hips on the seat) and the desk-seated note in figure-rig s.4; no stand-up, feet-up or seat-change poses exist yet. Check `source/moves.py`, `posegallery.py`, `figure.py` before building.




## Where things stand (project, 9 Nov, after Job C chat 1)

- **Rules that bite next:** 86 (tools: own chat, estimate first), 44 (12% a film), 85 (cost watch).
- **Done (9 Nov):** Job C chat 1: rulebook 99 rules to 81 by merging repeats (nothing dropped but the pypi.org line), contents lists, CLAUDE.md re-sectioned (Sam: Y to all 26 points). Handovers-at-the-bottom rule written (Sam: Y).
- **Next:** Job C chat 2, the guides: Opus high, new chat: "Tidy the guides, chat 2 (Job C in notes/next-jobs.md)". Job D (APPROVED) in its own chat, any time.
- **Needs Sam:** nothing.
- **Read:** this file; the rulebook's "Merged numbers" (last section); then the guides as listed in Job C below.
- **Open rule requests:** Job D's rule comes with its build.
- **For Claude:** chat 2 also points the 63 old-number mentions (e.g. "rule 55", "rule 73", "rule 84") in guides/, source/ and notes/ at their new homes, using the rulebook's "Merged numbers"; `git grep -nE "[Rr]ules? (12|15|23|33|35|45|46|51|53|55|60|68|69|71|73|82|84)\b"`. Cost watch WEEK_USD still to calibrate.

# Where things stand (project, 9 Nov; no film in progress)

- **Rules that bite next:** 86 (tools: own chat, estimate first), 44 (12% a film), 85 (cost watch).
- **Done (9 Nov):** Job C finished. Chat 2 (the guides, about 0.6% of a week): research and roadmap pages moved from
  guides/ to `research/`; quick-video's "Added 8 Oct" tail folded into its steps and fix table; best-practice Part 2 and
  Part 5 cut to what isn't written elsewhere (7,500 to 6,000 words; repeats of satire.md, tiktok-design.md, preflight.md,
  CLAUDE.md and the rulebook removed, nothing else dropped); contents lists on every guide; stale lines fixed (preflight's
  model sheet now front/side/back per rule 38; tiktok-design says no title by default; its "Working" section was a copy of
  CLAUDE.md); every old rule number in guides/, source/ and notes/ points at its new home.
- **Next:** Job D (APPROVED), new chat, Opus high: "Build the softer voices tool (Job D in notes/next-jobs.md)".
- **Needs Sam:** nothing.
- **Read:** this file's Job D section only.
- **Open rule requests:** Job D's rule comes with its build.
- **For Claude:** archives (`notes/archive/`, `guides/archive/`) keep old numbers on purpose (history). Cost watch
  WEEK_USD still to calibrate.



## Archived 9 Nov (Job E chat)
### Where things stand (project, 9 Nov; no film in progress)

- **Rules that bite next:** 86 (tools: own chat, estimate first), 85 (cost watch), 87 (notes restated before fixing).
- **Done (9 Nov):** Job D built: every film's voices now get a gentle polish (warmth, the 2-5 kHz edge and treble eased
  by how bright the take is, a de-esser on s-sounds), and long loud stretches (Ad-Vanced Notice's explosion, 4 dB over)
  are evened in the master. Before/after clip of Ad-Vanced Notice line 9 sent to Sam (17 s, 3.5 MB, not on GitHub).
- **Sam, 9 Nov, on the clip: "It's better, definitely."** Kept as built. Job D closed.
- **Next:** nothing queued.
- **Needs Sam:** nothing.
- **Read:** this file's Job D section only.
- **Open rule requests:** none (S10 was already the riding rule, so the voices rule is S11, written 9 Nov).
- **For Claude:** `mossad_audio.polish` (in `line()`, before `restore_tail`) and `even_out` (in `master` and
  `limit_check`), both under `MA.POLISH` (True). Strength knobs at the top of the softer-voices block: WARMTH_DB,
  EDGE_TARGET, EDGE_CUT, SHELF_DB, DEESS_MAX_DB. `python3 source/mossad_audio.py soft NAME...` prints each take's edge and
  hiss before and after. Cost watch WEEK_USD still to calibrate.



## Handover replaced 9 Nov (Job E rerun)

- **Rules that bite next:** 86 (tools: own chat, estimate first), 85 (cost watch), 81 (arm join, by hand: failed 4 times).
- **Done (9 Nov):** Job E measured: a chat starts at 79k tokens (76k the app itself); only 3 "Checks:" lines and 12 rules'
  catches were ever written down; Sam's body notes (47, last ten films) are 62% arms and hands, the top group hands on
  props. Results and cut list: `notes/job-e-measurements.md`.
- **Next:** rerun Job E on Opus high (Sam, 9 Nov: the first pass may have run on medium), new chat. Check and deepen
  `notes/job-e-measurements.md`, don't redo it blind: (1) read every film's notes in full, not only lines in note
  sections, for body notes the keyword sort missed; (2) look for rule catches in commit messages and check sheets too,
  not only in notes; (3) count tokens properly where possible. Then Job F. Type: "Rerun Job E on Opus high. Read
  notes/next-jobs.md, Where things stand, and notes/job-e-measurements.md."
- **Needs Sam:** (after the rerun) Q1 move finished films' notes to the archive (Y?); Q2 Job G order hands, shoulder seam, lying (Y?);
  Q3 the ledger logs every check's result (Y?).
- **Read:** this file's Build plan; `notes/job-e-measurements.md` cut list.
- **Open rule requests:** none.
- **For Claude:** costwatch WEEK_USD still to calibrate. Job E scripts were scratch only (not kept).



## Where things stand (Job E handover) (project, 9 Nov; no film in progress)

- **Rules that bite next:** 86 (tools: own chat, estimate first), 85 (cost watch), 81 (arm join, by hand: failed 4 times).
- **Done (9 Nov, rerun on Opus high):** Job E checked and deepened in `notes/job-e-measurements.md`: files cost about
  70% more tokens than first said (2.35 characters a token; satire.md 16k, rulebook 11k, CLAUDE.md 5k); 60 body notes
  (was 47), 57% arms and hands, and 9 caused by a turned, from-behind or mirrored view (a new group); rule 41's hand
  check is the busiest catcher on record (4 films), found only in commit messages; no check sheet is ever kept.
- **Next:** Job F (film ledger), new chat, **Opus, medium effort** (build plan table). Type: "Job F: build the film
  ledger. Read notes/next-jobs.md Where things stand and Build plan F, and the cut list in notes/job-e-measurements.md."
- **Sam's answers (9 Nov): Y Y Y.** Q1 done: Terfwarts, MidTerminal, Islamocommunism and sitting-kit notes moved to
  `notes/archive/` (Elder Swindon stays until Sam says posted). Q2: Job G order is hands, shoulder seam, every view
  (behind, three-quarter, mirrored), then lying. Q3: Job F's ledger keeps every round's check results and check sheet text.
- **Needs Sam:** nothing.
- **Read:** this file's Build plan (F row); `notes/job-e-measurements.md` cut list.
- **Open rule requests:** none.
- **For Claude:** costwatch WEEK_USD still to calibrate; FRESH 90k fits the measured 80k start. Job E scripts were
  scratch only. Not read in full (amber): the ten films' handover files, Flying Whales, Newsdesk (keyword search only).

# Where things stand (project, 9 Nov; no film in progress)

- **Rules that bite next:** 44 (now the film ledger), 86 (tools: own chat, estimate first), 81 (arm join, by hand: failed 4 times).
- **Done (9 Nov, Job F, Opus):** the film ledger, `source/ledger.py`. Sam's Y Y N: built (about 0.4% of a week, estimate
  0.5%); rule 44 rewritten to use it (shorter than before); no back-filling of old films. Every check's full result
  (clean ones too) now lands in `notes/ledger/FILM/round-N.txt` once a round is opened; `log` at each handover sums
  cost per film; `audit` gives the 10 lines when a film is posted. Tested on a pretend film, then removed.
- **Next:** Job G (bodies), new chat, **Opus, high effort**. Type: "Job G: bodies, hands first. Read notes/next-jobs.md
  Where things stand and Build plan G, and the cut list in notes/job-e-measurements.md." Estimate first (rule 86).
- **Needs Sam:** Y or N on the Job G estimate (section below).
- **Read:** this file's Build plan (G row); `notes/job-e-measurements.md` section 3 and the cut list.
- **Open rule requests:** none.
- **For Claude:** next film's plan runs `ledger.py estimate FILM N`; each round `ledger.py round FILM N`; each handover
  `ledger.py log FILM --stage .. --notes N --repeat "note | catcher"`. costwatch WEEK_USD still to calibrate.


## Where things stand (Job G chat 1 handover, 9 Nov)

- **Rules that bite next:** 86 (tools: own chat, estimate first; Sam said Y to Job G at about 4%), 81 (arm join, by
  hand: the seam check is chat 2's first job), 41 (every point must read: now checked).
- **Done (9 Nov, Job G chat 1, Opus high, about 1.7% of the 2% estimate):** pose test shows 6 views (mirrored added),
  whole body in each picture; new automatic body checks in the hand check (so films get them too); props in hands
  and tables right from every view; four kit poses fixed (phone read, cup, cup sip; pointing straightened); the
  one-piece finger is the house finger; front-on and from-behind people never draw mirrored (Islamocommunism 9).
- **Next:** Job G chat 2, new chat, **Opus, high effort**. Type: "Job G chat 2: read notes/next-jobs.md Where things
  stand and the Job G section." No new estimate: chat 2 was priced (1.5-2%).
  **After G: Job H (critique helper, about 2%)**, only once G chat 2 has handed over. First chat: the checklist
  design, **Opus, max effort**, short (Sam's 9 Nov table); then building, Opus high. Type: "Job H: critique helper.
  Read notes/next-jobs.md Where things stand and Build plan H. Estimate first (rule 86)." 
- **Needs Sam:** nothing.
- **Read:** this file's Job G section; `guides/pose-gallery.md` top paragraph; `notes/job-e-measurements.md` cut list.
- **Open rule requests:** none. Chat 2 proposes merging rules 41, 42 and 81 (by-hand parts now automatic).
- **For Claude:** checks in `handcheck.body_faults`; `grips.py` (held, Table, on_table, contact_faults, Carry);
  `views.aim`; views `_person` (no mirror at 0/180; three_back reach hands behind; on_face skipped from behind);
  `posegallery.py` (VIEWS 6, flip test, tiles); kittest `grips_contacts_and_carry`. Sheet: `guides/pose-gallery.jpg`.

## Job G chat 2 handover (10 Nov)

- **Rules that bite next:** 85 (cost watch: chat 2 went amber after step 1, so it handed over), 81 (seam now
  checked automatically), 86 (Job G stays inside its 3.5-4%).
- **Done (10 Nov, Job G chat 2, step 1, Opus high, about 0.6%):** the shoulder gap found and fixed at its cause: an
  arm joined the body left over from the last drawing (the last view, or the last frame as someone turned), cutting
  a gap or leaving dark ticks at the shoulder. Every pose redrawn and compared: only cleaner. New automatic seam
  check in the hand check (films get it in pre-flight), and a test that proves it catches a gap and a line.
- **Next:** Job G chat 3, new chat, **Opus, high effort**. Type: "Job G chat 3: read notes/next-jobs.md Where things
  stand and the Job G section." No new estimate: steps 2-6 fit in the rest of chat 2's price (about 1-1.4%).
  After G: Job H (critique helper, about 2%): first chat Opus, max effort; type "Job H: critique helper. Read
  notes/next-jobs.md Where things stand and Build plan H. Estimate first (rule 86)."
- **Needs Sam:** nothing.
- **Read:** this file's Job G section; `guides/pose-gallery.md` top paragraph.
- **Open rule requests:** none. Step 6 proposes merging rules 41, 42 and 81 (81's check column still says "no
  automatic seam test yet": put right in that proposal).
- **For Claude:** `limbs.DRAW/NEXT` (views._person counts drawings; an arm's body key is cam, id(img), drawing;
  handcheck.probe restores DRAW); `handcheck.seam_faults` (7 lines walked out along the upper arm: jacket, ink or
  gap, sleeve = seam; arms in `j2['_drawn']['behind']` only a gap); probe adds inkpx/other/cloth/behind; kittest
  `shoulder_seam_caught`. Sheet `guides/pose-gallery.jpg` redrawn.


## (archived 10 Nov, Job H chat 1) Where things stand (project, 10 Nov; no film in progress)

- **Rules that bite next:** 85 (cost watch: chat 3 went amber after step 3, so it handed over), 41 (the hand check now
  also tests a hand against what it holds, on the picture), 86 (Job G stays inside its 3.5-4%).
- **Done (10 Nov, Job G chat 3, steps 2-3, Opus high, about 1.5%):** phone at the ear redone (hand at the cheek, the
  phone flat along the side of the head, elbow forward; passes all 6 views; the left hand by default); a hand at the
  far cheek is now hidden behind the head (it was drawn across his face side on); phone reading from three-quarter back
  no longer sits over his back (hidden by it: the gallery notes say avoid that view); new automatic check: a hand must
  touch its prop on the picture (a test proves it catches a gap); sheet labels no longer run into the next column.
- **Next:** Job G chat 4, new chat, **Opus, high effort**. Type: "Job G chat 4: read notes/next-jobs.md Where things
  stand and the Job G section." Steps 4-6, about 1%. After G: Job H (critique helper, about 2%): first chat Opus, max
  effort; type "Job H: critique helper. Read notes/next-jobs.md Where things stand and Build plan H. Estimate first
  (rule 86)."
- **Needs Sam:** nothing.
- **Read:** this file's Job G section; `guides/pose-gallery.md` top paragraph.
- **Open rule requests:** none. Step 6 proposes merging rules 41, 42 and 81 (81's check column still says "no
  automatic seam test yet": put right in that proposal).
- **For Claude:** `moves.phone_at_ear` (3D slab, `V._hull`); `grips.hidden_by` adds depth tests (head: beyond 0.25 hw;
  torso: beyond half its depth and within 1.25x its screen width); views skips an `on_face` arm hidden by the head;
  `handcheck.held_faults` (PROBE['held'] layer per side, TOUCH 0.12), kittest `held_prop_touches`. Unfinished: a
  "prop hidden" check (keyed prop pixels came back lightened, ~x1.3, in the probe: find why, then AVOID phone reading
  from behind in the dict too); `posegallery._wrap`.


## Archived 10 Nov (Job L chat)
### Where things stand (before Job L) (project, 10 Nov; no film in progress)

- **Rules that bite next:** 89 (now holds old 56, 76, 79), 24 (every thing KNOWN or NEW in the estimate), 41.
- **Done: Job J FINISHED (10 Nov, Opus high, about 1.5% of the week, cap 3%).** Sam: Y to 1-6 and 8; 7 "do it
  yourself". Written: 15 rulebook rows merged or retired (list under "Merged numbers"); critique lines S5, M2, O1 took
  old 4, S1, 34; pre-flight refuses a film from the 10 Nov template with no acting list or rehearsal line (rules 74,
  8), warns on 61; CLAUDE.md rewritten shorter (2,180 to 1,540 words, every rule kept; film types moved to
  `guides/job-packs.md`); job packs live. Job G finished (hidden props flagged).
- **Next: Job L, five checks (Sam: Y, about 1%), Opus, medium effort:** "Job L: read notes/next-jobs.md, Where things
  stand, and notes/job-j-proposals.md question 5." Rules 72, 62, 50, 27 (now 26), 37.
- **Job I next (chat 3, Opus, medium effort):** Sam's look at `notes/sheets/job-i-driver-sheet.jpg` (panel numbers).
- **Job K next (overnight build, Opus, high effort, about 2.5%):** "Job K build: read notes/next-jobs.md, the Job K
  line in notes/archive/next-jobs-handovers.md, then notes/job-k-ai-tells.md 'Sam's answers' and Build plan K."
- **Needs Sam:** I: the sheet; K: Y/N on proposal 5 once its example is seen.
- **Read:** the pack in `guides/job-packs.md` ("A tool job" for L and K).
- **Open rule requests:** none.
- **For Claude:** `preflight.gate_warnings` (refuses when the notes have the template's 'KNOWN (where) or NEW');
  `handcheck` 'prop hidden' (`V.PROBE['skip_held']`, `PROP_SHOWN`); `critique.library`.



## Archived 10 Nov (Job L merge: the Job I round 2 / Job K build 1 version)
- **Rules that bite next:** 89 (now holds old 56, 76, 79), 24 (every thing KNOWN or NEW in the estimate), 41.
- **Done: Job J FINISHED (10 Nov, Opus high, about 1.5% of the week, cap 3%).** Sam: Y to 1-6 and 8; 7 "do it
  yourself". Written: 15 rulebook rows merged or retired (list under "Merged numbers"); critique lines S5, M2, O1 took
  old 4, S1, 34; pre-flight refuses a film from the 10 Nov template with no acting list or rehearsal line (rules 74,
  8), warns on 61; CLAUDE.md rewritten shorter (2,180 to 1,540 words, every rule kept; film types moved to
  `guides/job-packs.md`); job packs live. Job G finished (hidden props flagged).
- **Next: Job L, five checks (Sam: Y, about 1%), Opus, medium effort:** "Job L: read notes/next-jobs.md, Where things
  stand, and notes/job-j-proposals.md question 5." Rules 72, 62, 50, 27 (now 26), 37.
- **Job I round 2 done (chat 3, Opus medium):** Sam's 12-14, 17 and faces. Round 1's one-piece leg failed because a
  leg nearer than the trunk was still split (thigh under the shirt, knee to shoe on its own); now one piece after the
  trunk (past the hem only what shows; drawn up, from the hip). Lying faces use the face-on drawing when facing us.
  **Next (chat 4, Opus, medium effort):** Sam's look at `job-i-driver-sheet-numbered.jpg`, `job-i-round2-closeup.jpg`.
  Still open: slumped shirt a box; back hair a blindfold; side-on face (11); no critique pass this round.
- **Job K build 1 done (10 Nov, Opus high, about 1.5%; stopped on amber):** sent to Sam: 5's example (driver sheet;
  nothing built), 2's sheet (hard-edged shading: built but OFF, `ed.HARD`, its shapes spill over hands seen from
  behind, kittest pose_gallery fails with it on), 1's clip (head acting built into the rig, on), 4 half built (pre-flight
  copy check, kittest passes). **Next, build 2 (Opus, medium effort, about 0.5%):** "Job K build 2: read
  notes/job-k-ai-tells.md 'Build chat 1'": keep the hard shapes inside the body and switch them on, then the shirt
  check that bends round the body, its sheet to Sam; then 5 if Sam says Y.
- **Needs Sam:** I: the round 2 sheets; K: Y/N on proposal 5 (the driver sheet is sent).
- **Read:** the pack in `guides/job-packs.md` ("A tool job" for L and K).
- **Open rule requests:** none.
- **For Claude:** `preflight.gate_warnings` (refuses when the notes have the template's 'KNOWN (where) or NEW');
  `handcheck` 'prop hidden' (`V.PROBE['skip_held']`, `PROP_SHOWN`); `critique.library`. I: `lying_flat._leg` (front:
  whole leg after trunk, `keep` past `sc.hem`), `_head` 'three' to 'front'; goatee dark; `no_shine` in burnham too.



## Where things stand (archived 11 Nov) (project, 10 Nov; no film in progress)

- **Rules that bite next:** 62 (subtitle pieces now timed against the take: Terfwarts' fallback timing is 2.3 s off on
  line 8), 50 (every film needs a `FAMOUS` list), 89.
- **Done: Job L FINISHED (10 Nov, Opus, about 1.3% of the week, cap 1.5%).** Five by-hand rules now checked in
  pre-flight: 26 every swear has a bleep; 62 each subtitle piece within 0.3 s of its first word (0.6 s inside a phrase);
  72 a standing person's arm dropping back to rest in the last 0.4 s before a cut; 50 each FAMOUS face 240 px once;
  37 sounds and references not on GitHub listed at every `ledger.py log`. Five kittests pass; rulebook check columns
  and the critique checklist's rule 72 line put right. Found: the subtitle code's syllable fallback puts pieces up to
  2.3 s early (Terfwarts 8, 4, 5): the next film's pre-flight flags it.
- **Job I round 3 done (chat 3):** 12 knee falls out to the side (it pointed at the camera: no bend showed), 14 neck
  over an arm in front, 16 near legs from under the hem; turned head back (face-on one stared at us) with his brows.
  **Next, Job I (Opus, medium effort):** Sam's look at `job-i-driver-sheet-numbered.jpg`, `job-i-round3-closeup.jpg`
  and his pick on question 1 (a proper turned face: Opus, high effort). Open: slumped shirt a box; back hair a blindfold.
- **Next, Job K build 2 (Opus, medium effort, about 0.5%):** "Job K build 2: read notes/job-k-ai-tells.md 'Build chat
  1'": hard shapes kept inside the body and switched on, then the shirt check, its sheet to Sam; then 5 (Sam: Y, 11 Nov) as on the driver sheet, about 0.3% more.
- **Needs Sam:** I: the round 3 sheets and question 1
- **Read:** the pack in `guides/job-packs.md` ("A tool job" for K).
- **Open rule requests:** none.
- **For Claude:** L: `voices.caption_start_check`/`word_times`/`bleep_check` (SWEARS_OK); `kitchecks.cut_rests`
  (CUT_RESTS_OK; seated left out), `kitchecks.faces` (FAMOUS = fnmatch patterns, '*vance*'; refuses only on 10 Nov
  template films), `ledger.kept`. I: `lying_flat._leg` (`keep` past `sc.hem`), `_neck(foot=-6)`
  after a front arm, `lying.on_back` R knee out, views 'three' brows fierce at anger 3+. K: `ed.HARD` off.

## Replaced 11 Nov (Job I faces built)
### Where things stand (project, 11 Nov; no film in progress)

- **Rules that bite next:** 62 (subtitle pieces timed against the take: Terfwarts' fallback is 2.3 s off on line 8),
  50 (every film needs a `FAMOUS` list), 89.
- **Done: Job K FINISHED (build 2, 11 Nov, Opus medium, about 0.6%).** Hard-edged shading now ON, kept inside the
  body; the check shirt bends round the body (sheet `review/job-k/shirt-bent.jpg`); invented people a touch uneven (the
  weight-on-one-leg stand removed: Sam, awkward), the driver first (sheet `review/job-k/driver-lopsided-built.jpg`). All kittests pass. Found: the
  old blur had hidden a real fault (gun hands from three-quarter back: the far hand hidden); that view is now avoided.
- **Job I bodies DONE (chat 3, rounds 2-4, Opus medium):** Sam: "seems good" (near legs from the end of the shirt).
- **Next, Job I faces (Opus, high effort; chat opened 11 Nov): Sam said Y (about 0.8%; stop at 1.2% and leave a note).**
  Sam's design: a turned head for ANY character, but built only when a shot needs it (the screenplay says which person
  faces which way, lying included); otherwise planning and check sheets as usual. So: (1) the turning tool lives in the
  kit, not in one film's cast file, and switches on for any person with a front design (today `views.head_view` is
  patched for Vance alone: why the lying driver got the old generic head); (2) the head measurements a person needs are
  taken from their own front layout where possible, not copied from Vance's; (3) planning/pre-flight lists each
  (person, direction) a film's shots need and builds and checks only those, the turnaround going on the check sheet;
  (4) the driver is the first user: draft on branch `claude/job-i-faces-wip` (merge it first; NOT on the main line:
  his hair is a black slab, the nose a spike, the goatee a stripe; Vance's turned heads come out pixel-identical).
  Lying 12, 15 turned, not straight on. Send Sam a turnaround sheet beside the lying driver sheet (`lying_flat.py sheet
  OUT man ball`, numbered as `notes/sheets/job-i-driver-sheet-numbered.jpg`), a kittest, then hand over. Open after:
  slumped shirt; back hair.
- **Needs Sam:** I: the faces sheet when that chat sends it. K: a look at the two sheets (nothing waits on it).
- **Read:** the pack in `guides/job-packs.md` ("A tool job" for tools; the film's type for the next film).
- **Open rule requests:** none.
- **For Claude:** L: `voices.caption_start_check`/`word_times`/`bleep_check`, `kitchecks.cut_rests`/`faces`,
  `ledger.kept`. I: `lying_flat._leg`, `_neck(foot=-6)`, `lying.on_back` R knee out, views 'three' brows. I faces: `ad_vanced_notice_cast.man_turned`/`turned_eyes`/`turned_brows`/`turned_mouth`, `turnhead.TurnFace` (`hair_top`). K:
  `ed.HARD` on, `ed.soft(clip=)`, `ed.bent_check`, `ad_vanced_notice_cast.BENT`, `patriots4_cast.lop`,
  kittest `lopsided_invented_only`; posegallery AVOID gun three-quarter back.

## Where things stand (replaced by Job I lying fixes, 11 Nov) (project, 11 Nov; no film in progress)

- **Rules that bite next:** 30 (a repeated note is a warning), 48 (one labelled sheet), 86 (estimate before building).
- **Done: Job I faces FINISHED (Sam, 11 Nov: "It seems good", no notes; Opus high, about 1.9%: over the 1.2% stop).** One shared turned
  head for anyone with a measured front design (`turnhead.py`), built only when a shot draws that direction; pre-flight
  lists the (person, view) pairs the shots need, flags a person drawn turned without one, and puts their turnaround on
  the check sheet. The driver is the first user: hair a horseshoe with an uneven top and strands (was a slab), a
  rounder nose (was a spike), the goatee standing off the chin, seen side on (was a stripe). Lying 12, 15 now turned
  (the shot names the head's roll). Vance pixel-identical (kittest). Sheets sent: `notes/sheets/job-i-driver-sheet-numbered.jpg`
  (1-18) and `notes/sheets/job-i-driver-turnaround.jpg` (19-23).
- **Next, Job I lying fixes (Opus, medium effort; Sam: Y, 11 Nov, for every character, both in one chat):** (1) slumped
  against a wall, the shirt drawn as a stiff box (lying 16); (2) lying with the back of the head to us, the neck drawn
  as a square block over it (lying 18; on the driver it reads as a blindfold with his hair band). Both are shared kit
  (`lying_flat`, `turnhead.neck_over`): check on Vance's lying sheet too; send Sam the remade sheets, numbered.
- **Needs Sam:** the remade lying sheets when that chat sends them.
- **Read:** the pack in `guides/job-packs.md` ("A tool job"); `turnhead.py` MAP, section "people".
- **Open rule requests:** none.
- **For Claude:** I faces: `turnhead.Person`/`register`/`install`/`draw`/`fitted`/`turnaround`/`SEEN`/`MISSING`,
  `TEMPLATE` (Vance's head); `ad_vanced_notice_cast.man_profile`/`_man_over` (swept goatee)/`_man_strands`;
  `lying_flat.ROLLED`, sp `head_roll`, `lying_flat.numbers`; preflight `heads_seen` (incremental runs list only the
  redrawn frames). Kittest `turned_heads_for_anyone` (VANCE_TURNED_MD5). Earlier: see `notes/archive/next-jobs-handovers.md`.



## Where things stand (replaced 11 Nov, Sam: "Fix the neck in 14 and 18") (project, 11 Nov; no film in progress)

- **Rules that bite next:** 30 (a repeated note is a warning), 48 (one labelled sheet), 86 (estimate before building).
- **Done: Job I lying fixes built (Opus medium), for every character.** (1) Slumped against a wall the shirt now sags as
  cloth: shoulders slope, sides bow at the belly, hem curves up over the lap, soft waist folds (was a stiff box).
  (2) Back of the head lying: no neck drawn over the head (was a square block, a blindfold with the driver's hair);
  the head inked all round. Standing views unchanged. All kittests pass (new: `lying_shirt_and_nape`).
  Sheets sent: `notes/sheets/job-i-lying-fixes-driver.jpg` (1-18: 16 slump, 18 back of head) and
  `notes/sheets/job-i-lying-fixes-vance.jpg` (the same panels, ball added so 18 shows his back of head).
- **Next:** Sam's reply on the sheets. Notes on them: Opus, medium effort, "Job I lying notes (notes/next-jobs.md)".
  No notes: nothing queued; the next film (Opus, high effort) starts from its brief.
- **Needs Sam:** a look at the two sheets (16 and 18 on each).
- **Read:** the pack in `guides/job-packs.md` ("A tool job"); `lying_flat.py` MAP.
- **Open rule requests:** none.
- **For Claude:** `lying_flat.Slump` (layer bend; `_sat` trigger: trunk upright, thighs forward; sleeves join
  `bend.moved` shoulders), `lying_flat.BACKS`; `turnhead.outline(whole=)`, sp `nape_in_head` (set by
  `lying_flat._head_draw`) skips `neck_over`. Kittest `lying_shirt_and_nape`. Earlier: `notes/archive/next-jobs-handovers.md`.



## Where things stand (archived) (project, 11 Nov; no film in progress)

- **Branch with the newest work:** `claude/job-i-lying-fixes` (also pushed to the main line).
- **Rules that bite next:** 30 (18 is a repeated note), 48 (one labelled sheet), 86 (estimate before building).
- **Done:** Slump shirt (16) and the first 18 fix sent on both sheets. Sam: "Fix the neck in 14 and 18" (both sheets).
  14 fixed: the neck now bends from the collar to the head (was one rigid block turned with the head); clip
  `notes/sheets/job-i-lying-14-neck.jpg` sent. Kittests: lying and turned-head tests pass.
- **Open, 18 (rule 30, why the first fix failed):** fix 1 removed the block drawn over the head, but the head then sat
  straight on the collar with NO neck. Found: the head lies about 85 px from the collar, and the new bending neck
  is drawn there, but the upper arm (drawn after it, round the top of the head) and the head cover it all; on Vance,
  the back collar (white strip in a dark band) stands up beside the head like a block. Try next: draw the neck after
  the 'first' arms when the head is seen from behind (or push the head out along the neck to the rig's 150), and turn
  the back collar band with the neck's foot; then remake both sheets, numbered.
- **Next:** Opus, medium effort: "Job I lying 18 neck (notes/next-jobs.md, Where things stand)".
- **Needs Sam:** a look at the 14 picture.
- **Read:** the pack in `guides/job-packs.md` ("A tool job"); `lying_flat.py` MAP, `_neck`, `draw`.
- **Open rule requests:** none.
- **For Claude:** `lying_flat._neck(img, hc, sp, aff, view, foot)` (bezier sides: foot in the trunk's frame, top in
  the head's; tops swapped when the head is mirrored); `lying_flat.Slump`, `_sat`, `BACKS`; sp `nape_in_head` skips
  `turnhead.neck_over`. Debug renders: one shot via `L.lie`/`L._fit`/`L.draw` as in `lying_flat.sheet`.


## Archived 13 Nov (chat 2 of 8): the 'Where things stand' before Job P
# Where things stand (project, 13 Nov; no film in progress; the aim: films at 15% of a week)
- **Rules that bite next:** CLAUDE.md "every film is new" (never trim the joke or repeat old content); Statement 1
  (the three aims); 85 (cost watch: hand over at amber).
- **Done (13 Nov):** rule 30 gains the end-of-film notes pass (FAULT / CHOICE / ASK, taste list in the critique
  checklist); CLAUDE.md "every film is new"; jobs O, N, P logged below (Sam: Y to all three).
- **Next, a chain:** Job O done (WEEK_USD 171). Chat 2 of 8, Opus high: Job P
  (the ranking list), which ends on one numbered message to Sam. Job N (Opus high) after P, or as P's list ranks it.
- **Needs Sam:** nothing until P's list.
- **Read:** this section and the job's own entry below; `guides/job-packs.md` "A tool job".
- **Open rule requests:** none.
- **For Claude:** WEEK_USD in `.claude/hooks/costwatch.py`; ledger in `notes/ledger/`; Blessed's real cost per Sam 80%.
  A separate pre-flight timing run (Sonnet) may also be in progress from the pre-flight audit: merge, don't clash.

## Where things stand (archived 13 Nov, chat 2 of 8) (project, 13 Nov; no film in progress; the aim: films at 15% of a week)
- **Newest work:** `claude/face-tool-c1` (also pushed to the main line).
- **Rules that bite next:** 49 (likeness pack and check), 86 (every tool gets a kittest), 85 (cost watch).
- **Done (chat 1 of 8, Opus high, amber at 2.1%):** photo packs filed (`references/faces/burnham/` a01-a05,
  `references/faces/badenoch/` k01-k05: news and Parliament portraits; Burnham now wears thick dark glasses, his
  trademark). The face tool `source/facepick.py` built and runs end to end on Burnham in 40 s: card, traced hair,
  neck and shoulders, glasses from the photo, three heads (A/B/C on the unsure measures), tuning loop, check, sheet.
  First sheet: 65/64/29%, first in a 4-photo line-up, but none passes (timid and wrong-way measures); not sent to Sam.
- **Next: chat 2 of 8, Opus high:** finish the face tool (list in For Claude), then Badenoch, then the Walliams
  replay (w06, w07, w01, w02; count tries vs his five chats), the name test (namer helpers), a kittest; send Sam
  both sheets. Then the critic bench (item 3, Opus medium).
- **Needs Sam:** nothing until the face sheets.
# Where things stand (project, 13 Nov; no film in progress; the aim: films at 15% of a week)
- **Newest work:** `claude/overnight-q-handover-check` (also pushed to the main line). Face tool chain runs on its own.
- **Rules that bite next:** 86 (every tool gets a kittest), 85 (cost watch), 30 (a repeated note: find why first).
- **Done (overnight chat 1, Job Q, Opus medium, ~2.2%):** `source/handover.py` (MAP; catalogue row; kittest
  `handover_drops` passes on Blessed's real chat 5 messages and notes files). The `log` hook (UserPromptSubmit) saves
  Sam's typed messages to `notes/ledger/sam/CHAT.md` and pushes. `end` / `start PARENT --film F` flag his asks not
  carried by a notes line written after he spoke, unanswered messages, unsent clips, an override he never typed.
- **Next: overnight chat 2, Opus medium: the critic bench (ranking item 3, `notes/ranking-list.md`).** Test on Blessed.
- **Needs Sam:** morning report: Y to the CLAUDE.md line that makes chats run `handover.py end`/`start` (pick Y).
- **OVERNIGHT RUN (Sam, 13 Nov 23:25 UTC): read `notes/overnight-run.md` first.** Order Q, critic bench, rounds-read-a-page,
  then people, places, moves, rough command; test only on Blessed (never Protest Tiers); each job may reach 150% of its
  estimate, then hard stop, `notes/morning-report.md`, next job. Face tool chain runs on its own.
- **Read:** this section; `guides/job-packs.md` "A tool job"; `source/facepick.py` MAP; rule 49.
- **Open rule requests:** none.
- **For Claude:** run `python3 source/facepick.py burnham OUT references/faces/burnham/a01-front-parliament2026.jpg
  .../a02-front-national2026.jpg .../a03-front-smiling-ap2026.jpg --tq .../a04... .../a05...`. Faults to fix:
  1 tune() aims at the 3-photo card but check() scores the first photo only: score the tune on what check scores;
  5 damped rounds do not converge (more rounds, keep the best by check's own pass rule). 2 glasses too big and high:
  scale lenses by the cartoon eye width, not half the eye gap. 3 hair a flat blob: two tones from the photo (grey
  sides), a few strand lines. 4 skin too pink (`_flat` boosts saturation). 5 line-up only 4: `_others` should find
  every film's front photos. 6 sheet's third phone tile cut off. Badenoch: braids (hair mask down past the jaw).

## Where things stand (project, 14 Nov; no film in progress; the aim: films at 15% of a week)
- **Newest work:** `claude/rounds-read-page-c3` (also on the main line); face tool: its own chain.
- **Rules that bite next:** 86 (every tool gets a kittest), 85 (cost watch), 61 (MAP; now the page).
- **Done (overnight chat 3, item 6, Opus high, ~0.75%, at the stop):** `source/page.py` (MAP, catalogue row, kittest
  `round_page`): `story/FILM-page.md` = every film file's codemap (Blessed 8% of the code); `find "note"` gives FILE:LINE.
  Notes-round pack now reads the page. Handover check: helpers' reports and parent seeds no longer read as Sam's.
- **Waits for 4, 5, 7:** the page carries the people/places/moves description lines, so notes change the page.
- **Next: overnight chat 4, Opus HIGH: people from a description (ranking item 4), per `notes/overnight-run.md`.**
- **Needs Sam (morning report):** Y to people close-ups in every critique pack; Y to the Sonnet critic (Lost: Opus critic).
- **Bench left (a later chat, Opus medium, ~0.5%):** second case (animatic 2, from 51e8d9f); see `critbench.py` MAP.
- **Read:** this section; `guides/job-packs.md` "A tool job"; `notes/ranking-list.md` item 4; `notes/overnight-run.md`.
- **Open rule requests:** none.
- **For Claude:** `find` scores by shared words: a note naming a note number ("note 28") hits best; item 4 should add
  each person's description lines to `page.build`.


# Where things stand (project, 14 Nov; no film in progress; the aim: films at 15% of a week)
- **Newest work:** `claude/people-kit-c4` (also on the main line); face tool: its own chain.
- **Rules that bite next:** 86 (every tool gets a kittest), 85 (cost watch), 61 (MAP; the page).
- **Done (overnight chat 4, item 4, Opus high, ~2.3%):** `source/people.py` + `people_parts.py` (MAP, catalogue row,
  kittest `people_from_a_description`); `story/blessed-people.txt`: Blessed's 16 invented people as ~8 lines each,
  redrawn by the kit to 0.00% pixel difference on 8 finished frames. The page carries each person's lines.
- **Next: chat 4b, Opus MEDIUM (building from the clear plan below):** steps 2-4 of "Item 4" below (Brand, Walliams,
  the press pack, turned heads); then the sheets for the morning report. Hard stop: 12% for the job.
- **Face tool: HARD STOP** (chat 3, ~8.2% of 7.5%): Burnham, Badenoch pass. **Bench left:** animatic 2 case (~0.5%).
- **Needs Sam (morning report):** pick Burnham and Badenoch A/B/C; Y to ~1% more for the face tool; Y to rule 49.3's
  age-lines line; Y to people close-ups in every critique pack; Y to the Sonnet critic (Lost: Opus critic).
- **Read:** this section; "Item 4" below; `guides/job-packs.md` "A tool job"; `notes/overnight-run.md`; `people.py` MAP.
- **Open rule requests:** none.
- **For Claude:** replicate swaps the film's own dicts IN PLACE and pops `BC.FRONT_FACES`; `_front_head` is spied to
  prove who the kit drew. Bespoke heads join as parts (`EXTRAS`, `install`), never as film imports.



# Where things stand (archived 14 Nov, chat 4d) (project, 14 Nov; no film in progress; the aim: films at 15% of a week)
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



# Where things stand (project, 14 Nov; no film in progress; the aim: films at 15% of a week)
- **Newest work:** `claude/overnight-people-c4d` (also on the main line); face tool: its own chain (stopped).
- **Rules that bite next:** 86 (every tool gets a kittest), 85 (cost watch), 61 (MAP; the page).
- **Done (overnight chat 4d, item 4, Opus medium, ~2.2%; job ~6.8% of 8%, stop 12%): item 4 finished.** Steps 3-5:
  the press pack as a crowd (31 journalists from 16 lines), every invented face turns with its own face
  (`people_turned.py`), sheets in `notes/morning/people-kit-*.jpg`, morning report written. Kittest extended (20 people,
  6 frames, the press keyed the film's way at 0.00%); every old kittest passes.
- **Next: chat 5, Opus HIGH: places from a description (ranking item 5,** `notes/ranking-list.md` row 5): estimate 8%,
  hard stop 12%; test only on Blessed (its sets in `blessed_sets.py`); replication of Blessed's places is the pass mark.
- **Needs Sam (morning report):** people kit picks 1-3 (turned heads on, the journalists' own hair, approve the kit).
- **Read:** `notes/overnight-run.md` in full; `notes/ranking-list.md` row 5; `guides/kit-catalogue.md` "Places"; the
  MAP of `source/sets.py` and of Blessed's set file; `people.py` MAP only for how replicate is built (the same plan).
- **Open rule requests:** none.
- **For Claude:** replicate's turned-head score: each frame drawn again with `people_turned.ON = False` (crowds keep
  theirs); the pass mark is that score. `--film-keys` keys crowd heads the film's way (first member's colours).

# Where things stand (project, 14 Nov; no film in progress; the aim: films at 15% of a week)
- **Newest work:** `claude/places-kit-c5` (also on the main line).
- **Rules that bite next:** 86 (every tool gets a kittest), 85 (cost watch), 61 (MAP; the page).
- **Done (overnight chat 5, item 5, Opus high, ~2.2%; job ~2.2% of 8%, stop 12%):** the places kit's design (below),
  its core (`places.py`: language, level cameras, layers from depth, pieces, rule 83 boxes, replicate) and the
  courtroom's library pieces (`places_parts.py`); Blessed's court_box redrawn from 15 lines at 0.00%.
- **Next: chat 5b, Opus HIGH, same job:** the other 12 views (step 2 below), then steps 3-5. Handed over on amber.
- **Needs Sam (morning report):** people kit picks 1-3 (unchanged).
- **Read:** `notes/overnight-run.md` in full; this file's item 5 section only; `places.py` and `places_parts.py` MAPs;
  `blessed_sets.py` only the painter being lifted (MAP line numbers).
- **Open rule requests:** none.
- **For Claude:** convert px to metres with the view's camera: x = (X - 540) * d / lens, z = up - (Y - horizon) * d /
  lens, 4 places; pick each depth so ppm (lens / d) equals the piece's REF (or its look's ref): then no `detail`.



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
