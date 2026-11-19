# Proposal: How the unfinished Learn step of finder-first gets finished

Status: open

## Problem
Sam adopted "finder-first" (18 Nov): first learn what Milburn's 779 hand searches were for, then fix one cause at a
time. The learning part is unfinished. To say what each search was for (steps 1-3), the chats' own transcripts are
needed; only a chat's step-by-step record, read through a tool, is left, and it is costly to read (about 10,000
tokens per 6 steps; the 15 Milburn chats hold about 1,300 steps). Without it the ledger gives counts per file but not
the purpose of each search, and not whether the 17 Nov reminder was shown. The question is how to get the measured
result, or whether to go on without it.

## Facts
- notes/proposals/finder-first/learn.md: step 4 (record each search's file and pattern on the ledger) done and pushed;
  steps 1-3 not done; transcripts of the 15 chats gone; reading all inline is "well over a million tokens".
- notes/ledger/milburn.json: searching $8.04 of $32.14 (25%, about 5.4% of a week, estimate); 779 searches, 248 on
  the film's code, 531 elsewhere (328 shared tools, 101 other, 81 notes, 21 guides); finder used 12 times.
- notes/proposals/finder-first.md: plan allowed about 1.5% of a week for the Learn step.
- Sam, 19 Nov: said Yes to queuing the finish as its own chat.
- A code-finder test (round_page) fails since 15 Nov and one head check since 14 Nov (see notes/proposals/finder-first/).
- Unchecked: the real cost of reading with several small chats at once; whether purposes can be told from the search
  text alone, without reading the chat around it.

## Record
notes/proposals/finder-first/learn.md
notes/proposals/finder-first.md
notes/ledger/milburn.json
source/stepcost.py
source/page.py
