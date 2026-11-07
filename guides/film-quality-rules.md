# The rulebook: every rule once, with the check that holds it

Every film (not quick videos) follows this page. Each rule is written here once; other guides say *how* (the tools,
the method) and point here by number. **A rule only holds if a check enforces it:** "check" names the tool that
pre-flight runs, or "by hand" (ticked on the check sheet before every animatic, or searched for at the handover).
When Sam approves a rule, it gets a row here in the same chat. Why each rule exists (the film and note that taught it)
is in git's history and `story/archive.md`, not here.

Working-with-Sam rules (asking, approvals, messages, handovers, models) live in `CLAUDE.md` only; they are listed at
the end with their checks.

## Planning
| # | Rule | Check |
|---|---|---|
| 1 | One plan of the world in metres per film: every place, opening, camera and facing; every shot reads from it. | `plan.py` (pre-flight; skipped for a film with no rooms: `HAS`) |
| 3 | Before building any place: 8-10 things that make it recognisable, our picture beside Sam's references on one sheet, each ticked. No references: stop and ask; never draw from memory. | `benchmark.py` (pre-flight); the sheet by eye |
| 8 | Rehearse the 3-4 riskiest moves as 2-3 s clips before building the rest. | by hand |
| 9 | Every group (crowd, police) has a plan for arriving, stopped and leaving. | by hand |
| 10 | Framing planned up front: the Hook Text's empty area, each key beat's hold (about 0.3 s per readable stage) and camera distance; no diagonal cameras unless the models hold up. | `hookcheck.py`; holds by hand |
| 11 | One rough composition sheet (the 3-4 key shots) before building. | `preflight.gates` ("Composition sheet sent:" in the notes) |
| 14 | Pre-flight refuses to run while the brief checklist has a blank "done?" row or no composition sheet was sent; a shot missing anyone in `SHOT_CAST` fails. | `preflight.gates`, `cast_faults` |
| 24 | Ambition estimate: the plan lists new builds and risky moves and the share of a week the film will cost. | by hand |
| 62 | Every cost estimate is checked against what past films actually cost (`story/archive.md`, `notes/archive/`) before it is sent, naming the films compared. | by hand (the estimate names them) |
| 76 | Every note on a person, place or prop is checked against every reference of it, not just the note's words; the sheet sent back shows ours beside each reference (Sam, 4 Nov: Islamocommunism's beard took three rounds because the fixes followed the words). | the side-by-side strip on the sheet (ours, then every reference); by eye |
| 25 | Eyelines and holds per shot: who looks where, how long each beat holds. | `LOOKS_AT` eyelines; holds by hand |
| 26 | Every sound effect listed at planning and asked for in one message; placeholders named in every send. | by hand |
| 27 | A bleep: Sam always says the word and I bleep over it (never ask); place it from the sound, never the script. Every swear is bleeped, whether or not the script writes it with asterisks (Sam, 4 Nov). | by hand |
| 28 | Reuse first (`guides/kit-catalogue.md`); every new build is added to the catalogue when building ends. | `catalogue.py` sheet; updating by hand |
| 35 | Lock the layout in planning (who sits or stands where, gaps, what must be in frame); a later change is named as a cost. | `plan.py` true-gap check; by hand |
| 36 | Say at planning when a tool is slow here; ask Sam once to allow pypi.org. | by hand |
| 38 | Front on by default (each person within about 25 degrees of the lens). A three-quarter view is a last resort (Sam, 3 Nov): only when no other way makes the shot work, listed with that reason. | `plan.py` (`SHOT_MARKS`, `THREE_QUARTER_OK`) |
| 68 | Characters are built in 2D first: front, side and back. A three-quarter view (or three-quarter back) is built only when the script calls for one, and named in the plan with the shot that needs it (Sam, 4 Nov). | by hand (the cast sheet shows front, side, back only) |
| 39 | 3D only when needed (the camera moves round or through it, 3+ angles that must agree, turned in the hand); otherwise one flat painting per camera, in layers. Each 3D build is in the estimate with its reason. | by hand (the estimate) |
| 40 | Showstopper Shots (Sam names them): before building, list the elements the screenplay implies (terrain, vehicles, props, how each moves, the action around, the effects); Sam approves or trims; ticked at the first rehearsal clip. | by hand |
| 44 | A usage budget per film; ask Sam for the week's figure only after a building stage, after the animatic and at the final; log it in the notes; over budget is trimmed before the next stage. | by hand (handover) |
| 54 | Build only what the camera shows: before splitting a model into parts, decide how its ending looks and which parts the camera sees break; build parts only there. | by hand (the plan) |
| 74 | Before the first animatic, every line gets an acting plan in the film's notes (shot and why, face, body, the word the move lands on), shown to Sam with the brief questions. Before the list is written, ask Sam what each line means wherever the tone could go two ways (sincere or wink, hopeful or doubtful), my pick first; there is no limit on questions, because a question costs far less than a fix (Sam, 7 Nov). | by hand (the notes' acting list, ticked on the check sheet); layout in `guides/satire.md`, "The acting list" |
| 55 | Every new build has its own cost in the estimate; each handover compares spent with estimated and names any item running over. | by hand (handover) |

## Building
| # | Rule | Check |
|---|---|---|
| 2 | Doorways and windows show the real next room (from the plan), never a flat colour. | `sets.house`; `sets.portal_faults` |
| 4 | Every set has layers (front, middle, back), a textured ground, and life. | by hand |
| 12 | Every person, prop, wall, door and piece of furniture is in the collision audit automatically; a film lists only what to leave out, with reasons (`SET_EXCLUDE`). | `sets.solids` in `audit.py` |
| 13 | Every check lives in the shared kit and runs on every film; never copy a check from a film file. | `kitchecks.py` |
| 20 | Held things aim in 3D with the holder's body, never at a fixed screen angle. | `viewchecks.turn_faults` |
| 21 | A limb pointing at the lens is foreshortened and drawn over the body. | by hand |
| 22 | My set dressing is shown on the cast or composition sheet, clear of every action spot, and in the audit. | `audit.py`; shown by hand |
| 23 | A film file over about 1,000 lines is split, one file per group of shots. | by hand |
| 32 | Falling pieces settle broadest side down, never overlap or rest on another piece, shadow only where they touch; a saved drawing records its camera. | `lying.py contact_faults` (bodies); pieces by hand |
| 41 | Every arm ends in a visible hand, every frame, every view. | `handcheck.py` (every frame) |
| 42 | Poses come from the tested gallery (`guides/pose-gallery.md`); a new pose is tested front, side and back first. | `posegallery.py`; picking by hand |
| 49 | Every famous head passes the likeness check (60%+, nothing pushed the wrong way, 1st in the line-up) before the cast sheet. | `likeness.py check` |
| 50 | Every famous person gets one shot with the face at least 240 px tall (of 1920). | by hand |
| 51 | The likeness pack: 3+ straight-on, close, not-smiling photos (plus three-quarter, talking, caricatures); photos beat caricatures. | by hand; `likeness.py card` warns |
| 53 | Long falling pieces land flat, never on their end. | by hand (tilt at landing) |
| 56 | A fault found in one piece is a fault of its kind: fix and test every piece of that kind (every piece a whale hits, not only the one Sam named). | by hand (check sheet) |
| S1 | People react before a hit lands. | by hand |
| S2 | A hand moves the object, drawn over it; a resting hand keeps 3 cm clear. | `kitchecks` (`TOUCHES`, `FREE_MOVES`) |
| S5 | Pupils are cut to the eye's outline. | built into `burnham.face` |
| S6 | Hips 15% narrower; a hem rises gradually on a lean. | built into `burnham.HEM`, `views.py` |
| S7 | No off-style shorthand (stars, sweat drops, motion lines). | `viewchecks.shape_faults`; sweat drops by hand |
| S8 | Bullet holes and marks only on real surfaces. | `kitchecks.marks` |
| S10 | Riding: `mounts.py`, real pace speeds, the rider's seat matches the pace. | `mounts.check` |
| L1 | People lying down or seen from high have real depth (one 3D body, one outline, resting on the floor). | `lying.py`; the look by hand |

| 63 | Running straight at the lens uses the kit's `front_run` gait and `front_run_arms` (low knees, tucked elbows, fists pumping forward at the chest and belt), never the side-on run or arms out to the side. | `moves.audit` (gait numbers); `handcheck`; the look by hand |
| 64 | A standing person never bobs: breathing and panting are a lean only. Someone pointing or gesturing is shown from the front, never cut to from behind. Seen from behind, use a pose that reads there (`moves.reads_from_behind`): hands on hips read as hands behind the back. | by hand; `moves.READS_FROM_BEHIND` |
| 65 | A speaker with no face of its own (the Sorting Hat) opens its mouth with the voice's loudness, one syllable at a time. | `mouths.loudness_open`; `voices.py` mouth check |
| 77 | Anyone with facial hair: run the beard tool first; Sam confirms its five plain lines (moustache, patch under the lip, chin, cheeks, colour), correcting any in a word, before the cast sheet (Sam, 7 Nov). | `beardkit.py analyse` (its five lines, sent with the empty-face sheet); by hand |
| 69 | Whenever anyone points, the hand shows a pointing finger (one finger out along the forearm), in every shot and every film (Sam, 4 Nov). | `kittests.py point_hand_shows_a_finger` (the house circle hands draw it); the look by hand on the check sheet |
| 78 | Anyone resting on a surface (desk, table, wall, rail) shows the weight: the elbow bends slightly, the forearm comes forward and turns a little, and no part of the arm, hand or body goes below the surface; a limb reaching out ends in a clear shape, never half hidden inside something (Sam, 7 Nov). | by hand on the check sheet, full size, beside the reference photo; the forearm-and-elbow test in `kitchecks` is still to be built (only for arms the film's notes list as resting) |

## Checks (what pre-flight and the tools must do)
| # | Rule | Check |
|---|---|---|
| 5 | One automatic collision test on every frame, swept areas included; only listed contacts allowed. | `audit.py` (`scene(t)`, `ALLOWED_CONTACTS`) |
| 6 | One automatic pop-in test: anything appearing, vanishing or jumping away from the frame edge is flagged. | `audit.py` (`ALLOWED_POPS`) |
| 7 | Script and mouth audit: recordings against script and subtitles; a mouth opens once a syllable, shut in silence. | `voices.py --film` |
| 15 | Effect shapes are checked: no star, regular spike or motion line. | `viewchecks.shape_faults` (`EFFECTS`) |
| 16 | Direction holds across a cut unless the plan says it swaps. | `viewchecks.direction_faults` (`movers(t)`) |
| 17 | Every figure in front of an effect hides it. | `viewchecks.hide_faults` |
| 18 | Every joke prop at least 40 px (of 1920) at phone size. | `viewchecks.readability_faults` (`JOKE_PROPS`) |
| 19 | Checks print a short summary; a file is written only when the list is longer than the summary shows. | `report.py` |
| 57 | Nothing flips from in front to behind (or back) between two frames of a shot unless planned (`ORDER_SWAPS`). | `clipcheck.flip_faults` on the film's `draw_order(t)` |
| 58 | Pre-flight runs only the checks for what the film contains (`HAS`: people, rooms, voices, effects, props); each skipped check is named in one line with why. | `preflight.py` |
| 59 | No animatic or final render unless pre-flight passed on the code as it is now; faults Sam has been told about need `--faults-named`. Pre-flight is incremental (Sam, 3 Nov): after a clean run it re-checks only the frames whose picture changed (and a few round them) and the bodies in their shots, and runs the text and sound checks in full; it runs in full when there is no earlier clean run, the last run found a frame-level fault, the check code or the film's allow-lists changed, or with `--full`. | `film_engine.render` (the lock); `preflight.py` (`-frames.json` fingerprints); `kittests.py incremental_preflight_fingerprints` |
| 60 | The hiss check listens only in the gaps between lines (where the voice is silent), never in speech. | `filmkit.hiss_check(voice=)` |
| 62 | Subtitles are a few words at a time, each coming up on the syllable it starts with in Sam's take, and made readable when cut: on screen at least 0.8 s, at most 220 words a minute, two rows at most. | `subtitles.py`; pre-flight caption check; `kittests.py subtitles_readable` |
| 66 | A render that is refused, stopped or fails leaves no file: the old output is deleted before anything else, so an old render can never be taken for the new one. | `film_engine.render`; `kittests.py render_leaves_no_old_file` |
| 75 | The Hook Text position comes from the film's brief (`HOOK`) into `finish.py`, and the Hook Text check (rule 10) runs on every animatic and final. | `finish.py CLEAN OUT --film NAME`: reads `HOOK` and runs `hookcheck.py` first (refuses on a fault unless `--faults-named`) |
| 70 | Subtitles are burned in at the finish step (`finish.py`, with the Hook Text and sign-off), never in the picture render, so a note on subtitle wording, timing or Hook Text position costs seconds, not a render. | `finish.py --film NAME` burns in the film's `caption_at` when it sets `SUBTITLES_AT_FINISH = True` (the template does; its whole renders leave subtitles out, stills and `--span` clips keep them) |
| 71 | A subtitle's wording change never moves its timing: timing always comes from the script as spoken; the changed wording is swapped in afterwards. Each subtitle starts within 0.3 s of its first word in the take. | by hand (the check's subtitle printout against the take) until pre-flight checks it |
| 72 | No pose returns to rest in the last 0.4 s before a cut (cut before the return); no hand or arm passes behind the person's own wings, cape or body. | by hand (the last frames of each shot on the check sheet) until the audit checks it |
| 73 | A pre-flight fault Sam has been told about is listed once: the film keeps a named-faults list and pre-flight shows only faults not on it. | by hand (the handover's "faults named" line) until pre-flight reads the list |
| 67 | One full pre-flight per round: make every fix, run the quick check (`preflight.py NAME OUT --text`, seconds) until it is clean, then the full pre-flight once, then the render in the same background chain. A background job is stopped with its own task stop, never by name. | `preflight.py --text`; by hand |

## Notes, review and sound
| # | Rule | Check |
|---|---|---|
| 29 | Every review copy (clip, animatic) shows the film time and shot in a corner. | `film_engine.render` stamp |
| 30 | The notes table stays short (one line per note, no "Was:"); each note "new kind" or "seen before"; seen before means a check is missing: add it. | by hand |
| 33 | Anything that falls or piles up is tested on a short close clip before the animatic. | by hand |
| 34 | Mirror test: cast-sheet tiles against their sources; every shot checked for flipped faces, lettering, props and glances. | by hand |
| 37 | Sounds and references go on GitHub; only a file over about 10 MB stays off, listed in the handover's first line. | by hand |
| 43 | Looks are tested at the shot's own camera; eyes that meet shown one frame each on the check sheet. | `filmkit.eyeline(aim=, drawn=, at=)`, `look_sheet` |
| 45 | The composition sheet is sent once; notes on it are applied, never re-sent for approval. | by hand |
| 79 | Never say a change "looks right" from a small preview. Look at the frame a note touches at full size and say in plain words what is seen ("the hand sits on top of the desk, the elbow is bent"); a small preview only shows where to look. Unchanged frames are not re-read (Sam, 7 Nov). | by hand; the "Checks:" line names any fix confirmed at full size |
| 46 | When Sam names frames, look at exactly those first, at his size, before changing anything. | by hand |
| 47 | A small fix to a finished film is spliced in (`--nostamp`, exact frames, original sound, corner and frame-count check), or trimmed with ffmpeg where only silence is lost; a full re-render only when neither can do it, and Sam is told why. | by hand; `kittests.py nostamp` |
| 48 | Look at several frames as ONE labelled sheet (at most 1080 px wide; a crop for a detail); full size only for faces, Hook Text and frames Sam names. | `sheet.py` (default width) |
| 61 | Every new film's code opens with a short `MAP`: what is at which line (smoke, paths, wreck), kept in step as it changes; a note is answered by reading those lines. Finished films are not retrofitted. | by hand (handover) |
| 52 | The sign-off lasts 1.6 s on every film. | `signoff.py` default (via `finish.py`) |
| S3 | No added room tone. | `filmkit.hiss_check` |
| S4 | ffmpeg joins always at fps=24. | by hand |
| S9 | One sound per hit, only with it in frame. | `kitchecks.sounds` |

## Working with Sam (written in CLAUDE.md; listed here for their checks)
| # | Rule (CLAUDE.md section) | Check |
|---|---|---|
| P1 | "I want a rule" means permanent, written in the same chat (Rules are permanent) | by hand; handover search |
| P2 | "Just go" skips the wait, never the checks (Asking me) | by hand |
| P3 | No animatic with a shot missing its people (Asking me) | `preflight.cast_faults` |
| P4 | Unattended runs stop after one animatic (Asking me) | by hand |
| P5 | A repeated note means the first fix failed (Sending work) | by hand |
| P6 | One handover section, 15 lines at most; old ones archived (Models and chats) | by hand |
| 31 | Routine work on Sonnet; a round of notes stays in one Opus-medium chat (Models and chats) | by hand |
| P7 | Every animatic carries the Hook Text and the CranbriJoos sign-off, made as the final is (Asking me) | by hand (`finish.py` on the animatic's clean render) |
| M1 | Every message opens with what I need from Sam, or "Nothing needed" (Messages) | by hand |
| M2 | Messages: Done / Needs you / Next, about 10 lines (Messages) | by hand |
| M3 | No code names or file internals in messages (Messages) | by hand |
| M4 | One line per note; losses and additions on their own line (Messages) | by hand |
| M5 | The self-review is one line (Messages) | by hand |
| M6 | The handover pasted into the chat is 3 lines (Messages) | by hand |
| P8 | Fewer rounds: moves checked against the acting list before every animatic (Models and chats) | by hand (check sheet) |
| P9 | Long check printouts filtered to the faults (Models and chats) | by hand |
| P10 | One wait per render, never repeated checks (Models and chats) | by hand |
| M7 | Questions numbered, answered by number or Y/N, my pick first (Messages) | by hand |

The old register gave S1 to two rules; riding is now S10. The old register and the old long rule texts are in
`guides/archive/rule-register.md` and git history.
