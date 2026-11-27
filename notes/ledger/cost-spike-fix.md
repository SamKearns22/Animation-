# Ledger: cost-spike-fix

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 1.41%; 1 chats, 0 rounds, 0 notes, 0 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-27 | 8b239ec0 | est | opus | auto |  | 1.41 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-27 8b239ec0 (auto): 108 steps, history 208k at the end; other 65.6%, tool search 26.4%, page.py 4%, pictures 4%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-27 8b239ec0 (auto): start-up floor 35.3%, carried history 23%, Claude's words 22.7%, new writes 19%. Biggest origins: Claude's words 37.7%, start-up floor 35.3%, result: tool search 18%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 21% of the film (0.29% of a week over 1 chats: start 0.29, re-learning 0.00; 0.29% a chat; step-1 context re-read is 32% of a chat on average).
- 2026-11-27 8b239ec0: step-1 context 85k; first real work at step 24 (0.29% of a week); read before it: /tmp/claude-0/-home-user-Animation-/8b239ec0-6ed9-56e9-aae5-92b8af726ecb/scratchpad/n19_before.png 3.2k, source/sitting.py 2k, source/brexit_is_done.py 1.8k, /tmp/claude-0/-home-user-Animation-/8b239ec0-6ed9-56e9-aae5-92b8af726ecb/scratchpad/n19_shot.png 1.6k, guides/fix-pack.md 1.3k, notes/cost-spike-fix.md 1.3k
