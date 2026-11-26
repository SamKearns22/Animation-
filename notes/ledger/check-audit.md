# Ledger: check-audit

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 0.94%; 1 chats, 0 rounds, 0 notes, 0 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-26 | 8f28cc94 | est | opus | auto |  | 0.94 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-26 8f28cc94 (auto): 51 steps, history 193k at the end; other 74%, tool search 21.5%, renders 4.5%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-26 8f28cc94 (auto): Claude's words 32.7%, start-up floor 27.2%, new writes 25.8%, carried history 14.3%. Biggest origins: Claude's words 45.3%, start-up floor 27.2%, result: tool search 15.9%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 24% of the film (0.23% of a week over 1 chats: start 0.23, re-learning 0.00; 0.23% a chat; step-1 context re-read is 22% of a chat on average).
- 2026-11-26 8f28cc94: step-1 context 82k; first real work at step 15 (0.23% of a week); read before it: notes/next-jobs.md 2.7k, guides/job-packs.md 1.2k, notes/brexit-is-done.md 1.2k, source/preflight.py 1.1k, guides/film-quality-rules.md 1k, story/status.md 0.9k
