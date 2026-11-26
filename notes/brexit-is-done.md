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

## Where things stand (chat 37, 26 Nov, session_01U3pKR3AXhEjf4GS3ZJpZ4k)
Rules that bite next: 30 (a note seen before: 23.1 and 23.4 were), 92 (move size: now a window, floor 10 px, ceiling 18 a nod), 11 (shot 2 held until Sam's framing number).
Done (chat 37): Sam's notes 23.1-23.4 (Notes table): head moves back to house size + movesize ceiling, kittest head_moves_not_comic; Kemi's backwards point path (acting.PLACES point back / mid / swing); chase drawn far to near in the corridor (places_site._beyond) and cover sees each guest and wolf and skips doorway-vs-wall; shot 2 framings sheet sent; May clip and chase clip sent (body check clean), Kemi before/after sheet sent. Chase order stuck while two overlap (_ranks; kittest chase_order_stuck).
Next: chat 38 (OPUS, medium): Sam's notes 24.1-24.4 (Notes table: May's sharp dip at 4.17 s, the 'wolves' smirk, Blair's sleeve colour, his shirt-and-tie ridge), clips; then on Sam's number for shot 2: build it for real (the site's depths in brexit-is-done-places.txt and the action depths nearer, all four background actions and some grey sky kept in frame; not the preview's enlarging), board, then a Kemi clip (13.5-16 s, the point back); then Sonnet: pre-flight, animatic with Override only if Sam says so, finish.py, send.
Needs Sam: shot 2 framing number; Y/N on check-knows-intent (V3). handover end (chat 37) REFUSED on 24 CAST SHEET stops (seated cross-legs and 'no bum' poses not used in this film; the judge record old): settle first.
Read: guides/job-packs.md "Notes round".
Open rule requests: none.
Locked by Sam: the script (as recorded), who is where, every background action, the three places' briefs, the cut on the lunge; film order; all three in May's place and size; the cast; every camera and framing (shot 2's distance to the site now Sam's to pick, note 23.2). No change to timing, lines, mouths, soundtrack.
For Claude: preflight name 'brexit-is-done'; branch claude/elegant-knuth-xlgo94; staging hold: python3 source/staging.py pick brexit-is-done 2 N "words".

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
| 19 | 3 (Blair in the armchair) | 17.5-26.9 | Sam (26 Nov, after the body kit went on): "One thing I noticed on Tony: his hands hover rather than resting on the chair arms." | seen before kind: contact (hands on objects; Seeing like Sam 1) | to name (body chat): the check that looks at hands resting on a seat's arms | fixed (chat 30): the armchair's resting hand curls over the arm's front end (sitting.spec_armrests, ARMREST_DROP; shared). Check: sitting.armrest_faults (the hand's centre above the arm's top), kittest hands_rest_on_armrests: catches chat 27's pose, passes the fix and a desk rest. Clip ow-n19-22-tony.mp4 |
| 20 | 3 (Blair, house style) | all | Sam (26 Nov): "Please make sure Tony matches the house style: if you look at previous characters like Netanyahu, Trump or Brand, there's something off that I can't pin down. He's a bit doll like?" | new: likeness / house look (compare with the house's Netanyahu, Trump, Brand) | to name (body chat): house look | fixed (chat 30): lined up with the house's Netanyahu (netan-yahoo-vertical), Trump (midterminal), Brand (blessed). What differed: brown brows under grey hair (painted on), almost no neck (the bigger house face grows down over it: 5-8% of his head vs Netanyahu's ~10%), a 73-year-old with almost no lines. Fixed: neck_up 0.09 (facehouse, front and turned: shared), grey brows, age_boost 1.5, lid 0.2. Check: facehouse.doll_faults, kittest house_head_not_a_doll |
| 21 | 2 (Kemi's face) | 7.5-17.5 | Sam (26 Nov): "Kemi, the lines around her mouth and eyes make her look less like the real life Kemi. Consult reference pictures of her face again." | new: likeness (face lines) | to name (body chat): likeness / name test | fixed (chat 30): her photos are smooth-skinned; the age measure read the shade under her round cheeks and eyes on darker skin as the deepest lines of all 13 faces (deeper than May's or Blair's). Her age lines off (age_boost 0). Check: facehouse.line_faults (dark skin + a top-two line drawn), kittest face_lines_photos_show; facehouse_whole_head re-held. Clip ow-n21-kemi.mp4 |
| 22 | 3 (the last wolf pounce on Blair) | end of shot 3 | Sam (26 Nov): "The final wolf pounce on Tony, so quick it's barely registered by the viewer." | seen before kind: an action too fast to read (note 13, the worker's pounce) | to name (body chat): the check on how long an action holds on screen | fixed (chat 30): was 0.33 s (four frames) from off-screen in mid-air. Now acted: the wolf creeps in low behind his shoulder 1.6 s before the cut, coils 0.4 s, leaps 0.5 s (six frames) up and over; the cut still on the lunge, chat 29's clock unchanged. Check: shared source/readtime.py (pre-flight, READ_TIMES), kittest pounce_long_enough_to_read. Clip ow-n19-22-tony.mp4 |
| 23.1 | 1 and 2 (May's lean, May's and Kemi's nods; Blair's too) | 0-24 | Sam (26 Nov): "May's lean, Kemi and May's head bobbing, have all become comically large. They were flagged as 'not strong enough' and 'too small for the phone' and they have gone so far overboard that they've lost the coherent acting of previous films. THIS IS A MAJOR ERROR." | seen before kind: move size (chat 32/35 fix overshot) | MOVE SIZE (movesize.py): it had a floor only (22 px, set from a sheet, never from the films Sam passed), so chats 32 and 35 pushed every move past it: nods 22-34 px, the lean in on "remember" 166 px | fixed (chat 37): nods 1.9-2.1 (12-14 px), lean in 5 with roll 1 (56 px), Kemi's chin up 1.7, May's opening chin up 0.9, Blair preen 1.5, nod 1.3. Check: movesize now a window (floor 10 px, ceiling 18 px a nod, 70 px a lean: MAX_PX); kittest head_moves_not_comic catches all 11 of the last animatic's moves, passes the film now. Exception row: May's opening chin up (the opening lean carries it). Clip ow-n23-may.mp4 |
| 23.2 | 2 (Kemi's site) | 9.4-24 | Sam (26 Nov): "Move Kemi a bit closer to the action so that everything isn't so distant." | new: staging | none (a wish, not a fault) | held (staging.py): 3 numbered framings sent (quick previews, the background enlarged); waiting for Sam's number, then built for real (the site and the four actions moved nearer, all in frame) |
| 23.3 | 2 (Kemi, "backwards") | 13.7-15.6 | Sam (26 Nov): "Kemi's motion on backwards isn't correct. Reassess the arm and elbow movements. The acting note is good but execution is poor." | new: gesture path (a hand's way between places) | none: no check looks at the in-between frames of a gesture (the hand on the hip, the arm across the belly) | fixed (chat 37; before/after notes/brexit-is-done-kemi-backwards.jpg): she faces left, so 'back' is screen right; the old path went across her belly, then a hand on the hip, then an arm reaching up and out ("over there"). Now the arm swings up at her side (point back swing), the hand comes up by the shoulder, elbow down, and jabs back past her ear (acting.PLACES, shared). Stills sent (the clip waits on note 23.2's framing). Check to build: a hand-on-hip / akimbo in-between check (learn first: what makes an in-between read as a pose) |
| 23.4 | 3 (the chase in) | 26.1-35.5 | Sam (26 Nov): "The wolves and guests are clipping over each other when they run in, you need to make sure they stick to their visual order. Decide who is in front of who and stick to it. Why did our clipping tests not work? Investigate" | seen before kind: drawing order (rule 57) | cover (pre-flight's clipping check): it recorded all four guests under one name and merged them, never recorded the wolves, and the corridor guests gave false 'over the panelling' lines that buried the rest; head_on / within_reach were kit tests on chat 13's paths only, never run on the film, and skip runs at the lens; and the last animatic skipped pre-flight under Override | fixed (chat 37): the corridor drawn far to near (places_site._beyond, shared: it drew in list order), a guest always in front of the wolf at their heels at the same depth; cover: each person under their own name (cover.person alias), wolves recorded, people seen through a doorway not judged against the wall (cover.through). Kit test cover_sees_each_runner (old order caught, new clean) |
| 24.1 | 1 (May) | 4.17 | Sam (26 Nov, on the chat 37 May clip): "There is a May head dip at 4:17 that doesn't work. It's very sharp and doesn't correspond to anything a person would actually do." | to judge (the nod on "referendum" at 4.07 s, rise 0.12: size now fine, its speed/shape not) | to name | open (chat 38) |
| 24.2 | 1 (May, "wolves") | 6.6-9.4 | Sam: "'Wolves' her mouth closes too soon. It doesn't read as a satisfied smirk but a neutral expression. Check references for 'smirk' or 'satisfied smirks' and add that to your repertoire of emotions." | seen before (fault 5, chat 35: "tight satisfied smile") : rule 30 | to name | open (chat 38): reference photos of a satisfied smirk (one-sided, lips pressed, cheek up), a 'smirk' mood in the shared moods, held to the cut |
| 24.3 | 3 (Blair) | all | Sam: "Tony's suit sleeves are a different colour to the jacket. Investigate why this was drawn like this." | new: colour match (sleeve v jacket) | to name | open (chat 38): find where the arm's cloth colour comes from (views.person arms v torso) |
| 24.4 | 3 (Blair) | all | Sam: "His shirt and tie section still seems like a small raised ridge, it doesn't quite look natural. A common fault at 3/4 views." | seen before ("still"): rule 30 | to name | open (chat 38) |
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

Cost line (recorded every handover; shown to Sam only on a problem): film so far 59.23% of 15%; forecast 66.2% (2026-11-26)
