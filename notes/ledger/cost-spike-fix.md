# Ledger: cost-spike-fix

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 2.86%; 1 chats, 0 rounds, 0 notes, 0 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-27 | 8b239ec0 | est | opus | tools |  | 2.86 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-27 8b239ec0 (tools): 192 steps, history 279k at the end; other 69.3%, tool search 21.3%, page.py 5%, pictures 3.5%, renders 0.9%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-27 8b239ec0 (tools): carried history 34%, start-up floor 29.9%, Claude's words 21.4%, new writes 14.8%. Biggest origins: Claude's words 41.4%, start-up floor 29.9%, result: tool search 16.9%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 10% of the film (0.29% of a week over 1 chats: start 0.29, re-learning 0.00; 0.29% a chat; step-1 context re-read is 28% of a chat on average).
- 2026-11-27 8b239ec0: step-1 context 85k; first real work at step 24 (0.29% of a week); read before it: /tmp/claude-0/-home-user-Animation-/8b239ec0-6ed9-56e9-aae5-92b8af726ecb/scratchpad/n19_before.png 3.2k, source/sitting.py 2k, source/brexit_is_done.py 1.8k, /tmp/claude-0/-home-user-Animation-/8b239ec0-6ed9-56e9-aae5-92b8af726ecb/scratchpad/n19_shot.png 1.6k, source/acting.py 1.5k, guides/fix-pack.md 1.3k
