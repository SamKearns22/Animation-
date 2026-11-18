# finder-first: Learn result (18 Nov) — PARTIAL, stopped on one question

## Done
- Step 4 (permanent): `source/stepcost.py` now writes every search's file and pattern on the ledger row
  (`search.list`: call number, film/other, target, file, pattern). Its tests pass (`stepcost.py test`). Every
  film from the next chat on reports the split at its review with no labelling chat. Nothing else in the films changed.
- Push to GitHub works (branch `claude/learn-finder-first`, and the main line).

## Not done, and why (steps 1-3)
The 15 Milburn chats' transcript files are not in this container (only this chat's). The only route is `list_events`.
Measured on the smallest Milburn chat: 6 steps cost about 10,000 tokens of reading (every step carries the
chat's hidden thinking and its tool input twice). The 15 chats hold about 1,300 steps, so reading them all in this chat
would be well over a million tokens, far past the ~1.5% of a week the plan allowed and past the cost watch. The
purpose labels (step 1), the 60-search replay (step 2) and "did the 17 Nov reminder print" (step 3) all need those
inputs, so none is measured. Nothing below is a guess presented as a measurement.

## What the ledger already says (counted from milburn.json, not new)
- Milburn cost $32.14; searching $8.04 = 25.0% of it (about 5.4% of a week, Sam's reading).
- 779 searches: 248 on the film's code, 531 elsewhere. Of the 531: 328 shared tools, 101 other, 81 film notes, 21 guides.
- Shared tools searched in many chats: handover.py 23 searches in 12 of 15 chats; people.py 27 in 7;
  people_parts.py 23 in 6; critique.py 29 in 5; facehouse.py 30 in 3.
- Finder (`page.py show`) used 12 times in all 15 chats.
- Cost per label and per remedy: NOT yet available (needs steps 1-3).

## The one remedy the numbers point to (only from counts, so provisional)
Kit learning and cross-chat repeats (shared-tool maps + a hook that answers a hand search with the finder's result):
328 of 531 non-film searches are in shared tools and the same few files recur across chats. Process-tool faults and
note-placing remain unmeasured. This ranking by count is not yet a ranking by cost.

## Question for Sam (one decision)
1. Y/N: let the Learn step finish by using helper chats (several Sonnet chats, about 3 Milburn chats each, each
   writing a short labelled list). Pick: Y. Added: a finished, measured result. Lost: the extra reading, roughly the
   plan's 1.5% of a week or a little over it (not measured). Other option: N, skip the labels and take the
   count-based remedy above through the proposal route as it stands (cheaper, but chosen on counts, not cost).
