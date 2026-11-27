# Ledger: cost-spike-fix

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 7.59%; 4 chats, 0 rounds, 0 notes, 0 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-27 | 8b239ec0 | est | opus | tools |  | 2.86 |  | 0 | 0 |
| 2026-11-27 | 59f68aa5 | est | sonnet | auto |  | 0.06 |  | 0 | 0 |
| 2026-11-27 | 2ba38a1f | est | opus | replay test 2 + savings S1-S4 |  | 2.52 |  | 0 | 0 |
| 2026-11-27 | 7f671c35 | est | opus | tool |  | 2.15 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-27 8b239ec0 (tools): 192 steps, history 279k at the end; other 69.3%, tool search 21.3%, page.py 5%, pictures 3.5%, renders 0.9%
- 2026-11-27 59f68aa5 (auto): 7 steps, history 96k at the end; other 80.9%, tool search 19.1%
- 2026-11-27 2ba38a1f (replay test 2 + savings S1-S4): 75 steps, history 196k at the end; other 76.1%, tool search 20.2%, pictures 2.2%, renders 1.2%, page.py 0.3%
- 2026-11-27 7f671c35 (tool): 139 steps, history 250k at the end; other 67.9%, tool search 26.9%, page.py 3.7%, whole-file .py read 1.4%, renders 0.2%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-27 8b239ec0 (tools): carried history 34%, start-up floor 29.9%, Claude's words 21.4%, new writes 14.8%. Biggest origins: Claude's words 41.4%, start-up floor 29.9%, result: tool search 16.9%. Leftover 0%
- 2026-11-27 59f68aa5 (auto): start-up floor 62.7%, new writes 22.3%, Claude's words 13.6%, carried history 1.3%. Biggest origins: start-up floor 62.7%, result: tool search 18.1%, Claude's words 17%. Leftover 0%
- 2026-11-27 2ba38a1f (replay test 2 + savings S1-S4): new writes 38.4%, start-up floor 22.5%, Claude's words 20.1%, carried history 19%. Biggest origins: messages and reminders 29%, Claude's words 28.6%, start-up floor 22.7%. Leftover 0%
- 2026-11-27 7f671c35 (tool): carried history 30.8%, start-up floor 29.1%, Claude's words 23.3%, new writes 16.8%. Biggest origins: Claude's words 43.1%, start-up floor 29.1%, result: tool search 18.9%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 17% of the film (1.26% of a week over 4 chats: start 1.22, re-learning 0.04; 0.32% a chat; step-1 context re-read is 25% of a chat on average).
- 2026-11-27 8b239ec0: step-1 context 85k; first real work at step 24 (0.29% of a week); read before it: /tmp/claude-0/-home-user-Animation-/8b239ec0-6ed9-56e9-aae5-92b8af726ecb/scratchpad/n19_before.png 3.2k, source/sitting.py 2k, source/brexit_is_done.py 1.8k, /tmp/claude-0/-home-user-Animation-/8b239ec0-6ed9-56e9-aae5-92b8af726ecb/scratchpad/n19_shot.png 1.6k, source/acting.py 1.5k, guides/fix-pack.md 1.3k
- 2026-11-27 59f68aa5: step-1 context 83k; first real work at step None (None% of a week); read before it: notes/cost-spike-fix.md 1.8k, notes/steps-breakdown.md 0.7k, notes/next-chat-prompt.md 0.5k, notes/cost-fixes.md 0.5k, notes/budget-job.md 0.5k, notes/ledger/sam/rxrsibqu.md 0.5k
- 2026-11-27 2ba38a1f: step-1 context 85k; first real work at step 39 (0.59% of a week); read before it: source/patriots4_cast.py 6.2k, notes/cost-spike-fix.md 1.5k, /tmp/claude-0/-home-user-Animation-/2ba38a1f-e9fb-50a1-8f95-188f11475c8c/scratchpad/refs/sheet.jpg 1.6k, /tmp/claude-0/-home-user-Animation-/2ba38a1f-e9fb-50a1-8f95-188f11475c8c/scratchpad/out/lk/pair.jpg 1.6k, guides/kit-catalogue.md 1.2k, source/satire_template.py 1.3k
- 2026-11-27 7f671c35: step-1 context 85k; first real work at step 22 (0.34% of a week); read before it: source/touch.py 4.7k, notes/cost-spike-fix.md 2.9k, source/kittests.py 1.9k, source/page.py 1.9k, notes/proposals/cost-spike-fix.md 0.8k, story/status.md 0.7k
