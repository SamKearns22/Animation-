# Ledger: check-repairs

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 3.43%; 2 chats, 0 rounds, 0 notes, 0 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-21 | 906480b5 | est | opus | auto |  | 2.07 |  | 0 | 0 |
| 2026-11-21 | 335c535e | est | opus | auto |  | 1.36 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-21 906480b5 (auto): 123 steps, history 267k at the end; other 77.8%, tool search 17.4%, renders 4.2%, page.py 0.6%
- 2026-11-21 335c535e (auto): 73 steps, history 231k at the end; other 72%, tool search 25.5%, renders 1.8%, page.py 0.8%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-21 906480b5 (auto): carried history 31.5%, start-up floor 29.4%, Claude's words 20.8%, new writes 18.3%. Biggest origins: Claude's words 34.9%, start-up floor 29.4%, result: tool search 14.7%. Leftover 0%
- 2026-11-21 335c535e (auto): Claude's words 29%, start-up floor 28.7%, new writes 21.8%, carried history 20.5%. Biggest origins: Claude's words 44%, start-up floor 28.7%, result: other 13.4%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 39% of the film (1.35% of a week over 2 chats: start 1.35, re-learning 0.00; 0.68% a chat; step-1 context re-read is 26% of a chat on average). Over 0.5% a chat: a warm handover goes to Sam through the proposal route.
- 2026-11-21 906480b5: step-1 context 91k; first real work at step 54 (0.84% of a week); read before it: story/status.md 2.2k, source/ledger.py 3k, source/handover.py 2.3k, source/kittests.py 1.3k, source/costline.py 0.7k, notes/ledger/grand-theft-autism.md 0.6k
- 2026-11-21 335c535e: step-1 context 95k; first real work at step 29 (0.51% of a week); read before it: source/stepcost.py 1.9k, notes/ledger/app-costs.tsv 1.2k, notes/overnight-run.md 0.8k, tests/stepcost-transcript.jsonl 0.2k
