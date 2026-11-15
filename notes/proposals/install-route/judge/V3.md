# Helper B: install the proposal route?

## Leak
None. (I glimpsed the top of `install-route/chat.md`; this answer comes from the record.)

## Results
- Films run about 4x the 15% aim: Protest Tiers 53.56%, 33 chats; Blessed 62.21%, 24 chats (ledger headers).
- Every ledger reads "0 rounds, 0 notes" (all `notes/ledger/*.md`). `propose.py review` takes its notes count from the ledger, so step 6 would report 0 notes for every film. **The route's success measure has no data.**
- Replay run 2: chat's version 10-14, picks 21-22 (`run2/replay-*/judge/verdict-raw.md`); same-model judge.
- One route run costs about 1.3% of a week (ledger rows 03420c9e and 7e532a65: 6.53% over 5 cases).
- From 12 to 15 Nov, 50 commits touched the rulebook, catalogue or CLAUDE.md (git log). Changes per film are unchecked. At 10 routed changes per film, the route costs about 13% of a week.
- I tested the hook (`reply_faults`): four change questions all passed, e.g. "Y or N to add a new check before every animatic?" and "tighten the gate". A routine word overrides a change word, "gate" is unlisted, and its refusal invites the chat to "reword the question". Changes made without a Y/N question go unseen (problem file).

## The real decision
The decision is how changes to the system come to deliver fewer notes and films within 15%, judged per film. Two levers are bigger than the gate: measuring results, and the number of changes per film, since that sets what the route costs.

## Root cause
A chat writes and judges its own idea, with no outside critic and no record of results. The route fixes the critic but not the record. Replay judges said so themselves: "every ledger records 0 rounds, 0 notes" (run2 replay-1 V3, replay-2 V1). Enforcing by reading has already failed: page.py was named in a pack and run 0 times in chats 29 and 31.

## Approaches weighed
1. Install as built, permanent. Its measure is blind and its holes are known.
2. Undo the hook and keep a by-hand rule. Rejected: by-hand rules have already failed.
3. **Reframe:** install permanently, make results measurable, and put the route's own weak points through the route one at a time.
4. Learn first, read-only: count notes and system changes per film before anything else.
5. Route only "large" changes. Rejected: the chat's own sizing is the failure being fixed.

Chosen: 3, with 4 as its first job.

## Proposal
**Change 1 (one Y, permanent):** write the rule as sent and keep the hook on. End the Protest Tiers hiatus: the route is proven on real films (step 6), not by more replays.
**Learn (read-only; the queued results-first review of Protest Tiers; about 2-3%, unchecked):** from the transcripts, count Sam's notes per round, the faults a check should have caught, and each chat's cost by cause. Then run `propose.py review protest-tiers`, which is step 6's first real run. Baseline: notes, faults, % of a week, system changes per film, route spend.
**Then, each its own routed proposal and its own Y, after the learn result:**
- **Change 2:** the ledger fills notes and faults at each handover. Beat: no "0 notes" ledger for a film that had notes.
- **Change 3:** fix the hook. Beat: kittest built from real past replies; every change question blocked, every routine one passed, no "reword" advice.
- **Change 4 (only if changes per film are many):** one route run per problem, not per edit. Beat: route spend per film below Protest Tiers' system-change spend.

Enforced by hook, kittests and step 6, not Sam. Cost: 1.3% per run; learning 2-3%; changes 2-4 about 1.3% each plus builds (unchecked), against films at 54-62%.
What Sam notices: fewer back-end questions, each with two judged options, and a results line at each film's end.

## Sam test
Q1: An expert measures before tuning and tests the filter. Done here.
Q2: The unit is the whole film plus all its system changes.
Q3: Root cause found (no outcome record). The hook's holes are shown by test; enforcement is by hook and kittest.
Q4: Five approaches weighed; this gives the route a working measure.
Q5: Each change can be undone alone. The trust gap is closed by film results, not by Sam.
Q6: Sources named; the gaps are listed as unchecked.
Q7: Sized to make results measurable, not the cheaper "as built".
Q8: Permanent from the first Y; every change is reviewed at film completion.

## Lost / Added
Lost: speed on every system change, Sam's own rule requests included (about 1.3% each).
Added: a baseline per film, three later Y/N questions, and a route-spend line.

## Unchecked
Prompt tuning to the five cases; changes per film; cost of learning and of changes 2-4; how often changes skip a Y/N question.
