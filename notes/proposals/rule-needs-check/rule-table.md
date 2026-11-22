# Rules to test, step 1: the table (lesson 7, rule-needs-check; changes no rule, no tool)

Made 22 Nov 2026 by chat 1 of chain A (Sonnet). Every figure below is read from the records (the rulebook, the kit tests, the Milburn and Grand Theft Autism notes, check-repairs, the case study, the unrouted list). Nothing was re-run on a film; "ever caught a bad example" means a kit test in `source/kittests.py` runs the check on a real earlier mistake (named), not that the check is fine today.

## The four numbers (to beat)

65 notes from Sam on two films: Milburn 33 (by hand, from the review) and Grand Theft Autism 32 (every numbered note in the notes and the shot 4 case study; Sam's earlier version 1 to 3 words are not itemised, so this count is low: lesson F7). Each note is sorted by the rule that should have stopped it, as the rules stand today.

| | what stopped it should have been | Milburn | Grand Theft Autism | together |
|---|---|---|---|---|
| **1** | a rule whose check is by hand, or a judge a chat must remember to run, and it was not done | 3 | 6 | **9** |
| **2** | a coded check that did not fire, was off, or gave way | 2 | 2 | **4** |
| **3** | no rule at all (or a rule with no check written) | 4 | 6 | **10** |
| **4** | a coded check that ran and missed | 2 | 13 | **15** |
| | not a fault: Sam changing direction, taste, new requests | 18 | 4 | 22 |
| | not recorded well enough to sort | 4 | 1 | 5 |

So 38 of the 65 notes were faults a rule could have stopped: 15 (40%) from checks that ran and missed (13 of them the same cause: the body, car and arm checks on Grand Theft Autism's shot 4 measured too little), 10 from no rule, 9 from by-hand rules, 4 from checks that did not fire. By-hand and no-rule together are 19 (50%): half the faults sit where nothing automatic was meant to catch them.

Plus 9 check-repairs findings (21-22 Nov; not Sam notes): by hand 3 (handover size, push notice, repeat counting), did not fire 4 (budget stages, model guard unwired, 11 red kit tests, tools built but not switched on), no rule 2 (a refused send reported as sent, the cost audit's "other" bucket). And 39 let-throughs of the proposal-route guard on its second try (15-20 Nov, unrouted.md): coded check gave way 39 times.

Caveats, named: (a) I sorted the notes from what the records say; Milburn notes 12 to 33 are known from the chats' "Done" lines, not Sam's exact words (four of them could not be placed); (b) where records do not say whether a check ran, the note is "not recorded", not guessed; (c) 13 of 15 "ran and missed" are one cause, so after the body-check fixes the real "missed" load may be far lower; (d) rules that look covered may be covered only when a film supplies the data the check needs (rules 5, 17 and 19 on Milburn and GTA: see the table).

## Counts across the 103 rules on the list Sam saw

By the kind the list gave: code 43, code + by hand 15, code + judge 7, judge 2, by hand 12, none 24. Step 1 finds seven of the 24 "none" rows do have a coded check (N6, N10, N16, N20, N21, N22, N24: all on, but not on the rulebook list). Of the 103: **42 have a kit test that runs the check on a real earlier mistake**; **61 never have**. Rule 61's own test (round_page) is red now, so it is counted among the 61. Rule 24 is paused by Sam. 30 rows have at least one note or finding against them (column "notes it should have stopped").

Switched on: the coded rows are on in pre-flight, a hook or finish.py, with three exceptions that matter: rules 5, 17, 19 (and 13, 16, 20) run only where a film hands in `scene(t)`, `layers(t)`, `movers(t)` or the lists they read; the 21 Nov wiring check now flags a tool nothing switches on (one open now: bench_move.py, not a rule).

## The table: every rule on the list Sam saw

Columns: id; the rule (short, from the list); its check as the rulebook names it; kind; whether it is switched on; whether it has caught a bad example (kit test); notes and findings it should have stopped (M = Milburn, G4/G7/G58/G8/GCS/GR = Grand Theft Autism, CR = check-repairs; the key is below).

| id | rule | check (rulebook) | kind | switched on | caught a bad example? | notes it should have stopped |
|---|---|---|---|---|---|---|
| | **Planning 12** | | | | | |
| 1 | One measured plan of every place, camera and who stands where; the layout is fixed at planning. | `plan.py` (pre-flight, with its true-gap check; skipped for a film with no rooms: `HAS`); the layout by hand | code + by hand | on only for films with rooms | no | - |
| 3 | Before building a place: 8–10 things that make it recognisable, our drawing beside your photos. Real places shown beside their photos before every animatic. | `benchmark.py` (pre-flight); the film's own route check (e.g. `traffic_faults`: every car on the road); critique S3, S2 | code + judge | on (pre-flight) | no | - |
| 8 | Rehearse the 3–4 riskiest moves as short clips first; your Showstopper Shots get everything the script implies. | `preflight.gate_warnings`: no "Rehearsal clips sent:" line (date and file, or "none: why") refuses a film started from t | code | on (warns; refuses only films started from the 10 Nov template) | no | G4-9, G4-12, G4-13 (events the screenplay implies, not built) [by hand] |
| 10 | Framing, who looks where, and how long each beat holds are planned up front. | `LOOKS_AT` eyelines; holds: critique M2 | code + judge | on (LOOKS_AT lines only) | no | G58-2 (Jason faces forward while pointing) |
| 11 | Every shot drawn on one board (start, key moment, end) before any movement is built. | `python3 source/rough.py board FILM OUT.jpg` (every shot; the row from story/FILM-board.txt); `rough.py sent FILM OUT.jp | code | on, but gave way | yes: shot_board_every_shot, board_gate_refusals | M5 (reverse framing: 10 shots had no delivered board, the animatic stood in) |
| 14 | The pre-start check refuses to run with a blank brief row, no composition sheet, or anyone missing from a shot. | `preflight.gates`, `cast_faults` | code | on | no | - |
| 24 | The cost estimate and forecast (paused by you on 18 Nov). | `ledger.py estimate FILM PCT --stages` and `ledger.py stage FILM NAME` (the forecast line); `ledger.py auto` (the Stop h | code | PAUSED by Sam 18 Nov | yes: estimate_forecast_and_alarm, stage_share_stop (while on) | CR1 (stages never marked, notes never logged) |
| 26 | Every sound effect asked for in one message at planning; every swear bleeped. | `voices.bleep_check` (pre-flight; kittest `bleeps_every_swear`); where the bleep sits: by the sound | code + by hand | on | yes: bleeps_every_swear | - |
| 28 | Reuse before building; anything new is added to the catalogue of reusable parts. | `catalogue.py` sheet; updating by hand | code + by hand | by hand only | no | - |
| 38 | Everyone faces the camera by default; a three-quarter view only as a last resort, with a reason. | `plan.py` (`SHOT_MARKS`, `THREE_QUARTER_OK`); pre-flight refuses a film with people and no `SHOT_MARKS`, and `posecheck. | code | on | yes: drawn_angle_every_film | - |
| 74 | Every line and every shot gets an acting plan before the first animatic. | `preflight.gate_warnings`: no acting list refuses a film started from the 10 Nov template, warns on older ones; ticked o | code + by hand | on for a missing list and a speaker with no head life; the acting itself is by hand | partly: phone_size_poses | G4-1, G4-16, M8 (face read soft not cross), G58-2 |
| 86 | Learn first: anything new or difficult gets research or a tool first, proposed to you. | by hand: the proposal, its cost and Sam's Y in the job's or film's notes before anything is built | by hand | by hand only | no | - |
| | **Building 20** | | | | | |
| 2 | Doorways and windows show the real next room, never a flat colour. | `sets.house`; `sets.portal_faults` | code | on | no | - |
| 13 | Every check is shared and runs on every film and every person; anyone left out has a written reason. | `kitchecks.py`; the exceptions: `waivers.gate_faults` (pre-flight refuses any `*_OK`, `ALLOWED_POPS` entry with no row i | code | on | yes: exceptions_need_a_written_reason, every_face_has_a_mouth, moving_figures_*, townsfolk_not_in_the_house_walls, copies_in_a_group | M6 (face with no mouth: bad shape name slipped through), G4-10 (ERG bald fix lived in one film, not shared) |
| 20 | Held things point in 3D with the body, never at a fixed angle on screen. | `viewchecks.turn_faults` | code | on, only where the film lists LOOKS_AT/held things | related only: held_prop_through_the_camera | G4-8 (gun fired away from target; not recorded whether the check ran) |
| 22 | My set dressing is shown on the cast sheet and kept clear of where the action happens. | `audit.py`; critique S1 | code + judge | on | no | - |
| 32 | Falling pieces land flat, broadest side down, never overlapping. | `lying.py contact_faults` (bodies); pieces by hand (tilt at landing) | code + by hand | on for bodies; pieces by hand | yes: tilt_at_chest_height, lying_and_pose_checks (bodies) | - |
| 41 | Bodies and hands: poses come from the tested gallery and are never shown from a bad view; hands checked every frame. | `handcheck.py` every frame (hands, points, a held thing over or behind the head, hands meeting props, props hidden, the  | code | on (every frame, but only what it measures) | yes (10 tests: hands_round_the_head, hands_in_sleeves, pose_gallery, point_hand_shows_a_finger, elbow_folded_back_is_a_stop, shoulder_seam_caught, held_over_or_behind_the_head, body_check_shot4_v4, body_check_back_view, outfit_every_view) | G4-6, G4-7, G4-15, G7-1, G7-4, G8 (arms and bodies: check ran and missed); GCS (cast sheet: check never run on it) |
| 49 | Every famous face passes the likeness test before the cast sheet. | `likeness.py check` (run on the clean twin: the head script's `--clean`, as `blessed_walliams.py head --clean`); `likene | code | on (clean twin) | yes: facepick_* (6 tests) | M4 (Pat's dome "alien carrot man": likeness 62% passed) |
| 50 | Every famous person gets one shot with the face big enough to read. | `kitchecks.faces` from the film's `FAMOUS` list (pre-flight; kittest `famous_face_size`) | code | on | yes: famous_face_size | - |
| 63 | Running at the camera uses the proper front-on run. | `moves.audit` (gait numbers); `handcheck`; critique M3 | code + judge | on | no | - |
| 65 | A speaker with no face of its own (like the Sorting Hat) opens its mouth with the voice, one syllable at a time. | `mouths.loudness_open`; `voices.py` mouth check | code | on | no | - |
| 77 | Anyone with facial hair: the beard tool first, and you confirm its five lines. | `beardkit.py analyse` (its five lines, sent with the empty-face sheet); by hand | code + by hand | on + by hand | yes: facepick_beard_from_any_front | - |
| 78 | Leaning on a desk, table, wall or rail shows weight; nothing sinks into it; a reaching arm ends in a clear shape. | critique P1, P7 (full size, beside the reference photo (`references/body-weight/leaning-on-table-forearm-forward.jpg`: h | judge | judge + kitchecks rests | no | - |
| 80 | Seated people facing us show knees and lap; standing up never makes the head dip. | `sitting.py` checks (`check_no_sink`, the lap drawn when `j['lap']`); on films, `waivers.lap_faults` (pre-flight: seated | code | on | yes: standing_legs_straight_elbows_out, house_look_and_lap | - |
| 83 | Painted objects in a set never overlap unless meant; the same for people and what they hold. | `setcheck.py` (the film's checks(), so pre-flight); people and held things by hand: stills of every shot with props at p | code + by hand | on for sets; people and held things by hand | no | - |
| S2 | A hand moving an object is drawn over it; a resting hand stays just clear. | `kitchecks` (`TOUCHES`, `FREE_MOVES`) | code | on | yes: grips_contacts_and_carry, held_prop_touches | - |
| S5 | Pupils stay inside the eye on every character. | every cast's eyes cut to the outline (`burnham.face`, `remakes_cast._eye`, new casts `eyekit`); pre-flight's house style | code + judge | on | yes: eyes_cut_to_the_outline | - |
| S7 | The house look: paper grain, light top edges and soft shadows on every drawing. | `film_engine.look_faults` (pre-flight); kittest `house_look_once_in_pairs` | code | on | yes: house_look_once_in_pairs, house_look_and_lap | - |
| S8 | Bullet holes and marks only on real surfaces. | `kitchecks.marks` | code | on | no | G7-5 (blood splatter did not turn with the windscreen: rule covers holes, not this) |
| S10 | Riding: real speeds, and the rider's seat matches the pace. | `mounts.check` | code | on (films with a mount) | no | - |
| L1 | People lying down or seen from above have real depth. | `lying.py`; critique P7 | code + judge | on | yes: lying_shirt_and_nape, lying_neck_from_behind, lying_and_pose_checks | - |
| | **Checks 17** | | | | | |
| 5 | A bump test on every frame: nothing passes through anything. | `audit.py` (`scene(t)`, `ALLOWED_CONTACTS`; `sets.solids`) | code | on only where the film supplies scene(t) | no (audit has no test; only the render lock does) | G4-4, G7-3 (body through the car; ran and missed) |
| 6 | A pop-in test: nothing appears or vanishes mid-frame; crowds arrive and leave on screen. | `audit.py` (`ALLOWED_POPS`); critique M1 | code + judge | on; judge for crowds | yes: critique_where_pops (judge half only) | - |
| 7 | Recordings match the script and captions; mouths open once per syllable and shut in silence. | `voices.py --film` | code | on | no (subtitle timing tests only) | - |
| 16 | Direction of travel holds across a cut unless planned. | `viewchecks.direction_faults` (`movers(t)`) | code | on only where the film lists movers(t) | no | - |
| 17 | Whatever is nearer the camera hides what's behind it, everywhere. | `viewchecks.hide_faults` (effects against every scene thing); `viewchecks.layer_faults` (every listed thing against ever | code | on only where the film lists layers(t) (GTA did; Milburn did not) | no for hide_faults/layer_faults (rule 57 tests only) | G4-2, G4-3, G4-11, G7-2, G7-7 (see-through bonnet, body through car, hydrant water through car: ran and missed); M19 (name card clipping: Milburn had no layers(t)) |
| 18 | Every joke prop is big enough to read on a phone. | `viewchecks.readability_faults` (`JOKE_PROPS`) | code | on | no | - |
| 19 | Every check ends with pass, fault or “couldn't look”; “couldn't look” stops the animatic. | `report.py` (counts COULD NOT TEST in the summary's first line), `round.py`; pre-flight: a film with people and no `soli | code | on for the summary line; the stop for COULD NOT TEST was not wired on Milburn | no | M19 (clipcheck COULD NOT TEST carried as an old line, name card clipped twice); GR (v3 sent with every check off, Sam's order) |
| 57 | Nothing flips from in front to behind between two frames unless planned. | `clipcheck.flip_faults` on the film's `draw_order(t)` | code | on | yes: order_flip_mid_shot, near_thing_after_the_haze | - |
| 58 | The pre-start check runs only what the film contains and names what it skipped. | `preflight.py` | code | on | no | - |
| 59 | No animatic or final unless the pre-start check passed on the current version. | `film_engine.render` (the lock, the picture checks while drawing); `preflight.py` (`probe`, `picture_faults`); `kittests | code + by hand | on | yes: render_lock | CR (48 to 61 named lines carried through Milburn: rule 59 allows them with --faults-named) |
| 62 | Captions on in every animatic and final, in the series style. | `subtitles.py`; pre-flight caption check; `kittests.py subtitles_readable`; the 0.3 s start: `voices.caption_start_check | code | on | yes: subtitles_readable, subtitle_starts_on_its_word, finish_captions_by_default | - |
| 66 | A failed render leaves no file, so an old one is never mistaken for the new one. | `film_engine.render`; `kittests.py render_leaves_no_old_file` | code | on | yes: render_leaves_no_old_file | - |
| 67 | One pre-start check per round of fixes. | `preflight.py --text`; by hand | code + by hand | by hand (quick check on) | no | - |
| 70 | Captions, Hook Text and sign-off added at the finishing step; everything delivered at 1.1× speed. | `finish.py --film NAME`: captions, then 1.1x with pitch kept (`subtitles.SPEED`), then the Hook Text and sign-off; the c | code | on | yes: finish_delivers_at_one_point_one, caption_check_at_delivered_speed | - |
| 72 | No pose drifts back to rest just before a cut; no arm passes behind its own body or cape; turns snap. | the return: `kitchecks.cut_rests` (pre-flight, standing people; kittest `cut_before_the_return`); behind wings or cape:  | code + by hand | on for the return and camera feel; wings/cape by hand; turn by judge | yes: cut_before_the_return, camera_feel | - |
| 75 | The Hook Text sits where it hides nothing important, in the tilted card style. | `finish.py CLEAN OUT --film NAME`: reads `HOOK` and runs `hookcheck.py` first (refuses on a fault unless `--faults-named | code | on | yes: hook_text_planned | - |
| 85 | The cost watch. | automatic (`.claude/hooks/costwatch.py`, every step and every message; its warning lines count the chat's steps; kittest | code | on | yes: cost_watch_lines | - |
| | **Notes, review and sound 15** | | | | | |
| 29 | Every review copy shows the time and shot in a corner. | `film_engine.render` stamp | code | on | no | - |
| 30 | The notes table stays short; a note you've given before means a check is missing. | by hand; end-of-film pass (Stage 5) | by hand | by hand | no (handover_drops covers dropped notes, not repeats) | 9 repeats: M3, M5, M6, M19 (name card again), G4-10, G7-1, G7-4, G7-8, G8; CR (repeat notes never counted) |
| 37 | Sounds and reference photos are saved on GitHub. | `ledger.py log` (or `kept`) lists what git does not hold (kittest `sounds_and_references_kept`) | code | on | yes: sounds_and_references_kept | - |
| 43 | Who-looks-at-whom is tested at the shot's own camera. | `filmkit.eyeline(aim=, drawn=, at=)`, `look_sheet` | code | on | yes: looks_at_the_shot_camera | - |
| 47 | A small fix to a finished film is patched in, not fully redrawn, unless you say Y. | `film_engine.render` refuses a full-size full render once `animations/NAME.mp4` exists, unless `--full-ok` (Sam's Y, 13  | code | on | yes: nostamp_in_the_template | - |
| 48 | Frames are looked at on one labelled sheet; never an unchanged picture again. | `sheet.py` (default width) | code + by hand | by hand (sheet default width on) | no | - |
| 52 | The sign-off lasts 1.6 seconds and carries the next follow line. | `signoff.py` default and `follow_line.line_for` (via `finish.py`, which stops when the list is used up); kittest `follow | code | on | yes: follow_line_on_signoff | - |
| 61 | Every film's code opens with a short map, so a note is answered in one step. | `preflight.gate_warnings` (no MAP, or a file over 1,000 lines: a warning) | code | warning only; its test round_page was red for the whole of Milburn | red: round_page | - |
| 87 | Each of your notes is restated in one line with its fix (and a marked still) before fixing. | by hand (the reply to the notes; 'fails twice' from the seen-before mark, rule 30) | by hand | by hand | no | - |
| 88 | One check sheet per round of notes; after that, only the frames that changed. | by hand | by hand | by hand | no | - |
| 89 | Critique before every send: everything new is drawn alone beside its references and judged cold. | `critique.py` (`pack` adds the close-ups from the film's scene(t) or the spec's "people" boxes; a fresh Sonnet helper (S | judge | judge: runs only when a chat runs it | yes: critique_record, critique_library, critique_closeups, critique_each_fault_once, critic_bench_scores (6 more) | M1, M3 (goth hair: first look "not yet critiqued"); GTA shot 4 v4 went out on a point check plus a judgement at full size that missed 16 notes |
| S3 | No added background hiss; the hiss check listens only between lines. | `filmkit.hiss_check(voice=)` | code | on | yes: hiss_heard_only_between_lines | - |
| S4 | Video joins always at 24 frames a second. | by hand | by hand | by hand | no | - |
| S9 | One sound per hit, and only when the hit is on screen. | `kitchecks.sounds` | code | on | no | M26 (uzi sound in scene 3; not recorded whether it ran) |
| S11 | The softer voice polish on every film. | automatic: `mossad_audio.POLISH` (on by default); `mossad_audio.py soft NAME` shows each take before and after | code | on by default | no | - |
| | **Working with you 15** | | | | | |
| W1 | Messages: first line says what's needed; Done / Needs you / Next only when they have something in them; about 10 lines. | (a CLAUDE.md row) | by hand | by hand | no | - |
| W2 | No code names or file names in messages. | (a CLAUDE.md row) | by hand | by hand | no | - |
| W3 | One line per note, with Lost and Added lines for anything a fix takes away or adds. | (a CLAUDE.md row) | by hand | by hand | no | - |
| W4 | Questions numbered, my pick first; every open decision in one message. | (a CLAUDE.md row) | by hand | by hand | no | - |
| W5 | “Just go” skips waiting for your yes, never the checks. | (a CLAUDE.md row) | by hand | by hand | no | - |
| W6 | No animatic while a shot is missing anyone. | (a CLAUDE.md row) | code | on (preflight.cast_faults) | no | - |
| W7 | Unattended runs stop after one animatic. | (a CLAUDE.md row) | by hand | by hand | no | - |
| W8 | Every animatic carries the Hook Text and the sign-off. | (a CLAUDE.md row) | code | on (finish.py) | yes: finish_captions_by_default, follow_line_on_signoff | - |
| W9 | “I want a rule” means a permanent rule, written in the same chat. | (a CLAUDE.md row) | by hand | by hand | no | - |
| W10 | The proposal route: every change put to you goes through helpers and a blind judge first. | (a CLAUDE.md row) | code | on (Stop hook, propose.py) | yes: proposal_route_hook | 39 second-try let-throughs 15-20 Nov; 5 Milburn blocks (4 false); the two-check design let through plain questions |
| W11 | The right model for each stage; chats open the next chat themselves. | (a CLAUDE.md row) | code + by hand | on for models (hook); chain opening by hand | yes: model_guard_stops_routine_on_opus | CR2 (guard never wired until 21 Nov); Milburn chat 10 (chain limit: Sam started chat 11), chat 18 on Sonnet |
| W12 | The handover: one section, 15 lines at most, the 3 lines at the bottom of the message. | (a CLAUDE.md row) | code + by hand | on (handover.py end: size, lines, push) | yes: handover_drops, handover_status_checks | CR3 (notes over 4,000 words, handovers over 15 lines: no check), CR5 (no push notification) |
| W13 | A drawing that failed to draw (black in the render) is named in the message, with the seconds and the plan to fix it. | (a CLAUDE.md row) | code + by hand | by hand | no | - |
| W14 | The latest animatic and its clean render are kept on GitHub until the film is posted. | (a CLAUDE.md row) | code | on (finish.py; handover DRAFT check) | no | - |
| W15 | Start with the project attached; branches merged at the start; save to the main line at the end; the order for searching reference photos. | (a CLAUDE.md row) | code + by hand | P13 on; branches listed at start; rest by hand | yes: branch_printout_lists_only_real_work, message_saver_keeps_typed_messages | CR6 (a tool built but never switched on: Sam, 21 Nov) |
| | **Not on the rulebook&#x27;s lis** | | | | | |
| N1 | Be honest about what I can't do yet, and say what I'd need to learn. | (none on the rulebook list) | none | none | no | - |
| N2 | Fix the drawing, never the shot; every handover names what's locked by you. | (none on the rulebook list) | none | none | no | no breach recorded in GTA chats 28-30 (camera kept); nothing would have caught one |
| N3 | Seeing 1: look as a viewer, at phone size and then full size wherever two things meet. | (none on the rulebook list) | none | none; phone-size look is by hand (posecheck.py look for poses only) | no | the 13 GTA and 2 Milburn "check ran and missed" notes are this failing: looked as a measurer |
| N4 | Seeing 2: every note becomes a saved example that a check must catch. | (none on the rulebook list) | none | none | partly: critic_bench_scores (Blessed notes) | GTA v7 note 10 ("I do not know how to teach you to recognise it") |
| N5 | Seeing 3: before fixing a frame, name the check that missed it and improve it. | (none on the rulebook list) | none | none | no | every repeat (rule 30 row) |
| N6 | Seeing 4: for new shots, choose views the flat drawings can carry. | (none on the rulebook list) | code (found) | back-view check inside the body check: on | yes: body_check_back_view | GTA v3 F1, F5, F7 (found by Claude, not a Sam note) |
| N7 | Seeing 5: physical things behave physically (weight, solidity, cause and effect). | (none on the rulebook list) | none | none | no | G4-9, G4-12, G4-13, G4-14, G7-5, G7-6, G7-8 (no hit, no reaction, no turning marks) |
| N8 | Plain words, always. | (none on the rulebook list) | none | none (the plain-check proposal) | no | CR (plain words failed in the 19 Nov review chat) |
| N9 | Files under 50 MB, MP4 by default; only the finished film and the latest animatic on GitHub. | (none on the rulebook list) | none | none (ledger kept lists >10 MB only) | no | - |
| N10 | Offer an animatic before any full render; ask before the final and wait for a clear yes. | (none on the rulebook list) | code + by hand (found) | film_engine refuses a full-size render once the file exists (rule 47); the ask itself by hand | partly: nostamp_in_the_template | - |
| N11 | No check sheet before an animatic unless you ask. | (none on the rulebook list) | none | none | no | - |
| N12 | Notes on movement get a short clip of just those seconds. | (none on the rulebook list) | none | none | no | - |
| N13 | A question about the film is answered, not acted on. | (none on the rulebook list) | none | none | no | - |
| N14 | “Hold” means collect notes and change nothing until you say go. | (none on the rulebook list) | none | none | no | - |
| N15 | Up to three fix rounds on my own after each batch of notes, each with a two-line summary. | (none on the rulebook list) | none | none | no | - |
| N16 | The brief is a checklist, ticked before the first animatic. | (none on the rulebook list) | code (found) | preflight.gates refuses a blank "done?" row (rule 14) | no | - |
| N17 | Every stage aims at high quality, fewer notes and about a week per film. | (none on the rulebook list) | none | none | no | - |
| N18 | Every film is new: never repeat old characters, places or jokes. | (none on the rulebook list) | none | none | no | - |
| N19 | Before every handover, search the notes for rule requests not yet written. | (none on the rulebook list) | by hand (found) | by hand (handover search) | no | - |
| N20 | One wait per render, a push notification when it's done, and how long it took. | (none on the rulebook list) | code (found) | push_faults in handover end: on | no | CR5 (no push at handovers) |
| N21 | A fresh chat for every round of notes and every cost warning. | (none on the rulebook list) | code (found) | costwatch hook, amber and red (rule 85): on | yes: cost_watch_lines | - |
| N22 | Read little: this file, one pack, and only what a note names; notes kept short. | (none on the rulebook list) | code (found) | size_faults in handover end (notes 4,000 words): on | no | CR3 |
| N23 | Voices only, no sound effects unless the script names them; you record every voice. | (none on the rulebook list) | none | none | no | - |
| N24 | Hook Text in TikTok's white-box style; every video ends with the CranbriJoos sign-off. | (none on the rulebook list) | code (found) | hookcheck.py and signoff.py in finish.py: on | yes: hook_text_planned, follow_line_on_signoff | - |

Row ids W1 to W15 are the CLAUDE.md rows in the rulebook's last table, in the order Sam saw them; N1 to N24 are the "not on the rulebook's list" lines.

## Notes key (65 notes, 9 findings; class 1 by hand, 2 did not fire, 3 no rule, 4 ran and missed, E direction/taste, NR not recorded)

Milburn (33; 17 to 19 Nov). Chat 11, 13 and 18 notes are from the chats' Done lines.

| id | note | rule | class |
|---|---|---|---|
| M1 | goth's hair: blue and purple strands, not one block | 89 (first look never critiqued) | 1 |
| M2 | goth: brow, lip, nose piercings | new request | E |
| M3 | goth's hair "crest of an alien monster" (repeat of M1) | 89, 30 | 1 |
| M4 | Pat's bald dome "alien carrot man" | 49 (likeness 62% passed) | 4 |
| M5 | reverse two-shot framing poor (chat 6) | 11 (10 shots had no delivered board) | 2 |
| M6 | "character 3 has no mouth" (repeat of confusion over scene) | 13 (every_face_has_a_mouth; bad shape name slipped) | 4 |
| M7 | Andy's eyes look at Pat when he speaks | new request | E |
| M8 | Andy's last face should be more cross (it read as surprise) | 74, 89 | 1 |
| M9 | NEETs dodge and fire in personality | new request | E |
| M10 | Vimto and glass forward on coasters | new request | E |
| M11 | trim the gaps between scenes | new request | E |
| M12 | reverse re-stage, equal and centred (third pass) | direction after two failed stagings | E |
| M13 | shot 1's extra glass | satire guide "never add a joke/prop Sam hasn't approved" (no check) | 3 |
| M14 | scene 3 re-stage | direction | E |
| M15 | goth's first bolt | direction | E |
| M16 | angry brows tip into slashes through the glasses | no rule (brow cap lives only in Milburn's notes) | 3 |
| M17 | goth "stoked" grin | direction | E |
| M18 | lemon slice on Pat's glass | as M13 | 3 |
| M19 | name card clips hands (twice: chat 13, chat 18) | 17/19 (clipcheck COULD NOT TEST carried) | 2 |
| M20 | fourth of chat 13's notes | not recorded | NR |
| M21-M25 | five wording changes ('will have to', 'report', 'Hunger Games slash Battle Royale', 'where this one goes', 'recommend') | direction | E |
| M26 | uzi sound in scene 3 | S9 (not recorded whether it ran) | NR |
| M27 | goth backs off in the ambush | direction | E |
| M28, M29 | two of chat 18's nine | not recorded | NR |
| M30 | Swindon's crouch bob on a fixed second left over from the old clock | no rule (best-practice: tie beats to events; no check) | 3 |
| M31 | goth 'focused' in combat | direction | E |
| M32 | 'obtain' to 'receive' | direction | E |
| M33 | starred swear | direction | E |

Grand Theft Autism (32; 20 to 22 Nov).

| id | note | rule | class |
|---|---|---|---|
| G4-1 | Lucia's hands in opposite grips | 74 (acting by hand) | 1 |
| G4-2 | Jason's lower body visible through the bonnet | 17 | 4 |
| G4-3 | bonnet clipping and the sausage arm | 17, 41 | 4 |
| G4-4 | knees, door, wheel clip through the car | 5, 17 | 4 |
| G4-5 | a crowd of bald people (should be by city) | none: no rule anywhere | 3 |
| G4-6 | Jason a monstrosity (limbs curled) | 41 | 4 |
| G4-7 | arms come out of his back | 41 | 4 |
| G4-8 | the gun fires away from its target | 20 | NR |
| G4-9 | the cop not hit: no blood, no reaction | 8, Seeing 5 | 1 |
| G4-10 | all the cops bald too (repeat: the ERG fix did not carry) | 13, 30 | 3 |
| G4-11 | legs 2D, inside the doorframe | 41, 17 | 4 |
| G4-12 | the cop is a different cop from a few frames before | 8 (beat not built) | 1 |
| G4-13 | the hydrant is never seen being hit | 8, Seeing 5 | 1 |
| G4-14 | the bald crowd does not react to the explosion | Seeing 5 | 3 |
| G4-15 | the horror show in reverse | 41 | 4 |
| G4-16 | no acting notes anywhere | 74 | 1 |
| G58-1 | acting lacks imagination (use the focus kit) | direction | E |
| G58-2 | Jason faces forward while he indicates things | 10, 74 | 1 |
| G58-3 | Jason's arm poses need work | direction | E |
| GCS | cast sheet breaks body rules (sleeves, shoulders, Lucia a man's box body) | 41 (check never run on the sheet) | 2 |
| GR | "riddled from shot 4 on" (v3 made with every check off, Sam's order) | 19 | 2 |
| G7-1 | Lucia's arms still crossed on the wheel (repeat) | 41, 30 | 4 |
| G7-2 | see through the bonnet to Jason (repeat of G4-2) | 17 | 4 |
| G7-3 | Jason clips through two parts of the car | 5, 17 | 4 |
| G7-4 | the backwards arm, a gross sausage (third time) | 41, 30 | 4 |
| G7-5 | blood splatter is 2D, does not turn with the windscreen | Seeing 5; S8 covers holes only | 3 |
| G7-6 | no hydrant strike, no physicality | Seeing 5 | 3 |
| G7-7 | hydrant water clips through the car | 17 | 4 |
| G7-8 | no death reaction by the officer (repeat of G4-9) | Seeing 5, 30 | 3 |
| G7-9 | wobble the car for two seconds before it turns | direction | E |
| G7-10 | "so much wrong, I do not know how to teach you to recognise it" | Seeing 1-3 | E |
| G8 | "same arm problem" on 0.92 to 2:42 of version 8 (fourth time) | 41, 30 | 4 |

Counted: class 1 = M1, M3, M8, G4-1, G4-9, G4-12, G4-13, G4-16, G58-2 (9). Class 2 = M5, M19, GCS, GR (4). Class 3 = M13, M16, M18, M30, G4-5, G4-10, G4-14, G7-5, G7-6, G7-8 (10). Class 4 = M4, M6, G4-2, G4-3, G4-4, G4-6, G4-7, G4-11, G4-15, G7-1, G7-2, G7-3, G7-4, G7-7, G8 (15). E = 22, NR = 5.

Check-repairs findings (CR): CR1 budget stages never marked and notes never logged (rules 24/85, coded, did not fire); CR2 model guard never wired into settings (models rule, coded, not switched on); CR3 notes over 4,000 words and handovers over 15 lines (by hand, no check existed); CR4 chat 26 told Sam a refused clip was sent (no rule); CR5 no push notification at handovers (by hand); CR6 tools built but never switched on (coded, off); CR7 eleven kit tests red (coded, gave way); CR8 repeat notes never counted (rule 30, by hand); CR9 the cost audit's 69% "other" with nothing sending the dearest items to the proposal route (no rule).

## The six guides: rule-like lines, sorted

Method: a search for always / never / must / every / only found 349 lines (satire 128, best-practice 91, figure-rig 44, tiktok-design 31, critique-checklist 31, pose-gallery 24). Lines that repeat a rulebook rule are mapped to it; the rest are "rule (needs a check)" or "advice". Rules phrased without those words may exist: not found, named.

| guide | lines found | already a rulebook rule (check exists) | rule, no check written (needs a check) | advice |
|---|---|---|---|---|
| satire | 128 | 24 (rules 1, 2, 3, 5, 6, 13, 17, 19, 38, 47, 59, 62, 66, 67, 72, 75, S2, S3, S7, S10, 89, and `linecheck`, `frozen`, `copies` checks) | 9 | about 95 |
| best-practice | 91 | 14 (rules 1, 5, 17, 32, 41, 47, 62, 75, S2, S7, 89) | 12 | about 65 |
| figure-rig | 44 | 12 (rules 41, 78, 80, 83, S5; `figure.guard`, `check_on`, `moves.audit`) | 4 | about 28 |
| tiktok-design | 31 | 4 (rules 52, 62, 75; finish.py defaults) | 3 | about 24 |
| critique-checklist | 31 | 21 (the judge's own lines A3, P1-P14, C3, O1, O5, S4-S9, M1-M5: each is a rule whose check is the fresh-eyes judge; 9 of them match a rulebook row, 12 exist only here: P8, P13, C3, O1, O5, S4, S5, S6, S9, M2, M5, A3) | 0 | 10 (helper instructions) |
| pose-gallery | 24 | 3 (rule 41, posecheck.py, phone_size_poses) | 1 (hands behind the back from side or behind: "no check catches it", owed by check-repairs) | about 20 |
| **total** | 349 | 78 | **29** | about 242 |

The 29 rule lines with no check (satire.md and best-practice.md line numbers in brackets; each one is a rule an expert would want checked or dropped):
- satire: never add a joke or prop Sam has not approved [92] (hit twice on Milburn: M13, M18); never draw from memory, stop and ask [45] (rule 3 says so, no check refuses a build); look lines up by number, never position [37]; never copy photo texture, flat shapes only [61]; every prop at its real size [62]; never ahead of the voice [276, rule 62 covers captions only]; cut a recording only in silence [284]; animatic is always the small render [336]; never `pkill -f` [350].
- best-practice: never satirise Grenfell [29] and the organisations/logos line [28]; shots aimed at a person must hit, never pass in front [84]; bend, don't tilt [133]; never resize a person to fit a prop [138]; never slice a drawing of a body [144]; never give a tool an existing file's name [165]; no flicker [215]; chains and ropes never cross a face [300]; repeating actions vary, no twins [332]; stand-in voices never on anything sent to Sam [344] (breached by Sam's own orders on Milburn animatic 1 and GTA); mastered at about -16 LUFS [196].
- figure-rig: hips 15% narrower than shoulders on every character [46] (GTA's cast-sheet widths were set by eye with no check); a head prop fits the head as drawn [140]; no twins, side-by-side people never move identically [164]; clothes never change the skeleton [44].
- tiktok-design: never a held title card [45]; the first frame moves, with sound from the start [48]; Claude never suggests post lines or wording [135].
- pose-gallery: hands behind the back checked from side, three-quarter back and behind.

## What step 2 should take first (worst first, by these numbers)

1. Checks that ran and missed (15): rules 41 and 17 (and 5) on shot 4's body, car and arm: the check measures lengths and angles, not "reads as a person" or "passes through a car". Already partly rebuilt on 21 Nov (body_check_back_view, cutmatch); proof against Sam's own frames still needed.
2. No rule or no check (10 notes, 29 guide lines): Seeing 5 (a hit gets a reaction; marks turn with the surface; 7 notes), crowds by city (2), the brow cap, set-dressing Sam did not ask for, fixed seconds left over in film code.
3. By-hand rules (9 notes): rules 74 (acting, 4 notes), 8 (screenplay beats, 3), 89 (run the judge before the first look, 3).
4. Did not fire (4, plus 39 let-throughs, shared with step 3 and could-not-test): rule 19 COULD NOT TEST must stop; rule 11's board gate; checks never run on the cast sheet; checks off by order.
5. Rules never proved on a bad example: 61 of 103 (list in the table). Taste rules (74, 78, S5 shape, 89) need the judge proof.

## Cost and method

Step 1 ran on Sonnet in one chat (about 55 steps). Cost: see the line below, filled in at the end of the step. Nothing was changed except this file, the handover and the status line.
