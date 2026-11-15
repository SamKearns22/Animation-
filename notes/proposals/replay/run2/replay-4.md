# Proposal: find out which rules and tools work

Status: open (replay case 4)

## Problem
Sam: "This then is a systemic issue that could apply to every rule, test, kit and process ever written into the
project." We do not know which of the project's rules and tools are followed, or which of them actually help (fewer
notes, fewer faults reaching Sam, lower cost). Decide how to find out, and what to do with what is found.

## Facts
- About 64 rules (guides/film-quality-rules.md plus CLAUDE.md) and about 115 tools and kits (guides/kit-catalogue.md);
  counts unchecked.
- Only a few act on their own, as hooks in .claude/settings.json: the cost watch, the handover log and the ledger
  (check the file); others (pre-flight, checks) run only when a chat runs them.
- The notes-round section of guides/job-packs.md already tells a chat to use page.py; chats 29 and 31 still ran it 0
  times and searched code by hand 25 and 26 times (record: tool-use file).
- Earlier failures named in this chat: cost stops fed chats' own cost figures that were 20-75% too low; the critic
  found 8 faults in a "pillar" rule only after Sam asked for a critique.
- Protest Tiers' ledger holds every chat's real cost; its notes file holds Sam's notes; the handover check can read a
  chat's own record for free (source/handover.py).
- Sam's own messages so far are in the record.

## Record
notes/proposals/replay-record/sam-to-case4.md
notes/proposals/replay-record/tool-use-29-31.md
notes/proposals/replay-record/bills-29-31.md
notes/ledger/protest-tiers.md
notes/protest-tiers.md
CLAUDE.md
guides/film-quality-rules.md
guides/kit-catalogue.md
guides/job-packs.md
source/handover.py
source/ledger.py
.claude/settings.json

## Verdict (the judge, word for word)
<!-- verdict-hash: ecfa03c4596255e2 -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper B, V3 = helper A. Picked: V3 (helper A). Critiqued: 6 found, 3 fixed, 3 named.

## Leak
yes: mild. The Facts list says the ledger holds every chat's real cost, the notes file holds Sam's notes and "the handover check can read a chat's own record for free (source/handover.py)". That points toward measuring from the chats' own records automatically, which is the answer V2 and V3 both reach. It does not name a remedy, so all three versions could still have gone elsewhere (V1 did).
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 2 | 2 | 2 | 2 | 4 | 12 |
| V2 | 4 | 4 | 4 | 4 | 5 | 21 |
| V3 | 5 | 4 | 4 | 4 | 5 | 22 |
## Sam test
Q1: Yes. An expert in agent workflows would measure results before pruning or adding, record them automatically, and enforce with code rather than text. That is the shape of V3.
Q2: Whole chats of the three most recent films (Remakes 19, Blessed 24, Protest Tiers 32: 75 chats; ledger counts checked). This is wider than Sam's "last two films" and is chosen by results, not by which chats were cheapest or dearest.
Q3: Root cause named with evidence: the page.py tool was ignored even though the pack requires it; the notes column is filled only by a manual command, so the ledger reads 0 notes for all 75 chats; the cost stops trusted self-reported figures. The meter runs in the Stop hook that already exists, so no chat has to choose it. Each change has a number to beat. Weak spot: the trace starts from bad results, so a rule that is followed but useless only shows up through the meter over three films (named, F3).
Q4: Four approaches were weighed (sweep, learn from the record, self-measuring film, enforce). The sweep was rejected for a stated reason: it judges paper, not results.
Q5: The learning pass changes nothing. Change 1 only writes ledger rows and can be undone alone. Each later change gets its own yes. Risk left: the automatic note count may miscount (F2), so its number to beat is a hand count.
Q6: Mostly checked: 54 numbered rule rows plus 14 P-rule mentions, 124 catalogue table rows, the ledger figures, the hook list, page.py 0 runs against 25 and 26 hand searches, and the model-column error (chats 27, 30 and 31 are titled Opus but logged "sonnet"). The learning pass's cost is marked unchecked.
Q7: Sized by the result: every chat of three films plus a permanent meter, not a sample. The cost is stated honestly (3-5% plus 1-2%, unchecked).
Q8: The meter is permanent. No trials. Each change is reviewed when Sam declares the film complete.
## Pick
V3
## Why
V2 and V3 reach the same correct decision: learn from the results first (changing nothing), make the ledger record notes and tool use on its own, then make one change per yes. V3 wins on evidence. It covers all three recent films rather than two, it finds a second ledger fault (the wrong model column), and its rule count is right (54 numbered rows; V2's "65" does not match a grep). From V2 I took the per-stage money breakdown (moves and round-1 moves cost about five times their plan), as a likely top row for the trace, and the instruction that the trace also covers stages that ran over plan, not only Sam's notes. V1 is a paper sweep of every rule. It rests on wrong facts: it says pre-flight and the handover check act on their own (only setup, the cost watch, the handover log and the ledger do), and it says 29 chats where the ledger shows 32. It asks one yes for a removal-heavy audit at an unchecked 8-12%.
## Faults in the pick
- F1 [fixed] The learning pass and Change 1 could have been read as one yes. They are now two numbered questions.
- F2 [named] Counting "Sam's notes" automatically from a transcript can miscount (a question, a "Y", a list of notes). Change 1's number to beat is an exact match with the film's notes file. If it fails to match, it is fixed or not adopted.
- F3 [named] The trace starts from bad results, so it cannot show a rule that is followed but changes nothing. The meter's run counts over three films cover that, so removals come later, not from this pass.
- F4 [fixed] The trace now covers stages over plan as well as notes (from V2).
- F5 [named] Whether every older chat record can still be read is unchecked. Any chat that cannot be read is listed, never guessed.
- F6 [fixed] The ledger's model column fix is folded into Change 1, because it is the same automatic row.
## Final version
**Step 1, learn (changes nothing).** Read-only Sonnet helpers go through every chat of Remakes, Blessed and Protest Tiers (75 chats) and their notes files. A script counts which tool ran in each chat and how many times code was searched by hand. The helpers write one table. Each row is one of Sam's notes, a stage that ran over plan, or a fault that reached Sam. For each row: its cost, the rule or check that should have caught it, and whether that rule ran and missed, never ran, or does not exist. A second table gives each tool's runs and cost per film. Sam gets the top 5 causes of notes and cost in plain English. Any unreadable chat is listed. Cost about 3-5% of a week (unchecked), filed as project work.

**Step 2, the ledger fills its own row (separate yes).** The Stop hook that already runs after every reply records, from the chat's own record: Sam's notes, repeated notes, checks run, named tools run against hand searches, and the model that actually ran. Numbers to beat: on chats 29 and 31 it must give 0 page.py runs and 25/26 hand searches; on Protest Tiers it must match the notes file exactly. About 1-2%.

**Step 3 onward, one per yes.** Each change targets a top row of the table (likely: the moves stages at about five times plan, and hand code searches). Each is enforced by a hook or a pre-flight refusal, not by text, and carries its own number. Each is reviewed when Sam declares the film complete. A rule or tool that the ledger shows caught nothing over three films is offered for removal on its own "Lost:" line.
## For Sam
### Option 1: Learn from the last three films, then let the films measure themselves
Helpers read every chat of your last three films and trace each of your notes, and each stage that ran over budget, back to the rule or tool that should have stopped it. You get the top 5 causes in plain words. Separately, the cost record starts writing down your notes and which tools were really used, by itself, after every reply. Every later fix is judged on real numbers, one yes at a time.
Lost: nothing now. Any later removal comes on its own line.
Added: one read-only study (about 3-5% of a week) and a cost record that counts notes and tool use on its own (about 1-2%).
### Option 2: Same study, two films only
The same tracing over Protest Tiers and Remakes only, plus the same self-filling record. It is a little cheaper, but it leaves out Blessed's 24 chats, so it gives fewer examples to show which rules matter.
Lost: Blessed's evidence (24 chats, its two rounds of notes).
Added: the same study on two films, and the same self-filling record.
