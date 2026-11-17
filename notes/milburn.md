# Notes for Milburn (one file, numbered; mark each done as it is fixed)

## Where things stand (the ONE handover)
- **Rules that bite next:** 41 (every new pose looked at from the views it is seen), 89 (one critique pack for the build), 74 (moves land on their words).
- **Done (chat 5):** scenes 3 and 5 planned (shots 3, 5, 6, 7; timing; acting list rows 3-7; estimate); McFadden's head (face tool pick B, 62%; house head gains a bald piece, round glasses, bigger ears); Andy (Sam's finished head) and Pat in the people file; the Cabinet Room reverse built (places view `reverse`: fireplace, portrait, Vimto can, tall glass, name cards). Questions Q1-Q7 sent to Sam. Chat 4 (alongside): note 3, the goth's hair read as an alien crest: redone as a shag (people kit `hair: shag`: wolf cut, fringe, dark roots, blue panels), front only; still and 2a clip sent.
- **Spent:** chat 5 about 2.8% (Opus high, ~115 steps); film ~10.9% so far; estimate from here ~8.5 (total ~19%, over the 15% aim: two likeness heads, six held props).
- **Next:** chat 6, Opus HIGH (building new): the field turned level and further in with six grey plinths (`milburn_sets`: a level TiltCam at 1.6 m, the ring 150 m away); the props (crossbow from prepper_cast; katana, twin uzis, grenade new, flat); Andy and Pat seated in `reverse` (milburn.py: `reverse_shot` like `cabinet`); shots 3, 5, 6, 7 and lines 3-7 in SHOTS/LINES/SHOT_CAST; the moves in story/milburn-moves.txt (acting list rows 3-7); one critique pack; the goth's turned shag if shot 3 turns her (turned views draw long hair now); then Sonnet for the animatic of the whole film. Sam then sent scenes 6 (forest hunt: a NEW place, travelling camera, gunfire, flamethrower, morning stars) and 7 (four more reverse-shot exchanges): brief rows 38-52; plan them (shots, timing, acting list, estimate) before building. Q1 answered (scene 4). Take Sam's answers to Q2-Q7 first if in.
- **Needs Sam:** answers Q2-Q7; notes on the goth's new hair (note 3); recordings (lines 1-7 and 3b) when ready.
- **Read:** job pack Build; this file's Shots, acting list, estimate.
- **Open rule requests:** none.
- **For Claude:** facehouse: `hair: bald` (bald_shapes, bald, dome arc via L['round_top'], `L['dome']` caps it at -0.44), `ear_k`, glasses `round`/`w_k` (in the pick json); McFadden's pick at references/faces/mcfadden/pick (picked B, by Claude: Sam to confirm Q6); CAST['mcfadden']. places_tables gains fireplace, portrait, tall glass, can. The reverse view puts the lens 0.3 m right of Milburn's seat so both fit. Kittests failing before this film (named, not from it): facehouse_whole_head, round_page. Moves critique items from chat 3 still open (see archive). Branches named, not merged: claude/blessed-c2-mics-wip, claude/audit-honest-checker.

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
| 5 | Cabinet Room, the reverse (places view `reverse`, built chat 5) | from Milburn's seat, level 1.2 m, lens 1500 | Andy in the PM's chair (left of centre), Pat on his left (screen right); fireplace and old portrait behind Andy | 4 | 15.3-20.6 |
| 6 | Cabinet Room (shot 1's camera) | as shot 1 | Milburn | 5 | 20.6-27.6 |
| 7 | the reverse | as 5 | Pat speaks, eyes on Andy; then Andy arms up, folds them, leans back | 6, 7 | 27.6-34.0 |

Timing (stand-in, about 3.2 words a second): line 3 11.4-15.1; line 3b (Swindon's pow-pows) 12.6-14.6; line 4 (Andy)
15.4-20.1; line 5 (Milburn) 21.0-27.2; line 6 (Pat) 27.8-30.6; line 7 (Andy) 31.2-32.4. **The film is ~34 s so far**
(the first estimate said ~45 s for the whole film; with more screenplay to come it will run to about a minute).

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
| 23 | Scene 3. Camera: mid shot. Location: further into the field | planned: shot 3, level mid shot, 150 m in (field painting turned level: next chat) |
| 24 | The NEETs have found a series of weapons on grey plinths; like the lift, vary the positions to avoid a flat look | planned: 6 plinths staggered 3-9 m, never in a row |
| 25 | 1 (goth): hoisting a heavy crossbow, pleased with her choice | planned (acting list row 3) |
| 26 | 2 (rangy): picking up a katana from the plinth and staring at it, unsure | planned (acting list row 3) |
| 27 | 3 (Swindon): picking up twin uzis, 'pow, pow' motions and mouth noises, aiming at invisible targets | planned (row 3; pow-pows Q4) |
| 28 | 4 (waif): shaking, clutching a single large hand grenade like she's been charged with looking after an ostrich egg | planned (row 3; grenade size Q2) |
| 29 | "Each NEET must arm themselves before heading further into the Zone.—" (Milburn, voice over) | planned: line 3, cut on the dash |
| 30 | Scene 4 (Sam, 17 Nov: "Scene 4, not shot 5"; Q1 answered). Cut suddenly to the opposite side of the table from Milburn: the 180 of shot 1 | built: places view `reverse` (Q1: no shot 4) |
| 31 | New character: Andy Burnham (the Prime Minister in this film), angrily accusing, pointing furiously, clearly incensed; a Vimto before him | head ready (Sam's finished Andy); Vimto can built; pointing on the acting list |
| 32 | New character: Pat McFadden, Work and Pensions Secretary, beside Andy, listening patiently, fingers steepled; sparkling water in a tall glass | head built (pick B, Q6); tall glass built; steeple on the acting list |
| 33 | Andy: "God damnit, Milburn. You're pulling a Battle Royale slash Hunger Games on us, aren't you?" | planned (line 4) |
| 34 | 180 back to Milburn: nonplussed, softly spoken, attentive | planned (shot 6 = shot 1 camera) |
| 35 | Milburn: "This report has been long in the making. Would you care to hear the findings or would you prefer to interrupt?" | planned (line 5) |
| 36 | 180 again. Pat (eyes on Andy): "I'd like to hear where this goes, Prime Minister" | planned (line 6; eyes on Andy) |
| 37 | Andy throws his arms up, then folds them and leans back: "Fine! Continue." | planned (line 7) |
| 38 | (Sam, 17 Nov) Scene 6. Cut: travelling alongside the NEETs as they hunt through the thick growth of a forest | open |
| 39 | Weapons gripped in ways that show each one's personality (goth pleased with the crossbow, rangy unsure with the katana, Swindon gung-ho with the uzis, waif terrified nursing the grenade), with matching faces and acting | open |
| 40 | Milburn VO: "The NEETs will form a unit." | open |
| 41 | Gunfire rips from the greenery ahead | open (sound effect named by the script) |
| 42 | A blast of flamethrower fire whips outward | open |
| 43 | Morning stars whip from the trees | open |
| 44 | Milburn VO: "And will encounter teams of their erstwhile colleagues—" | open |
| 45 | Scene 7. Back on Andy: "You fucker! You're pulling a Maze Runner-Squid Games-Fortnite on me!" | open |
| 46 | 180 on Milburn: "I am sorry that you feel that way." | open |
| 47 | 180 on Andy, despairing and angry: "Are you or are you not sending NEETs to kill each other on live TV?" | open |
| 48 | 180 on Milburn: he looks briefly to the side with his eyes, then back to Andy | open |
| 49 | Milburn: "My report is nuanced and multifaceted. I also suggest taking away PIP after they obtain their life-changing injuries in the Blood Dome." | open |
| 50 | 180 on Andy: mouth open in angry outrage | open |
| 51 | Pat: "I think the backbenchers will like this one, sir." | open |
| 52 | (Scene 5 not given: Sam numbered 3, 4, 6, 7; taken as his numbering, not a missing scene, as Q1) | open |

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

## Exceptions (rule 13)
| check | who | why | looked at full size |
|---|---|---|---|

## Notes
| # | shot | time | note | line | status |
|---|------|------|------|------|--------|
| 3 | 2a, 2b, 3 | all | Goth's hair shape looks like the crest of an alien monster, not real hair; look into purple/blue dyed alternative hair and try again (Sam, 17 Nov; repeat of note 1's area) | why note 1's fix failed: strands fanned OUT from the crown like spokes, hair falls DOWN. New people-kit cut `hair: shag` (wolf cut from alt-hair photos: crown volume, choppy layers to the shoulders, heavy choppy fringe, dark roots, blue peekaboo panels and a blue fringe chunk) | fixed chat 4: still + 2a clip sent; front only (turned views fall back to long hair: build the turned shag if scene 3 turns her) |
| 2 | 2a | all | Goth: give her an eyebrow, lip and nose piercing (Sam, 17 Nov) | people kit: `piercings: brow, lip, nose` (silver, front head, sized to the face) | fixed chat 4: still + 2a clip sent |
| 1 | 2a, 2b | all | Goth's hair: blue and purple as different strands, not one block (Sam, 17 Nov) | people kit: `hair: ... streaks C` | fixed: wavy strands from the crown, blue and purple in turn (front on; side and back views not built, not used in this film); stills sent |

Decisions made:
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
- Pose looked at: Milburn (heard), aerial | 9.60 s | phone size, 17 Nov: deck level with the grass, tiny figures on it: reads
- Pose looked at: Milburn (heard), NEETs (seen), medium on the four | 6.30 s | phone size, 17 Nov: heads lifted, necks long, eyes up: reads as looking up, if gently
- Pose looked at: Milburn, single | 2.70 s | phone size, 17 Nov: seated upright, hands on the folder, leaned in on 'simple': reads
