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

## Where things stand (chat 31, 26 Nov, session_01J1JB7WQi6LkF56PZE9rCCe)
Rules that bite next: 89 (the critique gate), 59 (render lock), 30 (kinds seen before).
Done (chat 31): pre-flight run; it REFUSES the animatic on 3 faults: (1) critique round 27 pass 1: 7 faults open (3 "can't tell"); (2) 13.50 s shot 2:
the frame drawn over the big orange pipe riser (4 of 142 frames); (3) pop-in shot 3: a guest vanishes mid-shot at 33.88-34.12 s away from the edge.
Sam (26 Nov): "1. If the current fresh eye review picked up on them, fix them. If they didn't, leave them. Two. I don't know. You will have to show me a
still of what you're talking about. 3. Guest vanishes. That sounds like something you should fix."
Next: Opus medium chat: (1) fix the review faults the fresh eye named (leave the ones it could not tell); (2) show Sam ONE still of 13.50 s shot 2 (pipe/frame),
plain words, ask Y/N, do not fix before his word; (3) fix the guest's vanishing at ~34 s (draw it leaving through a door or the edge, the beat unchanged);
then pre-flight, and hand to Sonnet for the animatic, finish.py (Hook Text, sign-off), drafts, send. Then the body-kit chat (Opus medium): the 22 cast-sheet STOPs.
Needs Sam: the still of 13.50 s (his Y/N). Read: guides/job-packs.md "Checks and animatic"; python3 source/waivers.py todo brexit-is-done; this section.
Open rule requests: none. Branches claude/gta-*: GTA's, left.
Locked by Sam: the script (as recorded), who is where, every background action, the three places' briefs, the cut on the lunge; film order; all three in May's place and size; the cast; every camera and framing. Do not change timing, lines, mouths, soundtrack.
For Claude: ACT.site_actors / room_actors guests; ALLOWED_POPS needs a why row in Exceptions.

## Sam's words held elsewhere (chat 4, so the handover check finds each)
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
| HANDS_OK | *workers 2 | real staging: the runner on the top lift runs side on; at the back of each arm swing his far hand passes behind his body at the back of each swing, as a real runner's does (rule 41's 'no hand'; all of shot 2, 7.5-17.5 s, chat 25: the far arm stays closed, moves.open_back yaw) | chat 19, shot 2 at 10.67-12.08 s, 2x zoom: the arm reads as swinging, the hand back the next drawing; he is 40 px tall | chosen | chat 19 |
| HANDS_OK | *fleeing staff and guests* | real staging: the guests run side on across the room; each far hand passes behind the body at the back of each swing (all of shot 3, 17.5-26.9 s; chat 25: the far arm stays closed, so it hides on more drawings), as a real runner's does | chat 19, shot 3 at 20.92 and 23.0 s full size: the near arm swings clear, the far one reads behind the body | chosen | chat 19 |
| ALLOWED_POPS | guest | 17.6-17.9 s: the first guest appears in the doorway as the double doors open (through a door, the brief's beat) | chat 19, shot 3 at 17.63 and 17.88 s full size | chosen | chat 19 |
| ALLOWED_POPS | guest | 19.9-20.2 s: the woman in red runs off the frame's right edge at 4.4 m/s; the drawing before she is half out of frame, so the check sees her vanish away from the edge | chat 19, shot 3 at 20.0-20.25 s full size | chosen | chat 19 |
| ALLOWED_POPS | guest | 22.4-22.75 s: a guest runs in at the frame's right edge, half hidden by Blair's shoulder, so the check sees her appear away from the edge | chat 19, shot 3 at 22.42-22.67 s full size | chosen | chat 19 |
| ALLOWED_POPS | guest | 25.2-25.55 s: the last guest runs off the left edge ahead of the wolves | chat 19, shot 3 at 25.25-25.5 s full size | chosen | chat 19 |
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

Cost line (recorded every handover; shown to Sam only on a problem): film so far 49.05% of 15%; forecast 56.1% (2026-11-26)
