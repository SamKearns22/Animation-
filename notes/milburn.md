# Notes for Milburn (one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover)
- **Rules that bite next:** 59 (pre-flight pass before the animatic), 89 (the 7 named critique faults still go in the Checks line), 41 (posecheck look/seen at phone size for scene 3's new moves and scene 6's sky shot).
- **Done (chat 11, Sam's notes 18 Nov):** reverse (4a/4c/7a/7c/7e): Andy and Pat equal and centred, same chairs, same depth 2.2 m, camera up 1.2 like Milburn's (lens 1450); Andy drawn after Pat (arm no longer half under the table); drinks smaller, front-left of each; chair buttons kept on the chair (kit); Pat faces forward throughout, eyes only to Andy. Shot 1: the extra left glass gone. Scene 3 re-staged: four plinths only (stapler and mace gone), goth front left lifts the crossbow off her plinth, pleased; rangy dead centre lifts and stares at the katana; Swindon back right takes the uzis and pow-pows; waif back left shaking with the grenade (35% smaller). Scene 6: goth jerks and fires a bolt into the air on the first gunfire, the bolt leaves the crossbow (empty until reloaded). House legs: knee holes on a bend fixed (views.py). Budget alarms paused by Sam (ledger ALARMS_PAUSED; rule 24 note); tracking continues. Clips and pictures sent for all.
- **Checks (for the animatic message):** the 7 chat 10 critique faults still named, not fixed (Andy's soft mouths; scene 3 four facing camera (Q1 torsos); round mouths on listeners; goth's stray blue strip, Pat's grey ear patch, Milburn's thin glasses; dashed morning-star chains; Andy's ball hands). Kittests: round_page, facehouse_whole_head failing before this film; places/moves "before Sam approves" tests are stale (Sam approved both 14 Nov), not a film fault; claude_md test passes once CLAUDE.md is unchanged.
- **Done (chat 12, Sonnet):** rule 41 poses looked at and recorded; rule 11 board (rows filled for the 10 new shots) sent and recorded; plan's window given a size (pre-flight crashed on it); animatic 1 rendered small (8 min), finished (Hook Text, sign-off), 3.8 MB, sent, kept in animations/drafts/.
- **Done (chat 13, Opus medium):** note 1 fixed. Why it looked wrong: scene 7's moods pushed the brow pull past scene 4's (rage 0.16, gape 0.22 + brows lowered); past ~0.14 the brows tip into steep slashes through the glasses. Now rage and gape use furious's 0.14 (anger kept by squint, lids, mouth). Rule 56: no other mood anywhere above 0.14. Clip of the last scene (38.9-65.1 s) sent, 1.1 MB, 2 min.
- **Done (chat 13, Sam's 4 notes after the brows, 18 Nov):** (a) scene 3 goth: new mood 'stoked' (big grin 'v:grin', squint) once the crossbow is up, plus a nod: "yeah, sick, this one's mine"; her dark lipstick doesn't show in the grin shape (told Sam). (b) Pat's glass: lemon slice off (`lemon 0`). (c) Name cards moved forward to depth 1.4, drawn over (layer over): clear of hands and arms in every reverse pose checked (fists, flung, folded, plead); Milburn's shot-1 card already clear. Why the clipping check missed it: it never ran on this film ("COULD NOT TEST": the film gives it no solids or layers), and that line was carried as an old quick-check line. Proposal for the end-of-film review: a check that could not test stops the animatic instead of passing as a line (proposal route first). (d) Fireplace from Sam's photo: 2 m wide, 1.75 m tall, scroll consoles on the jambs, iron frame (kit: fireplace `scrolls 1`), new kit pieces mantel clock and candlestick (places_tables), portrait back above it (Sam allowed it). Clip of scene 3 and a still of the table sent.
 48 quick-check lines, all there before this chat and none from the brow change (plan gaps, SHOT CAST 'never on screen' because the film has no scene(t) for the checker to read, house-style lists missing, two fast captions, the 'fucker' bleep waiting on Sam's recording). Named here; chat 14's pre-flight (rule 59) settles or names them in the animatic's Checks line.
- **Next:** chat 16, Sonnet (routine): animatic 2 (small; the 5 fixes of 18 Nov and Sam's voices; 71.8 s), finish.py (Hook Text, sign-off), send, save to animations/drafts/. Check that "Report" = line 1 by ear in the animatic message.
- **Note 1 (Sam, 18 Nov):** angry brows in the last scene: fixed chat 13 (see Done). 7c's 'despair' brows (up in the middle) left as they are: a worried look by design, not the angry brow.
- **Needs Sam:** his notes on the animatic; Q1 torsos, Q2 cast sheet tile (still open); sound effects for animatic 2 (gunfire, flame, morning stars; voices are in).
- **Read:** job pack Checks and animatic; this section.
- **Handover check (chat 11 end) settled:** rule 11 (10 shots, no delivered board: the animatic stands in, as before) and rule 41 (11 body moves: `posecheck.py look` then `seen` at phone size) are chat 12's first routine items, before pre-flight; the stale-test question was withdrawn and Sam told it went unjudged (06:11), listed for the end-of-film review.
- **Open rule requests:** none (the alarm pause is written in rule 24).
- **For Claude:** milburn.py FIELD3/PLINTHS3 (owner per plinth), _picked, ON_PLINTH; SKY_SHOT/_sky; props crossbow_empty; SEATS andy (-0.35, 2.2) pat (0.35, 2.2), SPLIT 540; places reverse camera up 1.2 horizon 900 lens 1450; moves: pat head_yaw lines removed; views.py knee fold > -0.8; places_parts chair_back buttons clipped. Branches named, not merged: claude/blessed-c2-mics-wip, claude/audit-honest-checker.

## The screenplay so far (Sam, 17 Nov: about 25% of the film)
- Title: Milburn. Hook Text: "The Milburn Report is released 😬"
- Context: Alan Milburn's report on NEETs (not in employment, education or training). Joke: the report advocates a
  battle-royale scenario; Burnham is outraged; Milburn keeps denying it, then describes the same scenario some more.
- Length: line 1 (7 words) ~2.5 s; line 2 (18 words) ~5.5 s; with the aerial hold, this part ~11 s, so the whole film ~45 s.

## Shots (draft, for the board)
| shot | place | camera | who | line | about |
|---|---|---|---|---|---|
| 1 | Cabinet Room | level, head height, straight opposite Milburn across the table | Milburn seated, empty chair each side | 1 | 3.0 s; Hook Text 0.5-3.0 s in the band above his head |
| 2a | lift shaft | level, head height, medium (to bottom of torso, room above heads) | 4 NEETs on the rising platform, 4 depths | 2 (Milburn heard over) | ~4 s; light sweeps down, all look up |
| 2b | field | high, looking down ~45 deg (my pick: keeps the peaks in the tall frame) | platform rising out of the ground at the centre | 2 ends | ~4 s; grass waving, forest ring, alpine peaks; tiny figures (F8) |
| 3 | field, ~150 m further in (forest ring ~150 m behind) | level, standing head height 1.6 m, mid shot (the nearest to the waist) | 4 NEETs by grey waist-high plinths at 3.0, 4.2, 5.4, 7.0 m, staggered across; 2 more plinths behind still holding weapons (Q3) | 3 (Milburn heard; Swindon's pow-pows under, Q4) | 11.0-15.3; cut on Milburn's dash |
| 4a | Cabinet Room, the reverse (places view `reverse`, built chat 5) | from Milburn's seat, level 1.2 m, lens 1500 | Andy in the PM's chair (left of centre), Pat on his left (screen right); the fireplace behind Andy, no portrait (Sam Q7) | 4 | 15.3-20.6 |
| 4b | Cabinet Room (shot 1's camera) | as shot 1 | Milburn | 5 | 20.6-27.6 |
| 4c | the reverse | as 4a | Pat speaks, eyes on Andy; then Andy arms up, folds them, leans back | 6, 7 | 27.6-34.0 |
| 6 | the forest (NEW place, chat 6 plan) | level 1.4 m, side on, TRAVELLING right with them at walking pace (foreground ferns and trunks race past, far trunks crawl: 4 depth layers); the camera eases to a stop on the gunfire | the four in single file walking right, turned three-quarter to us (yaw 35: faces read, weapons read): goth, Swindon, rangy, waif last; the attackers never seen, only their weapons from the greenery ahead (screen right) | 8, 9 | 34.0-41.6; cut on Milburn's dash |
| 7a | the reverse | as 4a | Andy explodes: up out of the lean, both fists on the table, then the point | 10 | 41.6-45.9 |
| 7b | shot 1's camera | as 4b | Milburn | 11 | 45.9-49.2 |
| 7c | the reverse | as 4a | Andy, despairing and angry | 12 | 49.2-54.4 |
| 7d | shot 1's camera | as 4b | Milburn: eyes to the side and back, then line 13 | 13 | 54.4-63.4 |
| 7e | the reverse | as 4a | Andy frozen, mouth open in outrage; Pat, eyes on Andy, line 14 | 14 | 63.4-68.4 (the end for now) |

Timing (stand-in, about 3.2 words a second): line 3 11.4-15.1 (Swindon mouths his pow-pows silently, Sam Q4 N);
line 4 (Andy) 15.4-20.1; line 5 (Milburn) 21.0-27.2; line 6 (Pat) 27.8-30.6; line 7 (Andy) 31.2-32.4; line 8 (Milburn
heard) 34.5-36.4; gunfire 36.7; flame 37.5; morning stars 38.2; line 9 (Milburn heard) 38.9-41.5, cut on the dash;
line 10 (Andy) 41.8-45.5; line 11 (Milburn) 46.2-48.7; line 12 (Andy) 49.5-54.0; Milburn's glance 54.6-55.3; line 13
(Milburn) 55.6-63.0; Andy's mouth falls open 63.5; line 14 (Pat) 64.8-67.6. **The film is ~68 s** (stand-in; Sam's
takes re-time it).

## Plan extras: estimate (rule 24; not yet entered in the ledger: waits on Q10)
Unmeasured share: sets and moves rows (nothing like a rising shaft or alpine vista measured yet).

| thing, build or risky move | KNOWN (where) or NEW | why (3D? parts the camera sees) | stage | estimate (% of a week) | measured from | spent |
|---|---|---|---|---|---|---|
| Alan Milburn (Lead: speaks, close) | NEW (people kit, `head: measured`) | flat, front only in shot 1 so far; front/side/back on the sheet | cast | 3.2 | rule 24 Lead unit | |
| 4 NEETs (Support) | NEW (people kit lines) | flat; front views, look-up pose | cast | 3.7 | rule 24 frame-of-Glimpses unit (likely low: Support) | |
| Cabinet Room | KNOWN in part (places kit: panels, chairs, papers) + NEW green curtains, baize table | one flat painting, one camera | sets | 1.0 | unmeasured | |
| Lift shaft + rising platform + light sweep | NEW | flat painting, walls scroll down as it rises | sets | 1.5 | unmeasured | |
| Field vista from above (grass in wind, forest ring, peaks) | NEW | flat painting in layers (F1 bands) | sets | 2.0 | unmeasured | |
| look-up pose x4, rise, grass wind | NEW (pose) | | moves | 1.5 | unmeasured | |
| shot board | KNOWN (`rough.py board`) | | board | 0.5 | | |
| animatic 1 | KNOWN | | animatic1 | 1.0 | | |
| notes round | | | round | 2.7 | rule 24 unit (past films: ~9 per round) | |
| final | KNOWN | | final | 0.35 | | |
| **total (old way)** | | | | **17.5** | past films landed 2.5-3.3x their old-way price | |

Rewritten after Sam (17 Nov: "if these two parts cost 17.5% something has gone terribly wrong"). Why the old figure was
wrong: it charged this quarter with the whole film's notes round, animatic and final (4%); it priced the five people at
hand-built rates (7%), but the people kit drew all five in about ten steps; the set lines were guesses. New, this part:
people done (in the plan chat's ~2.5%); Cabinet Room on the places kit 0.5; shaft + field paintings 1.5; critique 0.5;
look-ups and the rise 1.0; board 0.3; this part's share of animatic 0.3 = **about 4-5% more** (unmeasured: sets, moves).

## Plan extras: estimate for scenes 3 and 5 (chat 5; from this film's real chats: build 2.8%, moves 3.1%)
| thing | KNOWN or NEW | stage | estimate (% of a week) |
|---|---|---|---|
| Andy Burnham | KNOWN (face tool pick, Sam: "Andy is finished"; people kit) | cast | 0 |
| Pat McFadden | NEW head, done chat 5 (face tool B; house head's new bald piece, round glasses, ears) | cast | done (in chat 5) |
| Cabinet Room reverse | KNOWN room + NEW fireplace, portrait, tall glass, can (places kit), done chat 5 | sets | done (in chat 5) |
| field, level, further in + 6 grey plinths | NEW: the field painting turned level (milburn_sets TiltCam), plinths | sets | 0.8 |
| crossbow, katana, twin uzis, grenade (+ longbow, mace if Q3) | crossbow KNOWN (prepper_cast); the rest NEW, flat 2D props | props | 0.8 |
| moves: hoist, lift and stare, aim and recoil, shake; point, steeple, arms up, fold, lean back (seated) | pointing, arms folded, lean back, hands folded KNOWN; holding props, steeple, arms up NEW | moves | 2.5 |
| shots 3, 5, 6, 7 wired into the film | | build | 0.5 |
| critique | | critique | 0.5 |
| animatic 1 (Sonnet) | KNOWN | animatic1 | 0.4 |
| notes rounds (2) and final | | round, final | 3.0 |
| **total from here** | | | **about 8.5** (film so far ~10.6% incl. chat 5) = **~19% of a week**: over the 15% aim; why: this part doubles the cast (2 likeness heads) and adds 6 held props |

## Plan extras: estimate redone with scenes 6 and 7 (chat 6; spent before chat 6: 12.2%)
| thing | KNOWN or NEW | stage | estimate (% of a week) |
|---|---|---|---|
| field level + 6 grey plinths (scene 3) | NEW painting view (milburn_sets) | sets | 0.8 |
| props: crossbow KNOWN (prepper_fx); katana, twin uzis, grenade, spiked mace, "DLC" stapler NEW (flat 2D, held by grips) | props | 0.8 |
| table scenes 4 and 7 (Andy, Pat seated in the reverse; Milburn reused) | KNOWN cameras, NEW seated pair | build | 0.8 |
| the forest (scene 6): 4 parallax layers, travelling | NEW place | sets | 1.0 |
| walking three-quarter with weapons (4 walks; the goth's turned shag) | walk KNOWN (moves kit gaits), turned shag NEW | moves | 1.5 |
| gunfire flashes, a flame jet, two swinging morning stars | NEW effects | fx | 0.8 |
| table moves: point, steeple, arms up/fold/lean, fists, despair, eye glance, mouth open | pointing, folded, lean back KNOWN; the rest NEW | moves | 2.0 |
| critique (one pack) | | critique | 0.5 |
| animatic 1 (Sonnet) | KNOWN | animatic1 | 0.4 |
| notes rounds (2) and final | | round, final | 3.0 |
| **from here** | | | **about 11.6** = film **~24% of a week**: over the 15% aim; why: the screenplay doubled (34 s to 68 s) with a new travelling action scene and a second cast of two likeness heads |

## The world (rule 1): plans to come (`plan.py`) once the people and places lines exist
- Cabinet Room: green-baize table, Milburn mid-side facing camera; empty chair left and right of him; cream panelled
  wall behind with green damask curtains at a tall window (from the reference). On the table: red leather folders,
  cut-glass water glasses, name cards, papers, pens.
- Shaft: round, platform ~17 m across (10 people holding hands); the 4 stand near the centre at 4 depths.
- Field: shaft mouth at the centre of an open meadow; forest ring at ~300 m; alpine peaks far off.
- Cabinet Room turned round (shots 5, 7): from Milburn's seat (shot 1's depth 2.2) back across the table: Andy at
  shot 1's lens (directly opposite Milburn) in the PM's chair, Pat on his left; the fireplace wall 1.25 m behind them
  (marble fireplace centred on the PM's chair, the portrait above); red folders, his Vimto, Pat's tall glass, name cards.
- Field further in (shot 3): 150 m from the shaft towards the forest (ring 150 m beyond); six grey plinths 1.0 m high,
  0.5 m square, staggered at 3.0-9 m from the lens, never in a line.
- Forest (scene 6): thick growth, deep green, shafts of light; the four walk a narrow track 4.5 m from the lens,
  left to right, 1.4 m apart; the camera travels with them at 1.2 m/s, then eases to a stop (36.7). Layers: ferns
  and trunks 1.5 m (race past, partly over them), the track and its undergrowth 4.5 m (they walk here), trunks 9 m
  and 18 m (crawl). The greenery ahead (screen right, 3-6 m beyond the leader): gunfire flashes in the leaves, a
  flame jet whips out of a bush across the track, two morning stars on chains swing down out of the trees. The
  attackers are never seen (the VO names them: "teams of their erstwhile colleagues").

Rehearsal clips sent: none yet: why: no moves exist yet; chat 3 makes the light sweep + look-up and the rise as clips first

Shot board sent: notes/sheets/milburn-board.jpg (17 Nov, chat 2; story/milburn-board-sent.txt)

## The brief as a checklist
| # | from the brief (word for word) | done? |
|---|------|------|
| 1 | Title: Milburn. | yes (NAME) |
| 2 | Hook Text: The Milburn Report is released 😬 | planned (HOOK, band above his head); drawn by finish.py at the animatic |
| 3 | Scene 1. Location: The Cabinet room. | yes: places kit view `cabinet` |
| 4 | New Character: Ex-Minister Alan Milburn | yes (people kit) |
| 5 | Camera: Sat directly opposite Milburn at head height. | yes: lens 1.2 m, across the table |
| 6 | Milburn sits opposite, an empty chair at each side. He stares directly into the camera. | yes: chairs both sides; facing lens (gaze: moves stage) |
| 7 | "The essence of my proposal is quite simple." | stand-in timing until Sam records |
| 8 | Scene 2 Location: a large lift vent that is raising up through the earth and rising up into a wide field, with forest encircling and mountains in the distance. | yes: shaft + field paintings |
| 9 | Camera shot 1: head level, medium shot down to bottom of torso and leaving space above the head | yes: lens 2000, torso, room above |
| 10 | New characters: 4 NEETS, aged 17-20 | yes |
| 11 | 1. Alternative, overweight girl with big blue/purple hair, goth-adjacent clothing, blooming black dress, pudgy nose | yes (broader after critique) |
| 12 | 2. Thin rangy Arabic guy with pencil moustache, grey sweatshirt and trackies | yes (thinner after critique) |
| 13 | 3. A stout lad in a Swindon FC shirt, sports-casual attire, not very handsome but good build. | yes (broader after critique) |
| 14 | 4. A waif of a girl, woollen jumper with flowers on, glasses, nervous, clearly diagnosed with Autism and Anxiety, pale as if she never leaves her room. | yes |
| 15 | the characters stand at the centre of a large lift shaft upon the rising platform. | yes, near the centre |
| 16 | The platform is ten people across if they were holding hands. | yes: 17 m across |
| 17 | It is rising towards the light. | yes: wall slides down, light above |
| 18 | All four characters look up as the light sweeps down. | ticked: light sweeps; all four lift their heads and look up on "training" (moves file) |
| 19 | They are standing at four different distances to the camera. | yes: 2.6, 3.6, 4.8, 6.2 m |
| 20 | An aerial shot shows the lift rise into the centre of an open natural space — a wide field, lush green grass flowing in the wind, distant encircling forest and tall alpine peaks. | yes: 33 deg down; grass gusts; forest ring; peaks |
| 21 | "Those not in education, employment or training will be presented with a unique opportunity to serve their country." | stand-in timing until Sam records |
| 22 | (Sam, 17 Nov, chat 4) Wait for the animatic: it comes once scenes 3 and 5 are built | open |
| 23 | Scene 3. Camera: mid shot. Location: further into the field | built chat 6 (level field, a row across the frame, Sam note 5) |
| 24 | The NEETs have found a series of weapons on grey plinths; like the lift, vary the positions to avoid a flat look | built: 6 plinths staggered, stapler and mace in the near corners |
| 25 | 1 (goth): hoisting a heavy crossbow, pleased with her choice | built (raises it to aim off the right edge) |
| 26 | 2 (rangy): picking up a katana from the plinth and staring at it, unsure | built (holds it out flat, stares down) |
| 27 | 3 (Swindon): picking up twin uzis, 'pow, pow' motions and mouth noises, aiming at invisible targets | built (mouths silently) |
| 28 | 4 (waif): shaking, clutching a single large hand grenade like she's been charged with looking after an ostrich egg | built (grenade 1.6x, shaking) |
| 29 | "Each NEET must arm themselves before heading further into the Zone.—" (Milburn, voice over) | planned: line 3, cut on the dash |
| 30 | Scene 4 (Sam, 17 Nov: "Scene 4, not shot 5"; Q1 answered). Cut suddenly to the opposite side of the table from Milburn: the 180 of shot 1 | built: places view `reverse` (Q1: no shot 4) |
| 31 | New character: Andy Burnham (the Prime Minister in this film), angrily accusing, pointing furiously, clearly incensed; a Vimto before him | built (fists, the point) |
| 32 | New character: Pat McFadden, Work and Pensions Secretary, beside Andy, listening patiently, fingers steepled; sparkling water in a tall glass | built (steepled, eyes on Andy) |
| 33 | Andy: "God damnit, Milburn. You're pulling a Battle Royale slash Hunger Games on us, aren't you?" | built (line 4) |
| 34 | 180 back to Milburn: nonplussed, softly spoken, attentive | planned (shot 6 = shot 1 camera) |
| 35 | Milburn: "This report has been long in the making. Would you care to hear the findings or would you prefer to interrupt?" | built (line 5) |
| 36 | 180 again. Pat (eyes on Andy): "I'd like to hear where this goes, Prime Minister" | built (line 6) |
| 53 | (Sam, Q3) the extra plinths: "Spiked Mace and a stapler from DLC" | built (no "DLC" sign, Sam note 6) |
| 54 | (Sam, Q7) the fireplace only, no portrait over it | done (portrait gone) |
| 37 | Andy throws his arms up, then folds them and leans back: "Fine! Continue." | built (line 7) |
| 38 | (Sam, 17 Nov) Scene 6. Cut: travelling alongside the NEETs as they hunt through the thick growth of a forest | planned (shot 6, chat 7 builds) |
| 39 | Weapons gripped in ways that show each one's personality (goth pleased with the crossbow, rangy unsure with the katana, Swindon gung-ho with the uzis, waif terrified nursing the grenade), with matching faces and acting | planned (acting row 8) |
| 40 | Milburn VO: "The NEETs will form a unit." | planned (line 8) |
| 41 | Gunfire rips from the greenery ahead | planned (sound: Sam supplies for animatic 2) |
| 42 | A blast of flamethrower fire whips outward | planned |
| 43 | Morning stars whip from the trees | planned |
| 44 | Milburn VO: "And will encounter teams of their erstwhile colleagues—" | planned (line 9) |
| 45 | Scene 7. Back on Andy: "You fucker! You're pulling a Maze Runner-Squid Games-Fortnite on me!" | built (7a) |
| 46 | 180 on Milburn: "I am sorry that you feel that way." | built (7b) |
| 47 | 180 on Andy, despairing and angry: "Are you or are you not sending NEETs to kill each other on live TV?" | built (7c) |
| 48 | 180 on Milburn: he looks briefly to the side with his eyes, then back to Andy | built (7d: look keys) |
| 49 | Milburn: "My report is nuanced and multifaceted. I also suggest taking away PIP after they obtain their life-changing injuries in the Blood Dome." | built (7d) |
| 50 | 180 on Andy: mouth open in angry outrage | built (7e) |
| 51 | Pat: "I think the backbenchers will like this one, sir." | built (7e) |
| 52 | (Scene 5 not given: Sam numbered 3, 4, 6, 7; taken as his numbering, not a missing scene, as Q1) | answered (Sam Q1: Scene 4) |

## References as checklists
| reference | what it shows | ours matches? |
|---|------|------|
| references/milburn/milburn-official.jpg | front, slight smile; short swept side-parted light brown hair greying at sides; dark grey-tortoiseshell rectangular glasses; long face, strong straight nose, thin lips; navy suit, white shirt, navy patterned tie | |
| references/milburn/milburn-2014.jpg | three-quarter, talking; black thick-rimmed glasses; same hair swept up and back; navy suit, white shirt, dark tie | |
| references/milburn/milburn-1.jpg | older, small; no glasses; hair darker | (low use) |
| references/faces/mcfadden/a01, a02 (official, no glasses), a03 (2026, talking, glasses), b01 (2026, three-quarter) | bald dome, short grey-ginger sides, ears standing out, round dark tortoiseshell glasses, long face, thin lips; navy suit, white or pale blue shirt, blue patterned tie | yes (pick B; sheet notes/sheets/mcfadden/mcfadden-sheet.jpg) |
| references/milburn/cabinet-room-burnham.jpg | cream panelled walls; green damask curtains at a tall bright window; green-baize table; red leather folders; cut-glass water tumblers; white name cards; dark wood chairs with leather backs | |

## The acting list (rule 74, draft: faces wait on Sam's answers)
| line | who | shot and why | face | body | lands on |
|---|---|---|---|---|---|
| 1 "The essence of my proposal is quite simple." | Milburn | single, straight to lens: he is addressing us like a broadcast | ask Sam (Q4) | seated upright, hands folded on the folder, tiny lean in | "simple" |
| 2 "Those not in education, employment or training..." | Milburn (heard), NEETs (seen) | medium on the four: their faces are the joke | goth: unimpressed; rangy lad: mouth open; Swindon lad: chest out, squint; waif: shrinks, grips her sleeves | all four look up as the light sweeps down | "training" (heads up) |
| 2 cont. "...a unique opportunity to serve their country." | Milburn (heard) | aerial: the size of the arena is the joke | (tiny figures) | platform locks level with the grass | "country" |
| 3 "Each NEET must arm themselves before heading further into the Zone.—" | Milburn (heard), NEETs (seen) | mid on the four: their choices are the joke | goth: pleased, small smile; rangy: unsure, staring at the blade; Swindon: grinning, mouthing "pow"; waif: terrified, wide eyes | goth hoists the heavy crossbow to her shoulder; rangy lifts the katana off its plinth, holds it out flat and stares; Swindon grabs both uzis, swings them at invisible targets, recoil jerks; waif clutches the grenade to her chest in both hands, shaking | "arm themselves" |
| 4 "God damnit, Milburn. You're pulling a Battle Royale slash Hunger Games on us, aren't you?" | Andy | two-shot reverse: his outburst beside Pat's calm | furious: brows down hard, mouth wide, eyes on Milburn (the lens) | leans in, jabs a pointing finger at Milburn (a touch to the side, so the point reads) | "Milburn", again on "aren't you" |
| 5 "This report has been long in the making. Would you care to hear the findings or would you prefer to interrupt?" | Milburn | single, as shot 1: the calm is the joke | nonplussed, soft, attentive: neutral, slow blink, small head tilt | hands folded on the folder, still | "interrupt" (the tilt) |
| 6 "I'd like to hear where this goes, Prime Minister" | Pat | the reverse: he quietly sides with Milburn | patient; eyes sideways to Andy, never the lens | fingers steepled, elbows on the table; a small nod | "Prime Minister" |
| 7 "Fine! Continue." | Andy | the reverse | exasperated, then sulky | arms flung up on "Fine!", then folds them and leans back in the chair | "Fine", "Continue" |
| 8 "The NEETs will form a unit." | Milburn (heard), NEETs (seen) | travelling beside them: four misfits as a "unit" is the joke | goth: pleased, crossbow on her shoulder; rangy: uneasy, glancing at the blade; Swindon: grinning, gung-ho; waif: terrified, eyes darting | walking in single file; goth's crossbow shouldered, Swindon's uzis up at his chest swinging side to side, rangy holds the katana out in front like a torch, waif hugs the grenade in both hands at her chest | "unit" (Swindon swings the uzis forward, the others close up) |
| 9 "And will encounter teams of their erstwhile colleagues—" (after the gunfire 36.7, the flame 37.5, the morning stars 38.2) | Milburn (heard), the greenery (heard: gunfire) | the camera stops: what is ahead is the joke | shock on the gunfire; then goth grim and pleased, Swindon thrilled, rangy aghast, waif terrified, screaming | a jolt on the gunfire; then each dodges and hits back in character (note 9, chat 10): goth barely bothered, a cool lean aside from the flame, then looses a bolt, cocks, looses another, pleased; Swindon a token dip, sprays back wildly, a cocky bob under the morning star still firing; rangy ducks too deep, then hacks wildly back and forth at the morning stars over his head, aghast; waif waves the grenade over her head, screaming, eyes everywhere (no curling) | "colleagues" (the second swing) |
| 10 "You fucker! You're pulling a Maze Runner-Squid Games-Fortnite on me!" | Andy | the reverse: his explosion beside Pat's calm | rage: brows down hard, mouth wide | up out of the lean, both fists down on the table on "fucker", then jabs the point at Milburn (the lens) | "fucker" (fists), "Fortnite" (the point) |
| 11 "I am sorry that you feel that way." | Milburn | single, as shot 1: the non-apology is the joke | soft, sorry-not-sorry: small sympathetic frown with the faint smile | hands folded, a slow small nod | "feel" (the nod) |
| 12 "Are you or are you not sending NEETs to kill each other on live TV?" | Andy | the reverse | despairing and angry: brows up in the middle, mouth wide | both hands out, palms up, then shaking them | "live TV" (hands out) |
| 13 "My report is nuanced and multifaceted. I also suggest taking away PIP..." | Milburn | single: the shifty glance then the calm cruelty | eyes slide to the side and back first (54.6-55.3), then calm, faintly pleased | hands folded, still; small nods | "multifaceted" (nod), "Blood Dome" (smile) |
| (silent) | Andy | the reverse | outrage: mouth hanging open, eyes wide | frozen mid-lean | 63.5 (the mouth drops) |
| 14 "I think the backbenchers will like this one, sir." | Pat | the reverse, Andy frozen beside him | patient, a small approving smile; eyes on Andy | fingers steepled; a small nod | "like this one" (the nod) |

## Exceptions (rule 13)
| check | who | why | looked at full size |
|---|---|---|---|

## Notes
| # | shot | time | note | line | status |
|---|------|------|------|------|--------|
| 11 | all cuts (1/2a, 2b/3, 3/4a, 4c/6, 6/7a, and within 4 and 7) | whole film | Sam (17 Nov, night): "trim the pacing gaps between scenes so there is no interruption in the scene flow" | close the dead air at each cut: LINES starts and SHOTS cut times pulled together (stand-in timing until Sam records); each cut lands on the next line or action; DUR shrinks to match | fixed chat 9: 3.3 s of dead air taken out at four cuts (after the deck locks 1.3 s, after Andy's first rant 0.4, after "Fine! Continue." 1.0, after Andy's cross face 0.6); every time moved with it; film 68.4 to 65.1 s. Lost: the long hold on the locked deck |
| 10 | 4a-4c, 7a-7e (the reverse) | all | Sam (17 Nov, night): "the Vimto and sparkling water should come forward diagonal of Andy and Pat and sit on a little coaster" | places file, view reverse: the can and the tall glass moved nearer the lens, each diagonally in front of its owner (Vimto by Andy, water by Pat), each on a small coaster; fit with note 5's re-stage | fixed chat 10: the Vimto and the water forward on new round coasters (places kit: coaster), drawn over everyone, each diagonally in front of its owner; clip sent |
| 9 | 6 (and 3 if it fits) | 34.0-41.6 | Sam (17 Nov, night): "make the NEETs dodge and fire their weapons back in line with their personalities. The anxious girl should just wave her grenade around whilst freaking out." Waif: no curling round it; she flails the grenade, panicking. Goth, Swindon, rangy: each dodges and fires back in character | acting row 9 and forest_pose | fixed chat 10: goth leans aside, looses two bolts; Swindon dips, sprays, bobs under the star; rangy ducks deep, hacks at the stars overhead; waif waves the grenade over her head screaming (no curling, eyes open); clip sent. Lost: the waif's eyes shut |
| 8 | 7e (Andy's last expression) | end | Sam: "work on Andy's final expression, it should be more cross" | Andy's closing face (brows, mouth, head): visibly cross; rule 74 | fixed chat 9: the closing face now brows hard down and knitted, eyes narrowed, tight downturned mouth, chin dropped into a glare (was brows up: read as shock); clip sent. Lost: the mouth hanging open |
| 7 | 4 (Andy, mid-film, when he speaks) | the middle | Sam: "have Andy's eyes look over at Pat when he speaks in the middle of the film" | Andy's eyes and head life: eyeline to Pat on that line | fixed chat 9: on "Fine! Continue." (31 s, the film's middle; Pat has just sided with Milburn) Andy's eyes and head turn to Pat, back to the lens as he sulks; clip sent |
| 6 | 3, 6 (Swindon; Sam said "scene 4") | all | "character 3 has no mouth" (Sam, 17 Nov, chat 7) | Sam (17 Nov 23:11): "the no mouth character is the stocky lad in the weapon picking scene" = scene 3, the stout lad in the Swindon FC shirt (row 13), NOT scene 4. Check his mouth in every shot he is in (3, 6): the uzi-grinning "pow" mouth must show | fixed chat 8, checked chat 9: the pow mouth shows in scene 3 (11.7 s) and the grin in scene 6 (36.8 s), on the new turned head |
| 5 | 4a, 4c, 7a, 7c, 7e | all | "the scene composition in scene 4 as proposed is poor" (Sam, 17 Nov, chat 7) | the reverse two-shot's framing: re-stage (where Andy and Pat sit, the lens, what is behind them) | fixed chat 10 (rule 30: chat 6 failed with equal busts dead centre, 40% empty baize, fireplace hidden, cards cut): lens lower (1.02 m), Andy leaning in at 2.0 m, Pat sat back at 2.42 m, staggered across, the fireplace between their heads, name cards in frame, drinks forward; head life: Pat's head turned to Andy, Andy's head works the rants; clip sent. The bottom baize stays under TikTok's caption area |
| 4 | 4a, 4c | all | Pat: good likeness, but the bald dome is too tall and narrow: "alien carrot man" (Sam, 17 Nov) | facehouse bald piece: dome height (`L['dome']` -0.44) and its width over the temples | fixed chat 6: measured off a01 (skull widest at the temples, 1.1x the cheeks, a near half-circle over the top); facehouse bald dome now `dome_wide` 0.405, `dome` -0.33 (CAST mcfadden); still sent (notes/sheets/milburn/pat-dome-note4.jpg). Sam's words: "Good likeness", "suffering from the bald person 'extended head' problem where they look like an alien carrot man." |
| 3 | 2a, 2b, 3 | all | Goth's hair shape looks like the crest of an alien monster, not real hair; look into purple/blue dyed alternative hair and try again (Sam, 17 Nov; repeat of note 1's area) | why note 1's fix failed: strands fanned OUT from the crown like spokes, hair falls DOWN. New people-kit cut `hair: shag` (wolf cut from alt-hair photos: crown volume, choppy layers to the shoulders, heavy choppy fringe, dark roots, blue peekaboo panels and a blue fringe chunk) | fixed chat 4: still + 2a clip sent; front only (turned views fall back to long hair: build the turned shag if scene 3 turns her) |
| 2 | 2a | all | Goth: give her an eyebrow, lip and nose piercing (Sam, 17 Nov) | people kit: `piercings: brow, lip, nose` (silver, front head, sized to the face) | fixed chat 4: still + 2a clip sent |
| 1 | 2a, 2b | all | Goth's hair: blue and purple as different strands, not one block (Sam, 17 Nov) | people kit: `hair: ... streaks C` | fixed: wavy strands from the crown, blue and purple in turn (front on; side and back views not built, not used in this film); stills sent |

Decisions made:
- Handover check (chat 9, end) settled by handing on to chat 10, inside its re-stage and critique: the board redrawn for shots 3, 4a-4c, 6, 7a-7e and sent (`sent --board`) once note 5 re-stages the reverse; every table and forest pose looked at with posecheck.py at phone size after notes 5 and 9 change them (rule 41: looking now would be thrown away); head life for Andy and Pat from the voice (rule 74, HEAD_LIFE like Milburn's), built with note 5. Carried from chat 6 and 7's checks, not new.
- Chat 9 (18 Nov, 1 am run): the three-quarter proposal (notes/proposals/three-quarter-people.md) taken on Sam's advance Y (17 Nov 23:07: "Y the strongest recommendation"): Option 1, heads only; the torso (step 2) and the cast sheet tile (step 3) need their own Y: on the 09:00 list. Note 7 read as line 7 "Fine! Continue." (31 s, the film's middle, Pat has just sided with Milburn). Note 8: the hanging-open mouth dropped for a tight scowl (the open O read as "oh!"). Cost watch amber at 68 steps: notes 5, 9, 10 left to a fresh chat (no new round here).
- Handover check (chat 7, end) settled: FINDER: this chat built scene 6 new (forest_shot and milburn_forest.py did not exist), searching the code on purpose; no notes were fixed here.
- Sam, 17 Nov 23:07 (chat 7): "At 1am, continue this work until animatic 1 is done. At 1am, run the 3/4 build fix through the proposal tool. Y the strongest recommendation and proceed to remodel the characters with the new 3/4 kit and then show those poses in motion in scenes 4 and 6." Plus notes 5 and 6. Also carried: Sam's chat-6 words on scene 3 ("see them from the side rather than from directly on"; "move that camera to their side"; "their focus is to something on the frame's other side"; "our 3/4 characters still look like shit compared to our other poses"; "The direction is now correct"; "the actual models themselves have an immediate reduction in quality and fidelity"): the direction was fixed in chat 6; the models are the three-quarter job above.
- Sam, 18 Nov ~00:05 (chat 8), for the 1 am run: "I want any budget stops or other work freezes overruled until 9am. Save any Y or N questions until the end of the work. Complete as much as you can without my intervention." So until 09:00 18 Nov: a ledger STAGE STOP or other freeze is noted and carried on past (close the stage with `ledger.py stage` where it is done, name the figure in the final message), never a stop; every Y/N question goes in ONE numbered list at the end; the checks and the critique still run (CLAUDE.md: an override never skips them). Props stage closed on this (1.93% against 1.66%; coasters for note 10 are left, inside note 5's re-stage).
- Sam, 17 Nov (chat 6): "Y" to the budget stop (rule 24, 'sets' 14.88% against 3.72%: mostly the whole film's spend counted against sets, the estimate entered late): carry on, the forest built as flat sliding layers (~1%). Sound effects: "I will find the sound effects in time for animatic 2, along with the dialogue": animatic 1 has stand-in voices and no sound effects.
- Handover check (chat 6, end) settled by handing on to chat 7, in its build and critique: the board redrawn for the new shots (3, 4a-4c, 6, 7a-7e) and sent with `sent --board`; every table and field pose looked at with posecheck.py at phone size (rule 41; chat 6 looked only at its own stills); head life for Andy and Pat from the voice (rule 74, HEAD_LIFE like Milburn's); scene 6's poses once built.
- Handover check (chat 6, start) settled: BROKEN kittests (facehouse_whole_head, round_page) failed before this film, named again; NOT CARRIED quotes (note 1 = Sam's chat-5 answers) now carried word for word in note 4 and brief row 53.
- Sam, 17 Nov (chat 5's Q1-Q7): 1 Y, and the table scene is called **Scene 4** (not shot 5): shots 4a (Andy), 4b
  (Milburn), 4c (Pat, then Andy); cut straight from the field on Milburn's dash. 2 Y: the grenade ostrich-egg size.
  3: the extra plinths hold **a spiked mace and a stapler "from DLC"** (my reading: a plain office stapler on its own
  plinth with a small bright "DLC" tag, the video-game extra-content joke). 4 N: no pow-pow take; Swindon mouths it
  silently. 5 Y: purple Vimto can. 6: likeness good, but the bald dome is too tall: "the bald person 'extended head'
  problem ... alien carrot man" (note 4). 7 Y, "just do the fireplace": the portrait over it comes off.
- Handover check (chat 5, end) settled: FINDER: no notes this chat; it built new things (people and places lines, facehouse's bald piece, four places pieces) and read the film's code to plan the new shots, on purpose.
- Handover check (chat 5, start) settled: BROKEN kittests facehouse_whole_head and round_page failed before this film (since 15 Nov, named in protest-tiers' notes); Andy's head is drawn as the kit draws it now and is looked at in the cast sheet. NOT CARRIED (the goth's hair: "crest of an alien monster", "purple/blue dyed alternative hair") is note 1, fixed chat 4.
- Chat 5: no photo of the Cabinet Room's fireplace side could be fetched (Wikimedia refused; the tour page has none): the reverse is drawn from the room's known pieces and is Q7 to Sam.
- Chat 5: McFadden wears round dark glasses in his 2026 photos (not in the official portraits): the head has them.
- Handover check (chat 3, end) settled: FINDER: this chat built the moves and the film's face, clip and head-life code new, on purpose (no notes yet to look up).
- Handover check (chat 2, end) settled: poses (rule 41) and head life (rule 74) wait for the moves stage (chat 3: no moves exist yet); FINDER: this chat built the film's code new, on purpose (no notes to look up).
- Sam, 17 Nov 20:12: "Go ahead with the rest" = build this part (chat 2 did: board and cast sheet sent).
- Chat 2: the aerial is tilted 33 deg, not 45 (critique: 28 read as level; 45 loses the peaks in the tall frame).
- Hook Text sits in the band above Milburn's head in shot 1 (never over his face).
- Line 2 is Milburn's voice over the shaft and field shots; cut to the aerial on "unique opportunity".
- Sam, 17 Nov: all recommended answers taken (tone calm and reasonable with a faint pleased smile; aerial high and tilted; bright midday; red Swindon Town shirt, simple robin badge; the four faces as proposed). No new photos. No showstopper shots. Estimates Option 1.
- Handover check settled (17 Nov, plan chat): FINDER: no film code exists yet; the edits were new kit parts (people.py,
  people_parts.py), built on purpose. UNROUTED: the estimates proposal was judged (notes/proposals/estimates.md);
  the first ask lacked its "Critiqued: 8 found, 5 fixed, 3 named" line, given to Sam in the next reply.

## Record (pre-flight reads these lines here; never archive them)
- Pose looked at: Milburn (heard), the greenery (heard: gunfire), the camera stops | 37.50 s | phone size, 18 Nov: flame and a crouching dodge read; goth firing
- Pose looked at: Milburn (heard), NEETs (seen), travelling beside them | 32.00 s | phone size, 18 Nov: four in single file walking right, weapons read
- Pose looked at: Andy, the reverse | 29.00 s | phone size, 18 Nov: Andy leaning back, arms folded; reads as sulk
- Pose looked at: Pat, the reverse | 17.50 s | phone size, 18 Nov: Pat upright, hands steepled at the chest, still; the nod is small
- Pose looked at: Andy, two-shot reverse | 14.50 s | phone size, 18 Nov: Andy's arm out jabbing toward the lens side reads, mouth open
- Pose looked at: Milburn (heard), NEETs (seen), mid on the four | 12.50 s | phone size, 18 Nov: goth lifts crossbow, pleased; the four read in a row
- Pose looked at: Milburn (heard), aerial | 9.60 s | phone size, 17 Nov: deck level with the grass, tiny figures on it: reads
- Pose looked at: Milburn (heard), NEETs (seen), medium on the four | 6.30 s | phone size, 17 Nov: heads lifted, necks long, eyes up: reads as looking up, if gently
- Pose looked at: Milburn, single | 2.70 s | phone size, 17 Nov: seated upright, hands on the folder, leaned in on 'simple': reads
