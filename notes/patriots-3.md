# Notes for Patriots 3 (one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover: overwrite it at every stage switch; move the old one to notes/archive/patriots-3-handovers.md)
- **Sounds are on GitHub now (Sam, 27 Oct: free assets, 4.3 MB):** `source/audio/patriots3-sfx/` (battlefield-ambience,
  distant-shots, german-angriff, german-see-enemy, german-fire-at-target, explosion, mg42, rubble-slide, field-artillery).
  Nothing to re-attach. Not placed in the film yet (voices-only build until Sam says).
- **Done (27 Oct, building, Opus):** Sam sent the missing photos (`references/patriots-3/` room-1, room-2, lean-1, -2,
  salute-1, -2, blast-1, -2, air-4, -5). Sam: **"Build without dialogue for now, just subtitles."** Built: the
  casemate (`patriots3_room.py`), the coast (`patriots3_coast.py`), the blast and dust (`patriots3_fx.py`), all the
  acting (`patriots3_act.py`), the film (`patriots3.py`: 3D gun with hands on its grips, subtitle chunks). Rehearsal
  clips (rule 8) done and fixed (dust over the Patriot, a pop in the push-in, weak flapping, a wrong-way glance).
  `python3 source/patriots3.py check`: audit clean. Pre-flight: shared checks clean; 11 named (10 subtitles under
  reading speed because the timing is a guess until the voices; shot 9 is 9.1 s, chosen: one unbroken shot from the
  slit). Sent: `review/patriots3-stills.jpg` and five clips (coast, turn, salute and flapping, blast, firing and
  push-in). No animatic yet.
- **27 Oct, round 2 (Opus):** Sam's notes 5-9 done (badge, boat through the slit, the coast, the poppy, his hands on the
  gun: note 9 fixed after the first animatic render; hand targets moved onto the receiver). Sounds (9 files) are on
  GitHub now and rule 37 is rewritten (on GitHub by default; only files over ~10 MB stay off).
- **27 Oct (latest): animatic 3 sent (`review/patriots3-animatic-3.mp4`) with Sam's real Patriot recordings; notes 15-16 done.** Earlier: animatic 2 sent (`review/patriots3-animatic-2.mp4`, 2.5 MB, 43 s)** with notes 10-14 done (see the notes table). Next: Sam's notes on it; final render needs a new yes. Earlier: test recording cut and animatic 1 rendered. `source/patriots3_cut.py` cuts
  `patriots3-test-all.m4a` into patriot-1..6, loader-1, loader-2, heil (placeholders; levelled, pauses shortened to
  0.25 s, sped up at most 1.27x to fit the film's slots). Sam's two first lines are very quiet in the take (boosted).
  Pre-flight: 9 named (caption speeds on the fast placeholders, line 4 syllables 27 v 23, shot 9 at 9.1 s chosen).
  Animatic with hook text "Small Boats Crisis, June 1944" and sign-off: `review/patriots3-animatic-vertical.mp4`
  (2.3 MB, 43 s), sent to Sam. `signoff.py` now scales the sign-off to a small animatic's size. Sam: pauses can go
  entirely (done to 0.25 s; say if he wants 0). Next: Sam's notes on the animatic; final render needs a new yes.
- **Rule requests and proposals not yet in a guide:** usage proposals 2 (budget per film) and 3 (composition sheet
  once) from 27 Oct, still waiting for Sam's numbers; and four kit lessons from this build, proposed (below,
  "Proposed kit lessons").
- **Files to open:** `prompts/patriots-3.md`; this file; `source/patriots3.py` (STORY, picture, checks),
  `source/patriots3_act.py` (timeline at the top), `patriots3_room.py`, `patriots3_fx.py`, `patriots3_coast.py`.

## What Sam has sent (27 Oct; he said "noted" only until the drawing request)
- References, `references/patriots-3/`: lander-pov-1..5 (D-Day seen from a landing craft, facing the beach),
  landers-1..5 (the craft), air-1..3 (D-Day from the air), bunker-1..4 (German bunker, MG crews, embrasure inside),
  german-1..6 (uniforms and soldiers), mg42-1..6 (the MG42, crews, firing at the beach).
- Sounds: D-Day beach warfare (3 files) and German soldiers' lines firing from the bunker (2 files). Not used yet
  (no sound effects unless the script names them).
- Requests: "Apply all our new drawing guidelines to the patriot character." "Design two German D-Day soldiers. Give
  them the ability to fire an MG42 through a bunker slit, one as the firer, the other as a spotter/reloader."

## The brief as a checklist (Sam's brief, prompts/patriots-3.md; the planning chat fills "done?")
| # | from the brief or a note | done? |
|---|------|------|
| 1 | The Patriot redrawn to all the new drawing guidelines | yes |
| 2 | Two German soldiers who fire an MG42 through a bunker slit, a firer and a spotter/reloader | yes (Gunner, Loader) |
| 3 | From high above the coast: black cliffs in the distance flashing with machine-gun fire | built: shot 1, black cliffs with one-frame flashes and tracers |
| 4 | Artillery thundering down into the sands and spray | built: 15 lumpy bursts of sand and spray |
| 5 | Six landers, stuffed to the brim with Allied troops, creep closer to the shore | built: six LCVPs, 36 helmets each, creeping in |
| 6 | A thunderous howl of gunfire | sound: needs Sam's files (subtitles-only build, Sam 27 Oct) |
| 7 | Cut to inside the bunker: the gunner fires, the spotter directs him | built: shot 2, two bursts; the Loader spots and points (barks silent for now) |
| 8 | Patriot (off): "Small boat problem?" The men turn around, startled | built: subtitle; they freeze 6.45, turn 6.95 (straight turn), startled |
| 9 | The Patriot framed in the bunker doorway, leaning nonchalantly: "What can I say? Foreign invaders coming across the sea? Happens everywhere these days." | built: shot 3, leaning on the west post, arms folded, ankles crossed |
| 10 | The soldiers look at each other and back to him: "Who are you?" | built: shot 4, glance at each other 12.6, back 13.1; the Loader asks |
| 11 | Patriot, approaching: "Just a concerned citizen. Just a regular man with regular problems." | built: shot 5, he walks up; hand on his chest on 'regular man' |
| 12 | Spotter: "Ah, you are with the Furhër?" Both soldiers perform the Nazi salute: "Heil!" | built: shot 6, both salute (front on), 'Heil!' once |
| 13 | Patriot: "Jesus Christ, lads. The Free Speech Police are everywhere. Save that s*** (shit) for Whatsapp." Visibly upset, waving his arm to quiet them, arms darting around | built: shot 7, front on, arms darting: up, pat down, point round, wag; bleep: no sound yet |
| 14 | An explosion hits the lip of the bunker; the soldiers stumble back | built: shot 8, flash, shake, dust, chips settle; Gunner thrown to the east wall, Loader staggers back |
| 15 | Patriot: "Anyway, got problems with the Establishment? People trampling on your sovereignty? Let's just say I'm here to assist." | built: shot 8, he walks to the gun on 'Anyway...' |
| 16 | Camera in the slit facing into the bunker; the Patriot mans the gun, shakes his head sadly: "They ain't even wearing poppies." | built: shot 9, camera in the slit; head shake 33.7 |
| 17 | He begins to fire; the bunker lit by muzzle flare | built: fires 36.6 (four bursts), room lit on every flash |
| 18 | Zoom back in on the soldiers standing dumbfounded in the background; their eyes meet in confusion | built: push-in 39.2-40.8; their eyes meet 41.0 |

## References as checklists
| reference | what it shows | ours matches? |
|---|------|------|
| german-1, -2, -6 | M40 helmet (dome, short visor, flared skirt, vent lugs), field-grey tunic, 4 pleated pockets with scalloped flaps, 5 buttons, collar tabs, breast eagle, Y-straps, black belt with steel buckle, triple ammo pouches, stick grenade, gas-mask canister, bread bag, canteen, ankle boots and gaiters / jackboots | yes (eagle drawn as a plain bird) |
| german-4 (MG gunner) | helmet cover, pistol, MG tool kit | net on the Gunner's helmet, holster and tool pouch on his belt |
| mg42-5, -6 | bakelite stock and brown grip, receiver and feed cover, vented barrel jacket, muzzle booster, front sight, bipod, belt from the left | yes |
| mg42-1, -4 | two-man crew at a concrete ledge; loader holding the belt from the box | yes |
| mg42-2, -3 | firing over the beach, big flash, hedgehogs | yes (flash in the house style: lumpy, no star) |
| bunker-1..4 | concrete casemate, embrasure, log roof, camouflage | concrete slit, earth bank and grass on top |

## Planning (27 Oct)
Composition sheet sent: 27 Oct, review/patriots3-composition.jpg

**Sam's answers (27 Oct):** 1 he says "shit", we bleep it, subtitle "s***"; 2 "Führer"; 3 "WhatsApp"; 4 the salute as
written but brief (under a second before he flaps them down), "Heil!" once, no symbols; 5 the SPOTTER (Loader) says
"Who are you?", both say "Heil!"; 6 recordings as listed, Voice Isolation off (told how); 7 the German barks as
planned, no subtitles; 8 the blast throws one (the Gunner) against the far (east) wall, the other (the Loader) back a
few steps, both faces turn to the camera on the west wall; 9 Hook Text "Small Boats Crisis, June 1944"; 10 about 44 s
is OK, judge on the animatic; 11 the poppy on the Patriot's jacket: YES; 12 no whistle before the blast. Photos: find
them (blocked: ask Sam). Sounds: he sent an explosion, an MG42 (the rapid burst is about 2.8-5.0 s into the file) and a
rubble slide (for the debris after the blast: Sam sent it, so it is asked for). **Go given.**

**Recordings Sam owes:** Patriot 1 "Small boat problem?", 2 "What can I say?...", 3 "Just a concerned citizen...",
4 "Jesus Christ, lads..." (says "shit"), 5 "Anyway...", 6 "They ain't even wearing poppies."; Loader 1 "Who are you?",
2 "Ah, you are with the Führer?", "Heil!"; Gunner "Heil!". Files: `source/audio/patriots3-<who>-<n>.m4a` (patriots3-heil
for the two Heils, or one each).

**The plan in metres** (`source/patriots3_plan.py`): x east along the slit wall, z north to the sea, y up; the Gunner's
spot at the gun is (0, 0). Casemate 4.6 m wide x 3.5 m deep (x -2.6 to 2.0, z -2.4 to 1.11), ceiling 2.4 m. The slit
in the north wall (x -1.3 to 0.62, sill 0.99 m, top 2.05 m, wall 0.7 m thick) shows the beach. The door is in the
back wall behind the gun and to its right (x 0.2 to 1.1, 1.95 m high) onto a covered concrete passage that runs east
to daylight. Marks: crew at the gun; turned to the door; facing the Patriot (side on to s6); after the blast against
the west wall (Gunner -1.7, -1.35; Loader -2.05, -0.6). Patriot: in the doorway (0.62, -2.32) leaning on the west
post; approached (0.75, -0.7); at the gun (0, 0).

**Shots** (times are guesses until the recordings): 1 coast from high above (0-3.6) | 2 behind the crew, firing, the
Loader's barks, "Small boat problem?" off, they turn (3.6-7.6) | 3 over their helmets, the Patriot in the doorway
(7.6-12.4) | 4 the crew from in front, the battle behind: a look at each other, "Who are you?" (12.4-14.5) | 5 the
wide from the back-right corner: he walks up (14.5-18.7) | 6 the crew side on: "Führer?", the salute, "Heil!"
(18.7-21.5) | 7 the Patriot, arms darting (21.5-26.3) | 8 the wide: the blast, they're thrown to the west wall, he
walks to the gun, "Anyway..." (26.3-33.5) | 9 from the slit: head shake, "poppies", he fires, the push-in on their
glance (33.5-42.6) | sign-off 2 s. About 44 s in all.

**Sound list (rule 26):** battlefield ambience (have; booms at 10.7, 28.7, 42.4, 60.4, 82.7 s for the artillery);
distant shots for the cliffs (have); German barks (have: see-enemy, fire-at-target, angriff); MG42 burst close up
(have: mg42, the rapid burst 2.8-5.0 s); explosion close up (have: explosion, peak at 0.6 s); debris falling after it
(have: rubble-slide); bleep (kit); slurp (sign-off).

**Ambition (rule 24):** new builds: the coast from the air (cliffs, beach, six packed craft, bursts, flashes); the
room's inside and the passage; Patriot poses (lean in the doorway, flapping arms, at the gun firing); the salute; the
blast, the stumble, dust and chips settling (rules 32-33); the room lit by the flash; the push-in. Reused: the cast,
the MG42, the slit, the beach backdrop, prepper_fx flashes/debris/smoke/room flash, moves.travel. Risky moves to
rehearse as clips: the turn round; the salute and the flapping; the blast and stumble; firing from the slit with the
push-in. Estimate: about 20-25% of a week (the coast about 5%).

**Usage (Sam, 27 Oct: "weekly usage seems to be increasing with each film")** proposals, waiting for his numbers:
(1) the coast as ONE painted shot (layers that move: craft creeping, bursts, flashes), not a 3D world: saves about
3-5% of a week (YES: covered by rule 39); (2) a rule: every film's plan states a usage budget (share of a week), and at each handover I ask Sam
for the week's figure and log it here; a film over budget is trimmed before the next stage (guides/film-quality-rules.md,
"Planning", and rule-register "by hand"); (3) a rule: the composition sheet is sent once; notes on it are applied and
named in the handover, never re-sent for approval (saves a round of pictures).

## Decisions made (my choices, Sam can change any)
- The Patriot is the same man as before: balaclava, black jacket with grey sleeves, combat trousers, PP and doodle badges.
- Gunner: about 30, lean, stubble, narrowed eyes, older tunic with the dark collar, jackboots. Loader: about 18, fair,
  round face, the later plain tunic, ankle boots and gaiters. Different on purpose so they never read as twins.
- The breast eagle is a plain bird with an empty roundel: no swastika anywhere.
- The slit is taller than a real one (up to 2.05 m) so the crew's faces read from the beach.
- MG42 sound: none of Sam's files is an MG42 burst; the clip is silent. (Later he sent `mg42`: the burst is 2.8-5.0 s.)
- (Build, 27 Oct) Shot 9's camera moved 70 cm west along the slit (-0.25 instead of 0.45): from the old spot the slit's
  east side hid the Gunner at the east wall. The Gunner's turned marks moved 14 cm east (their arms touched in the
  salute). The Patriot leans 12 cm further from the door's middle so his shoulder meets the post. His back against
  the wall at x 1.66 (the arms went into it at 1.72).
- (Build) The salute: the right arm swung up round the shoulder, the Gunner's straight up and forward (the Loader is on
  his right side), the Loader's up and out; the hands are the house's plain circles, so it may read as a raised fist:
  say if it should change.
- (Build) The blast is seen from inside (shot 8 looks along the slit wall): the flash lights the room, black smoke
  outside, dust rolls in, chips land and stay, the camera jolts; a bite stays in the lintel for the rest of the film.
- (Build) The German barks and the MG42 are silent until Sam re-attaches the sounds; the bleep has no sound yet.

## My additions (say no and they go)
- A camouflage net on the Gunner's helmet; a stick grenade in the Loader's belt; binoculars for the Loader.
- The beach through the slit: ships on the horizon, two landing craft, hedgehogs, smoke puffs.
- Earth bank and grass over the bunker; board marks on the concrete.
- In the room: ammo crates (front right), a shelf with a field telephone (east wall), a range card above the slit.
- A red poppy on the Patriot's jacket (Sam: yes).
- (Build, 27 Oct) A cable run under the ceiling and a caged lamp over the door (room-2); lamps along the passage; the
  trench, sandbags and grass seen at the passage's far end; two warships passing at the bottom of shot 1; shell
  craters and hedgehogs on the beach; the bite out of the lintel after the blast.

## Proposed kit lessons (27 Oct, building; waiting for Sam's numbers, nothing written into a guide yet)
1. `views.person`: a head can only turn the way the body's drawing is mirrored (a soldier facing us could not look
   to his other side). Fix in views.py: mirror the head by its own direction. (Worked round in patriots3.draw_actor.)
2. `sets.Cam.yaw_of`: uses the camera's own right, so a camera that only turns (a push-in) changes how people are
   drawn: the Patriot popped mid push-in. Fix in sets.py: measure from the line to the person (patriots3.view_yaw).
3. `lying.stand`: the camera tilt is measured at the floor, so close up a hand held out at chest height is drawn far
   too low (the salute sank to the chest). Measure it at chest height (patriots3._tilt).
4. Held 3D props: draw them through the real camera and put the hands on the grip points the camera sees
   (patriots3.hold_gun): the old way drew the MG42 sideways and below the Patriot in shot 9. Move into the kit.
Bugs fixed in the shared kit this build (fixes, not new rules): kitchecks dropped the camera tilt; voices.py did not
know "gunner+loader" speak together, flagged lines meant to have no subtitles, and matched "s***" to "speech".

## Notes
| # | shot | time | note | status |
|---|------|------|------|--------|
| 1 | crew, inside | all | the Loader's reach to the belt read as an arm round the Gunner ("a little cuddle") | done: he stands half a step forward beside the gun, belt held low under the feed; new kind |
| 2 | 1 (coast) | composition | come in closer; behind the cliffs read as more sea, not French countryside | done on the sheet: camera nearer, fields and hedgerows to the horizon; new kind |
| 3 | 6 (salute) | composition | front on to them | done: camera beside the Patriot, both face us; the arms must be foreshortened (rehearsal clip); new kind |
| 4 | 8 (blast) | composition | camera on the left (west) wall, side on: gun and blast left, Patriot right; their faces turn to us as they stumble | done in the plan: Gunner thrown to the east wall, Loader a few steps back, both face west; new kind |
| 5 | 7 (flapping) | 21.6-26.0 | his hand slips under his PP badge | done: the badge drawn under its own forearm and hand (`patriots3_cast._patch_under_forearm`); new kind |
| 6 | 2-9 (through the slit) | all | the boat seen through the slit is on the beach; it should still be out at sea (it would be unloading men under fire) | done: both craft near the horizon, smaller; new kind |
| 7 | 1 (coast) | 0-3.6 | the money shot, the hook: bunker redoubts the shooting comes from, more texture, bullets skipping in the water, boats not all on one heading, craters and scorch marks where shells land, more beach defences, ripples in the wakes, explosions varied and less cartoony; anything else from D-Day | done: casemates in the cliff face firing (flash at the slits, tracers), MG pits, cliff strata and ledges, shingle, sand ripples and pools, ragged scorched craters (old and new), wire, mined stakes, hedgehogs, steel gates, swell, bullets walking across the water, three kinds of burst (sand and drifting dust, a water column and foam ring, black smoke off the cliff top) as soft billows, each craft on its own heading with rippling wakes; additions (Sam: yes): two P-47s with invasion stripes, a rocket salvo, barrage balloons, inland smoke; new kind (note 2 was the framing) |
| 8 | 9 | 34.4-36.2 | the poppy visible when he says the poppy line | done: he stands up behind the gun, one hand on it, chest clear (33.5-36.25), never drawn mirrored facing us; poppy 24 units; new kind |
| 9 | 9 | 33.5-42.6 | his hand is not on the gun, it is to the side | done: hand targets moved from the grip's underside (11 cm below the gun, read as beside it) onto the receiver (`hold_gun`); new kind |
| 10 | all | all | where are the sound effects? (and: battle muffled inside the bunker so we focus on the dialogue, except while the MG42 fires) | done: `soundtrack`/`sound_events`: ambience, artillery and distant shots in shot 1; inside, the ambience muffled and low, opening up during each burst; MG42 bursts, explosion, rubble slide, bleep on "shit" (placed by syllable count on the test take); the barks now play (they are .wav and were never loaded); new kind |
| 11 | 9 | 39-42.6 | no push-in at the end; the soldier on the right isn't looking at the other (looking at the wall) | done: camera holds still; the Loader turns three-quarter to the Gunner (profile read as looking past him), eyes on him; repeat of the glance in planning row 18: the push-in framing hid it, and the head snapped to profile |
| 12 | 9 | 36.6-42.6 | his arm should be partly behind the gun (reference sent) | done: `views.person` 'wrap': arm drawn before the gun, only the hand over it, whenever the gun is nearer the lens than him (`hold_gun`); follows note 9 (the hand moved onto the gun, the arm stayed on top) |
| 13 | 1 | 0-3.6 | hook text in the sky, not over the action, as agreed | done: I ran finish.py without the film's HOOK height (y 300); repeat: the film's setting was not passed on. Always pass `--y` from HOOK |
| 14 | 9 | 39.75 | new line after his last: "Traitors." | done: line 12 (`patriots3-patriot-7.m4a`, Sam's take, trimmed), burst 3 moved to 40.65 to leave it clear, before their eyes meet (41.0) |
| 15 | 5 | 14.5-19 | change "regular concerns" to "regular problems" | done in the script and subtitles; Sam's real recording says "problems" |
| 16 | all | all | Sam's real Patriot recordings (7 files, 27 Oct 20:51-20:55, in order patriot-1..7 incl. "Traitors"); German lines unchanged | done: matched by order and words (speech reader), trimmed, pauses over 0.2 s shortened, no speed-up; line starts nudged (6 to 14.5, 7 to 19.0, Heil 20.75) so nothing overlaps; subtitles regrouped into longer chunks; the bleep on "shit" placed by syllable count (3.68-3.95 s into line 9) |
