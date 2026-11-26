# Ledger: pose-test

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 2.0%; 1 chats, 0 rounds, 0 notes, 0 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-26 | 05666102 | est | opus | auto |  | 2.0 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-26 05666102 (auto): 114 steps, history 264k at the end; other 63.9%, tool search 24%, renders 5.1%, pictures 4.3%, film-file search 2.6%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-26 05666102 (auto): carried history 28.8%, start-up floor 25.8%, Claude's words 25.7%, new writes 19.7%. Biggest origins: Claude's words 43.2%, start-up floor 25.8%, result: tool search 20.7%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 24% of the film (0.48% of a week over 1 chats: start 0.48, re-learning 0.00; 0.48% a chat; step-1 context re-read is 24% of a chat on average).
- 2026-11-26 05666102: step-1 context 84k; first real work at step 29 (0.48% of a week); read before it: source/solid_seat.py 9.5k, source/brexit_is_done_action.py 4.3k, source/views.py 4.1k, guides/pose-kits.md 1.7k, source/lying.py 1.7k, /tmp/claude-0/-home-user-Animation-/05666102-7e83-59cc-b6e1-ccccd0b98a4f/scratchpad/t1_cmp.png 1.6k
