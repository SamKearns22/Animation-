# Ledger: cost-diagnosis

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 11.29%; 8 chats, 0 rounds, 0 notes, 0 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-13 | b8292e2c | est | opus | auto |  | 1.63 |  | 0 | 0 |
| 2026-11-13 | 3fdc1b09 | est | opus | auto |  | 2.26 |  | 0 | 0 |
| 2026-11-13 | fad08afe | est | opus | auto |  | 1.46 |  | 0 | 0 |
| 2026-11-13 | fe5c762d | est | opus | auto |  | 1.07 |  | 0 | 0 |
| 2026-11-13 | 1f73e167 | est | opus | auto |  | 1.45 |  | 0 | 0 |
| 2026-11-16 | 523cd351 | est | opus | auto |  | 1.68 |  | 0 | 0 |
| 2026-11-16 | e992c7dc | est | opus | auto |  | 1.51 |  | 0 | 0 |
| 2026-11-26 | 52f3dc5e | est | opus | auto |  | 0.23 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-16 e992c7dc (auto): 30 steps, history 116k at the end; other 78.5%, tool search 21.5%
- 2026-11-26 52f3dc5e (auto): 12 steps, history 124k at the end; other 78.9%, tool search 21.1%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-26 52f3dc5e (auto): start-up floor 55.6%, new writes 23%, Claude's words 18.7%, carried history 2.7%. Biggest origins: start-up floor 55.6%, Claude's words 23.3%, result: tool search 18.7%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 0% of the film (0.00% of a week over 1 chats: start 0.00, re-learning 0.00; 0.00% a chat; step-1 context re-read is 23% of a chat on average).
- 2026-11-26 52f3dc5e: step-1 context 99k; first real work at step None (None% of a week); read before it: story/status.md 0.4k
