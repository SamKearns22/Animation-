# Helper B: the guard stops plain film questions

## Leak
Mild: the problem file names "the context-lines rule" as the likely trigger, and points to Milburn review lesson 6, which states a fix (let questions naming film content through). Both ignored.

## Results
- **The guard cannot hold a reply back.** It is a Stop hook: it runs after the text is already on Sam's screen, blocks once, then always lets the second try through (source/propose.py `hook`, `stop_hook_active`). So every block shows Sam the message twice (the 22 Nov status chat in the problem file; Sam, notes/ledger/sam/gr9hlufs.md, 22 Nov 17:05: "Why did you write your response 3 times?"). The guard has never stopped an ask from reaching Sam. All it can do is make the chat write a second message.
- **What gets logged:** notes/proposals/unrouted.md lists only replies that were still faulty on the second try. It has 39 lines, 15 to 22 Nov. A block that the chat fixed leaves no trace, so the total number of blocks is unknown. That gap is a finding in itself.
- **My reading of the 39** (unchecked against each chat's full reply):
  - 10 named a judged proposal but did not use the exact "Critiqued:" wording.
  - 9 were film or budget questions: props stage, "Report" file, effects under speech, Hook Text options, shot 4 camera, "does that match what you pictured", protest round-2 spend, end-of-film review, "is job 3 the Learn step".
  - 8 asked whether to *start* the route ("put it through the proposal route?", "do you want that as a permanent rule?"). CLAUDE.md requires that question.
  - 3 were parsing bugs: proposal files that do not exist, such as "notes/proposals/2.md".
  - About 6 to 9 were real system asks with nothing behind them.
  - So about 17 to 20 of the 39 should never have been blocked.
- **The 15 Nov widening never landed.** I re-ran the old probe (notes/proposals/guard-holes/probe.py) today. It still misses 9 of 12 change questions and wrongly blocks 1 of 10 routine ones, the same as before guard-holes was "adopted". Option 1 of guard-holes promised a set of Sam's real questions to test against. No such set exists: I searched source/ and notes/proposals/ and found none.
- **Cost:** a re-send per block, plus chats learning to word around the guard (problem file). It is not measured in % of a week (unchecked). Milburn review item 7 says a guard block stopped a stale-test fix from ever being asked. The log says that reply was sent. This is unresolved.

## The real decision
The real question is not "which words mean film?". It is **where the proposal route should be enforced so that unjudged changes cannot happen, without Sam paying for it in duplicate messages**, across every chat of every film. The guard checks the *wording of a question*. The bigger lever is the *act* that matters: a chat editing rules, tools, checks or kits.

## Root cause
1. A check that runs after the reply is shown can only add messages, never withhold one.
2. It sorts free text by keywords, and that has failed in both directions twice (the 15 Nov probe and today's re-run).
3. The 15 Nov fix skipped its own learning step, so there was nothing real to test against.

## Approaches weighed
1. **Tune the keyword lists** (add film words, drop the context lines). This is the named lever. It has failed twice and still repeats messages. Rejected.
2. **Reframe: guard the change, not the question.** A check that runs before any tool step refuses an edit or commit to rule, tool, check or kit files unless an adopted, judged proposal covers that file. Asking Sam costs nothing. An unrouted change cannot happen, and nothing is shown twice.
3. **Declared asks:** the chat marks each ask "film" or "change". This relies on honest labelling (fails Sam-test question 3).
4. **Learn first:** build the real-question set and measure every design on it before changing anything.

Chosen: 4, then 2, then trimming the reply guard. Each is a separate step.

## Proposal
**Learn (changes nothing):**
- A Sonnet chat gathers every numbered or Y/N question put to Sam in Milburn and the film before it (from notes/ledger/sam/ and the 39 log lines, with the six lines above each). It adds a list of every system file edited in those films.
- A blind helper labels each question film / start-the-route / system.
- Also from now on, every block is logged, not only the second-try ones.
- Cost: about 1% of a week (estimate).
- Result: today's guard scored on Sam's real questions.

**Change 1, alone: the change gate.**
- The check that runs before each tool step refuses writes to CLAUDE.md, guides/, .claude/ and the shared parts of source/ (not film files, using the same line `propose.py review` already draws) unless the file is named by an adopted proposal with a valid verdict.
- A sound kit test guards it.
- To beat: 0 unrouted system edits on the learned list, and 0 film-file edits refused.
- About 1.5% of a week, Opus medium.

**Change 2, alone, after change 1 has held for one film:**
- The reply guard stops sorting questions as film or system.
- It keeps only the mechanical checks on replies that name a proposal. The three parsing bugs are fixed, and "Critiqued:" is accepted with the right numbers in any wording.
- To beat: 0 film or start-the-route questions blocked on the learned set, and duplicate messages Sam sees (counted from the full block log) down from today's count.
- About 0.5% of a week.

**What Sam would notice:** no repeated messages for film questions, and changes to the system that never happened without a judged proposal.

**Total:** about 3% of a week once, set against the 15% per film.

## Sam test
- Q1: An expert puts the gate where the harm happens (the change), not on wording.
- Q2: The real questions from two films, not five Milburn lines.
- Q3: Enforced by hooks in every chat, with no reading or choosing needed. Each change has a number to beat.
- Q4: Four different approaches weighed. The keyword fix has failed twice.
- Q5: Each change can be undone alone. Risk: an urgent tool repair mid-film needs a proposal first. That is named, and it is shown on the learned list before Sam says yes.
- Q6: Sources are named. The 39-line split and the costs are marked unchecked.
- Q7: Sized to stop unrouted changes completely, not just to trim words.
- Q8: Permanent changes, reviewed at the end of the film. There is no trial period.

## Lost / Added
- Lost: the reply guard no longer judges unnamed questions, so a system *question* with nothing behind it can reach Sam. The change itself still cannot be made.
- Added: the change gate, the real-question test set, and a log of every block.

## Unchecked
- The 39-line split, done without each chat's full context.
- The cost per false block.
- Whether Milburn's stale-test ask reached Sam.
- The step costs (estimates).
- Whether the plain-check proposal overlaps with change 2.
