# Proposal: Chats hunt by hand instead of using the code finder

Status: open

## Problem
When a chat fixes one of Sam's notes it is meant to look at the code first with the code finder (one step, ~40
lines). In practice chats still hunt by hand (search, ranged reads of the film's files and of shared tools), and each
hunt's result is re-read at every later step of a long chat. On 16 Nov, the first full day after the finder's first
improvement was adopted, hand searching cost about 46 times what the finder did, and the check meant to show this said
nothing. The finder also only covers the film's own code files, not the shared tools a fix often touches.

## Facts
- 16 Nov, 19 Opus Protest Tiers chats, 35.2% of a week, all after the finder went on (ledger step kinds,
  notes/proposals/chat-size-and-model/sam.md last lines): hand search of the film's files 6.65% of a week, of shared
  tools 3.22%, the finder 0.21%. The finder log (notes/logs/protest-tiers-show.log) holds 23 calls, all 16 Nov.
- The finder (source/page.py `show`) reads only source/FILM*.py (page.py MAP, build()). Shared tools (moves.py,
  checks, kit files such as people.py) are not on it.
- Adopted 16 Nov (notes/proposals/code-finder.md, Final version): change 1 (--shot/--at, a log line per call, a
  handover flag) built; change 2 (tables and constants on the page; lines holding the note's words first) to be asked
  "only after it is shown"; the real bar is at the next film's review: 80% of held-out notes answered by the first
  show, hand searches under 15% of round-chat steps.
- The handover flag (source/handover.py lines ~408-426) fires only when the film's code changed today and NO show call
  was logged today; one call anywhere that day silences it for every chat. It never fired on 16 Nov
  (notes/logs/handover-end.log has no FINDER line).
- Before the finder improvement (notes/proposals/learn/search-cost.md): 7 round chats, 169 of 564 steps (30%) were hand
  searches, estimated 7-30% of a round chat's cost; finder replay hit 50% strict / 69% loose on 26 Blessed notes.
- `handover.py start` prints the per-note reminder "look at the code with ONE step: page.py FILM show ... never grep
  or sed a film file first" (seen at this chat's start).
- Unchecked: the finder's hit rate after change 1 on real 16 Nov notes; how many of the 16 Nov hand searches came
  after a show call that missed versus with no show call at all; which shared tools were searched most.

## Record
notes/proposals/code-finder.md
notes/proposals/learn/search-cost.md
notes/proposals/chat-size-and-model/sam.md
notes/logs/protest-tiers-show.log
notes/logs/handover-end.log
notes/ledger/protest-tiers.json
source/page.py
source/handover.py
source/stepcost.py
guides/kit-catalogue.md

## Verdict (the judge, word for word)
<!-- verdict-hash: 681f94b84aa0e90a -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper B, V3 = helper A. Picked: V2 (helper B). Critiqued: 6 found, 2 fixed, 4 named.

## Leak
yes: mild. "The finder also only covers the film's own code files, not the shared tools" points at extending the finder, and "one call anywhere that day silences it for every chat" points at a per-chat flag. No fix is stated outright.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 2 | 2 | 2 | 2 | 3 | 11 |
| V2 | 4 | 4 | 4 | 4 | 5 | 21 |
| V3 | 4 | 3 | 4 | 4 | 5 | 20 |
## Sam test
Q1: Yes. An expert would first measure where the search cost goes, then check at the moment a chat searches, not at the end of the day. A warning, not a block, because searches made while building are legitimate.
Q2: Scope is every chat in the film's round days, split by purpose, with a count per note. That is the right evidence. The 16 Nov day alone cannot say whether the gap comes from skipping the finder or from building.
Q3: The root causes have evidence: the check runs once a day, so it never fires (first show call 09:15). 6 of 19 Opus chats never called the finder. The measure mixes different purposes. Both the measure and the warning run automatically in every chat. A chat can still call show once and then search by hand. The split catches that afterwards; nothing blocks it (named).
Q4: Five different approaches were weighed: per-chat warning, capping result size, splitting the film's files, extending the finder to shared tools, and measuring first. The ones without a number behind them wait for one.
Q5: The warning only warns and never blocks. Each part has its own yes and can be removed alone. Sam is asked to trust nothing that has not been shown, except the per-chat warning, which rests on a correlation (named).
Q6: The ledger figures were re-added (19 chats, 35.18%, 484 + 407 searches against 21 finder calls, 6 chats with no finder call, 26.5% against 15.5%). The facts about the per-day flag and the end log were checked in the code. Savings and the 16 Nov hit rate are marked unchecked.
Q7: It finishes the adopted per-note check rather than a cheap day flag. Bigger fixes (layout, result size, shared tools) each have a trigger number, so it is sized by the result, not trimmed.
Q8: Measure and warning are permanent and reviewed at the film's completion; nothing is called a trial.
## Pick
V2
## Why
V2 checks its facts best. It found that the finder's change 2 is already built and on by default (page.py line 352, Sam's yes 16 Nov). V1 proposes building it "now", and V3 calls it "unbuilt" and keeps a branch that leads to it, so both rest on a wrong fact. V2 found that the end log stores no faults, so "never fired" cannot be read from it, and that the "film-file" and "tool search" kinds mislabel what they count. Unlike V3, it acts on the evidence already in: the per-chat warning finishes the adopted spec, which was built short, and 6 of 19 chats skipped the finder. V1 bundles three builds into one yes, before any measure, and one of them is already built.
Taken from V3: a count of notes ticked per chat (the ledger's `notes`/`round` are empty in every row, so V2's per-note bar could not be measured without it); a "miss" window (hand searches within 10 calls after a show); the point that a hand search and a finder call cost about the same per call (0.014% against 0.010%), so the bar is searches per note, not a ratio.
## Faults in the pick
- F1 [fixed] V2's bar "under 1 pre-show film-code search per note" needed a notes count the ledger never records; the count of notes ticked per chat is added.
- F2 [fixed] "46 times" counts uses, not price; the bar is per note, not hand-searches against finder calls.
- F3 [named] The warning goes in on a correlation: the 6 chats that skipped the finder spent 26.5% on film search, against 15.5% for the others. Some may have been build chats. It only warns, and the split will show it.
- F4 [named] A chat can call show once and then search by hand freely. This is measured (after-show and miss splits), not blocked.
- F5 [named] Whether change 2 was on during the 16 Nov chats is unchecked, so the first measured round, not 16 Nov, is the baseline.
- F6 [named] The saving (about 2-3% of a week per round day) is an estimate.
## Final version
**Learn (own yes, about 0.5-0.6% of a week, no film change).** stepcost, run by the Stop hook on every chat, adds to each ledger row:
- the notes ticked by that chat ("[x]" lines its commits add to the film's notes);
- film-code searches split into: before the chat's first show / within 10 calls after a show (a miss) / later after a show / in a chat with no show;
- other searches split by target: shared code (named per file) / film notes / guides and rules / other. ls stops counting as a search.

The finder log gains the chat id. These are read at the next film's first notes round. They answer: the "locate" share of round cost, the finder's miss rate on real notes, and which shared tools are searched.

**Change 1 (own yes, about 0.5%): the adopted per-note check, made per chat.** A hook prints one line at a chat's first film-code search when that chat has no show call yet. It warns and never blocks. `handover.py end` lists each chat that edited film code with no show, with its count of searches before any show. This replaces the per-day flag.
Bar: no Opus round chat edits film code without a show; under 1 search per ticked note before the first show; hand searching under 15% of round-chat cost (28% on 16 Nov, measured).

**Later changes (each its own yes, only if Learn's numbers call for it):**
- the finder covers shared tools, if shared-code locate searches reach 3% or more of round cost;
- a cap on result size, if search results average over 1,500 tokens;
- rule 61's file split as a gate for new films, if search cost per note rises with file size over two films.

Each change has its own bar and is undone alone.

**Cost:** about 1% of a week once, against 9.87% spent searching in one day. The saving is estimated, not checked.
**Sam notices:** nothing in the films; one line of results at the film's review.
## For Sam
### Option 1: Measure, and nudge each chat
On the busiest day of note fixes, chats spent more than a quarter of their cost searching the code by hand. A third of them never used the quick code look-up. The warning meant to catch this checked once a day, so it never went off. This makes every chat record what it searched for and why, and how many notes it fixed. Separately, a chat that starts searching by hand without the look-up gets a one-line reminder at that moment. Bigger fixes wait until the numbers show they matter.
Lost: the once-a-day warning that never fired.
Added: a per-chat search record, a one-line reminder at the moment of searching, and a per-chat line in the end-of-chat check.
### Option 2: Measure first, then one fix
The same record of what each chat searched and how many notes it fixed. Nothing else changes until the next film's first round of notes is measured. Then the one fix the numbers point to comes to you for a yes. It is slower to help, but nothing is added before it is shown to matter.
Lost: a round of notes at today's search cost before any fix.
Added: a per-chat search record, and later one fix chosen by its numbers.
