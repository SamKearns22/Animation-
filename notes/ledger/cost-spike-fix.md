# Ledger: cost-spike-fix

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 14.44%; 7 chats, 0 rounds, 0 notes, 0 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-27 | 8b239ec0 | est | opus | tools |  | 2.86 |  | 0 | 0 |
| 2026-11-27 | 59f68aa5 | est | sonnet | auto |  | 0.06 |  | 0 | 0 |
| 2026-11-27 | 2ba38a1f | est | opus | replay test 2 + savings S1-S4 |  | 2.82 |  | 0 | 0 |
| 2026-11-27 | 7f671c35 | est | opus | tool |  | 2.15 |  | 0 | 0 |
| 2026-11-27 | d251ebda | est | opus | auto |  | 2.29 |  | 0 | 0 |
| 2026-11-27 | 774a3f06 | est | opus | auto |  | 2.6 |  | 0 | 0 |
| 2026-11-27 | 38fe1c77 | est | opus | auto |  | 1.66 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-27 8b239ec0 (tools): 192 steps, history 279k at the end; other 69.3%, tool search 21.3%, page.py 5%, pictures 3.5%, renders 0.9%
- 2026-11-27 59f68aa5 (auto): 7 steps, history 96k at the end; other 80.9%, tool search 19.1%
- 2026-11-27 2ba38a1f (replay test 2 + savings S1-S4): 162 steps, history 278k at the end; other 77.3%, tool search 18.6%, renders 2.3%, pictures 1.3%, page.py 0.6%
- 2026-11-27 7f671c35 (tool): 139 steps, history 250k at the end; other 67.9%, tool search 26.9%, page.py 3.7%, whole-file .py read 1.4%, renders 0.2%
- 2026-11-27 d251ebda (auto): 121 steps, history 280k at the end; other 64.2%, tool search 30.3%, renders 3%, pictures 2.4%
- 2026-11-27 774a3f06 (auto): 159 steps, history 278k at the end; other 63.7%, tool search 30.4%, pictures 5.5%, renders 0.4%
- 2026-11-27 38fe1c77 (auto): 99 steps, history 221k at the end; Claude's words (thinking and writing) 27.5%, start-up reading 23.3%, tool search 21.1%, memory lapses (re-paying for the whole chat after a gap) 11.8%, pictures 6.1%, messages and reminders 3.9%, reading kit code 1.8%, small shell commands (listing, moving, copying) 1.4%, whole-file .py read 1%, renders 0.9%, reading guides 0.5%, app tools (chats, files sent) 0.3%, reading chat records 0.2%, reading notes 0.1%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-27 8b239ec0 (tools): carried history 34%, start-up floor 29.9%, Claude's words 21.4%, new writes 14.8%. Biggest origins: Claude's words 41.4%, start-up floor 29.9%, result: tool search 16.9%. Leftover 0%
- 2026-11-27 59f68aa5 (auto): start-up floor 62.7%, new writes 22.3%, Claude's words 13.6%, carried history 1.3%. Biggest origins: start-up floor 62.7%, result: tool search 18.1%, Claude's words 17%. Leftover 0%
- 2026-11-27 2ba38a1f (replay test 2 + savings S1-S4): carried history 46%, new writes 24.7%, Claude's words 18.6%, start-up floor 10.8%. Biggest origins: messages and reminders 41.8%, Claude's words 30.5%, result: tool search 13.6%. Leftover 0%
- 2026-11-27 7f671c35 (tool): carried history 30.8%, start-up floor 29.1%, Claude's words 23.3%, new writes 16.8%. Biggest origins: Claude's words 43.1%, start-up floor 29.1%, result: tool search 18.9%. Leftover 0%
- 2026-11-27 d251ebda (auto): carried history 30.1%, Claude's words 26.5%, start-up floor 24.6%, new writes 18.9%. Biggest origins: Claude's words 46.3%, start-up floor 24.6%, result: tool search 23.1%. Leftover 0%
- 2026-11-27 774a3f06 (auto): carried history 30.1%, start-up floor 28.1%, Claude's words 25.1%, new writes 16.6%. Biggest origins: Claude's words 45.8%, start-up floor 28.1%, result: tool search 15.4%. Leftover 0%
- 2026-11-27 38fe1c77 (auto): new writes 32%, start-up floor 27.7%, carried history 20.4%, Claude's words 19.9%. Biggest origins: Claude's words 32.8%, start-up floor 27.7%, cache re-write 14.1%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 14% of the film (2.05% of a week over 7 chats: start 2.01, re-learning 0.04; 0.29% a chat; step-1 context re-read is 25% of a chat on average).
- 2026-11-27 8b239ec0: step-1 context 85k; first real work at step 24 (0.29% of a week); read before it: /tmp/claude-0/-home-user-Animation-/8b239ec0-6ed9-56e9-aae5-92b8af726ecb/scratchpad/n19_before.png 3.2k, source/sitting.py 2k, source/brexit_is_done.py 1.8k, /tmp/claude-0/-home-user-Animation-/8b239ec0-6ed9-56e9-aae5-92b8af726ecb/scratchpad/n19_shot.png 1.6k, source/acting.py 1.5k, guides/fix-pack.md 1.3k
- 2026-11-27 59f68aa5: step-1 context 83k; first real work at step None (None% of a week); read before it: notes/cost-spike-fix.md 1.8k, notes/steps-breakdown.md 0.7k, notes/next-chat-prompt.md 0.5k, notes/cost-fixes.md 0.5k, notes/budget-job.md 0.5k, notes/ledger/sam/rxrsibqu.md 0.5k
- 2026-11-27 2ba38a1f: step-1 context 85k; first real work at step 39 (0.59% of a week); read before it: source/patriots4_cast.py 6.2k, notes/cost-spike-fix.md 1.5k, /tmp/claude-0/-home-user-Animation-/2ba38a1f-e9fb-50a1-8f95-188f11475c8c/scratchpad/refs/sheet.jpg 1.6k, /tmp/claude-0/-home-user-Animation-/2ba38a1f-e9fb-50a1-8f95-188f11475c8c/scratchpad/out/lk/pair.jpg 1.6k, guides/kit-catalogue.md 1.2k, source/satire_template.py 1.3k
- 2026-11-27 7f671c35: step-1 context 85k; first real work at step 22 (0.34% of a week); read before it: source/touch.py 4.7k, notes/cost-spike-fix.md 2.9k, source/kittests.py 1.9k, source/page.py 1.9k, notes/proposals/cost-spike-fix.md 0.8k, story/status.md 0.7k
- 2026-11-27 d251ebda: step-1 context 85k; first real work at step 28 (0.44% of a week); read before it: source/facehouse_c.py 9.7k, source/facehouse_b.py 3.2k, source/facehouse.py 2.5k, source/people.py 1.9k, source/facepick.py 2.1k, /tmp/claude-0/-home-user-Animation-/d251ebda-2d1a-518b-be92-d3a745668a10/scratchpad/refs.jpg 1.6k
- 2026-11-27 774a3f06: step-1 context 85k; first real work at step 6 (0.09% of a week); read before it: source/data/freeze/films.json 0.6k, source/freeze.py 0.6k
- 2026-11-27 38fe1c77: step-1 context 85k; first real work at step 19 (0.26% of a week); read before it: source/kittests_health.py 1.9k, source/facehouse_b.py 1.7k, source/people_famous.py 1.7k, notes/cost-spike-fix.md 1.6k, guides/fix-pack.md 1.6k, /tmp/claude-0/-home-user-Animation-/38fe1c77-5205-5a9f-8533-eac35b839ecf/scratchpad/look1.jpg 1.6k
