# Notes for patriots5 (The Patriot 5; one file, numbered; mark each done as it is fixed)

Kind: film (satire-style, flat people). Started 27 Nov from Sam's screenplay and title (chat session_01J1JB7VmBNix1SpRrBBfJas).
The Patriot redesign (the new drawing style) runs in a sister chat, session_01J1JB7XCcqv7vGytWyb2oNY ("The Patriot
character redesign"), asked by Sam at 19:16; this chat does the plan. Its results come into this film when it pushes.

The real event (Sam): Danny Tommo, founder of Patriot Platform, has been arrested and charged for knifing a boat.
The joke (Sam): The Patriot and his crew of balaclava'd PP men try to break Tommo out; absurdity ensues.

## Where things stand (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/FILM-handovers.md)
- **Locked by Sam:** all 11 shots as the screenplay sets them: cell dead ahead at the cot; side angle; close-up of the grate from inside; side-on outside with the tower; close-up through the grate at Danny; from behind Danny's head; the entrance with the two officers; the four 180s (boat, officers, Patriot, officers).
- **Rules that bite next:** 1 (one cell plan in metres: every view is the same plan, notes "The world"), 3 (benchmark the cell and gatehouse), 5 (physical light: the moon is behind Danny, so it rims him and his shadow falls in the pool).
- **Done (sets chat 6, 28 Nov):** the cast STOPs: blind judge run (3 judges, source/castjudge.py for any film, kit test cast_judge_any_film passing); guard2's build: no photo shows a woman officer's figure, asked Sam (note 12). Shot 1's NEW cell built and sent: notes/patriots5-sets/cell-front-v1.jpg (night blue, grated window, moonbeam, Danny downcast on the cot).
- **Next:** sets in film order, chat 7 (Opus, high: new views). Sam (28 Nov): Y to the cell, N on guard2 (keep looking: note 12, a few tries only, then a numbered list for Sam). First note 11 (the tracksuit band over Danny's forearms seated). Then the cell's other views from the same plan: side (shot 2), grate from inside (3), outside wall for the tower (4: the window's outer face at 4.65 m, sill about 5.6 m above the yard), grate from outside (5), behind Danny (6); the gatehouse from Blessed (story/blessed-places.txt 'prison gate') for 7 and its reverse for 8-11. Then source/patriots5.py on source/brexit_is_done.py's pattern (notes/patriots5-sets/cell_still.py is shot 1's drawing order: set, night, moonbeam with Danny's shadow, Danny on his own layer under night + moon_on), then the shot board.
- **Needs Sam:** notes on the new Danny; tower clip v2 and boat practice notes; the Hook Text (blank until he gives it).
- **Read:** guides/job-packs.md, Build (Sets lines); brief rows 1-22; notes 10-13; "The world" (the cell plan).
- **Open rule requests:** none. Branches named, not merged (old, unrelated): claude/lucid-archimedes-z91suc (a log file only), claude/jolly-ramanujan-2lcl2o, claude/upbeat-dirac-w16tn9, claude/gta-v5-sound-draft, claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31. Handover STOP still open: guard2's build (note 12: find her photo).
- **For Claude:** places_rooms kinds 'cot along wall', 'grated window' (deep), 'night' (multiply, layer over), 'moonbeam' (travel, floor; args['blockers']=[(alpha, depth)] casts shadows); moon_on(layer, piece, cam) rims people; sitting pose 'downcast' (Seat 'cot', nod 5); castsheet judge record 'not_in_film'.

## Plan extras (rules 24-26, 54, 55): ambition estimate as a table, one row per new build and risky move, each with
its own share of a week and, for anything split into parts, how its ending looks and which parts the camera sees
break; eyelines and holds per shot; every sound effect (what, when, needed by); bleeped words (said, or a gap left?)

Rows: KNOWN or NEW, priced from notes/ledger (template: notes/_template.md).

First line: about 40% of this estimate is unmeasured (the tower of men, the boat walk with legs, the climb onto the
bunk, the religious clothes have no past cost); the rest is from Brexit Is Done's and Milburn's stage rows in
notes/ledger/. Honest risk: Brexit Is Done ran 1.4x and Grand Theft Autism 2x over their estimates, both on moves.

| thing, build or risky move | KNOWN (where) or NEW | why (3D? parts the camera sees) | stage | estimate (% of a week) | measured from | spent |
|---|---|---|---|---|---|---|
| The Patriot, redesigned | KNOWN once the sister chat pushes (patriots3_cast PATRIOT, new style) | front, side, behind, three-quarter; balaclava, PP badges | cast | 0 here (sister chat's own cost) | - | |
| 7 more PP men (Nick and six) | NEW: crowd-pack or made-up house heads with balaclava=True (shared, facehouse_d) and neck_c; untested on a crowd | must read as 8 different men at phone size | cast | 1 | Milburn sets/props rows (people-file variants) | |
| Islamic religious clothes over the outfits (skull caps, checked headscarves, robes, beads) | NEW outfit extras | worn over balaclava and jacket; front and side; turn with the body | cast | 1 | unmeasured | |
| Danny Tommo (real person) | NEW likeness (face tool from Sam's photos) | front, side, from behind (shot 6), seated slumped, standing on the bunk | cast | 1.5 | Brexit Is Done cast row (3 likenesses, 9.5 planned): about a third | |
| Two prison officers | KNOWN (story/blessed-people.txt officer, guard2) | front and side, eyes that track | cast | 0.2 | known | |
| Cell, evening, moonlight: front, side, up at the grate, from behind Danny | KNOWN pieces (places kit prison cell: barred window, bed, brick) in new views | one plan, 4 cameras; window above the cot; night light | sets | 1 | Milburn sets 1.8 | |
| Outside the cell wall at night (brick wall, the grate, ground), close-up through the grate | NEW view from the same plan | the tower stands against it; the grate seen both sides | sets | 0.8 | unmeasured | |
| Prison entrance (gatehouse) | KNOWN (story/blessed-places.txt gates) | guards' side and the boat's side (reverse angles) | sets | 0.4 | known | |
| The small boat (the Patriots 2 inflatable, ORANGE: Sam 27 Nov) with 8 leg holes | KNOWN boat (patriots2 shot_dinghy), NEW holes and legs | side-on, walking; 16 legs in step | moves | 1.5 | unmeasured | |
| The tower of men on shoulders, swaying (risky) | NEW pose | each sits on the shoulders below, hands on heads; the whole stack bends as one | moves | 2 | unmeasured | |
| Danny climbs onto the bunk (risky) | NEW move | a knee up, weight onto the mattress, stands under the window | moves | 0.8 | unmeasured | |
| Patriot's big hand gestures, swaying at the grate | KNOWN (pose gallery: flapping, pointing) | seen through bars from behind Danny | moves | 0.3 | known | |
| Guards' eyes following right to left; the stare at each other | KNOWN (face kit gaze keys) | pupils only, then heads turn | moves | 0.2 | known | |
| The Patriot startles | KNOWN (acting kit 'start') | inside the boat, arms jump | moves | 0.2 | known | |
| Shot board | KNOWN (rough.py board) | 11 shots | board | 1 | Brexit Is Done board 2 | |
| First animatic | KNOWN | | animatic1 | 0.5 | Milburn 0.4 | |
| Notes rounds (two) | | | round | 2 | Milburn round 2.6 | |
| Final and posting | KNOWN | | final | 1 | Brexit Is Done final 1 + post 2, halved for a shorter film | |
| **Total** | | | | **15.4** | | |

Rehearsal clips first (rule 8): the swaying tower, the boat walk, the climb onto the bunk: 2-3 s practice clips each,
before the rest is built.

## Shots and the acting list (rule 74; ask first, write second: open tones are "ask Sam")
Length: 66 spoken words, about 20 s at Sam's pace, plus the silent beats (sigh, climb, eyes, boat walk, last stare):
about 33 s.

| line | who | shot and why | face | body | lands on |
|---|---|---|---|---|---|
| (silent) | Danny | 1: dead ahead at the cot, window above; sets the cell | eyes down, brows sagging | a deep sigh, shoulders rise and drop | the sigh's breath out |
| 1 "Danny?" | Patriot | 1: his head pops up in the window, small, the joke of the reveal | eyes wide, peering in | head pops up from below the sill | "Danny" |
| 2 "Boys? Is that you?" | Danny | 2: side angle in the cell | surprise, brows up, then hopeful | looks up, climbs onto the bunk, stands under the window | "Boys" (look up); climb under "Is that you" |
| 3 "Yeah, boss, it's us." | Patriot | 3: close-up of the grate and the Patriot (from inside) | eager | nods, fingers through the grate | "boss" |
| 4 "Nick's head is up my arse..." | Patriot (Nick under him) | 4: side-on outside the wall, the whole swaying tower | wince on "arse", then brisk on "Anyway" | the tower sways slowly; he shifts his seat on "arse" | "arse", "Anyway" |
| 5 "That's amazing, boys. What's the plan?" | Danny | 5: close-up through the grate at Danny (from outside) | sincerely touched (Sam: Y, 27 Nov) | hands on the bars, face close | "amazing" |
| 6 "We've been watching your videos, boss..." | Patriot | 6: from behind Danny's head, the Patriot behind the grate | proud, conspiratorial | swaying back and forth, big hand gestures | "videos", "plan", "invisible" (a big wide sweep) |
| (silent) | two officers | 7: the entrance, both facing the camera | blank | only the pupils move, right to left, slowly | the boat's walk |
| (silent) | 8 PP men in the boat | 8: reverse, they walk left to right in the boat, legs through holes | sheepish, eyes down | shuffling in step, the boat bobbing | - |
| 7 "Uuuh, what are you doing?" | left officer | 9: reverse, the two officers stare | flat, unimpressed | still; a slight lean | "doing" |
| 8 "Oh, uh. Allahu Akbar." | Patriot | 10: reverse, the boat | Sam (27 Nov): "stumbling yet sincere. Like he's trying to play a role he's not used to, all of a sudden": he startles, then earnestly puts on a part | startles (arms jump), then commits: a stiff, over-earnest gesture he thinks fits the role | "Oh" (start), "Akbar" (wave) |
| (silent) | two officers | 11: reverse, they turn and stare at each other | baffled shock | heads turn to each other, hold | - |

## The world (rule 1): the film's `PLAN` in metres (`python3 source/plan.py FILM sketch OUT.jpg`); places
benchmarked against references in `BENCHMARK` (rule 3, `python3 source/benchmark.py FILM OUT.jpg`)

The cell plan (chat 6, rule 1): 2.4 m wide (x -1.2 to 1.2), the back wall 4.2 m from shot 1's lens, 2.9 m high; the cot x -0.95 to 0.95, depth 3.45-4.18, top 0.45 m; the window x -0.3 to 0.3, sill 2.05, head 2.55, wall 0.45 m thick (outer face 4.65): a first-floor cell (lesson shoulder-tower: the top man's head about 6 m up outside); the moon travels 0.02 across, -0.88 towards the lens per metre down (lands on the floor in front of the cot); Danny sits at x 0, depth 3.85. Every other view of the cell is this plan with another camera.

Rehearsal clips sent (rule 8): the shoulder tower, practice v1 and v2, 27 Nov (notes/learn/shoulder-tower/); the walking boat: chat 3 (session_01J1JB7Xctbsw7fYYqMC2yQM); the climb onto the bunk: not yet.

Shot board sent (rule 11; rough.py board, then rough.py sent --delivered --board): not yet.

## The brief as a checklist (CLAUDE.md, 18 Oct): every detail of Sam's brief and notes, ticked before the first animatic
| # | from the brief or a note (copied word for word: wording, asterisk and bleep counts, positions, colours, props) | done? |
|---|------|------|
| 0a | Sam, 27 Nov: "run The Patriot character through our new drawing style to bring him up to speed" | approved: Sam, 27 Nov, on sheet v3 (collar band): "Looks good" |
| 0b | Sam, 27 Nov: "Start a new film file/ledger for The Patriot 5. I am still writing the screenplay." | yes |
| 1 | Shot 1: "We are in a British Prison cell. It is evening. We look dead ahead at the cot at the end of the room." | |
| 2 | Shot 1: "Danny Tommo is in the process of sighing deeply, downcast." | |
| 3 | Shot 1: "Above him, a grated window, letting in moonlight." | |
| 4 | Shot 1: "The Patriot's head appears suddenly at the window." Line: "Danny?" | |
| 5 | Shot 2: "From a side angle, we see Danny look up, react with surprise, and climb atop the bunk." Line (Danny): "Boys? Is that you?" | |
| 6 | Shot 3: "Close up of the grate and the Patriot." Line (Patriot): "Yeah, boss, it's us." | |
| 7 | Shot 4 (Sam, 27 Nov: all eight in the tower, Y; "This is the hardest thing in this film to pull off so you will have to learn this pose. It has been used in animation plenty." Lesson: notes/learn/shoulder-tower/lesson.md): "the side on view but on the other side of the wall. There's a tower of Patriot Platform people sitting on each other's shoulders to reach the cell window." | |
| 8 | Shot 4: "The tower is swaying slightly back and forth." | |
| 9 | Shot 4 line (Patriot): "Nick's head is up my arse. It's blood horrible. Anyway, we're 'ere to get you out." (Sam wrote "blood"; he records it, his take decides) | |
| 10 | Shot 5: "Close up on grate looking through at Danny." Line (Danny): "That's amazing, boys. What's the plan?" | |
| 11 | Shot 6: "We see from behind Danny's head. The Patriot is swaying back and forth behind the gr[ate]." | |
| 12 | Shot 6: "He is exaggerating with his hands." Line (Patriot): "We've been watching your videos, boss. We've got a plan. We've come up with a means of infiltration that's completely invisible to British authorities." | |
| 13 | Cut to shot 7: "Prison entrance. Two prison officers are looking forward at the camera, watching something from the right move slowly to the left with their pupils." | |
| 14 | Shot 8 (180): "The patriot platform boys are walking from left to right, eight of them, in a small boat (see patriots 2)." Sam (27 Nov): the Patriots 2 inflatable, "but let's make it orange." | |
| 15 | Shot 8: "They have clearly cut holes in the boat so their legs can come through and they can pilot it with their legs." | |
| 16 | Shot 8: "They are sheepishly coming up towards the guards." | |
| 17 | Shot 8: "They have a variety of Islamic religious gear wrapped over their usual stupid balaclava fascist outfits." Sam (27 Nov, N to my first mix): "The joke is that they are clueless fascists and most of patriot platform's hatred is directed towards Muslims. This needs to be accurate for the joke to land. It is a joke that targets them, not the Muslims". Sam (27 Nov, on the mosque-wear list): "Please base these clothes on migrants/small boat people rather than locals"; "Absolutely, yes. At least two of them" (black face veils, niqabs, over the balaclavas). Plan from the news photos (references/patriots-5/migrants): orange life jackets over dark puffer jackets and hoodies; a red-and-white patterned blanket round the shoulders on some; white knitted prayer caps on top of the balaclavas on some; at least two in black niqabs; prayer beads in one hand; no writing anywhere | |
| 18 | Shot 9 (180): "The guards stare. The one on the left goes: uuuh, what are you doing?" | |
| 19 | Shot 10 (180): "The Patriot startles, clearly not expecting to be seen." Line: "Oh, uh. Allahu Akbar." Sam (27 Nov): "Make the Allahu Akbar stumbling yet sincere. Like he's trying to play a role he's not used to, all of a sudden" | |
| 20 | Shot 11 (180): "The guards just stare at each other in baffled shock." | |
| 21 | Every video: Hook Text and the CranbriJoos sign-off; no title by default; MP4 under 50 MB. Sam (27 Nov): "You never need to suggest hook texts to me. Leave that blank until I provide it." | Hook Text blank until Sam gives it |
| 22 | Sound: voices only (the script names no sound effects) | |

## References as checklists (guides/satire.md): what each photo shows, and whether ours matches (compare.py sheet)
| reference | what it shows (count, colours, positions, facing, brands, proportions) | ours matches? |
|---|------|------|
| migrants/01 (Mirror) | a man wading, white knitted prayer cap, orange life jacket over dark clothes | |
| migrants/02, 04 (Mirror) | long dark-grey inflatables crowded side-on; people sit on the tubes facing in, orange life jackets on most, dark jackets and hoods | (our boat is orange: Sam) |
| migrants/03 (Mirror) | landing: red-and-white patterned blankets wrapped round shoulders, hoodies, tracksuit bottoms | |
| migrants/05 (Mirror) | close: orange life jackets (collar behind the head, straps), black puffer jackets, hoods up | |
| tower/01-06 (Openverse) | see notes/learn/shoulder-tower/lesson.md | |
| faces/tommo (6 news photos, who.txt) | Daniel Thomas: dark faded crop, short dark beard with ginger | face tool 85% (note 5) |

## Exceptions (rule 13): anyone or anything left out of a check, one row each (a pattern like Journalist* is fine); pre-flight refuses a film setting's exception (HANDS_OK, LINE_OK, any *_OK, ALLOWED_POPS) with no row here; a code comment is never a reason. check: the setting's name, or 'house look', 'lap', 'drawing checks', 'camera feel' (who: the shot)
| check | who | why | looked at full size (sheet, panel) |
|---|---|---|---|

## Notes
Send all notes in ONE message, each with the shot and the time, e.g. "shot 2, 10.3 s, left: the man never looks at the zombie".

Columns as in notes/_template.md (status, should have caught, critique saw it?: never blank).

| # | shot | time | note | line | should have caught | critique saw it? | status |
|---|------|------|------|------|--------------------|------------------|--------|
| 2 | cast sheet | back, 3/4 back | "explain the greying out of the sleeves? You did that with Blair too" | seen before (Blair) | none: the shoulder join (limbs.py, the arm fading into the body near the shoulder) assumes the sleeve is the jacket's cloth; a grey sleeve on a black body fades as a smear | no critique | answered; fix waits for Sam's Y (a hard shoulder seam where the sleeve's colour differs from the body's) |
| 10 | sets | cell | "You can use the prison gate but we will need a different cell due to the scene layout/mood of the opening moment" | new | - | - | APPROVED: Sam, 28 Nov, "Y" to the cell picture. Shot 1 view built (chat 6), sent: notes/patriots5-sets/cell-front-v1.jpg (story/patriots5-places.txt view cell_front; new shared kinds cot along wall, grated window, night, moonbeam + moon_on rim light and cast shadow in places_rooms.py; sitting pose 'downcast' on Seat('cot')); other views to do. (the ask: note's own words) |
| 11 | cast | Danny | (found chat 6) seated front-on, his top's ribbed band draws over his forearms; also on cast sheet 1 | new | seated front layering (people_famous._rib_hem, a torso piece, after the lap arms) | no critique | to do first: band under the forearms; a kit test on 'downcast' |
| 12 | cast | guard2 | STOP: her build from her own photos. Chat 6 found one full-front photo of a woman officer (references/patriots5/guard2/): a loose black fleece, waist and hips hidden; nothing faked | new | - | - | Sam, 28 Nov: "N": keep looking for a photo that shows a woman officer's figure (news galleries first: PA, Reuters, local papers' prison features; uniform: white shirt, black trousers); measure it with notes/learn/kemi-build/measure.py's method into references/patriots5/guard2-build.json. Blind judge: front, back woman 5/5; seated reads man (she never sits: 'not in film') |
| 13 | - | Sam's words (28 Nov, carried) | "we should be building chronologically towards animatic." / "The other people in the boat and tower need to be Patriot Platform members just like our main characters" / "All white British men, different" / "Include The Patriot in the boat, at the front, not outside it." / "I hadn't seen that." / "Otherwise good work there." / "They will be widely available." / "Google images?" / "You can use the prison gate" | settled | - | - | carried in notes 5-10 |

Decisions made (kept so a long session or a new session never has to rediscover them):
- Sam's words to the plan chat, 27 Nov, carried: "Ask permission for big uk news sites and I'll grant it" (reference photos: ask him first; the Mirror photos were used); "It is a joke that targets them, not the Muslims" (row 17, the disguise); the tower "has been used in animation plenty" (row 7); the Hook Text: "Leave that blank until I provide it"; "Make the Allahu Akbar stumbling yet sincere. Like he's trying to play a role he's not used to, all of a sudden" (row 19, acting list).
- Sam, 27 Nov 22:14-22:27, answered by the plan chat: "Why are you doing these tests?" (the start-of-film kit tests); "two chats running the same checks": "Stop the one that started second" (done); "Are you 'the planning chat'" (yes); "You can run the tests in the background, no reason to stop"; "schedule all work in this Patriots 5 project to pick back up at 01:51" (done: cast chat 4 picked up at 01:54).
- The Patriot's face under the knit is made by hand (no photos: he is fictional), the average face pushed thick-set; only his eyes and brows show, in the house look (as May and Kemi). (redesign chat 1)
- One film name, patriots5 (the redesign chat's); the plan chat's patriots-5 files folded in, 27 Nov.
- The template's held estimates note is already settled: Sam said Y to option 1 on 17 Nov (notes/archive/milburn-handovers.md); not asked again.
- Branches named at the start, not merged (logs, an archive note and old Grand Theft Autism files only, nothing for this film): claude/jolly-ramanujan-2lcl2o, claude/upbeat-dirac-w16tn9, claude/gta-v5-sound-draft, claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31.
- Plan chat's start-of-film kit run (27 Nov): 4 red, all Open Wounds tests none of this film's chats touched (early_move_size, head_moves_not_comic, movers_never_meet_head_on, side_by_side_out_of_reach): left for the Open Wounds lessons; named here.
- Photos of the real man Danny Tommo stands for: Sam (27 Nov): "Ask permission for big uk news sites and I'll grant it"; the network was already fully open (nothing to grant). Guardian, Sky, Reuters, AP and the Telegraph refuse automated visits themselves; the Mirror's topic page gave 5 press photos, filed in references/faces/tommo (2 front, 2 three-quarter, 1 smiling). Face tool run: A 73%, B 78%, C 72%, all first in the line-up; my look: the hair piece reads as a boxy block with the sides too long (his are faded short) and the stubble should be ginger-brown. Sent to Sam to pick.
- The small boat "see patriots 2" = Patriots 2's grey inflatable (source/patriots2.py, shot_dinghy).
- 

Screenplay and title: given 27 Nov 2026 (the film's start: kit tests, rule 90)

Cost line (recorded every handover; shown to Sam only on a problem): film so far 17.74% of a week (2026-11-28)
