# Helper B: the guard stops plain film questions

## Leak
Mild: the problem file names the context-lines rule as the likely trigger and points to review lesson 6, which states a fix (let film-content questions through). Both are ignored.

## Results
- **The guard cannot withhold a reply.** It is a Stop hook. It runs after the text is on Sam's screen, blocks once, and always lets the second try through (source/propose.py `hook`). Every block therefore shows Sam the message twice. Sources: the problem file's 22 Nov status chat, and notes/ledger/sam/gr9hlufs.md (17:05, "Why did you write your response 3 times?").
- **The log shows only part of it.** notes/proposals/unrouted.md records only replies that were still faulty on the retry: 39 lines, 15–22 Nov. A block the chat fixed leaves no trace, so the total number of blocks is unknown.
- **My split of the 39** (unchecked against each chat's full context):
  - 10 named a judged proposal but did not use the exact "Critiqued:" wording.
  - 9 were film or budget questions (props stage, "Report", effects, Hook Text options, shot 4 camera, round-2 spend).
  - 8 asked whether to *start* the route. CLAUDE.md requires that question.
  - 3 were parser bugs (blocks on proposal files that do not exist, e.g. "notes/proposals/2.md").
  - About 6–9 were real unrouted system asks.
  - So about 17–20 of the 39 were wrong blocks.
- **The 15 Nov widening never landed.** Re-running notes/proposals/guard-holes/probe.py today still misses 9/12 change asks and blocks 1/10 routine ones, the same as before "adoption". Its promised test set of Sam's real questions does not exist (searched source/ and notes/proposals/).
- **Cost in % of a week:** not measured (unchecked). Milburn review item 7 says a block meant the stale-test fix was never asked; the log says that reply was sent. The two conflict.

## The real decision
The decision is not which words mean "film". It is **where the route is enforced** so that unjudged changes cannot happen without costing Sam duplicate messages, in every chat of every film. The bigger lever is guarding the act (editing rules, tools, checks, kits), not the wording of a question.

## Root cause
1. A check run after display can only add messages; it can never hold one back.
2. Keyword sorting of free text has failed both ways, twice.
3. The 15 Nov fix skipped its learning step, so nothing real was ever tested.

## Approaches weighed
1. **Tune the keywords.** This is the named lever, and it has failed twice. It still repeats messages. Rejected.
2. **Reframe: guard the change.** A before-tool-step hook refuses edits to system files unless an adopted, judged proposal names them. Asking costs nothing, and nothing is shown twice.
3. **Declared asks.** The chat labels each question "film" or "change". This relies on honest labelling (fails Q3).
4. **Learn first.** Build Sam's real-question set and score every design on it.

Chosen: 4, then 2, then trim the reply guard. These are separate steps.

## Proposal
**Learn (changes nothing).**
- A Sonnet chat gathers every numbered or Y/N question put to Sam in Milburn and the film before it, from notes/ledger/sam/ and the 39 log lines with their context. It also lists every system file edited in those films.
- A blind helper labels each question: film, start-route or system.
- Every block is logged from now on, not only the failed retries.
- Cost: about 1% of a week (estimate).

**Change 1, alone: a change gate.**
- A before-tool-step hook refuses writes to CLAUDE.md, guides/, .claude/ and shared source/ files (film files are exempt, using `propose.py review`'s existing line) unless the file is named by an adopted proposal with a valid verdict.
- A kit test covers it.
- To beat: 0 unrouted system edits and 0 film edits refused, on the learned list.
- Cost: about 1.5% of a week, Opus medium.

**Change 2, alone, after change 1 has held for a film.**
- The reply guard stops sorting unnamed questions as film or system.
- It keeps the checks on replies that name a proposal. The parser bugs are fixed, and "Critiqued:" is accepted in any wording if the numbers are right.
- To beat: 0 film or start-route questions blocked on the set, and fewer duplicates Sam sees (from the full block log).
- Cost: about 0.5% of a week.

**What Sam notices:** no repeated messages for film questions, and no system change without a judged proposal.

**Total:** about 3% of a week, once, against the 15% per film.

## Sam test
- Q1: An expert guards the harm (the change), not the wording.
- Q2: The evidence is the real questions from two films, not five Milburn lines.
- Q3: Hooks enforce it in every chat, with no reading or choosing needed. Each change has a number to beat.
- Q4: Four different approaches were weighed. Keyword tuning has failed twice.
- Q5: Each change can be undone alone. Risk: an urgent mid-film tool repair needs a proposal. This is shown on the learned list first.
- Q6: Sources are named. The split and the costs are marked unchecked.
- Q7: Sized to stop unrouted changes fully, not to trim words.
- Q8: The changes are permanent, with no trial, and reviewed at the end of the film.

## Lost / Added
- Lost: an unnamed system *question* can reach Sam unblocked. The change itself still cannot be made.
- Added: the change gate, the real-question set, and a full block log.

## Unchecked
- The split of the 39 blocks.
- The cost per false block.
- Whether the stale-test ask reached Sam.
- The step costs.
- Whether this overlaps with the plain-check proposal.
