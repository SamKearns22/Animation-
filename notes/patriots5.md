# Notes for patriots5 (The Patriot 5; one file, numbered; mark each done as it is fixed)

Kind: film (satire-style, flat people). Started 27 Nov from Sam's screenplay and title (chat session_01J1JB7VmBNix1SpRrBBfJas).
The Patriot redesign (the new drawing style) runs in a sister chat, session_01J1JB7XCcqv7vGytWyb2oNY ("The Patriot
character redesign"), asked by Sam at 19:16; this chat does the plan. Its results come into this film when it pushes.

The real event (Sam): Danny Tommo, founder of Patriot Platform, has been arrested and charged for knifing a boat.
The joke (Sam): The Patriot and his crew of balaclava'd PP men try to break Tommo out; absurdity ensues.

## Where things stand (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/FILM-handovers.md)
- **Locked by Sam:** all 11 shots as the screenplay sets them: cell dead ahead at the cot; side angle; close-up of the grate from inside; side-on outside with the tower; close-up through the grate at Danny; from behind Danny's head; the entrance with the two officers; the four 180s (boat, officers, Patriot, officers). Shot 6's camera (chat 8's draft) left as it was: a try at moving it was refused, so Danny moves along the cot instead.
- **Rules that bite next:** 1 (one cell plan in metres; the yard level for shot 4 is decided once, "The world"), 4 (views the drawing can carry: the tower side-on only), 5 (physical: what rests on something lands on it on screen: views.hands_onto; the tower sways towards/away from the wall, so at the window he nears and leaves the bars, never through them).
- **Done (sets chat 9, 28 Nov):** 1. Cot: every plan piece now takes one true-depth path for every camera (places.py Piece.turned); shot 1's cot gains its legs' inner sides and the pillow's end (physically right; example notes/learn/turned-cot/); kit test turned_camera_same_plan passes and checks it. Tell Sam: "Added: in the opening shot the bed's steel legs show their inner side and the pillow's end shows (tiny)". 2. Shot 6 learned (notes/learn/back-neck/): the neck from behind is thick and flares into the shoulders (shared views.back_neck: body, old heads, house heads, back collars); hands rest ON the sill by contact on screen (shared views.hands_onto); Danny at plan x -0.14 so the Patriot shows; the Patriot sways as the tower's top (patriots5_cast.top_sway, window_depth) and talks with his hands (GESTURES, GESTURE_ORDER). Still: notes/patriots5-sets/cell-behind-wip-v2.jpg. Kit tests back_neck_flares, hands_onto_lands (new, pass).
- **Chat 9 was cut off by the 5-hour limit (28 Nov 09:39) mid-try:** it was about to move Danny to plan x -0.16 and re-aim shot 6's camera from `at 0.35 2.75, facing -11` to `at 0.3 2.75, facing -6` (story/patriots5-places.txt, cell_behind), to show more of the Patriot; that command was refused/never ran, so the places file is still the old camera. Try it once (`DANNY_X=-0.16 ... cell_behind OUT both`), keep it only if it reads better. Camera stays Sam's (shot 6 locked; only Danny's place and the lens aim inside the same view). Photo search, chat 10 (28 Nov, on Sam's word that I should find them myself): tried prisonjobs.blog.gov.uk (16 images), prisonandprobationjobs.gov.uk, jobhelp.campaign.gov.uk (all head-and-shoulders or from behind), Wikimedia Commons categories Prison guards / Female police officers of the UK (guards: all men or old; police: hi-vis coats or body armour hide the figure), Openverse (throttled ~3.5 h more), Flickr feed (blocked). Still no standing woman showing waist and hips. NOT YET TRIED: Pexels/Unsplash pages, Geograph, the Mirror/PA galleries (Sam's Mirror permission, 27 Nov), Commons 'Category:Women in uniform' / 'Category:Female police officers of the United Kingdom' subcategories, a standing woman in plain close-fitting work clothes (the build needs only the figure; the uniform is drawn from the polo refs). Judge round 3 (chat 10, 3 fresh Sonnet helpers, sheet outlines-v3, my own plain prompt): guard2 front/back/seated read man, but guard2 3/4 woman 3/3/4, and Danny (front 2, back 3, seated 2) and officer 1 (3/4) read woman on drawings that PASSED round 2 unchanged: the judge itself is noisy (no fixed prompt in castjudge.py), so do not trust one round either way; next: write one fixed judge prompt into castjudge.py, rerun, then widen guard2's 3/4 shoulders only if it still reads woman. SAM DECIDED (28 Nov, after the search): officer 2 is a second MAN, no photo needed (note 12 closed; guard2 redrawn in story/patriots5-people.txt; the build STOP is gone). Chats 8-9 were refused for the old STOPs.
- **Open on shot 6:** the Patriot's hands read small and dim behind the mesh at phone size: draw a raised hand over his face (views.RAISED_OVER covers hands above the face only) and make the moves bigger; lay the beats on Sam's recorded line. Danny's left hand is hidden behind his head (physically right).
- **Next:** chat 10 (Opus, high: building views). 1. Shot 6's open line above. 2. Shot 4: the outside wall ('outer wall' kind) with the tower of eight (source/shoulder_tower.py, lesson notes/learn/shoulder-tower), side-on outside; settle the yard level against the plan once (sill 5.6 m up: first floor). 3. The gatehouse (story/blessed-places.txt 'prison gate') for 7 and its reverse for 8-11. 4. source/patriots5.py (pattern source/brexit_is_done.py), then the shot board.
- **Needs Sam (account switch, 28 Nov: Sam moves to his other account; main line `claude/create-claude-md-oe8z4g` holds everything, attach the Animation- repo first):** (officer 2's photo no longer needed: he is a man now) notes on the new Danny; tower clip v2 and boat practice notes; the Hook Text (blank until he gives it). Optional: 2 photos of a man from behind with both hands on a high ledge (Wikimedia and Openverse gave nothing; Openverse throttled for about 7 hours).
- **Read:** guides/job-packs.md, Build (Sets lines); brief rows 1-22; notes 10-12; "The world"; story/patriots5-places.txt views cell_side..cell_behind; notes/learn/back-neck/README.md.
- **Open rule requests:** none. Branches named, not merged (old, unrelated): claude/lucid-archimedes-z91suc, claude/jolly-ramanujan-2lcl2o, claude/upbeat-dirac-w16tn9, claude/gta-v5-sound-draft, claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31; claude/p5-chat9-savetest (chat 9's save test, the delete was refused; empty, delete when allowed). Handover STOP on guard2 closed 28 Nov (note 12).
- **For Claude:** stills: grate_still.py VIEW OUT [patriot|danny|both] [MOOD] with env DANNY_X (his place on the cot), T (seconds: sway) and TALK=1 (gestures); shot 6 = `DANNY_X=-0.14 T=t TALK=1 ... cell_behind OUT both`. views.hands_onto(cam, x, y, s, sp, yaw, j, want) returns (pose, misses). Kit tests use B.SS = 1.
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
| 12 | cast | guard2 | WAS: her build from her own photos | new | - | - | CLOSED 28 Nov: Sam, after chat 10's photo search found no standing woman officer: "Or you could just make another man. I don't really mind". Officer 2 is now a second man (story/patriots5-people.txt guard2: 1.74 m, sandy crop, pale; sheet looked at, two distinct men). No woman, no photo needed. Still to do (Opus): look at him in the shots and rerun the blind judge on the cast sheet |

Decisions made: moved to notes/archive/patriots5-notes.md (28 Nov). Kept: Sam 27 Nov: reference photos of big UK news sites need his OK (the Mirror's were used); the Hook Text stays blank until he gives it; the Allahu Akbar line is "stumbling yet sincere".

Screenplay and title: given 27 Nov 2026 (the film's start: kit tests, rule 90)

Cost line (recorded every handover; shown to Sam only on a problem): film so far 24.9% of a week (2026-11-28)
