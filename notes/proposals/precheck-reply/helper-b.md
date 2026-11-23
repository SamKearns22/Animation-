# Helper B: precheck-reply

## Leak
The name "precheck-reply" and the fact "reply_faults already exists; only hook() calls it" point to "check before sending"; ignored. I also opened chat.md by mistake while listing the folder; the answer below comes from the record.

## Results
- A Stop hook runs after the reply has been streamed to Sam (.claude/settings.json "Stop"; propose.py hook). So **every block, right or wrong, is a second message Sam sees**. No hook can run before the text is shown, so being honest, nothing can make a block invisible.
- unrouted.md: 43 lines, 15-22 Nov. These are only the blocks where the resend *also* failed; blocks fixed on the first resend are logged nowhere. This chat had 3 blocks in 4 minutes (23:17, 23:19, 23:21, from the chat's own record); only 2 are in unrouted.md. So the record **under-counts duplicates**, and the real number is unknown (a gap).
- My reading of the 43 lines (rough sorting, done by me alone, not checked by anyone else):
  - ~22 were not change approvals: starting or scoping the route (e.g. "may I put a fix through the proposal route", "Run the proposal route only for cause 1"); asking what Sam meant ("was the file called Report…", "15% every film?"); film decisions ("Close the props stage", "shot 4's camera back", "lower the effects", "Hook Text options", "keep spending on round 2").
  - 11 were real proposals with a verdict whose reply lacked the exact "Critiqued: N found…" line. brow-limit failed this twice in two minutes (22:40, 22:41).
  - 3 were the tool's own misreading: a path in the reply that names no proposal ("2.md", "failing-checks.md", "one-route-kit-brief.md").
  - About 6-8 were real unjudged change asks.
- Sam's note, 22 Nov 23:18: "You keep sending me messages twice" (notes/ledger/sam/kpp1tyq4.md). Sam's rule (CLAUDE.md line 54): after a block, resend only the changed line. The block's own wording (propose.py line 485) does not say this.

## The real decision
This is not about one chat or a pre-send command. It is about how the proposal guard (the check that stops an unjudged change being put to Sam) works across every chat so that it costs Sam no duplicate messages. It has three bigger levers: how often it wrongly blocks, how often a right block can't be fixed in one go, and what a block makes the chat send.

## Root cause
1. Timing: a check that runs after sending can only catch a fault by producing a second message.
2. The word test (CHANGE_RE matches "process", "rule", "tool", "proposal route"; "Need:" + Y/N counts as an ask) treats any question *about* the route, or any film question near those words, as a change approval. That is about half the logged double-failures. A resend can't fix a false block, so it fails again.
3. The Critiqued line has to be copied by hand, word for word. The chats keep getting it slightly wrong even after being told.
4. When it blocks, the message tells the chat what was wrong but not that Sam has already read the reply, so the chat sends the whole message again.

## Approaches weighed
1. **Check before sending** (the chat writes a draft, runs the check, then sends). This depends on each chat remembering to do it, and the false blocks would stay: the chat would just reword innocent questions to get past it.
2. **Reframe: guard the action, not the wording.** Never block a reply Sam has seen. If Sam answers Y to a change ask that was not judged, the next turn is stopped from acting on it. This removes every duplicate, but unjudged asks reach Sam, which is exactly what the route exists to stop.
3. **Make the check right.** Use the labelled record to stop the false blocks and fix the misread names. This happens inside the hook, so it works in every chat.
4. **Make the unavoidable block cheap.** The block tells the chat "Sam has read this; send only the corrected line", and gives the exact Critiqued line to paste.
5. **Learn first:** count and sort every block, not just the double failures.

Chosen: 5, then 3, then 4, one at a time. 1 waits for its numbers. 2 is turned down because it weakens the guard.

## Proposal
- **Learn (changes nothing):** sort every block from 15-22 Nov into right / wrong / Critiqued-line / misread. Sources: the 43 lines, plus each chat's stop-hook records found with list_events. The output is a fixed, labelled test set and the real count of duplicates per film. About 1% of a week (estimate).
- **Change 1, count every block:** one line per block in the same log, marked first or second. Enforced in the hook. Number: this makes the baseline measurable from now on. About 0.5%.
- **Change 2, fix the check:** questions about meaning, about starting or scoping the route, and film decisions pass. So does a proposal name the reply doesn't ask about, and a path that is not a proposal. Enforced in the hook. Number to beat: on the test set, zero wrong blocks and every right block still caught. Live, wrong blocks per film go to 0. About 1.5-2%.
- **Change 3, the block message:** tell the chat Sam has already seen the reply. The resend starts "Correction:" and is that one line only, and for a Critiqued fault the hook prints the exact line to paste. Enforced by the second check: a resend over about 3 lines is logged as a fault. Number: double failures (from 43 in 8 days) to 0, and every resend to one line. About 1%.
- **Then, only if right blocks are still more than about one per film:** a pre-send check command, as its own proposal.
- Total about 4-4.5% of a week, once, not per film, against 15% per film. What Sam would notice: no more questions repeated because of the checker, and at most a one-line "Correction:" when one of his asks really was unjudged.

## Sam test
Q1: Yes. An expert measures the false-block rate before adding steps, and fixes the check, not the chat's habits.
Q2: The scope is every chat's blocks since the guard began, not one chat's two.
Q3: Changes 1-3 live in the hook, so they don't rely on a chat choosing to follow them. Each has a number, and the test set stops it working only on paper.
Q4: Five different approaches were weighed. Approach 2 was turned down for risk, with the reason given.
Q5: Each change can be undone on its own. The guard still blocks every real unjudged ask (the test set shows it).
Q6: Each source is named. My sorting and the costs are marked unchecked.
Q7: Not the cheap option: the learning step comes first and each part is built properly, rather than a single line added to the rules.
Q8: Permanent changes, reviewed against the film's results.

## Lost / Added
Lost: nothing Sam sees. Wrong blocks on route and film questions stop.
Added: one log line per block, and a one-line "Correction:" in place of a repeated message.

## Unchecked
My sorting of the 43 lines. Whether list_events shows earlier chats' blocks. All the costs. Why the Critiqued resends failed.
