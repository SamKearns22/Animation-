# Proposal: Sam sees a message twice when the proposal checker blocks after sending

Status: open (23 Nov: its Learn and the guard's Change 1 built by guard-film-questions; its Change 3 = that proposal's Change 2; the watcher part not yet asked: Sam's hold, 23 Nov)

## Problem
When the proposal checker (the Stop hook in source/propose.py) decides a reply asks Sam to approve an unjudged change,
it blocks only after Sam has already seen the reply. The chat must then write again, so Sam gets the same message
twice (or a near copy). Sam, 22 Nov: "You keep sending me messages twice." Some blocks were also on questions that
were not change approvals (a question about what Sam meant; a question whether to start the route itself), so each
false block costs Sam a duplicate message and the chat extra steps.

## Facts
- The checker runs as a Stop hook: after the reply is written and shown (.claude/settings.json, "Stop"; propose.py hook()).
- On a block the chat must answer again; on a second fault it lets the reply through and logs it
  (notes/proposals/unrouted.md): 43 such lines, 15-22 Nov (counted). Blocks that were fixed on the first resend are
  not logged anywhere (unchecked how many).
- This chat (session 56d8e5c4, 22 Nov): blocked twice. Once on "did you mean every film or a normal-size film"
  (a question about Sam's own request), once on "should I start the suggest-and-judge process on way 1" (a question
  about running the route, not approving a change). Both resent; Sam noticed the doubles.
- Sam's rule added 22 Nov (CLAUDE.md, Messages to me): after a block, resend only the changed line.
- reply_faults(reply, touched) already exists as a plain function (propose.py ~line 391); only hook() calls it.
- Statement One (CLAUDE.md top): quality within 15% of a week; cost down by catching faults before Sam sees them.

## Record
source/propose.py
.claude/settings.json
notes/proposals/unrouted.md
CLAUDE.md
guides/proposal-route/

## Verdict (the judge, word for word)
<!-- verdict-hash: a2589ec4b210f41e -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper A, V3 = helper B. Picked: V2 (helper A). Critiqued: 6 found, 3 fixed, 3 named.

## Leak
yes: the problem's name ("precheck-reply") and the fact "reply_faults already exists as a plain function; only hook() calls it" point straight at one answer, a check the chat runs on its draft before sending. V1 is that answer; V2 and V3 both named the leak and looked past it.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 2 | 2 | 3 | 3 | 5 | 15 |
| V2 | 4 | 4 | 4 | 4 | 5 | 21 |
| V3 | 3 | 3 | 2 | 3 | 4 | 15 |
## Sam test
Q1: Yes. An expert stops the repeat at its source (what every block makes the chat send, and what the guard re-reads on the retry), measures every block, and only then adds steps; a precheck that depends on each chat remembering it is the weaker tool.
Q2: Yes once widened: all three after-the-reply checks (proposal guard, watcher, ledger) across every chat, from the whole block log and the chats' records, not this chat's two blocks.
Q3: Root cause checked here: the guard runs after Sam has read the reply, its block text says "put it through the route ... or reword", and on the retry it re-reads the first copy (the block note is stored as a hidden message, not Sam's), so a withdrawn question is blocked again and always logged. All fixes live in the hooks and kit tests, not in a chat choosing to obey; the full block log shows whether repeats reached 0.
Q4: Yes: precheck, one-line corrections, fixing the guard's sorting, guarding the action instead of the words, learn-first, removing the guard were all weighed across V2 and V3.
Q5: Each change is one hook edit with its own kit test, undone alone; the guard still stops every real unjudged ask. Only Change 2 (watcher) is a new yes; the rest is Sam's 22 Nov adoption, built.
Q6: Checked: 43 log lines 15-22 Nov; this chat's 3 blocks (23:17, 23:19, 23:21) are all in the log; block text at propose.py ~414; retry re-reads the first copy (chat record: block note is a hidden message); guard-film-questions adopted 22 Nov 23:01 (git 10437bef) and not built; Sam's note in notes/ledger/sam/kpp1tyq4.md. Labels of the 43 and all costs remain unchecked.
Q7: Sized to zero repeated replies from any hook and zero missed real asks, not to a rule line; honest cost about 1.4% of a week once.
Q8: Permanent, no trial; reviewed at the end of the next film against the full block log.
## Pick
V2
## Why
V2 sees that this problem was already judged and adopted on 22 Nov (guard-film-questions) and never built, so the right move is to build it, extend its one-line rule to the watcher, and keep the precheck until numbers ask for it. V1 is the leaked answer: it relies on each chat remembering to run a check, and loosens the guard by hand without a labelled test list. V3 finds the same causes but re-proposes the adopted plan as new work at three times the cost, and says only 2 of this chat's 3 blocks were logged (all 3 are). Fixed in V2 from my own check: its one-line correction cannot work alone, because the guard re-reads the blocked first copy on the retry; the guard must judge only what was written after its block. Taken from V3: for a missing "Critiqued:" line, the block prints the exact line to paste; the resend starts "Correction:".
## Faults in the pick
- F1 [fixed] On the retry the guard re-reads the first copy, so "withdrawn" or a corrected line is blocked again and logged as a let-through; it now judges only the text after its own block.
- F2 [fixed] V2 said propose.py last changed in d54ffbba; it changed on 23 Nov (5ed46270), making every let-through stop the handover and the animatic until settled. A block cleared by its one-line retry is now logged as cleared, not as a let-through.
- F3 [fixed] "Blocks fixed on the first resend are not logged" holds only for missing-line faults; unjudged-ask blocks are always logged today.
- F4 [named] The sorting of the 43 lines is rough until the Learn step reads each full reply.
- F5 [named] An after-the-reply check cannot hold a reply back; one short correction line per true catch remains (unchecked whether Claude Code offers a check before the text shows).
- F6 [named] Change 2 moves the watcher's daily line to the next reply.
## Final version
Learn (adopted 22 Nov; changes nothing, about 0.4% of a week): every block from the proposal guard and the watcher is logged, first time included, with hook, whole reply and retry length. The 43 logged lines plus new ones are labelled from the chats' records (film question, ask to start the route, Critiqued wording, path misread, real unjudged ask) into a fixed kit-test list.

Change 1 (adopted; build it, about 0.4%): the guard's block says "Sam has already read this reply. Send only one line starting 'Correction:': the missing line, or 'ignore question N, it is withdrawn'." For a missing Critiqued line it prints the exact line. On the retry the guard judges only the text after its block; a correct one-liner passes and is logged as cleared, not as a let-through, so it does not stop the handover or animatic. Kit test checks both. To beat: full repeated replies per film to 0.

Change 2 (new, its own yes, about 0.1%): the watcher's block says the same, and its once-a-day line goes into the next reply instead of forcing a resend. To beat: watcher repeats to 0.

Change 3 (adopted, after Learn, about 0.5%): retune the guard on the labelled list. To beat: 0 wrong stops, 0 real asks missed.

Change 4 (only if the log still shows more than one block per film after 1-3; its own route run): the draft precheck.

Total about 1.4% of a week once. Reviewed at the end of the next film.
## For Sam
### Option 1: Build the fix you already chose, and make it work
You chose on 22 Nov that a stopped reply gets only a one-line correction, but it was never built, and the checker also re-read the first message, so even a one-liner was stopped again. This builds it properly, does the same for the other checker that asks for a daily line, and logs every stop so the checker is retuned on real messages.
Lost: the daily "Watcher" line arrives in the next reply, not the stopped one.
Added: no repeated messages; at most one "Correction:" line when an ask really wasn't judged.
### Option 2: Check each reply before sending
Before a reply with a question, the chat runs the checker on its draft and fixes it first. Quicker to add, but it only works when a chat remembers to do it, and the wrong stops stay.
Lost: nothing you see.
Added: one extra step per reply with a question.
