# Helper A: early warning

## Leak
None.

## Results
- **Four silent failures in about 3 days**, none found by the system:
  - **People kit:** Sam: Y, 14 Nov (morning-report.md line 104), but the catalogue said "NOT for films" until 16 Nov (kit-catalogue.md line 44), 2 days; its kit test failed meanwhile (facetool-handovers.md line 372).
  - **Model check:** silent while 19 Opus chats cost 35.2% of a week on 16 Nov (protest-tiers.json).
  - **Finder flag:** never fired (problem file).
  - **Message saver:** the newest saved message is from 16 Nov 19:02 (notes/ledger/sam). Its errors are thrown away (handover.py `log_hook`).
- **Already measured:** the ledger records each chat's real model and step costs at every reply end.
- **Kit tests:** 91, over 7 minutes per full run (17 Nov); never run automatically.
- **A hold exists:** a reply-end hook can hold a reply (propose.py `hook`).
- **Gap:** how many other tools fail silently, how long.

## The real decision
Tools are judged by being built, not by working. The decision: how the system proves daily that each tool does its job, and tells Sam plainly when one fails.

## Root cause
1. **Checks read what chats wrote, not what happened.** The model check reads the notes' Next line, not the model a chat actually ran on (why-model-switch-failed.md).
2. **Silence means both "fine" and "broken".** No check reports what it saw; background errors are discarded; kittests waits to be called.
3. **No tool states the result it must reach,** so a finder nobody used counted as fine.

## Approaches weighed
1. **Run kittests at every start.** Misses the model and finder failures (no errors).
2. **Promises watch.** One line per tool: the real result it promises, where it is measured, the limit. A script run by the reply-end hook checks them.
3. **Reframe: a build gate.** No tool counts as finished until its promise is written and it has fired once on the case that taught it.
4. **Learn first: an audit** of every tool since 1 Nov: did its result happen, and how many days passed before a failure was seen?
5. **A status page.** Sam must open it. Rejected.

Chosen: 4, then 2, then 3, asked separately.

## Proposal
- **Learn first (changes nothing).** One Opus high chat audits every tool against git, ledgers and logs: its promise, whether it held, and how long failures went unseen. About 3% of a week (unchecked).
- **Change 1: the watch.** `source/watch.py` checks the audit's promises against the real records. Examples:
  - Sam's messages are saved within the chat.
  - Routine stages ran on Sonnet, according to the ledger.
  - Hand search is under 15% of a round chat's steps.
  - The kit tests passed within the last day (run in the background at session start).

  A broken promise holds the reply (reply-end hook) until it carries a plain "Checks:" line; a push is sent. The morning report states "N promises checked, all held"; a missing line means a dead watch.
  - **To beat:** failures are now seen 1-2 days late. Every failure must be flagged by the next reply's end, and none first found by Sam at the next film's review.
  - **Cost:** about 4% of a week, once.
- **Change 2: the build gate**, asked only after change 1 shows results. `handover.py end` refuses a new tool lacking a promise or a recorded firing.
  - **To beat:** every tool built in the next film has both (checked against git at the review).
  - **Cost:** about 0.2% of a week per tool.
- **Totals:** under 1% of a week per film to run, against the 15% limit; the one-offs come to about 7%, once.
- **What Sam notices:** silence while all works; when something breaks, a push and one line: "Checks: messages not saved since 19:02 yesterday – fixing."

## Sam test
- Q1: Checks real outcomes, as experts do.
- Q2: Every tool, sized by the audit.
- Q3: Reads records, not notes; a hook enforces it; a heartbeat shows if the watch dies.
- Q4: Five approaches weighed; only this catches a tool that runs but does the wrong thing.
- Q5: One change at a time, each removable; the audit changes nothing.
- Q6: Sources named; estimates marked unchecked.
- Q7: Kit tests alone (the cheap version) miss 2 of 4 failures.
- Q8: Permanent, reviewed at the film's end.

## Lost / Added
- **Lost:** a reply is held until a broken tool is named in it.
- **Added:** the audit, the watch and its promises, a morning-report line; later, a promise per new tool.

## Unchecked
- Why the message saver stopped (shallow history).
- The audit's cost; how many promises existing records can measure; how to tell routine stages apart in the ledger.
