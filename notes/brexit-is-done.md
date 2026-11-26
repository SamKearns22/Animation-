# Notes for Brexit Is Done (working name) (one file, numbered; mark each done as it is fixed)


## Brief checklist (Sam's words, 23 Nov; tick each against the film before the first animatic)
(Template note, raise at the plan: the estimates proposal, notes/proposals/estimates.md, options 1 and 2.)
News: Theresa May "aghast" at Burnham's EU plans, says "Brexit is done" (BBC, Sunday with Laura Kuenssberg, 22 Nov 2026).
- [x] 1. Theresa May "in this exact interview" (`references/brexit-is-done/may-interview-*.jpg`): seated, turned to
      screen-left, looking at the interviewer off-frame left; dark wood-panelled backdrop; plum jacket, patterned
      blouse, hands gesturing in front of her.
- [x] 2. Kemi Badenoch in hard hat and site clothes (`badenoch-hardhat-sam.jpg`: white hard hat, glasses, long braids,
      orange-and-navy hi-vis jacket); faces the same way as May; a construction site behind her (Sam will describe it).
- [x] 3. Tony Blair as he is today (`blair-today-sam.jpg`: grey swept-back hair, big smile, dark suit, red tie, white
      shirt); ends up facing the same way as May; place not decided ("maybe some swanky embassy sort of place?").
- [x] Title: "Open Wounds". News: Andy Burnham's new EU deal, criticised as "opening up the wounds" of Brexit.
- [x] The joke: the critics talk about packs of wolves instead of Brexit, ignoring wolf attacks all round them while
      they criticise ("people not noticing the damage they have done").
- [x] 4. Theresa (her interview): "The Prime Minister would do well to remember that we had a referendum, and in that
      referendum, the British Public chose wolves."
- [x] 5. Cut to Kemi interviewed on a building site: an expanse of dusty ground; behind, a large complex under
      construction, "all holes and pipes and scaffolding".
- [x] 6. From the first second: two wolves leap on a construction worker in the background and tear him to shreds
      (as Cry Minister, the old wolves "spruced up" with the new body kits and rules).
- [x] 7. Background: a worker runs from two wolves across the scaffolding and leaps off it, off frame, to escape.
- [x] 8. Background: a group of men with steel bars staving off another group of wolves on the next level down.
- [x] 9. Background: wolves milling round the dirt in hard hats and construction vests, blood-drenched: sitting,
      pawing the dirt, wandering.
- [x] 10. Kemi, staring at the interviewer as if none of it was happening: "Andy Burnham needs to spend less time trying
      to take us backwards and more time doing his job: reducing the number of British people with their faces chewed off."
- [x] 11. Embassy scene, "a bit more, uh, classic British": oak and bookshelves, a political room like Westminster "or
      some other august locale". Behind Tony Blair, doors thrown open as wolves run rampant, chasing staff and guests.
- [x] 12. Blair: "Well, in my opinion, you shouldn't listen to anything I say, I'm Tony Blair, I invaded Iraq, I belong in
      The Hague." Big cheesy grin.
- [x] 13. (Sam, 23 Nov, Q5) Blair holds the big grin about 1.5 s, then a wolf lunges at him; cut to the sign-off on
      the lunge (chat 3's pick, before it reaches him).
- [x] 14. (Q3) The interviewers are never seen or heard; all three look off-frame left at them.
- [x] 15. (Q4) Hook Text: "Andy is opening old wounds... 🇬🇧" (the flag drawn as one picture: hook_text fixed chat 3,
      kittest hook_text_flag_emoji).
- [x] 16. (Q6) Kemi's site in daylight under a grey British sky, as her photo.
- [x] 17. (Q7) Blair's room: Sam: "He would do his interview in the UK but sure why not" -> a grand oak-panelled,
      book-lined room in London (chat 3's pick from his words), not Brussels.
- [x] 18. (Q2) Blood: Sam: "Can we do better?" than Cry Minister's flat red: plan sent (two reds and a shine, arcs that
      land and soak into the dust, stained muzzles, paws and vests, torn hi-vis and a tumbling hard hat, dust at every
      leap; chunks as Cry Minister, no bones or insides); waiting for his Y.
- [x] (Q1) Woman's body: option 1 (Sam: Y, 23 Nov): notes/proposals/womans-build.md "Final version".
- Locked by Sam: the script above (lines, order, who is where, every background action).
- Sam's words kept: Kemi and Blair face "the same way she is facing, being interviewed"; the script and site: "I'll describe
  both to you soon." "For now, please work on the characters."
- Reuse: Badenoch's face is already built (`source/facehouse.py` 'badenoch'); May and Blair are new faces.

## The Learn-First rule (rule 91) on Open Wounds (R7 chat 15, 26 Nov; Sam: "implement this rule on the entirety of Open Wounds")
The new pose tool is proven only on sitting upright. Open Wounds now draws everyone with the flat house kit (seated legs OFF,
locked by Sam), so nothing changes until Sam picks. Before any shot moves to the new tool, what must be learned:
- Shot 1, May on the office chair: sitting proven; her lean in and nods: the hips' angle as she leans, a motion clip checked frame by frame.
- Shot 2, Kemi: she STANDS on the site (chat 27): standing, the legs straight under the outfit, feet on the floor, a reference photo, a sheet.
- Shot 3, Blair in the armchair: the armchair's height and depth, his lean back, a reference photo, a sheet.
- Background, worker torn by wolves (item 6): the body on the ground, its weight, a reference photo, a sheet.
- Background, worker running and leaping (7); staff fleeing (11): the legs through a stride, feet on the ground, a motion clip.
- Background, men with steel bars (8): arms as part of the body (now flat, drawn on top), hands gripping the bars.
The start check prints this for the film (handover.py start, LEARN-FIRST; kittest learn_first).

## Where things stand (chat 38, 26 Nov, session_01U3pKR2WHJZY1fpHB58yXS7)
Rules that bite next: 30 (24.2 and 24.4 were seen before: the first fixes never changed the drawing's shape), 11 (shot 2 built only as Sam's framing 2), 93 (checks advise, never lock).
Done (chat 38): Sam's notes 24.1-24.4 fixed in the shared kit, not by new checks (Sam: "not make this mistake in the first place"): acting.HEAD_MIN + headlife eased nods; faces.lips 'smirk' (FACS: one corner up) on May's 'satisfied'; sleeves the jacket's colour (limbs.DARK_RIM edge) and a suit with a tie one cloth; a man's suit front at 3/4 redrawn (views.torso_view). Kittests head_moves_never_snap, suit_one_cloth, smirk_one_corner, dark_sleeve_reads. Clips ow-n24-may.mp4, ow-n24-blair.mp4 sent (Blair's clip was drawn with the one-cloth trousers, since undone). Sam's note 25 (leg gap back): the trouser change undone. Sam (26 Nov): the seated 'no bum' test deleted (castsheet; the body kit draws the bottom); the crossed-leg tone test off for the body kit (Sam's note 7). Reserve job R8 'check audit' added (notes/next-jobs.md). Rule 93 given its proof entry (status next).
Next: chat 39 (OPUS, HIGH: a new way of drawing): note 26 first (Sam: "It's not a nod, it's a head-bob": learn a nod as a pitch, grey practice head, then the cast; Kemi's 7 px nods wait on it), then settle the 2 handover stops left (chat 37's): CAST SHEET CROTCH kemi front (look as a viewer: the line between her legs from the crotch; fix the drawing if it reads as note 8) and JUDGE (draw the outlines again, three fresh judges: castsheet judge_faults says how). Then shot 2 at Sam's framing 2 (picked 26 Nov): the site and all four background actions a third nearer (places file depths and brexit_is_done_action ATTACK, LIFT_D, runner, bars, milling positions), every action and some grey sky in frame; board (rough.py board brexit-is-done OUT.jpg --shots 2), send, rough.py sent --board; a Kemi clip 13.5-16 s (the point back). Then Sonnet: pre-flight, animatic, finish.py, send.
Needs Sam: Y/N on check-knows-intent (V3); his look at the chat 38 clips; Q2 (full kit check now: my pick N) and Q3 (check-knows-intent) unanswered; Q1 answered as note 26. Kemi's nods at 17.55 s (7 px) and 18.64 s (10 px) are now under the floor because HEAD_MIN slows them: kittest head_moves_not_comic fails on them; wait for Sam's word on the floor before resizing.
Read: guides/job-packs.md "Notes round" (stops), "Plan" staging lines (shot 2).
Open rule requests: none. Notes file 4,800 words (over 4,000: 'Sam's words held elsewhere' and Exceptions are what's left; trim at the animatic).
Branches: claude/gta-v5-sound-draft, claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31: GTA's, left.
Locked by Sam: the script (as recorded), who is where, every background action, the three places' briefs, the cut on the lunge; film order; all three in May's place and size; the cast; every camera and framing (shot 2 now framing 2). No change to timing, lines, mouths, soundtrack.
For Claude: preflight name 'brexit-is-done'; main line claude/create-claude-md-oe8z4g; chat 38 branch claude/brexit-chat38; acting.HEAD_MIN, faces.SMIRK_UP, limbs.DARK_RIM/_lit, views.DARK_SLEEVE_LIFT now 0.

## Open from chat 36 (Sam's picks pending)
- Proposal check-knows-intent: option 1 or 2 (notes/proposals/check-knows-intent.md).
- Proposal seeing-five-candidates: Sam picked 1 without the video model (26 Nov); built in its own chat.
- The 3 resting-hand faults (May's thigh 2.6 s, Blair's armrests 24 s): fix Y/N.
- Rule 93 still to build: circled stills and why-line (on Sam's word), kittest checks_advise_never_lock.

## Sam's words held elsewhere (chat 4, so the handover check finds each)
- Sam 26 Nov 20:00-20:26 (chat 36, after the animatic: "So what did the pre-flights pick up on and why were they not noticed or fixed in previous rounds?"; "It can advise on problems and show me stills of where it is concerned, with circles around what it t[hinks]..."; "It must also report on why the drawing systems we use got it wrong the first time."; "The failure to fix: an answered fault should come back when the drawing changes (rule 59 says it sho[uld]..."; "I don't know what this means"; "What's a reopened list"; "No, that doesn't seem like a good solution."; "I think if something changes, it should just recheck the new film and recognise that it is fine agai[n]..."; "Here, it introduced things as new faults when actually it had decided before that it was already fin[e]..."; "Well, I mean, why didn't it decide it was fine this time?"; "Why does it need a new rule when it was already deciding it was fine?"; note 1: "Is it a fault or are the characters contextually doing something that requires overlap?"; "So it seems like the check isn't being balanced against _what the scene is trying to achieve_"; "Run the proposal through the route on opus."; "The checks can't be stupid."; "They need to understand when something is intentional in the image."; "They need to be able to ask the image and the screenplay, when they are unsure, 'is this normal in t[he context]...'"): rule 93 (checks advise, never lock, chat 36); answered-faults-return.md declined; the route ran: notes/proposals/check-knows-intent.md, pick V3 (the meaning written where the action is drawn, a picture judge only for what is left unclear); chat 37 asked Sam for his Y.
- Sam 26 Nov 19:09: "Question: if these were not right, why were they animated in that way originally?" and 19:10: "Do you see the problem if something is being designed in a way that will later fail a check?": answered in chat 34; the fix is rule 92 (move size checked the moment a move is written, chat 35).
- Sam 26 Nov, note 1 (fault 3): "Please provide a picture of how you would fix this." / "Our characters have circle hands and only show a finger when they point.": the picture was made and sent in chat 35 (notes/brexit-is-done-finger-fix.jpg); waiting for his Y.
- Sam 26 Nov, note 1 (fault 9): "No idea until animatic": the mouths on 'remember'/'referendum' are judged on the animatic.
- Sam 26 Nov, note 1: "Once you get to animatic stage, override everything and deliver the animatic.": the Sonnet chat's task (Where things stand).
- Sam 26 Nov (chat 28, voice notes): "Point number two." / "Point number three." / "That doesn't look very good, and I think it affects the choreography of the rest of the scene.": the headings and words of notes 14 and 15.
- Sam 26 Nov 16:08: "What safety check is holding up the speech-to-text install, and how can we get past it?": answered in chat 28; Sam then said "Y install" (chat 29 installed it the normal way, faster-whisper).
- Sam 26 Nov (Q1): "Kemi question - 1". Speech-to-text then showed Kemi.m4a and Kemi_2.m4a are the two halves of her one line ("...his job." / "reducing the number of British citizens with their faces chewed off"): both used, back to back.
- Sam 26 Nov: "Once work is finished on both these chats render an animatic." (the voice chat 29 and the body chat 30): the last of the two to finish opens the Sonnet animatic chat.
- Note 1 (Q4) Hook Text, Sam: "Andy is opening old wounds..." with the British flag: brief item 15.
- Note 1 (Q5) Sam: "Yes, before a wolf lunges at him": Blair's grin then the wolf lunge, brief item 13.
- Sam 22:00: "I do think we need multiple body shapes in our kit, maybe 6 for male and female": reserve job R1 (notes/next-jobs.md), waits for Sam to name it.
- Sam 22:06: "I'd be keen to answer your script questions soon": answered as Q1-Q7 (brief items 13-18); only Q2, the blood, is still open.

- Sam 25 Nov 08:02: "So I'm thinking about this film, and obviously we need to hook people in the first 3 seconds, and it's just Theresa May giving dialogue in a seat ... really fluid acting throughout her and the other characters' lines ... make sure it's implemented": the Acting plan section (built chat 15).
- Sam 24 Nov (sets chat): "We always want the character in centre right of the frame. With a decent amount of space around them." Then: "In the case of this film. For the interview joke. Always in the same position as May." Carried in notes/brexit-is-done-sets.md (shot table: all three centre right, face about 60% across, space round them); note 9 lets May be framed a little wider, Kemi and Blair matching her.

## The world (rule 1): the film's `PLAN` in metres (`python3 source/plan.py Brexit Is Done (working name) sketch OUT.jpg`); places
benchmarked against references in `BENCHMARK` (rule 3, `python3 source/benchmark.py Brexit Is Done (working name) OUT.jpg`)

Rehearsal clips sent: none: Sam, 24 Nov (Q8), build in film order instead. (rule 8: the 3-4 riskiest moves as 2-3 s clips, before building the rest; the date and file,
or "none: why". Pre-flight warns until this line is filled)

Shot board sent: (rule 11: every shot on one board before any move is written: `rough.py board Brexit Is Done (working name) OUT.jpg`, send
it, then `rough.py sent Brexit Is Done (working name) OUT.jpg --delivered --board`, which records it. Pre-flight refuses to run until the record
holds every shot, each with someone in SHOT_CAST, sent before the first move; and while any "done?" box below is blank:
rule 14)

## The brief as a checklist (CLAUDE.md, 18 Oct): every detail of Sam's brief and notes, ticked before the first animatic
| # | from the brief or a note (copied word for word: wording, asterisk and bleep counts, positions, colours, props) | done? |
|---|------|------|
| 1 | Brief items 1-18 (list at the top: May plum jacket seated left-facing; Kemi hard hat, braids, hi-vis, site in grey daylight with the four background actions; Blair grey hair, red tie, oak library, chase, grin then lunge; the three lines; Hook Text) | ticked 25 Nov (chat 17) against stills at 0.3, 6.6, 9.0, 12.0, 16.5, 20.0, 25.2, 26.7 s and the animatic |
| 2 | Locked by Sam: seated legs off (R7), cast, order | respected |

## References as checklists (guides/satire.md): what each photo shows, and whether ours matches (compare.py sheet)
| reference | what it shows (count, colours, positions, facing, brands, proportions) | ours matches? |
|---|------|------|
|   |      |      |

## Exceptions (rule 13): anyone or anything left out of a check, one row each (a pattern like Journalist* is fine); pre-flight refuses a film setting's exception (HANDS_OK, LINE_OK, any *_OK, ALLOWED_POPS) with no row here; a code comment is never a reason. check: the setting's name, or 'house look', 'lap', 'drawing checks', 'camera feel' (who: the shot)
| check | who | why | looked at full size (sheet, panel) |
|---|---|---|---|
| THREE_QUARTER_OK | 1 | locked by Sam (24 Nov): the interview look, May turned to the interviewer off-frame left (item 14); the camera may not move | chat 18, shot 1 frames full size: face and look read | chosen | Sam |
| THREE_QUARTER_OK | 2 | locked by Sam (24 Nov): the interview look, Kemi turned to the interviewer off-frame left (item 14); the camera may not move | chat 18, shot 2 frames full size: face and look read | chosen | Sam |
| THREE_QUARTER_OK | 3 | locked by Sam (24 Nov): the interview look, Blair turned to the interviewer off-frame left (item 14); the camera may not move | chat 18, shot 3 frames full size: face and look read | chosen | Sam |
| MOVESIZE_OK | 1 (May, chin up at -0.25 s) | the opening lean (keys lean 0 to 7.5 by 0.75 s, the hook, unchanged since Sam's earlier animatics) carries her head 25 px; the chin up itself is 0.9 (was 1.4) | chat 37, stills 0-0.6 s: one forward settle, not a bob | chosen | Claude |
| HANDS_OK | *workers 2 | real staging: the runner on the top lift runs side on; at the back of each arm swing his far hand passes behind his body at the back of each swing, as a real runner's does (rule 41's 'no hand'; all of shot 2, 7.5-17.5 s, chat 25: the far arm stays closed, moves.open_back yaw) | chat 19, shot 2 at 10.67-12.08 s, 2x zoom: the arm reads as swinging, the hand back the next drawing; he is 40 px tall | chosen | chat 19 |
| HANDS_OK | *fleeing staff and guests* | real staging: the guests run side on across the room; each far hand passes behind the body at the back of each swing (all of shot 3, 17.5-26.9 s; chat 25: the far arm stays closed, so it hides on more drawings), as a real runner's does | chat 19, shot 3 at 20.92 and 23.0 s full size: the near arm swings clear, the far one reads behind the body | chosen | chat 19 |
| ALLOWED_POPS | guest | 17.6-17.9 s: the first guest appears in the doorway as the double doors open (through a door, the brief's beat) | chat 19, shot 3 at 17.63 and 17.88 s full size | chosen | chat 19 |
| ALLOWED_POPS | guest | 19.9-20.2 s: the woman in red runs off the frame's right edge at 4.4 m/s; the drawing before she is half out of frame, so the check sees her vanish away from the edge | chat 19, shot 3 at 20.0-20.25 s full size | chosen | chat 19 |
| ALLOWED_POPS | guest | 22.4-22.75 s: a guest runs in at the frame's right edge, half hidden by Blair's shoulder, so the check sees her appear away from the edge | chat 19, shot 3 at 22.42-22.67 s full size | chosen | chat 19 |
| ALLOWED_POPS | guest | 25.2-25.55 s: the last guest runs off the left edge ahead of the wolves | chat 19, shot 3 at 25.25-25.5 s full size | chosen | chat 19 |
| `*13.50 s (shot 2): the frame (26.00 m away) is drawn over a big orange pipe riser (25.85 m, nearer)*` | - | Sam (26 Nov, on the still): "Leave it": the scaffolding's planks and tape cross in front of the pipe, as scaffolding stands in front of a building | chat 32, shot 2 at 13.50 s full size, the marked still sent to Sam | chosen | chat 32; Sam's word |
| `HANDS: 1 *: Theresa May (*)'s right arm: the hand pushed back into its own sleeve *` | - | the chop gesture, forearm raised and angled toward the interviewer: seen from the front the forearm is foreshortened (55% of its length) but the hand stays clear and visible beside the sleeve | chat 20, shot 1 at 1.75 s full size (1080 px): hand and raised forearm read as a bent arm gesturing | real | chat 20; named to Sam |
| `HANDS: 2 *: Kemi Badenoch on site (*)'s right arm: the hand pushed back into its own sleeve *` | - | the wave: forearm raised and turned toward camera, foreshortened (51%); the hand circle sits clear of the sleeve | chat 20, shot 2 at 12.42 s full size: reads as a wave | real | chat 20; named to Sam |
| `HANDS: 2 *: the site's workers *'s right arm: an arm with no hand (the hand covered) *` | - | the three scaffold workers (about 40 px tall) walk side on with the far hand behind the body, as the runner's; the hand shows on the other frames | chat 20, shot 2 at 8.67 s, 3x crop: they read as walking, hands behind | real | chat 20 |
| `caption "*": * s on screen at 1.1x for * words (too fast to read)` | - | stand-in voice at ~220 words/min: a 3-4 word piece cannot stay longer without lagging the words, and joining makes 7-8 words; re-timed on Sam's takes | chat 19: every piece listed, the joins tried | real | the chat that times Sam's takes |
| `* s (shot 2): *worker * passes through it on screen *` | - | painting order: the digging worker is painted in front of the pipes and hoarding, the building frame and ground behind him; the check reads his plan depth (25 m), not the painting order | chat 19, shot 2 at 7.5 s full size: he reads in front, on the ground | chosen | chat 19 |
| `11.25 s (shot 2): the frame (26.00 m away) is drawn over a big orange pipe riser *` | - | background painting order inside the building, one frame, 91 px | chat 19, 11.25 s | chosen | chat 19 |
| `* s (shot 3): guest * passes through it on screen *` | - | the guests in the corridor and stepping through the double doors are drawn inside the doorway's cut; the check knows the wall's depth, not the doorway | chat 19, shot 3 at 18.25-19.0 s full size: each guest inside the opening | chosen | chat 19 |
| `the bookcases, *: * m wide; a real bookcase is about 0.8 m *` | - | built-in wall shelving (the brief: 'book-lined'), several 0.8 m bays wide | chat 19, shot 3 at 18.25 s full size | chosen | chat 19 |
| `blair: edge with no line at (502, 14)*` | - | the line test draws the head against the top of its canvas; in the film the hair top is outlined | chat 19, shot 3 full size | chosen | chat 19 |
| `may: no outline at (674, 14)*` | - | the line test draws the head against the top of its canvas; in the film the hair top is outlined | chat 19, shot 1 full size | chosen | chat 19 |

## Notes
Send all notes in ONE message, each with the shot and the time, e.g. "shot 2, 10.3 s, left: the man never looks at the zombie".

Status: one line of what was done (no "Was:"; git keeps the history), "new kind" or "seen before" (a "seen
before" note means a check is missing: add it), and the note's line in `guides/critique-checklist.md` (rule 30):
a new line's id, or an old one and why it missed (line unclear, sheet didn't show it, no critique).
"Should have caught": the check that should have caught the note before Sam saw it (its name as pre-flight prints
it, e.g. AUDIT, SHOT CAST, caption), or "none" when no check could; the handover check refuses a blank one
(check-catches change 2, Sam's Y 20 Nov), so misses are counted without guessing.

| # | shot | time | note | line | should have caught | status |
|---|------|------|------|------|--------------------|--------|
| 23.2 | 2 (Kemi's site) | 9.4-24 | Sam (26 Nov): "Move Kemi a bit closer to the action so that everything isn't so distant." | new: staging | none (a wish, not a fault) | Sam picked 2 (the site a third closer, 26 Nov): build it for real (the site and the four actions moved nearer, all in frame) |
| 24.1 | 1 (May) | 4.17 | Sam (26 Nov, on the chat 37 May clip): "There is a May head dip at 4:17 that doesn't work. It's very sharp and doesn't correspond to anything a person would actually do." | new: speed of a head move | none: movesize measured how far, never how fast (her head dropped 15 px in ONE drawing, then took four to come back); and the voice's own accent nods (headlife) jumped in one drawing too | fixed (chat 38) in the kit, not by a check (Sam, 26 Nov: "not make this mistake in the first place"): acting.HEAD_MIN, a nod can't go down or back faster than a real head (0.2 s), whatever a moves file writes; headlife's accent nods eased over half a second; May's two 0.1 s nods on "that referendum" one firm nod. Now no drawing moves her head more than 6 px (3.9-9.4 s). Kittest head_moves_never_snap. Clip ow-n24-may.mp4 |
| 24.2 | 1 (May, "wolves") | 6.6-9.4 | Sam: "'Wolves' her mouth closes too soon. It doesn't read as a satisfied smirk but a neutral expression. Check references for 'smirk' or 'satisfied smirks' and add that to your repertoire of emotions." | seen before (fault 5, chat 35: "tight satisfied smile"): rule 30 | why the first fix failed: 'smile' lifts BOTH lip corners only 0.004 of the face a unit, so 0.45 was half a pixel: no smile could ever read | fixed (chat 38): references (FACS: a smirk is one corner pulled up and back, lips closed, unilateral AU12; satisfied adds the cheek up, AU6). Shared faces.lips 'smirk' (0..1, below 0 the other side): one corner lifted SMIRK_UP, lips pressed, a crease at the corner. May's 'satisfied' moods: smirk on her near cheek, lids narrowed, held to the cut. Kittest smirk_one_corner. Clip ow-n24-may.mp4 |
| 24.3 | 3 (Blair) | all | Sam: "Tony's suit sleeves are a different colour to the jacket. Investigate why this was drawn like this." | new: colour match | why: chat 14 (critique r5 b) lifted every dark sleeve 14% to grey so a black arm read over a black jacket (views.sleeve_colour); and house heads never took a trousers colour, so his suit trousers were the house grey | fixed (chat 38): the sleeve is the jacket's own colour, a thin lit edge (limbs.DARK_RIM, turned views) keeps a dark arm readable. Trousers in the jacket's colour were tried and undone (note 25). Kittests suit_one_cloth, dark_sleeve_reads (now asks the same cloth). Clip ow-n24-blair.mp4 |
| 24.4 | 3 (Blair) | all | Sam: "His shirt and tie section still seems like a small raised ridge, it doesn't quite look natural. A common fault at 3/4 views." | seen before (face tool chat 12, "like a ridge"): rule 30 | why the first fix failed: chat 12 only moved the V's place (v_at 0.32 to 0.24); the shape stayed a parallel white strip between thin lapel slivers outlined on both sides, with a tie bar and no knot | fixed (chat 38, views.torso_view, every man in a suit and tie at three-quarter): an open V narrowing to the button, collar points, a knot and a widening blade, broad lapels lying flat with their inner edge on the V. Clip ow-n24-blair.mp4 |
| 25 | 3 (Blair's legs) | all | Sam (26 Nov, a still of Blair's lap): "The leg gap you previously fixed is back, why" | seen before (the leg gap): rule 30 | why: chat 38 made his trousers the jacket's colour (a suit as one cloth); the seated legs' drawing shows the lap and crotch by the trousers' different tone, so the line between the legs ran up into the jacket (castsheet crotch check: blair 0.51) | fixed (chat 38): the trouser change undone (people.py), sleeves still matched; crotch check clean for Blair. Learn first before a one-cloth suit: the seated legs must read without a tone change |
| 26 | all (every nod: May, Kemi, Blair) | e.g. 17.6 s (Kemi) | Sam (26 Nov, on the 7 px phone demo): "It's not a nod, it's a head-bob." | new: what a nod IS (seen before only as size, notes 23.1/24.1) | why no check saw it: movesize and HEAD_MIN measure how far and how fast the eyes move, never HOW the head moves; the kit's nod (views.Rolled dy = nod x 5, plus 'down') slides the whole head down and up: a bob | open (chat 39, learn first, rule 91): reference photos of a nod side-on and three-quarter; draw a nod as a pitch about the top of the neck: chin down and in, the face lowered and squashed inside the head's outline, eyes down, the crown nearly still; a grey practice head first, then the cast. Sam's Q1 (the 7 px floor) is answered by this: size stops mattering until the move is a nod |
| 9 | framing (all three interviews) | - | Sam (24 Nov 00:42): "I don't mind if you zoom out on May a little to give the Kemi/Tony scenes more room to show their scenes" | new: framing | none (a wish, not a fault) | passed to the sets chat (staging): May may be framed a little wider, Kemi and Blair match her |
| 5 | cast sheet v2 | - | Sam: "Can I just say...I'm not sure we have female bodies? Kemi's body seems much more like a man's." | seen before (GTA 20 Nov, "Lucia on a man's box body"): rule 30 | none (no check knows who is a woman; the GTA fix was opt-in for Lucia only and never catalogued, so chat 2 told Sam no build existed) | open: through the proposal route (notes/proposals/womans-build.md); waiting for Sam's pick |

Decisions made (kept so a long session or a new session never has to rediscover them):
- 



## Acting rows: shots 1-3 (the acting plan: notes/archive/brexit-is-done-handovers.md, rule 74)
| line | who | shot and why | face | body | lands on |
|---|------|------|------|------|------|
| 1 "The Prime Minister would do well..." | May | 1: single, her face is the hook | patient smile, brows up on "remember", tight satisfied smile on "wolves" | raised finger, palm turning up, chops, hands settle | "wolves" |
| 2 "Andy Burnham needs to spend less time..." | Kemi | 2: single, deadpan against the carnage | disdain, flat stare, curt nod | ramrod straight, hand presses, thumb back, chop, pat | "backwards", "job" |
| 3 "Well, in my opinion..." | Blair | 3: single, the grin then the lunge | genial, sincere, chuckle, big grin | hand on chest, breezy shrug, grin held 1.5 s | "Hague", then the lunge |

Cost line (recorded every handover; shown to Sam only on a problem): film so far 61.63% of 15%; forecast 68.6% (2026-11-26)
