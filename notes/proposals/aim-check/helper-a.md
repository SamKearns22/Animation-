# Helper A: aim-check

## Leak
Yes. "or says so in its plan and handover" and "a check that notices when it is missing" point at a written-line-plus-check remedy. Set aside. (I also saw the first lines of chat.md in a directory listing; ignored.)

## Results
- Milburn: estimate 24%, ledger 32.85% over 17 chats (notes/ledger/milburn.md); Sam's own app reading 22% (notes/proposals/milburn-review.md). The two disagree; which is right is unchecked.
- "8.7 times plan" (29.43 spent vs 3.4 planned for sets, props, build, board) is true of the ledger but not clean: stage lines were closed late, so "sets" carries the whole plan and cast (milburn-review.md section 2). The record cannot say what each build stage really cost.
- The forecast "lands at 100.4%" was printed in the ledger and nothing acted on it: handover.py has no forecast or budget line (grep: 0 hits); only ledger.py prints it.
- Where Milburn's money went, by the review: screenplay doubled (34 s to 68 s) with a travelling forest, two likeness heads, six props; estimate redone three times, each up (17.5, ~19, 24); reverse two-shot staged three times; 3/4 fix 3.6% in one chat; search 15-35% of most Opus chats.
- Sam, 19 Nov 09:14 (notes/ledger/sam/h3akq5qv.md): he does not want cost messages "all the time", will sometimes choose to pass 15%, and wants Claude always asking "how can I make this work at maximum quality for minimum cost" while planning and building.
- Gap: no record of the moments a build route was chosen, so nobody can yet say how often a cheaper, equal-quality route was missed.

## The real decision
Not "does the handover name the aim" but: at the moments a film's cost is set (choosing the build route for each new thing, and when a stage runs past its share), is the aim weighed with numbers, across all the film's chats? Bigger levers than a line: stage shares that are closed on time, and a forecast that forces a re-plan.

## Root cause
1. The aim is prose read once at chat start; nothing at the choosing moment asks for routes and their cost, so chats build the first route that works (staging done three times; the 3/4 fix in one go).
2. The only live number per stage is broken: stages closed late, so overruns are invisible until the film is over, and the forecast feeds no check.
3. What was tried: the finder reminder (finder-use.md) was advice, and behaviour barely moved; a written "aim" line would be the same kind of advice, satisfiable by one stock sentence.

## Approaches weighed
1. Aim line in plan and handover, checked for presence. Cheap; passes on paper with a boilerplate sentence; adds nothing at the choosing moment.
2. Reframe, route choice priced: each new build item in the plan gets two routes (kit reuse vs new build) with a % estimate and a quality reason; the chosen one becomes a ledger stage share.
3. Reframe, numbers steer: stages closed at each stage end (refused at handover if not), and a stage over 1.5 times its share makes the chat (not Sam) re-plan the rest before more building; Sam told only when the forecast passes 15%.
4. Learn first: read Milburn's and Protest Tiers' planning and build chats for every route choice and score whether a cheaper equal route existed.

Chosen: 4, then 3, then 2, one at a time. Approach 1 dropped.

## Proposal
Learn (changes nothing, ~1% of a week, Sonnet): from the two films' chats list every build-route choice and every re-stage; for each, was a cheaper equal-quality route in the kit catalogue, and what did the miss cost. Output: count of misses and their % cost. This sets the number for Change B and says whether B is worth making.

Change A (first, one yes): handover.py end refuses a handover when the chat's stage is not closed in the ledger, and prints "stage X: Y% of its Z% share; film forecast F%". At 1.5 times a stage's share, the next chat's start check requires a re-plan written in the notes (cheaper route for the rest, never a cut) before building. Sam sees a line only when the forecast passes 15%, with his choice to accept it. Number to beat: Milburn's build stages, 8.7 times share; target every build stage within 1.5 times, or a re-plan written when crossed. Measured from the next film's ledger stage lines. Cost to build ~1.5% of a week once.

Change B (only after the learn result, its own yes): the plan's build list must give two routes per new item with a % and a quality reason; the check refuses a plan item with one route. Number to beat: the miss count from the learn step.

Sam would notice: no new message most of the time; one line when a film heads past 15%; fewer re-stages.

## Sam test
Q1: An expert steers on live numbers at the choosing moment, not on a stated intention.
Q2: Scope is the whole film and two films' chats; the 8.7 figure is flagged as distorted.
Q3: A handover refusal and a start-check gate, not a reading habit; a boilerplate sentence cannot pass a number.
Q4: Four different approaches weighed; the line idea fails Q3.
Q5: Learn changes nothing; A and B each undo alone.
Q6: Sources named; the 32.85 vs 22 conflict and the true stage costs marked unchecked.
Q7: Sized to where money went (route choices, unseen overruns), not to the cheapest line.
Q8: Both changes permanent, reviewed at the next film's end.

## Lost / Added
Added: a stage-close step at each handover; a re-plan when a stage runs 1.5 times over; later, two routes per new item. Lost: nothing in the film; a handover can be refused until the stage is closed.

## Unchecked
Which of 32.85% and 22% is Milburn's real cost; real per-stage costs; whether the search-first change (forecast at handover) is already queued with Sam ("All 3", 19 Nov 09:26, not traced); the 1.5 times threshold until the learn step.
