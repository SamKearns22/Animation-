# Helper B: front-on focus and unused best tools

## Leak
The problem file leans toward a solution: it tests "eyes + tilt + feature slide" and says "a real version must move whole pieces". Sam's own wish (front on, focus shown in the drawing, BoJack) is a brief, not a leak. Also: the folder held chat.md (the chat's own idea) and I read its opening while listing files. I have set it aside and reasoned from the record.

## Results
- Sam has given the same note twice: 17 Nov "3/4 characters still look like shit" (notes/ledger/sam/at3cudfk.md) and 19 Nov "weakest post ... sunken necks" (h3akq5qv.md). The 18 Nov fix (three-quarter-people.md, "one source for every view") did not clear it. That is a repeat note under rule 30.
- Milburn: 11.9 s of 65 s showed people turned (milburn-review.md). YAW3 = 40 is at milburn.py line 478. It cost 22% of a week against the 15% aim, and the 3/4 fix chat alone cost 3.6% (milburn-review.md).
- Rule 38 already says "front on by default" (rulebook row 38). The drawn angle is checked only when a film has no rooms plan (preflight.py lines 409-410). Milburn has one, so the turn passed with no reason line.
- The engine snaps every turn to 0/45/90/135/180 (views.py line 34). Nothing between front and 45 exists.
- In the test sheet, eyes plus head tilt read left or right on both people. The slide mock reads strongest. The 45 turn loses Kemi's braids and thins Andy's glasses (andy-kemi-test.jpg, seen).
- Weaker route: the first 60 lines of people.py (its MAP) list `head: measured` and `head: part walliams` but not `head: house`, which is parsed at line 361 (checked). The catalogue sorts heads by who the person is, not by which route draws best (kit-catalogue.md lines 44 and 68, checked). No reason for the four NEETs' route was ever recorded (problem file).
- Gap: nobody has counted turned seconds or turned-people notes in films before Milburn. Nobody has tested which route a fresh chat actually picks from the current guides.

## The real decision
The decision is not "fix the 3/4 head". It is: across every chat of every film, does each person get drawn on the best head, staged so that direction reads without leaving that head, and does each stage land on its best route by default? The bigger levers are a check that already existed but skipped Milburn, and what a planning chat reads. The drawing code is a smaller lever.

## Root cause
1. **Turned people got on screen.** The front head cannot show focus (no uneven brows, no off-centre mouth, no feature slide). So staging read Sam's "from the side" as a 40-degree turn, and rule 38's check had a hole that let it through.
2. **Turned people look worse.** They are drawn from a second source, a 3D head rebuilt from the 2D design. Designed qualities (glasses thickness, the mass of the hair, the neck line) do not survive that rebuild. The 18 Nov fix restored missing parts, not how they are designed. That is why the note came back.
3. **The weaker route was chosen.** Choosing the route relies on a chat finding the right file and deciding well. The file it read omitted the best head, and nothing in the plan or pre-flight asks "is this the best route?"

## Approaches weighed
1. Rebuild turnhead until turned views match the front design. It has already failed once, it is the costliest option, and it leaves turned shots on screen.
2. Reframe: stage front on and give the front head a focus vocabulary, built once on the house head, with turned views kept only for walks, exits and backs.
3. Reframe: one front head for everyone (the house head, fed by a description for invented people), so detail and focus exist in one place.
4. Learn first: measure turned seconds and notes across recent films, and run a blind route-pick test (a fresh helper given the planning pack and three briefs, recording which route it picks).

Chosen: 4, then 2, then the route guard, one change at a time. Approach 3 waits for evidence.

## Proposal
**Learn first (changes nothing, about 1% of a week, Sonnet):**
- L1: across the last four films, count turned seconds per film, Sam's notes on turned people, and which turns a walk or exit actually needed.
- L2: the blind route-pick test across people, places, effects and movement. Record each pick against the best route.
- L3: one invented person (the goth) drawn on both front heads, on one sheet. Sam picks one.

**Then, one change at a time:**
- **C1. Close rule 38's hole.** Pre-flight reads the drawn angle on every film. A person past 25 degrees with no THREE_QUARTER_OK reason stops the animatic. To beat: 0 unreasoned turned seconds (Milburn had 11.9). About 0.3%.
- **C2. A focus piece on the house head.** It moves whole pieces (pupils, brows uneven, mouth off centre, features slid, a tilt) and keeps glasses and hair in their front design. It is enforced through the moves kit: listeners get "focus", not "turn". To beat: a blind judge names left or right correctly 10 out of 10 at phone size, and Sam picks it over today's 45 on Andy and Kemi. About 1.5%.
- **C3. Best route named and guarded.** One "best route" line per stage at the top of the catalogue and in each tool's MAP. The plan's estimate table names a route for each item, and pre-flight refuses one marked superseded. To beat: L2's test re-run picks the best route every time, against today's score. About 0.7%.
- **C4. Only if L3 shows the house head wins for invented people:** a description-to-pick route, so invented people use it too, and focus is then built once. About 3%, with its own Y.
- **C5. Retirement.** From L2 and the ledger, each route unused in three films goes to Sam as its own numbered line with a "Lost:" line, archived rather than deleted. It is reviewed at each film's end.

**What Sam would notice:** people facing the lens with eyes, brows and mouth aimed. There would be fewer people turned on screen, no repeat note on turned models, and a sheet before C2 and C4.

## Sam test
- Q1 Expert: the record is measured first, and the guards act where choices are made, not on chat memory.
- Q2 Best result: the evidence covers four films and every stage, not just Milburn.
- Q3 Comprehensive: C1 and C3 are pre-flight refusals, so nothing relies on a chat choosing to comply. Each change has its own number.
- Q4 Intelligent: four different approaches were weighed, and the costliest failed route was rejected with its reason.
- Q5 Risk: each change is separate, undoable and shown on a sheet first. Retirements are archived, not deleted.
- Q6 Checked: sources are named, and the gaps are listed under Unchecked.
- Q7 Not cheap: focus moves whole pieces, not a pixel warp, and the route guard covers every stage.
- Q8 Nothing temporary: each change is permanent once Sam says yes, and is reviewed at the film's end.

## Lost / Added
- Lost: the true three-quarter look in new films, except with a written reason; about 3.5% of a week once (plus 3% if C4 goes ahead); some archived tools.
- Added: front-quality detail in every talking shot, direction that reads, and no film reaching a weaker route by accident.

## Unchecked
- Turned seconds and notes before Milburn.
- Whether the people-kit front head can share the focus piece.
- Whether any posted film still renders from a tool that is up for retirement.
- The cost figures above, which are estimates.
