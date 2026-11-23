# named-lines, the learning step (changes nothing; chain B chat 2, Opus high, 23 Nov)

Sam picked option 1 (22 Nov). The proposal's Final version: learn first; then changes 1-4, each with its own yes; "the
results decide what changes 2 and 3 cover". Sources: notes/ledger/milburn/checks.jsonl (pre-flight's two saved runs,
20 Nov, 61 lines each, identical), notes/archive/milburn.md (chats 13, 15, 18), notes/ledger/blessed-preflight-chat3.txt
and notes/archive/blessed*.md, notes/grand-theft-autism.md, the rule-needs-check note table (chain A, reused, not
redone), git history of the film code, a full kit-test run in this container.

## 1. Every pre-flight line, sorted into four kinds

**Milburn (the 61 lines named at every animatic, chats 13 to 18):**
| kind | lines | which |
|---|---|---|
| blind: the check could not see the film | 37 | SHOT CAST "never on screen" 21 (no scene(t)); house-style lists missing 4; plan inputs missing 7 (no facing x4, no SHOT_MARKS, no camera for 10 shots, camera 2b looks at nothing); camera feel 1 (no cam_for); effect shapes 1, readability 1 (no lists); collisions not run 1 (no scene(t)); clipcheck COULD NOT TEST 1 |
| false: the check is wrong about this film | 8 (+60) | rooms overlap 3 (three separate places put at one origin); "stands inside the platform" 5 (they stand on it; the check wants on=). Plus the 60 false script/mouth lines chat 18 removed by handing the checks the cleaned takes in milburn.py |
| chosen: real, kept on purpose | 14 | captions "too fast to read" (Sam's own quick speech) |
| real | 0 | none on the list itself |
| never settled | 2 | syllable counts, lines 2 and 8 ("Sam to listen"; line 8 is probably NEETs said as letters) |
- 61% of Milburn's list was blind. One blind line (clipcheck) hid the real name-card fault Sam noted twice.
- The picture checks (HANDS 14-17, LAP 14 each animatic) are not in the ledger: only their counts were saved, so they
  cannot be sorted now. A gap in itself: the ledger keeps the quick check's lines, not the render's.

**Blessed (99 lines, then 17, then 0):** pre-flight at chat 10 printed 99, "mostly tool noise" (SHOT CAST, plan room
overlaps, journalists' hands): the same blind and false kinds as Milburn. Chat 3 (12 Nov) built the missing inputs in the
film's own code (blessed_checks.py): the list fell to 17, and those 17 were mostly real: real 11 (Bible off the hand,
shoulder seams x2, hand hidden on a hold x2, cot pose, judge frozen x2, arm drops before cuts x1, van hand, oath hand),
false 3 (the famous-face check looked for the wrong name; 2 cut lines from all journalists pooled under one name),
blind 1 (turnaround sheet skipped), chosen 2 (journalists seen from behind; the officer's grip, a touch to list). Chat 4
fixed or recorded all 17. **This is the one film where the list was short and real, and it was because the checks were
handed what they needed.**

**Grand Theft Autism:** its own renderer runs only the body check (humancheck); pre-flight never ran on it, so every
other check was blind for the whole film. Version 3 was made with every check off on Sam's order. The body check's
lines were named in batches (33b: arms out of the back on shot 5's walkers; 33c: 11 named).

## 2. Sam notes that were already a printed line
| film | note | the line printed earlier | kind of line |
|---|---|---|---|
| Milburn | name cards cut by hands (chat 13, again chat 18) | clipcheck COULD NOT TEST, named at every animatic | blind |
| Blessed | note 45, the newsreader loses his mouth (REPEAT) | "newsreader mouth check at 52 s", named in chat 2 | real, named as if chosen |
| Blessed | note 6, the cot pose | rule 42 POSE line for the cot | real (fixed chat 4; order of line and note not certain) |
- Blessed's note 45 had a second cause: checks() skipped the newsreader in a code comment (blind by a skip; waivers.py
  has refused unwritten skips since 12 Nov).
- GTA's repeat arm notes (G7-4, G8: Jason's backwards arm, third and fourth time) were drawn with checks off: blind, not
  printed. Whether the 11 body-check lines named at 33c come back as notes: not known yet.
- Milburn's other 31 notes: no earlier line (direction, or checks that ran and missed: chain A's table).

## 3. Check fixes made in film code (none moved to the shared tools at the time)
- Blessed 7: scene(t), solids(t), SET_FEET, cam_for, audits (blessed_checks.py); touch_faults, furniture_faults
  (blessed.py). The word "furniture" is in the shared audit and clipcheck now; not checked whether it is the same check.
- Milburn 1: the cleaned voice takes handed to the checks (milburn.py; 60 false lines gone, film only).
- Grand Theft Autism 2: car and street solids for the body check, written twice (gta_rehearse.py, gta_shots58.py).
- Total 10 fixes in 3 films; each new film starts without them.

## 4. Kit tests that really fail (full run here, 23 Nov)
108 of 112 pass. round_page (the one broken.md named) now PASSES: already repaired, nothing to do. The 4 red:
| test | kind | why |
|---|---|---|
| body_check_back_view, body_check_headless | blind | crashed: this container cannot download the body model (a GitHub clone is refused); they test nothing here |
| dearest_things_named | real | Grand Theft Autism's repeat-note flag misses Sam's earlier gun note; red at chain B chat 1's handover and now (two handovers in a row) |
| claude_md_sentences_never_lost | real | the "every stage aims at three things (13 Nov)" sentence was reworded into Statement One (22 Nov) and the test cannot find where it went |

## What the results decide
- **Change 1 ("could not test" stops the animatic):** the same code gap as the could-not-test lesson, which Sam has
  approved and which is being built now in its own chat (stop plus cover plus readable). Not built here, so it is not
  built twice. Its must-beat on Milburn is the same. Blessed's mouth was NOT a "could not test" line (a printed real
  line plus a skip), so change 1 would not have caught it; change 2 would.
- **Change 2 (one written record per line) should cover the chosen and real lines only** (Milburn's 14 captions and 2
  syllable counts; Blessed's 17). A blind line cannot be recorded as settled: it stops until the film or the kit hands
  the check what it needs (change 3). Without that limit, 37 of Milburn's 61 would be recorded once and never seen
  again, which is the blanket-reason fault the judge warned about.
- **Change 3 (shared inputs) should start with the places and moves kits**, because Milburn was built on them and
  they already know where everyone is: scene(t) for the cast and collision checks and layers for clipcheck (23 lines),
  facing, on=, cameras and separate rooms for the plan (15), cam_for for camera feel (1), and the cleaned takes for the
  voice check (60 false). House-style and effect lists (6) come from the template's defaults. Together: 105 of
  Milburn's 121 lines (61 named + 60 removed) gone with no film code. The "move to shared" line for film-code fixes
  covers the 10 found above.
- **Change 4 (kit tests):** round_page needs nothing. The "red at two handovers in a row stops the handover" part
  is still needed: dearest_things_named is red at two in a row today, and the two blind tests would be caught as
  "could not test", not passed in silence. Chain A (lesson 7) is wiring handover gates now: change 4 is built on top of
  its gate, not beside it.
