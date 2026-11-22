# Helper B: the guard stops plain film questions

## Leak
Mild: the problem file names the context-lines rule as the likely trigger and points to review lesson 6, which states a fix. Both are ignored.

## Results
- **The guard cannot withhold a reply.** It is a Stop hook. It runs after the text is on Sam's screen, blocks once, then always lets the retry through (source/propose.py `hook`). So every block shows Sam the message twice. (problem file; notes/ledger/sam/gr9hlufs.md: "Why did you write your response 3 times?")
- **The log is partial.** notes/proposals/unrouted.md records only replies still faulty on the retry: 39 lines, 15–22 Nov. Fixed blocks leave no trace, so the total is unknown.
- **My split of the 39** (my reading; unchecked against each chat's full context):
  - 10 named a judged proposal but not with the exact "Critiqued:" wording.
  - 9 were film or budget questions.
  - 8 asked whether to *start* the route, which CLAUDE.md requires.
  - 3 were parser bugs (e.g. "notes/proposals/2.md").
  - About 6–9 were real unrouted system asks.
  - So about 17–20 were wrong blocks.
- **The 15 Nov widening never landed.** I re-ran notes/proposals/guard-holes/probe.py today: it still misses 9/12 change asks and blocks 1/10 routine ones. Its promised set of Sam's real questions was not found in source/ or notes/proposals/.
- **Cost:** the cost of a block in % of a week is not measured (unchecked). Milburn review item 7 says a block stopped the stale-test ask; the log says that reply was sent. The two conflict.

## The real decision
Not which words mean "film", but **where the route is enforced**, so unjudged changes cannot happen without costing Sam duplicate messages, in every chat. The bigger lever is guarding the act, not the wording.

## Root cause
1. A check run after display can only add messages, never hold one back.
2. Keyword sorting of free text has failed both ways, twice.
3. The 15 Nov fix skipped its learning step, so nothing real was ever tested.

## Approaches weighed
1. **Tune the keywords.** The named lever. Failed twice. Rejected.
2. **Reframe: guard the change.** A hook that runs before each tool step refuses edits to system files unless an adopted, judged proposal names them. Asking costs nothing.
3. **Declared asks.** The chat labels each question "film" or "change". This relies on honest labelling (fails Q3).
4. **Learn first.** Build Sam's real-question set and score every design on it.

Chosen: 4, then 2, then trim the reply guard, as separate steps.

## Proposal
**Learn (changes nothing).**
- A Sonnet chat gathers every numbered or Y/N question put to Sam in Milburn and the film before it and every system file edited then.
- A blind helper labels each question: film, start-route or system.
- Every block is logged from now on.
- About 1% of a week (estimate).

**Change 1, alone: the change gate.**
- The hook refuses writes to CLAUDE.md, guides/, .claude/ and shared source/ files unless an adopted proposal with a valid verdict names them. Film files exempt.
- A kit test covers it.
- To beat: 0 unrouted system edits and 0 film edits refused, on the learned list.
- About 1.5% of a week (estimate).

**Change 2, alone, once change 1 has held for one film.**
- The reply guard stops sorting unnamed questions.
- It keeps the checks on proposals a reply names: parser bugs fixed, and "Critiqued:" accepted when its numbers are right.
- To beat: 0 film or start-route questions blocked on the set, and fewer duplicates in the full block log.
- About 0.5% of a week (estimate).

**Sam notices:** no repeated messages, and no unjudged system change.

**Total:** about 3% of a week, once (estimate), against 15% per film.

## Sam test
- Q1: An expert guards the harm (the change), not the wording.
- Q2: Two films' real questions, not five lines.
- Q3: Hooks enforce it in every chat; each change has a number to beat.
- Q4: Four different approaches weighed. Keyword tuning has failed twice.
- Q5: Each change can be undone alone. Risk: an urgent mid-film tool repair needs a proposal, shown on the learned list first.
- Q6: Sources named; the rest marked unchecked.
- Q7: Sized to stop unrouted changes fully.
- Q8: Permanent, with no trial; reviewed at the end of the film.

## Lost / Added
- Lost: an unnamed system *question* can reach Sam unblocked. The change itself still cannot be made.
- Added: the change gate, the real-question set, and a full block log.

## Unchecked
- The split of the 39 blocks.
- The cost per false block.
- Whether the stale-test ask reached Sam.
- The step costs.
- Overlap with the plain-check proposal.
