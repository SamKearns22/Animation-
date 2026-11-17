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
