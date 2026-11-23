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
- Locked by Sam: the script above (lines, order, who is where, every background action).
- Sam's words kept: Kemi and Blair face "the same way she is facing, being interviewed"; the script and site: "I'll describe
  both to you soon." "For now, please work on the characters."
- Reuse: Badenoch's face is already built (`source/facehouse.py` 'badenoch'); May and Blair are new faces.

## Where things stand (the ONE handover, 15 lines at most: overwrite it at every stage switch; move the old one to notes/archive/brexit-is-done-handovers.md)
- **Rules that bite next:** 30 (note 5 is a repeat of GTA's "Lucia on a man's box body"), 49 (likeness), 89.
- **Done (chat 3):** note 6 fixed (Kemi's orange stops outside her collar, any build); note 5 through the proposal
  route (judged: helper B's, 8 found, 4 fixed, 4 named; sent to Sam as two options); Sam's v2 notes saved with
  pictures; reserve list made (Sam: 6+6 body shapes and today's tool chats, notes/next-jobs.md R1-R6).
- **Chats are named "Open Wounds"** (Sam, 23 Nov); the film's files keep the name brexit-is-done.
- **Next (Opus high: a new build):** Sam's pick on the woman's body; Option 1 = learn, then a woman's body by
  default with a check, then women's clothes, then cast sheet v3. Then the plan from the script (brief items 4-12):
  sets, the wolves from Cry Minister on the new kits, the estimate.
- **Needs Sam:** Q1 woman's body: option 1 or 2 (asked in chat 3).
- **Read:** `guides/job-packs.md` Build; notes/proposals/womans-build.md "Final version".
- **Open rule requests:** none (the proposal's check becomes a rule only with Sam's Y).
- **For Claude:** `castsheet.py sheet brexit-is-done OUT.jpg`; build switch `body: ..., build woman` (body.FIGS);
  chat 3's try: scratch kemi_torso.py style draw via castsheet.draw(sp, yaw, PP).

## Handover check, named not fixed (chats 1-3)
 Chat 3: the four CLAUDE.md SENTENCE alerts are the same ones chats 1-2 named (Sam's own CLAUDE.md edits; the
  sentences still stand there in his newer wording). No estimate yet (COST): set at the plan stage, after Sam's pick
  on the woman's body (the film is at 6.38% of a week). Kit test people_from_a_description crashes in a fresh copy
  (no film/blessed marker; named in notes/next-jobs.md, not this film's). Branches as chat 2 named them below.
 Chat 2: branches claude/gta-v5-sound-draft, claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31
  still hold only GTA logs/proposals/one-off tools (GTA posted): not merged, left for a tool chat. The two lost CLAUDE.md
  sentences ("Locked by Sam", "Just go") were red before chat 1 (Sam's own CLAUDE.md edits): for Sam/a tool chat, not
  this film. No film code yet, so no `page.py show` (FINDER): chat 2 changed only shared tools (facehouse, turnhead,
  people_parts, people, castsheet, handover). No estimate yet (COST): the plan stage sets it once the script comes.
  Kit tests: the start-up run (kittests-last.log) ran while chat 2 changed the code: its 2 reds (kit_people_never_generic,
  move_to_shared_catches_film_fixes) both PASS rerun on the saved code (N26 fixed: archived notes are NAME-notes.md).

 branches gta-v5-sound-draft, gta-chat46-build, dreamy-fermi-vkhutz,
  gta-chat31 hold only GTA logs/proposals (film posted): not merged, for a tool chat; CLAUDE.md "Locked by Sam" and
  "Just go" sentence alerts and kittest move_to_shared_catches_film_fixes (N26) were red before this chat (checked on
  the saved code); no estimate yet: the plan stage sets it once the script comes. No film code yet (no `page.py show`): only the shared face tool and people kit changed.

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
| 1 | cast sheet v1 | - | Sam: "Reference 1: these side images appear cut off?" The three-quarter full figures were cut in half by my sheet crop | new: sheet-edge | none (sheet maker had no edge test) | fixed: the sheet is built by `castsheet.py sheet`, which refuses a figure touching its tile's edge (selftest caught) |
| 2 | cast sheet v1 | - | Sam, Tony: "Reference 2, Tony: do you see how something is going wrong still with 3/4 views?" "That is not the same person and haircut as presented in the straight on view." Turned hair flattened by the crown clamp | new: front-3/4 match | none (front and 3/4 never judged side by side) | fixed: the turned hair is built to the front piece's own outline (hair shell), side/back strokes added; `castsheet.py match` caught Sam's picture |
| 3 | cast sheet v1 | - | Kemi: orange gone from her clothes; 3/4 not right (hat flat and wide, glasses off the face) | new: front-3/4 match | none | fixed: orange shoulders and sleeves, navy chest, waist band; turned brim dips like the front, side lines; far braid curtain; zipped navy collar; `match` caught Sam's picture |
| 5 | cast sheet v2 | - | Sam: "Can I just say...I'm not sure we have female bodies? Kemi's body seems much more like a man's." | seen before (GTA 20 Nov, "Lucia on a man's box body"): rule 30 | none (no check knows who is a woman; the GTA fix was opt-in for Lucia only and never catalogued, so chat 2 told Sam no build existed) | open: through the proposal route (notes/proposals/womans-build.md); waiting for Sam's pick |
| 6 | cast sheet v2 | - | Sam: "Do you see Kemi's orange detailing travels over her white collar?" | new: piece over collar | none (match checks colours, not layering: gap written in castsheet.py MAP) | fixed (chat 3): people_parts.workwear_torso's yoke starts outside the collar and lapel and follows the body's own outline (any build); saved: notes/sam-notes/brexit-cast-v2/n6 |
| 4 | cast sheet v1 | - | Sam asked: "Are we using our most recent 3/4 kit?" | - | - | answered in chat 1 (yes, the turned head kit; the fault was the hair built apart from the front); Sam said Y to the plan |

Decisions made (kept so a long session or a new session never has to rediscover them):
- 
