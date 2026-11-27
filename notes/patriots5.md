# Notes for patriots5 (The Patriot 5; one file, numbered; mark each done as it is fixed)

Kind: film (satire-style, flat people). Started 27 Nov from Sam's screenplay and title (chat session_01J1JB7VmBNix1SpRrBBfJas).
The Patriot redesign (the new drawing style) runs in a sister chat, session_01J1JB7XCcqv7vGytWyb2oNY ("The Patriot
character redesign"), asked by Sam at 19:16; this chat does the plan. Its results come into this film when it pushes.

The real event (Sam): Danny Tommo, founder of Patriot Platform, has been arrested and charged for knifing a boat.
The joke (Sam): The Patriot and his crew of balaclava'd PP men try to break Tommo out; absurdity ensues.

## Where things stand (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/FILM-handovers.md)
- **Locked by Sam:** all 11 shots as the screenplay sets them: cell dead ahead at the cot; side angle; close-up of the grate from inside; side-on outside with the tower; close-up through the grate at Danny; from behind Danny's head; the entrance with the two officers; the four 180s (boat, officers, Patriot, officers).
- **Rules that bite next:** 38 (front, side and back on the cast sheet), 89 (each new piece drawn alone and critiqued before the cast sheet), 49 (likeness: Danny checked against his photos).
- **Done:** redesign chat 1: the Patriot (sheet v2, Sam's look pending). Plan chat 1: brief checklist, shots, acting list, estimate 15.4%; Danny's photos and face tool (pick B); Sam's answers (orange boat, 8-man tower, clothes from the small-boat news photos with at least two niqabs, tones); rule: the Hook Text is Sam's (plain-words check, kittest hook_text_never_suggested). Chat 2: the shoulder tower practice clip (two notes fixed: clipping, neck; source/shoulder_tower.py); chat 3 (opened by chat 2 at Sam's ask): the walking boat practice. Chat 2 (tower practice): 8-man tower clip sent (notes/learn/shoulder-tower/, lesson's "What chat 2 learned"); Sam's notes "clipping errors" and "neck separated from the head" fixed with checks (tower_clipping, bent_neck_joined); boat chat opened at Sam's ask (learning the walking boat, practice, session ...Xctbsw7).
- **Next (tower):** a notes chat (Opus, medium): Sam's note on v1, "I don't like the hand thrusting the lower characters are doing": take out the arm throws (lesson, Still open), then a short clip. **Next (film):** chat 4 (Opus, high: new people and clothes; chat 2 opened chat 3 for the walking boat): the cast sheet: Danny Tommo (face B, fixing the boxy hair with long sides to his short faded sides, ginger-brown stubble; prison grey tracksuit), the 7 crew (house heads + balaclava=True, varied heights and builds), the crew's disguise per brief row 17, the 2 officers (Blessed's), the orange boat; each new piece drawn alone and critiqued first. Then send the sheet.
- **Needs Sam:** Y or N on the shoulder-seam fix for the grey sleeve fade (redesign chat); his look at the Patriot's sheet v2; Danny's face (going with B, my pick, unless Sam says otherwise); the Hook Text (blank until he gives it).
- **Read:** guides/job-packs.md, Build; guides/figure-rig.md 2-4, 5c; brief rows 1-22 and References in this file. Tower notes chat: guides/fix-pack.md and notes/learn/shoulder-tower/lesson.md.
- **Open rule requests:** none. Branches with old, unrelated work (named, not merged: logs, a GTA proposal, two GTA scripts): claude/jolly-ramanujan-2lcl2o, claude/upbeat-dirac-w16tn9, claude/gta-v5-sound-draft, claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31. Handover STOP left to the plan chat: the Hook Text rule has no entry in rule_proofs.json (its rule).
- **For Claude:** film name patriots5; boat = patriots2.shot_dinghy; cell, gates and officers = story/blessed-places.txt / blessed-people.txt; Patriot = patriots5_cast.patriot(mood) (`patriots5_cast.py sheet OUT.jpg`; balaclava facehouse_d). Open Wounds (brexit-is-done) notes stay in place: acting.py reads its acting list (move to shared: repoint, then archive).

## Plan extras (rules 24-26, 54, 55): ambition estimate as a table, one row per new build and risky move, each with
its own share of a week and, for anything split into parts, how its ending looks and which parts the camera sees
break; eyelines and holds per shot; every sound effect (what, when, needed by); bleeped words (said, or a gap left?)

Every person, set, prop, pose and move in the brief gets a row: KNOWN (its kit-catalogue line, pose-gallery row or
"Passed the critique" row: almost free) or NEW (priced; drawn alone and critiqued before the cast sheet, rule 89).

First line: how much of the total is unmeasured. Each cost is the nearest measured past cost in `notes/ledger/`
(name the film and row), or 'unmeasured'; no padding, no multipliers. Each row names its stage (cast, sets, board, moves,
animatic1, round, final; board: the shot board of rule 11, ended by `rough.py sent FILM OUT.jpg --delivered --board`; one 'round' row per notes round, priced from past films' real rounds); the stage totals go
into `ledger.py estimate FILM PCT --stages "cast 2, sets 2.5, ..."` and each stage's end runs `ledger.py stage FILM NAME`.

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

Rehearsal clips sent: (rule 8: the 3-4 riskiest moves as 2-3 s clips, before building the rest; the date and file,
or "none: why". Pre-flight warns until this line is filled)

Shot board sent: (rule 11: every shot on one board before any move is written: `rough.py board FILM OUT.jpg`, send
it, then `rough.py sent FILM OUT.jpg --delivered --board`, which records it. Pre-flight refuses to run until the record
holds every shot, each with someone in SHOT_CAST, sent before the first move; and while any "done?" box below is blank:
rule 14)

## The brief as a checklist (CLAUDE.md, 18 Oct): every detail of Sam's brief and notes, ticked before the first animatic
| # | from the brief or a note (copied word for word: wording, asterisk and bleep counts, positions, colours, props) | done? |
|---|------|------|
| 0a | Sam, 27 Nov: "run The Patriot character through our new drawing style to bring him up to speed" | sheet sent, awaiting Sam; known faults told to Sam: side-view collar sticks out with a thin white gap under it; three-quarter hood comes to a slight point at the chin; the from-behind-at-the-grate view untested |
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
| faces/tommo m01, m02 (Mirror) | Danny Tommo's model, front; m04 three-quarter; m05 smiling | face tool 72-78% |

## Exceptions (rule 13): anyone or anything left out of a check, one row each (a pattern like Journalist* is fine); pre-flight refuses a film setting's exception (HANDS_OK, LINE_OK, any *_OK, ALLOWED_POPS) with no row here; a code comment is never a reason. check: the setting's name, or 'house look', 'lap', 'drawing checks', 'camera feel' (who: the shot)
| check | who | why | looked at full size (sheet, panel) |
|---|---|---|---|

## Notes
Send all notes in ONE message, each with the shot and the time, e.g. "shot 2, 10.3 s, left: the man never looks at the zombie".

Status: one line of what was done (no "Was:"; git keeps the history), "new kind" or "seen before" (a "seen
before" note means a check is missing: add it), and the note's line in `guides/critique-checklist.md` (rule 30):
a new line's id, or an old one and why it missed (line unclear, sheet didn't show it, no critique).
"Should have caught": the check that should have caught the note before Sam saw it (its name as pre-flight prints
it, e.g. AUDIT, SHOT CAST, caption), or "none" when no check could; the handover check refuses a blank one
(check-catches change 2, Sam's Y 20 Nov), so misses are counted without guessing.
"Critique saw it?": yes if the fresh-eye critique of that round had already flagged it, no if it looked and missed
it, "no critique" if none ran (Sam's Y, 26 Nov): after a few films it shows whether the critique sees what Sam sees;
the handover check refuses a blank one.

| # | shot | time | note | line | should have caught | critique saw it? | status |
|---|------|------|------|------|--------------------|------------------|--------|
| 1 | cast sheet | front | "strange vertical lines in the belly area" | new | none: I looked at the sheet at phone size only, not each body at full size (Seeing like Sam, 1); no check sees pieces drawn for an old body landing inside a new one | no critique | fixed: Patriots 3's belly-swell edges no longer drawn; the shared body has a 'stout' build (belly in its own outline, side and three-quarter too) |
| 2 | cast sheet | back, 3/4 back | "explain the greying out of the sleeves? You did that with Blair too" | seen before (Blair) | none: the shoulder join (limbs.py, the arm fading into the body near the shoulder) assumes the sleeve is the jacket's cloth; a grey sleeve on a black body fades as a smear | no critique | answered; fix waits for Sam's Y (a hard shoulder seam where the sleeve's colour differs from the body's) |
| 3 | cast sheet | side, three-quarter | "Fix your notes": my named faults (collar a box beside the neck with a zip in the air; the chin's dark V) | new | none (I named them myself, unfixed) | no critique | fixed: the knit's neck stops at the collar so the collar wraps round it; zip and hem fitted to the stout body; ribs stop above the chin's bottom rings |

Decisions made (kept so a long session or a new session never has to rediscover them):
- The Patriot's face under the knit is made by hand (no photos: he is fictional), the average face pushed thick-set; only his eyes and brows show, in the house look (as May and Kemi). (redesign chat 1)
- One film name, patriots5 (the redesign chat's); the plan chat's patriots-5 files folded in, 27 Nov.
- The template's held estimates note is already settled: Sam said Y to option 1 on 17 Nov (notes/archive/milburn-handovers.md); not asked again.
- Branches the start listed (also named by the redesign chat) (jolly-ramanujan, upbeat-dirac, gta-v5-sound-draft, gta-chat46-build, dreamy-fermi, gta-chat31): logs, an archive note and old Grand Theft Autism files only, nothing for this film; left as they are.
- Photos of the real man Danny Tommo stands for: Sam (27 Nov): "Ask permission for big uk news sites and I'll grant it"; the network was already fully open (nothing to grant). Guardian, Sky, Reuters, AP and the Telegraph refuse automated visits themselves; the Mirror's topic page gave 5 press photos, filed in references/faces/tommo (2 front, 2 three-quarter, 1 smiling). Face tool run: A 73%, B 78%, C 72%, all first in the line-up; my look: the hair piece reads as a boxy block with the sides too long (his are faded short) and the stubble should be ginger-brown. Sent to Sam to pick.
- The small boat "see patriots 2" = Patriots 2's grey inflatable (source/patriots2.py, shot_dinghy).
- 

Screenplay and title: given 27 Nov 2026 (the film's start: kit tests, rule 90)

## Kit found at the start
(kitfilm begin, 27 Nov: the catalogue's best rows per brief line; the face tool per real person filed under references/faces; a row is KNOWN only once a person checks it)
- "Shot 1: "We are in a British Prison cell. It is evening. We look dead ": Places from a description (the places kit; ranking item 5, 14 Nov; APPROVED FOR  [`source/places.py` (`parse`, `load`, `install`, `set_boxes`,]; Seated lower body as one shape (R7, 25 Nov; Sam's "No bum/circular knees"): the  [`source/views.py` (`seated_lower`, `seated_knee_over`, `r7_o]
- "Shot 1: "Danny Tommo is in the process of sighing deeply, downcast."": A car chase through a stand-in junction from a low kerb camera: a route with a s [`source/gta_rehearse.py` (`route`, `car_at`, `tyre_smoke`, `]; The shot board and its gate (rule 11; craft chats 7-8, 17-18 Nov). Every shot in [`source/rough.py` (`board`, `board_frames`, `board_rows`, `m]
- "Shot 1: "Above him, a grated window, letting in moonlight."": A car chase through a stand-in junction from a low kerb camera: a route with a s [`source/gta_rehearse.py` (`route`, `car_at`, `tyre_smoke`, `]; Places from a description (the places kit; ranking item 5, 14 Nov; APPROVED FOR  [`source/places.py` (`parse`, `load`, `install`, `set_boxes`,]
- "Shot 1: "The Patriot's head appears suddenly at the window." Line: "Da": People from a description (the people kit; ranking item 4, 14 Nov; APPROVED FOR  [`source/people.py` (`parse`, `load`, `crowds`, `crowd_person]; A famous person's head for any film, READY (Sam, 14 Nov: look 2 'detail'): the f [`source/facehouse.py` (MAP; `person`, `house_head`, `swept`,]
- "Shot 2: "From a side angle, we see Danny look up, react with surprise,": A famous person's head for any film, READY (Sam, 14 Nov: look 2 'detail'): the f [`source/facehouse.py` (MAP; `person`, `house_head`, `swept`,]; People from a description (the people kit; ranking item 4, 14 Nov; APPROVED FOR  [`source/people.py` (`parse`, `load`, `crowds`, `crowd_person]
- "Shot 3: "Close up of the grate and the Patriot." Line (Patriot): "Yeah": Moves from the acting list (the moves kit; ranking item 7, 14 Nov; APPROVED FOR  [`source/acting.py` (`parse`, `load`, `pose`, `face`, `check`]; Space, flat cartoon (Halo No-No): planet (bands, dusk and night side, any light  [`source/halo_sets.py` (`space_wide`, `ring_close`, `_planet`]
- "Shot 4: "the side on view but on the other side of the wall. There's a": Blessed (11 Nov), flat paintings, one per camera, real metres: Southwark Crown C [`source/blessed_sets.py` (`back`/`mid`/`front(view, img, cam]; Seated lower body as one shape (R7, 25 Nov; Sam's "No bum/circular knees"): the  [`source/views.py` (`seated_lower`, `seated_knee_over`, `r7_o]
- "Shot 4: "The tower is swaying slightly back and forth."": Blessed (11 Nov), flat paintings, one per camera, real metres: Southwark Crown C [`source/blessed_sets.py` (`back`/`mid`/`front(view, img, cam]; Any measured-face person's head turned (three-quarter, side, three-quarter behin [`source/turnhead.py`: `register(Person(...))` + `install(vie]
- "Shot 4 line (Patriot): "Nick's head is up my arse. It's blood horrible": People from a description (the people kit; ranking item 4, 14 Nov; APPROVED FOR  [`source/people.py` (`parse`, `load`, `crowds`, `crowd_person]; A famous person's head for any film, READY (Sam, 14 Nov: look 2 'detail'): the f [`source/facehouse.py` (MAP; `person`, `house_head`, `swept`,]
- "Shot 5: "Close up on grate looking through at Danny." Line (Danny): "T": David Walliams (kit person, 22 Nov: the head Sam approved 15 Nov; face tool pick [`story/facetool-people.txt` (`walliams`: copy the 4 lines in]; Space, flat cartoon (Halo No-No): planet (bands, dusk and night side, any light  [`source/halo_sets.py` (`space_wide`, `ring_close`, `_planet`]
- "Shot 6: "We see from behind Danny's head. The Patriot is swaying back ": Any measured-face person's head turned (three-quarter, side, three-quarter behin [`source/turnhead.py`: `register(Person(...))` + `install(vie]; Blessed (11 Nov), flat paintings, one per camera, real metres: Southwark Crown C [`source/blessed_sets.py` (`back`/`mid`/`front(view, img, cam]
- "Shot 6: "He is exaggerating with his hands." Line (Patriot): "We've be": Places from a description (the places kit; ranking item 5, 14 Nov; APPROVED FOR  [`source/places.py` (`parse`, `load`, `install`, `set_boxes`,]; People from a description (the people kit; ranking item 4, 14 Nov; APPROVED FOR  [`source/people.py` (`parse`, `load`, `crowds`, `crowd_person]
- "Cut to shot 7: "Prison entrance. Two prison officers are looking forwa": Humpback whale (one model in metres, drawn flat in house style from ANY view and [`source/whale.py` (`draw(cam, pose, pattern, t, flap, beat, ]; The shot board and its gate (rule 11; craft chats 7-8, 17-18 Nov). Every shot in [`source/rough.py` (`board`, `board_frames`, `board_rows`, `m]
- "Shot 8 (180): "The patriot platform boys are walking from left to righ": The Normandy coast from the air, painted in moving layers: cliff-face casemates  [`source/patriots3_coast.py` (`picture`, `burst`, `craft`)]; Humpback whale (one model in metres, drawn flat in house style from ANY view and [`source/whale.py` (`draw(cam, pose, pattern, t, flap, beat, ]
- "Shot 8: "They have clearly cut holes in the boat so their legs can com": Any measured-face person's head turned (three-quarter, side, three-quarter behin [`source/turnhead.py`: `register(Person(...))` + `install(vie]; Fire, smoke and water effects, flat house style, in metres through any camera, e [`source/flying_whales_fx.py` (`fireball_sprite`, `Puff` + `p]
- "Shot 8: "They are sheepishly coming up towards the guards."": Any measured-face person's head turned (three-quarter, side, three-quarter behin [`source/turnhead.py`: `register(Person(...))` + `install(vie]; A car chase through a stand-in junction from a low kerb camera: a route with a s [`source/gta_rehearse.py` (`route`, `car_at`, `tyre_smoke`, `]
- "Shot 8: "They have a variety of Islamic religious gear wrapped over th": Any measured-face person's head turned (three-quarter, side, three-quarter behin [`source/turnhead.py`: `register(Person(...))` + `install(vie]; People from a description (the people kit; ranking item 4, 14 Nov; APPROVED FOR  [`source/people.py` (`parse`, `load`, `crowds`, `crowd_person]
- "Shot 9 (180): "The guards stare. The one on the left goes: uuuh, what ": A car chase through a stand-in junction from a low kerb camera: a route with a s [`source/gta_rehearse.py` (`route`, `car_at`, `tyre_smoke`, `]; Humpback whale (one model in metres, drawn flat in house style from ANY view and [`source/whale.py` (`draw(cam, pose, pattern, t, flap, beat, ]
- "Shot 10 (180): "The Patriot startles, clearly not expecting to be seen": People from a description (the people kit; ranking item 4, 14 Nov; APPROVED FOR  [`source/people.py` (`parse`, `load`, `crowds`, `crowd_person]; Moves from the acting list (the moves kit; ranking item 7, 14 Nov; APPROVED FOR  [`source/acting.py` (`parse`, `load`, `pose`, `face`, `check`]
- "Shot 11 (180): "The guards just stare at each other in baffled shock."": Offshore oil rig (Jackdaw-style) in 31 breakable pieces at real size, painted fl [`source/flying_whales_rig.py` (`draw(base, t, xf, gone, extr]; A car chase through a stand-in junction from a low kerb camera: a route with a s [`source/gta_rehearse.py` (`route`, `car_at`, `tyre_smoke`, `]
- "Every video: Hook Text and the CranbriJoos sign-off; no title by defau": Hook Text beside a person, three rows (`--w`); 😅 emoji [`source/hook_text.py`, `1f605.png`]; Word times from Sam's takes (speech-to-text; Open Wounds chat 29, 26 Nov, Sam's  [`source/words.py` (`times`, `text`, `track`, `at_word`); in ]
- "Sound: voices only (the script names no sound effects)": The proposal route (Sam, 15 Nov): any change to rules, tools, checks, kits or ho [`source/propose.py` (`new`, `pack`, `judge`, `record`, `show]; Any measured-face person's head turned (three-quarter, side, three-quarter behin [`source/turnhead.py`: `register(Person(...))` + `install(vie]

Cost line (recorded every handover; shown to Sam only on a problem): film so far 7.99% of a week (2026-11-27)
