# Helper B: early warning when tools stop working

## Leak
The problem file names no solution. Its Record lists `chat.md`, which holds the writing chat's own idea. I opened it before I saw what it was and did not use it.

## Results
- **Message saver.** The newest saved Sam message is 16 Nov 19:02 (headers in notes/ledger/sam/*.md). Nothing from 17 Nov 07:54-08:07 was saved. The ledger shows chats still running until 23:55 on 16 Nov (notes/logs/handover-end.log). So it was silent for at least 13 hours. The saver runs in the background and throws away its own output and errors (handover.py `log_hook` sends stdout/stderr to DEVNULL), so it fails without leaving any trace.
- **Model switch.** The check reads the plan written in the notes. It does not read the model a chat actually ran on (why-model-switch-failed.md, points 1 and 3). Yet the ledger does record the real model: on 16 Nov Protest Tiers ran 24 chats, 19 on Opus and 5 on Sonnet, costing 39.3% of a week (notes/ledger/protest-tiers.json). Its stage field reads "auto" in every row, so **the record cannot tell which Opus chats were routine work.** That gap is itself a finding.
- **People kit.** Sam said Y on 14 Nov (morning-report.md line 104). The catalogue only changed on 16 Nov (kit-catalogue.md line 44). The kit test failure was seen twice and filed as "not this job's" (facetool-handovers.md lines 372 and 403). So the fault was seen, but nobody owned it.
- **Code finder.** One finder use anywhere in a day silences the warning for every chat (handover.py `finder_faults`). Hand searching cost 9.87% of a week against 0.21% for the finder (finder-use.md).
- **Cost:** this set of failures cost at least ~10% of a week in wasted search, plus Opus spent on routine work (not measured). Sam found every failure himself.

## The real decision
The question is not "warn Sam". It is: **does any system Claude builds prove, from what actually happened, that it did its job, with a named chat responsible for fixing it when it doesn't?** That question covers every chat and every tool. Two levers are bigger than a warning: checking the real record instead of a tool's own report, and making sure every seen fault has an owner.

## Root cause
1. Each system checks itself, or something standing in for the real thing: the notes instead of the actual model, "any call today" instead of each note, catalogue wording that nothing compares with Sam's Y's.
2. Background steps hide their own failures.
3. A fault a chat has seen has no owner across chats.

The model check built on 15 Nov failed for reason 1: it replaced a text-reading guard with another text-reading guard.

## Approaches weighed
1. **Each tool tests itself at start (a heartbeat).** Rejected: the model check would have passed its own test while still missing every case.
2. **An outcome watcher (the reframe).** One list of promises. Each promise is tested against the real record: the ledger's model, the saved messages compared with the chat record, finder calls per note, the kit test result, Sam's Y's compared with the catalogue. A failure goes on a standing "Broken" list.
3. **Learn first.** Replay the last week's record against every system's promise before building anything.
4. **No silent failures.** Every background step writes "ran / failed" to a log, and a missing line is the alarm.

Chosen: 3, then 2. Approach 4 is folded in only if step 1 shows hidden failures matter beyond the message saver.

## Proposal
**Learn (changes nothing, ~1% of a week, Opus high):**
- List every automatic system and check from settings.json, handover.py and the adopted proposals.
- For each one, write its promise and the record that would prove it.
- Replay 10-17 Nov: what failed, for how many days, and at what cost.
- Find out why the saver stopped.

This answers the problem file's own two unchecked questions.

**Change 1, the outcome watcher (~2.5% of a week, Opus high; a few seconds per chat):**
- It runs inside the end-of-reply step that already runs (`ledger.py auto`) and inside `handover.py start`.
- It reads the promises list and tests each promise against the real record.
- A failure is written to a standing Broken list, which stays until a chat fixes it or names it. `handover.py start` lists it as a fault that must be dealt with first; that rule already exists.
- Sam's next message carries one plain line ("Broken: the message saver has not saved since 19:02 yesterday; fixing it first"), plus a push notification.
- **Number to beat:** replayed on last week's record, it must catch all four known failures, each within one chat of it starting, with at most one false alarm a day. This is tested the way kit tests are: the old record is put back and the watcher must flag it.
- To catch the model fault, the ledger must start recording the actual stage. That is part of this change.

**Change 2, after change 1 is shown (asked separately):** the watcher also flags any hook or check that has no promise line. New systems then cannot ship unwatched. Number to beat: zero unlisted systems at each film's end review.

**What Sam would notice:** a "Broken:" line on the day something stops, before he sees the result. He would not have to spot it himself.

## Sam test
- Q1 (Expert): Yes. Check outcomes rather than self-reports, and give every fault an owner. That is standard monitoring practice.
- Q2 (Best result): Yes. The scope is every system across the whole last week, not the three examples.
- Q3 (Comprehensive): Yes. The watcher runs automatically in steps that already run, the root cause is addressed, and "worked" is measured by the replay test.
- Q4 (Most intelligent): Yes. Four different approaches were weighed, and the heartbeat was rejected with evidence.
- Q5 (Risk): Low. The watcher only reports and changes no film. It can be undone by removing one step.
- Q6 (Checked): Yes. Sources are named above; gaps are listed under Unchecked.
- Q7 (Not the cheap version): Yes. It tests outcomes, not the cheap self-test.
- Q8 (Nothing temporary): Yes. It is permanent and reviewed at the film's end.

## Lost / Added
- Lost: nothing.
- Added: one "Broken:" line in Sam's messages when something fails, a few seconds per chat, and ~3.5% of a week once (spread over films, not per film).

## Unchecked
- Why the message saver stopped.
- The watcher's false-alarm rate.
- Both cost estimates.
- Whether other systems failed last week (the learn step will show this).
