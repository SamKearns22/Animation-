# Helper B: seated legs

## Leak
The file's name and Facts lean toward the GTA solid body; I weighed it alongside other routes.

## Results
- Four R7 chats in two days, no gain. Blind judges' scores (1-5, waist down):
  - after chat 2: front 3-4, side 4, 3/4 4, crossed 2-3 (results-r7.md);
  - after chat 4: front 2-3, side 3, 3/4 3, crossed 2-3, "no score moved by a whole point" (results-r7c4.md).
- Cost: 27% of a week (Sam's figure, ledger/sam/ss8plxqq.md). The r7 ledger shows 0 chats, so the real cost is unchecked. That is about 6.7% a chat; bench chats cost 2.0-2.6% each (GTA ledger lines 62-63, estimates).
- Sam has never seen the solid body's legs: the car door hides them (notes/bench/l2-side-by-side.jpg). Its trousers are painted on, Jason's build only (bench_pose.part_at).
- The solid body is missing from guides/kit-catalogue.md, and R7 began on 24 Nov without it.

## The real decision
How the kit draws any body whose parts face the lens or pass in front of each other (sitting, crossing, lying, leaning). Choose between hand-drawn outlines for each view and one solid body. Also decide what stops a failing kit job before it reaches 27%.

## Root cause
1. **Method.** Each view's outline guesses the shortening and the overlap again, so a patch to one view leaves the others guessed (handover-sam-25nov.md).
2. **No stop.** Rules 87 and 30 ("fails twice") are kept by hand, so they did not fire. The job had no budget line.
3. **Not findable.** The working solid body stayed as Jason-only film code, outside the catalogue.

## Approaches weighed
1. Outlines traced from photos: already failed in four chats.
2. Solid legs under the flat torso. Risk: the per-part 3D arm drew "sausage" four times, cause unchecked.
3. **Reframe:** one solid kit person on sitting.realize's skeleton, drawn in one pass with the house head, hands and colours, and clothes as shells.
4. **Reframe the process:** a kit job stops by itself when the judges' scores flatten.
5. **Learn first:** measure 2 against 3 before changing anything.

Pick: 5, then 3 if it wins, then 4 as a separate change.

## Proposal
**Learn (changes nothing).** One Opus-high chat, capped at 4%.
- Draw the v4 sheet (four views; May, Kemi, Blair) two ways: (a) the whole body solid; (b) solid legs joined at the waistband.
- Trousers: a shell pushed out from the leg, about 14-15 cm wide at the knee (results-r7.md).
- Skirt: the body's skirt helper surface, if it exists.
- Score both sheets with the same blind judges (judge_r7.py) and the bum check (no_bottom).

**Number to beat:**
- every view at 4 or more from all three judges;
- nothing below chat 4's scores;
- the right woman/man read for all three;
- the bum still reads.

If neither reaches it, stop and tell Sam what must be learned next.

**Change 1 (only on that result).**
- The winner becomes the kit's seated person for new films, with a catalogue line.
- Enforced by a kit test that redraws the sheet against the threshold and the seated checks.
- About 6-8%. To beat: the threshold, then Sam's Y on one sheet.

**Change 2 (its own yes).**
- The handover check stops a kit job after two chats whose scores rose by less than one point.
- Kit jobs' costs go into the ledger.
- Its example: it must flag R7 chat 3 from results-r7 and results-r7c3.
- About 1%. To beat: no kit job above 15% without Sam's word.

**Cost:** 10-12% of a week, under 15%, reused by every later film.

**What Sam would notice:** one sheet beside v4, then one numbered question.

## Sam test
- Q1: measures first, then fixes the method.
- Q2: all four rounds of judge scores and the bench record.
- Q3: the root cause is named; each change is enforced by a kit test or the handover check.
- Q4: five approaches weighed; the pick ends the guessing and the burn.
- Q5: learning changes nothing; each change undoes alone.
- Q6: sources named; gaps below.
- Q7: sized to reach the judges' 4, not to a price.
- Q8: learning records a fact; changes are permanent, reviewed at the film's end.

## Lost / Added
- Lost: chat 5's six outline fixes; with change 1, the drawn R7 legs leave new films.
- Added: 4% to measure, 6-8% to build, 1% for the stop check. A solid look on flat people is a risk the judges check.

## Unchecked
- The 27% figure.
- The bench chats' costs.
- What caused the arm's "sausage".
- Whether the helper surfaces exist in the data.
- Whether the solid body draws correctly at the kit's own scale.
