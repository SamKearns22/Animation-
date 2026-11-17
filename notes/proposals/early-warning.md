# Proposal: Sam cannot see when a tool or system stops working

Status: open

## Problem
Sam, 17 Nov, word for word: "Is there a way you can have an early warning system when important tools and systems
don't work? Chat switching, the people kit, the code finder are all examples from the last week alone. As you are the
one building these things, I can't see when they fail." Tools and systems that Claude builds stop working, or never
start working, without anyone noticing until Sam spots the result days later. Sam uses only an iPhone and does not
read code, so he cannot see a failure himself.

## Facts
- Chat switching (routine stages on Sonnet): the check (handover.py `model`, built 15 Nov) did not fire on 16 Nov
  although routine chats ran on Opus; causes in notes/proposals/chat-size-and-model/why-model-switch-failed.md
  (word list missed "splice"; reads notes, not the model a chat actually runs on).
- The people kit: Sam said Y to it for films on 14 Nov (notes/morning-report.md line 104, "people kit approved (Y)");
  the catalogue line kept "NOT for films until Sam approves it" until 16 Nov (guides/kit-catalogue.md line 44 now
  reads "APPROVED FOR FILMS by Sam, 16 Nov"; notes/proposals/craft-first-round.md line 45 quotes the old line). A kit
  test failed on it meanwhile (notes/archive/facetool-handovers.md ~line 372: people_from_a_description fails because
  protest_tiers_cast.py imports the kit before approval).
- The code finder: 23 uses on 16 Nov against hand searching ~46 times its cost; its handover flag never fired
  (notes/proposals/finder-use.md Facts).
- Found while writing this (17 Nov): Sam's messages in chat 10ea2689 (07:54-08:07, including the one above) are not in
  notes/ledger/sam/ (the message log hook, handover.py `log`); its last save is 16 Nov 22:17 (git log). `handover.py
  start` said "no saved log" and fell back to the chat record. Why it did not save: unchecked.
- What runs automatically now (.claude/settings.json): at session start setup.sh; on each message costwatch.py and
  handover.py log; after each tool costwatch.py; at each reply's end ledger.py auto and propose.py hook. kittests.py
  ("each shared-kit check tested against the film fault that taught it") runs only when a chat calls it; nothing
  calls it automatically (grep of setup.sh and handover.py).
- Sam is told things only in chat replies and push notifications (CLAUDE.md "Push notifications").
- Unchecked: how many other tools have silently failed or gone unused; how many days each failure lasted before it
  was seen, beyond the three above.

## Record
notes/proposals/chat-size-and-model/
notes/proposals/finder-use.md
notes/proposals/craft-first-round.md
notes/morning-report.md
notes/archive/facetool-handovers.md
notes/logs/
notes/ledger/
.claude/settings.json
.claude/hooks/
source/handover.py
source/kittests.py
guides/kit-catalogue.md

## Verdict (the judge, word for word)
<!-- verdict-hash: 262c9a09553e1fa4 -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper A, V3 = helper B. Picked: V3 (helper B). Critiqued: 6 found, 3 fixed, 3 named.

## Leak
none (the problem file names no solution; its Facts do point at where each failure lives, which is fair evidence, not an answer. One fact in it is wrong: the message saver's last save was 16 Nov 19:02 by git log, not 22:17.)
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 3 | 3 | 3 | 3 | 4 | 16 |
| V2 | 4 | 4 | 3 | 3 | 4 | 18 |
| V3 | 5 | 4 | 4 | 4 | 4 | 21 |
## Sam test
Q1: Yes. Check what actually happened (the real record), not a tool's own report, and give every seen fault an owner: standard monitoring practice. An expert would also want a sign that the watcher itself is alive; that is added from V2.
Q2: Yes. The scope is every automatic system over the whole last week, replayed, not just the three examples Sam named; the learn step answers the problem's own two unchecked questions.
Q3: Mostly yes. It runs inside steps that already run automatically (end of every reply, start of every chat), so no chat has to choose to follow it; the root cause (checks read notes, background steps hide errors, seen faults have no owner) is evidenced; "worked" is measured by replaying last week's four failures. Gap mended: a dead watcher would be silent, so a daily "all held" line is added (from V2).
Q4: Yes. Self-test heartbeat, outcome watcher, learn-first audit, no-silent-steps logging and a status page were weighed across V2 and V3; the heartbeat fails on the model check's own case, the page needs Sam to open it.
Q5: Low. It only reports; it changes no film and holds no reply. Undone by removing one step. Sam is not asked to trust it unseen: it must catch last week's four failures on replay first. Change 2 is a separate ask.
Q6: Checked: 24 Protest Tiers chats on 16 Nov, 19 Opus and 5 Sonnet, 39.3% of a week, stage "auto" in every row (ledger); newest saved message 16 Nov 19:02 (git log); saver discards its errors (handover.py); one finder use a day silences the flag (handover.py); kit test failure seen twice and filed "not this job's" (handover archive, lines 372 and 403). Costs are estimates, marked unchecked.
Q7: Yes. It tests outcomes, not the cheap self-test, and is sized by the replay test (all four caught), not by price.
Q8: Permanent, not a trial; reviewed against the film's results at the end-of-film review.
## Pick
V3
## Why
V3 answers the real decision (does each system prove from the record that it did its job, and who fixes it when not), rests on facts that check out against the ledger, git and code, and finds two things the others missed: the ledger cannot yet tell routine chats from others (stage "auto" in all 24 rows), so a model watcher is blind until that is recorded; and the people-kit fault was seen twice and nobody owned it. Its "number to beat" is a real test (replay last week, catch all four, at most one false alarm a day). V2 is close but holds Sam's replies until a fault is named (a heavier, riskier hook), and its 35.2% figure does not match the ledger (39.3%). V1 builds before learning, has no test that it works, and would check "model matches stage" against a stage that is not recorded. Taken from V2: the daily "N promises checked, all held" line so a dead watcher shows; the kit tests run in the background at session start so their result exists to be read; the aim that no failure is first found by Sam.
## Faults in the pick
- F1 [fixed] A dead watcher would look like "all fine": a daily heartbeat line added (from V2).
- F2 [fixed] V3 reads "the kit test result" but nothing runs the kit tests (7+ minutes): they now run in the background at chat start (from V2).
- F3 [named] Recording each chat's real stage in the ledger is bundled into Change 1; without it the model failure cannot be caught, so it stays in, said plainly.
- F4 [named] Why the message saver stopped is still unknown; the learn step must find it before the watcher is trusted on it.
- F5 [named] Costs (~1% learn, ~2.5% build) and the false-alarm rate are unchecked estimates.
- F6 [fixed] The problem file's "last save 22:17" is wrong; 19:02 is used.
## Final version
**Learn first (changes nothing; Opus high; ~1% of a week, unchecked).** List every automatic system and check (settings.json hooks, handover.py, adopted proposals). For each, write its promise (the real result it must reach) and the record that proves it. Replay 10-17 Nov: what failed, for how long, at what cost. Find why the message saver stopped on 16 Nov 19:02.

**Change 1: the outcome watcher (Opus high; ~2.5% of a week once; seconds per chat).**
- Runs inside the end-of-reply step that already runs and inside the chat-start check.
- Tests each promise against the real record: Sam's messages saved vs the chat record; the model each chat ran on vs its recorded stage; finder use per note, not per day; the kit tests' last result (run in the background at each chat start); Sam's recorded Y's vs the kit catalogue.
- The ledger starts recording each chat's real stage (needed for the model promise).
- A failure goes on a standing Broken list until a chat fixes or names it; the chat-start check lists it as a fault to deal with first, so every seen fault has an owner.
- Sam's next message carries one plain line ("Broken: the message saver has not saved since 19:02 yesterday; fixing it first") and a push.
- Once a day the morning report says "N checks ran, all held"; a missing line means the watcher itself is down.
- **Number to beat:** replayed on last week's record, it flags all four known failures within one chat of their start, at most one false alarm a day; after it is live, no failure is first found by Sam.

**Change 2 (asked separately, only after Change 1 shows results):** any hook or check with no promise is flagged; zero unlisted systems at each film's end review.
## For Sam
### Option 1: A watcher that checks results
First a look back over last week to list every automatic system, what it is meant to achieve, and how long each failure went unseen. Then a watcher, running by itself in every chat, checks each system against what really happened (were your messages saved, did routine work run on the cheaper model, was the code finder used, do the kit tests pass, does the kit list match your yes's). When one fails you get a push and one line: "Broken: ... fixing it first". Once a day a line says all checks held, so you know the watcher itself is alive. It must catch last week's four failures before it goes live.
Lost: nothing in the films; about 3.5% of a week once.
Added: a "Broken:" line and push when something fails; a daily "all held" line.
### Option 2: A start-and-end health check
A short list of live tests runs at each chat's start and end and puts any failure in your next message with a push, plus a weekly summary. Quicker to build, but built before checking which systems matter, with no test that it would have caught last week's failures, and the cheaper-model check would have nothing reliable to read.
Lost: nothing in the films; about 2% of a week once.
Added: a "Broken:" line and push at chat start or end; a weekly summary.
