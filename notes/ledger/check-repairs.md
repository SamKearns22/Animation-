# Ledger: check-repairs

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 8.07%; 4 chats, 0 rounds, 0 notes, 0 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-21 | 906480b5 | est | opus | auto |  | 2.72 |  | 0 | 0 |
| 2026-11-21 | 335c535e | est | opus | cost-audit |  | 2.24 |  | 0 | 0 |
| 2026-11-22 | 09ed7e0d | est | opus | cost-audit-2 |  | 2.95 |  | 0 | 0 |
| 2026-11-22 | f4f681d6 | est | opus | auto |  | 0.16 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-21 906480b5 (auto): 133 steps, history 281k at the end; other 82.3%, tool search 13.9%, renders 3.2%, page.py 0.5%
- 2026-11-21 335c535e (cost-audit): 93 steps, history 250k at the end; other 80%, tool search 17.3%, renders 2.2%, page.py 0.5%
- 2026-11-22 09ed7e0d (cost-audit-2): 49 steps, history 144k at the end; other 83.9%, tool search 16.1%
- 2026-11-22 f4f681d6 (auto): 5 steps, history 120k at the end; other 83.7%, tool search 16.3%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-21 906480b5 (auto): new writes 31.7%, carried history 26.9%, start-up floor 24%, Claude's words 17.4%. Biggest origins: Claude's words 29.6%, start-up floor 24%, cache re-write 16.9%. Leftover 0%
- 2026-11-21 335c535e (cost-audit): new writes 39%, start-up floor 21.3%, Claude's words 21.2%, carried history 18.4%. Biggest origins: Claude's words 34%, cache re-write 23.9%, start-up floor 21.3%. Leftover 0%
- 2026-11-22 09ed7e0d (cost-audit-2): start-up floor 60.6%, Claude's words 15.5%, new writes 14.7%, carried history 9.2%. Biggest origins: start-up floor 60.6%, Claude's words 23.5%, result: tool search 10.1%. Leftover 0%
- 2026-11-22 f4f681d6 (auto): start-up floor 48.5%, new writes 40.2%, Claude's words 10.1%, carried history 1.2%. Biggest origins: start-up floor 48.5%, result: tool search 21%, Claude's words 11.8%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 21% of the film (1.70% of a week over 4 chats: start 1.70, re-learning 0.00; 0.43% a chat; step-1 context re-read is 21% of a chat on average).
- 2026-11-21 906480b5: step-1 context 91k; first real work at step 54 (0.84% of a week); read before it: source/ledger.py 3k, story/status.md 2.2k, source/handover.py 2.3k, source/kittests.py 1.3k, source/costline.py 0.7k, notes/ledger/grand-theft-autism.md 0.6k
- 2026-11-21 335c535e: step-1 context 95k; first real work at step 29 (0.51% of a week); read before it: source/stepcost.py 1.9k, notes/ledger/app-costs.tsv 1.2k, notes/overnight-run.md 0.8k, tests/stepcost-transcript.jsonl 0.2k
- 2026-11-22 09ed7e0d: step-1 context 95k; first real work at step 13 (0.35% of a week); read before it: notes/proposal-route.md 1.3k, .claude/hooks/costwatch.py 1k, source/stepcost.py 0.9k, notes/proposals/dearest-grand-theft-autism-1/chat.md 0.2k
- 2026-11-22 f4f681d6: step-1 context 92k; first real work at step None (None% of a week); read before it: 
