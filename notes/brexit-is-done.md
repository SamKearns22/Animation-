# Notes for Brexit Is Done (working name) (one file, numbered; mark each done as it is fixed)


## Brief checklist (Sam's words, 23 Nov; tick each against the film before the first animatic)
(Template note, raise at the plan: the estimates proposal, notes/proposals/estimates.md, options 1 and 2.)
News: Theresa May "aghast" at Burnham's EU plans, says "Brexit is done" (BBC, Sunday with Laura Kuenssberg, 22 Nov 2026).
- [ ] 1. Theresa May "in this exact interview" (`references/brexit-is-done/may-interview-*.jpg`): seated, turned to
      screen-left, looking at the interviewer off-frame left; dark wood-panelled backdrop; plum jacket, patterned
      blouse, hands gesturing in front of her.
- [ ] 2. Kemi Badenoch in hard hat and site clothes (`badenoch-hardhat-sam.jpg`: white hard hat, glasses, long braids,
      orange-and-navy hi-vis jacket); faces the same way as May; a construction site behind her (Sam will describe it).
- [ ] 3. Tony Blair as he is today (`blair-today-sam.jpg`: grey swept-back hair, big smile, dark suit, red tie, white
      shirt); ends up facing the same way as May; place not decided ("maybe some swanky embassy sort of place?").
- [ ] Title: "Open Wounds". News: Andy Burnham's new EU deal, criticised as "opening up the wounds" of Brexit.
- [ ] The joke: the critics talk about packs of wolves instead of Brexit, ignoring wolf attacks all round them while
      they criticise ("people not noticing the damage they have done").
- [ ] 4. Theresa (her interview): "The Prime Minister would do well to remember that we had a referendum, and in that
      referendum, the British Public chose wolves."
- [ ] 5. Cut to Kemi interviewed on a building site: an expanse of dusty ground; behind, a large complex under
      construction, "all holes and pipes and scaffolding".
- [ ] 6. From the first second: two wolves leap on a construction worker in the background and tear him to shreds
      (as Cry Minister, the old wolves "spruced up" with the new body kits and rules).
- [ ] 7. Background: a worker runs from two wolves across the scaffolding and leaps off it, off frame, to escape.
- [ ] 8. Background: a group of men with steel bars staving off another group of wolves on the next level down.
- [ ] 9. Background: wolves milling round the dirt in hard hats and construction vests, blood-drenched: sitting,
      pawing the dirt, wandering.
- [ ] 10. Kemi, staring at the interviewer as if none of it was happening: "Andy Burnham needs to spend less time trying
      to take us backwards and more time doing his job: reducing the number of British people with their faces chewed off."
- [ ] 11. Embassy scene, "a bit more, uh, classic British": oak and bookshelves, a political room like Westminster "or
      some other august locale". Behind Tony Blair, doors thrown open as wolves run rampant, chasing staff and guests.
- [ ] 12. Blair: "Well, in my opinion, you shouldn't listen to anything I say, I'm Tony Blair, I invaded Iraq, I belong in
      The Hague." Big cheesy grin.
- [ ] 13. (Sam, 23 Nov, Q5) Blair holds the big grin about 1.5 s, then a wolf lunges at him; cut to the sign-off on
      the lunge (chat 3's pick, before it reaches him).
- [ ] 14. (Q3) The interviewers are never seen or heard; all three look off-frame left at them.
- [ ] 15. (Q4) Hook Text: "Andy is opening old wounds... 🇬🇧" (the flag drawn as one picture: hook_text fixed chat 3,
      kittest hook_text_flag_emoji).
- [ ] 16. (Q6) Kemi's site in daylight under a grey British sky, as her photo.
- [ ] 17. (Q7) Blair's room: Sam: "He would do his interview in the UK but sure why not" -> a grand oak-panelled,
      book-lined room in London (chat 3's pick from his words), not Brussels.
- [ ] 18. (Q2) Blood: Sam: "Can we do better?" than Cry Minister's flat red: plan sent (two reds and a shine, arcs that
      land and soak into the dust, stained muzzles, paws and vests, torn hi-vis and a tumbling hard hat, dust at every
      leap; chunks as Cry Minister, no bones or insides); waiting for his Y.
- [x] (Q1) Woman's body: option 1 (Sam: Y, 23 Nov): notes/proposals/womans-build.md "Final version".
- Locked by Sam: the script above (lines, order, who is where, every background action).
- Sam's words kept: Kemi and Blair face "the same way she is facing, being interviewed"; the script and site: "I'll describe
  both to you soon." "For now, please work on the characters."
- Reuse: Badenoch's face is already built (`source/facehouse.py` 'badenoch'); May and Blair are new faces.

## Where things stand (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/brexit-is-done-handovers.md)
- **Newest work: branch `claude/open-wounds-chat13`** (also pushed to the main line if allowed; the next chat merges it first).
- **Locked by Sam:** the script, who is where, every background action, the three places' briefs, the cut on the lunge; film order; all three in May's place and size (head top, eye row 700, chin, face centre about 64% across), May about waist up; the cast (no more character work); the seated bottom and knees are reserve job R7, never worked on in this film (R7 runs in its own chat since 25 Nov: session_01U3pKR21qH3HD4urog8SVBy; its new lower body is switched OFF for this film).
- **Rules that bite next:** 74 (May's gestures land on her words), 5 (nothing through anything: hands on the chair arms, Kemi's hands), 85 (cost watch).
- **Done (chat 13):** kit tests: the start-up run passed (139); after the fixes, the run, chase, gait and moves tests passed. shot 3 watched whole and fixed: runners sank into a lunge (shared run: a foot is down for at most 0.75 leg of travel, moves.RUN_SWEEP; kittest run_hips_stay_up, example notes/learn/run-lunge/); guests met head-on nose to nose and a wolf ran through a guest and past a hand (now waves: everyone in frame runs the same way, two abreast, the near one leading by 0.45 s, both wolves behind; shared checks moves.head_on and moves.within_reach, kittests movers_never_meet_head_on and side_by_side_out_of_reach, examples notes/learn/chase-meetings/). 14 passes became 11 (no animatic had them). Critique pack r5 (source/data/critique/brexit-is-done/r5-p1): see the line below.
- **Next (Opus high):** first, Sam's Y (25 Nov, chat 13, Q1): "the full kit tests run only when a chat changed a shared tool, and always before an animatic and a final render; a chat that changed only its film's files skips the run and the wait": take it through the proposal route (`source/propose.py new kit-tests-when`, pack, judge, record), then build it in handover.py's start-up/end check with a kittest. Then fix critique r5's faults as one list (`critique.py record` printed them; S4, S1 and panel 1-2 A1 were my strip crops, marked false): (a) the lunge wolf shows only as a brown blob with teeth at the right edge for 2 frames (26.75-26.83): make it read as a wolf leaping at his head in the frames before the locked cut; (b) side-on runners: the far arm's round hand shows on the chest while its arm is hidden (P5); (c) near-lane runners tread on the fallen tray and it never moves (rule 5): it skids or tips, or their feet clear it; (d) the tray reads as a disc and the flutes as specks at phone size, and its flat landing and the pools did not read in the strip: look at full size; (e) can't-tells: wolves long and stretched in run frames, Blair's hair a helmet. P7 (Blair's knee balls, no bottom) is R7, locked: name it to Sam with the animatic. Then `critique.py fixed`. Then the moves file story/brexit-is-done-moves.txt and its film side (acting.py FILMS has only blessed and milburn: add `_brexit`, as `_milburn`): May (hands low, one open palm turning up as her photos; small nods on "referendum" and "wolves"), Kemi (staring at the interviewer, a curt nod on "job"), Blair (the big grin held from 25.0); lips on stand-in timing (mouths.track), blinks (F.blinks), head life (headlife) for all three, all three `look` off-frame left; then the Sonnet chat for the animatic (tick the brief checklist first).
- **Needs Sam:** nothing blocks.
- **Read:** `guides/job-packs.md` Build; acting.py MAP (lines 1-90) and FILMS (840-905); milburn.py face_sp/acted (195-260); brexit_is_done.py seated/standing (88-150).
- **Open rule requests:** none.
- **For Claude:** moves.head_on / within_reach (shared, catalogued) run in kittests on this film's chase: a later film with movers calls them on its own table (moves.chase_movers). 8 old film files still draw see-through fills with Draw(img,'RGBA') (move to ink.glaze when touched). The evening gown reads as tunic and trousers front-on and side-on mid-stride: cast locked, name it to Sam with the animatic. override.py's quoted-Override logging still unchecked. castsheet._same_outlines is this film's only: move to shared. The stills command takes times one by one (the old handover's "17.5..26.9" form fails).

## Chat 13 end check, named
- Branches not this film's (GTA): claude/gta-v5-sound-draft, claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31 (a record only, Sam 22 Nov): left for the GTA chats.
- CLAUDE.md SENTENCE alerts: Sam's own edits (34f49840, 0945cc85), named as chats 1-12 did. Rule 74 acting rows, HEAD LIFE, rehearsal clips: the moves stage, chat 14. Framing quick checks (notes 3, 9): handled chats 9-10.
- Start check "NOT CARRIED" lines: chat 11's prompt words ("Blair's chase and t...") are the chase, done this chat.

## Chat 12 end check, named
- Brief checklist "empty" and framing notes 3/9: the checklist is above (unticked); notes 3 and 9 are cast/framing notes already handled (chats 9-10); ticked against the film before the first animatic (Sonnet chat).
- Rule 74 acting rows (shots 1-3) and HEAD LIFE for may, kemi, blair: the moves stage, next chat (chat 13).
- FINDER: chat 12 built new (shot 3's chase, the shared fixes), not a note: hand searches on purpose.
- SENTENCE: the same alerts on Sam's own CLAUDE.md edits that chats 1-11 named. COST: no ledger estimate (named since chat 4).
## Sam's words held elsewhere (chat 4, so the handover check finds each)
- Note 1 (Q4) Hook Text, Sam: "Andy is opening old wounds..." with the British flag: brief item 15.
- Note 1 (Q5) Sam: "Yes, before a wolf lunges at him": Blair's grin then the wolf lunge, brief item 13.
- Sam 22:00: "I do think we need multiple body shapes in our kit, maybe 6 for male and female": reserve job R1 (notes/next-jobs.md), waits for Sam to name it.
- Sam 22:06: "I'd be keen to answer your script questions soon": answered as Q1-Q7 (brief items 13-18); only Q2, the blood, is still open.

- Sam 24 Nov (sets chat): "We always want the character in centre right of the frame. With a decent amount of space around them." Then: "In the case of this film. For the interview joke. Always in the same position as May." Carried in notes/brexit-is-done-sets.md (shot table: all three centre right, face about 60% across, space round them); note 9 lets May be framed a little wider, Kemi and Blair matching her.

## Plan extras (rules 24-26, 54, 55): ambition estimate as a table, one row per new build and risky move, each with
its own share of a week and, for anything split into parts, how its ending looks and which parts the camera sees
break; eyelines and holds per shot; every sound effect (what, when, needed by); bleeped words (said, or a gap left?)

Every person, set, prop, pose and move in the brief gets a row: KNOWN (its kit-catalogue line, pose-gallery row or
"Passed the critique" row: almost free) or NEW (priced; drawn alone and critiqued before the cast sheet, rule 89).

First line: how much of the total is unmeasured. Each cost is the nearest measured past cost in `notes/ledger/`
(name the film and row), or 'unmeasured'; no padding, no multipliers. Each row names its stage (cast, sets, board, moves,
animatic1, round, final; board: the shot board of rule 11, ended by `rough.py sent Brexit Is Done (working name) OUT.jpg --delivered --board`; one 'round' row per notes round, priced from past films' real rounds); the stage totals go
into `ledger.py estimate Brexit Is Done (working name) PCT --stages "cast 2, sets 2.5, ..."` and each stage's end runs `ledger.py stage FILM NAME`.

| thing, build or risky move | KNOWN (where) or NEW | why (3D? parts the camera sees) | stage | estimate (% of a week) | measured from | spent |
|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |

## The world (rule 1): the film's `PLAN` in metres (`python3 source/plan.py Brexit Is Done (working name) sketch OUT.jpg`); places
benchmarked against references in `BENCHMARK` (rule 3, `python3 source/benchmark.py Brexit Is Done (working name) OUT.jpg`)

Rehearsal clips sent: (rule 8: the 3-4 riskiest moves as 2-3 s clips, before building the rest; the date and file,
or "none: why". Pre-flight warns until this line is filled)

Shot board sent: (rule 11: every shot on one board before any move is written: `rough.py board Brexit Is Done (working name) OUT.jpg`, send
it, then `rough.py sent Brexit Is Done (working name) OUT.jpg --delivered --board`, which records it. Pre-flight refuses to run until the record
holds every shot, each with someone in SHOT_CAST, sent before the first move; and while any "done?" box below is blank:
rule 14)

## The brief as a checklist (CLAUDE.md, 18 Oct): every detail of Sam's brief and notes, ticked before the first animatic
| # | from the brief or a note (copied word for word: wording, asterisk and bleep counts, positions, colours, props) | done? |
|---|------|------|
| 1 |      |      |

## References as checklists (guides/satire.md): what each photo shows, and whether ours matches (compare.py sheet)
| reference | what it shows (count, colours, positions, facing, brands, proportions) | ours matches? |
|---|------|------|
|   |      |      |

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

| # | shot | time | note | line | should have caught | status |
|---|------|------|------|------|--------------------|--------|
| 12 | 1 (May, board) | all | Sam (24 Nov, marked picture notes/learn/seated/no-bum-circular-knees-sam.jpg): "No bum/circular knees" | seen before: P7 (knee balls; the film after Blessed): rule 30 | none (P7 is a by-hand critique line and the board went out with no critique; the kit still ringed a knee aimed at the lens, and drew no bottom at all) | fixed in the shared kit (views.knee_cap: the knee is the thigh's rounded end, outlined only on its far side; views.seat_bottom: a seated bottom on the seat, under the hem, under a crossed top leg); check castsheet.seated_faults (catches Sam's frame, passes now; in castsheet build and the handover end); Blessed unchanged (0.01%). Sam (24 Nov): a reserve job, R7 in notes/next-jobs.md; the stopgap stays; shots go on |
| 1 | cast sheet v1 | - | Sam: "Reference 1: these side images appear cut off?" The three-quarter full figures were cut in half by my sheet crop | new: sheet-edge | none (sheet maker had no edge test) | fixed: the sheet is built by `castsheet.py sheet`, which refuses a figure touching its tile's edge (selftest caught) |
| 2 | cast sheet v1 | - | Sam, Tony: "Reference 2, Tony: do you see how something is going wrong still with 3/4 views?" "That is not the same person and haircut as presented in the straight on view." Turned hair flattened by the crown clamp | new: front-3/4 match | none (front and 3/4 never judged side by side) | fixed: the turned hair is built to the front piece's own outline (hair shell), side/back strokes added; `castsheet.py match` caught Sam's picture |
| 3 | cast sheet v1 | - | Kemi: orange gone from her clothes; 3/4 not right (hat flat and wide, glasses off the face) | new: front-3/4 match | none | fixed: orange shoulders and sleeves, navy chest, waist band; turned brim dips like the front, side lines; far braid curtain; zipped navy collar; `match` caught Sam's picture |
| 11 | Blair's grin v2 | - | Sam (24 Nov): "A stray line comes off the top of his smile on the right" | new: curve spikes | none (the curve tool overshoots where a closed curve passes one point twice; nothing looked for it; it was on cast sheets v1-v3 too) | fixed chat 7: the grin's outline no longer repeats its right corner; check castsheet mouth_spike_faults (every house mouth; catches the old outline). Seen, not fixed (shared with finished films): 7 more closed curves through one point twice in facehouse hair shapes (facehouse.py lines 987, 1042, 1056, 1156, 1385, 1570, 1639, 1651): look at full size for spikes next chat |
| 10 | cast sheet v3 (Blair's head) | - | Sam (24 Nov): "Tony's teeth look a bit...fleshy" (picture saved: notes/sam-notes/brexit-cast-v3/n10-blair-teeth-fleshy.jpg) | new: grin teeth | none (no check looked inside a mouth; the grin's top-lip line was drawn with the closed curve, so it doubled back, and sat across the teeth) | fixed chat 7: a full top row filling the grin's upper half, the thin lip on its edge, open lines (faces.house_mouth grin: only Blair uses it); check castsheet teeth_faults (catches the saved picture) |
| 9 | framing (all three interviews) | - | Sam (24 Nov 00:42): "I don't mind if you zoom out on May a little to give the Kemi/Tony scenes more room to show their scenes" | new: framing | none (a wish, not a fault) | passed to the sets chat (staging): May may be framed a little wider, Kemi and Blair match her |
| 8 | cast work, chat 7 (Kemi's new legs) | - | Sam (24 Nov 00:40, picture notes/sam-notes/brexit-cast-v3/n8-camel-toe.jpg): "This is a bit...camel toe" | new: crotch shape | none (no check looks at where the legs part; the blind judges read outlines at phone size, and I looked at the hips for nubs, not the crotch) | fixed chat 7: the legs part just under the seat, the crotch a small round point; check castsheet crotch_faults (catches the saved picture) |
| 7 | woman's body v1 (outlines, chat 4) | - | Sam (23 Nov 22:23): "How do I say this. Kemi Badenoch just does not have that body. Looks good for May though!" (picture: notes/learn/womans-build/outline-female-v1.jpg) | new: one woman's body for every woman is the same fault as one man's box for everyone | none (the learn step judged woman or man only, never "is this HER body"; Kemi's photo was not measured) | chat 6: Kemi measured from her 3 photos (build straight; numbers match the drawing), check built (catches n5 and n7); chat 7: woman in all 4 views to three fresh judges (v4g), on her measured widths |
| 5 | cast sheet v2 | - | Sam: "Can I just say...I'm not sure we have female bodies? Kemi's body seems much more like a man's." | seen before (GTA 20 Nov, "Lucia on a man's box body"): rule 30 | none (no check knows who is a woman; the GTA fix was opt-in for Lucia only and never catalogued, so chat 2 told Sam no build existed) | open: through the proposal route (notes/proposals/womans-build.md); waiting for Sam's pick |
| 6 | cast sheet v2 | - | Sam: "Do you see Kemi's orange detailing travels over her white collar?" | new: piece over collar | none (match checks colours, not layering: gap written in castsheet.py MAP) | fixed (chat 3): people_parts.workwear_torso's yoke starts outside the collar and lapel and follows the body's own outline (any build); saved: notes/sam-notes/brexit-cast-v2/n6 |
| 4 | cast sheet v1 | - | Sam asked: "Are we using our most recent 3/4 kit?" | - | - | answered in chat 1 (yes, the turned head kit; the fault was the hair built apart from the front); Sam said Y to the plan |

Decisions made (kept so a long session or a new session never has to rediscover them):
- 

