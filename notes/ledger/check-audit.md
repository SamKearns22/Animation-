# Ledger: check-audit

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 10.46%; 5 chats, 0 rounds, 3 notes, 1 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-26 | 8f28cc94 | est | opus | plan |  | 2.55 |  | 3 | 1 |
| 2026-11-26 | 686ea287 | est | opus | auto |  | 1.43 |  | 0 | 0 |
| 2026-11-27 | 3940790c | est | opus | auto |  | 2.44 |  | 0 | 0 |
| 2026-11-27 | e5800d1f | est | opus | tool job: R8 chat 4 |  | 2.47 |  | 0 | 0 |
| 2026-11-27 | 6b06e870 | est | opus | tool |  | 1.57 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-26 8f28cc94 (plan): 130 steps, history 278k at the end; other 76.6%, tool search 21.6%, renders 1.9%
- 2026-11-26 686ea287 (auto): 93 steps, history 222k at the end; other 64.2%, tool search 34.9%, page.py 0.5%, renders 0.4%
- 2026-11-27 3940790c (auto): 153 steps, history 260k at the end; other 75%, tool search 22.2%, pictures 1.6%, renders 1.2%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-26 8f28cc94 (plan): carried history 31.4%, Claude's words 25.2%, start-up floor 25.1%, new writes 18.3%. Biggest origins: Claude's words 43%, start-up floor 25.1%, result: tool search 16.3%. Leftover 0%
- 2026-11-26 686ea287 (auto): start-up floor 30.1%, carried history 24.9%, Claude's words 24%, new writes 21%. Biggest origins: Claude's words 38.7%, start-up floor 30.1%, result: tool search 26.7%. Leftover 0%
- 2026-11-27 3940790c (auto): carried history 33.9%, new writes 27.7%, Claude's words 20.7%, start-up floor 17.7%. Biggest origins: messages and reminders 34.7%, Claude's words 32.2%, start-up floor 17.8%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 5% of the film (0.53% of a week over 3 chats: start 0.50, re-learning 0.03; 0.18% a chat; step-1 context re-read is 25% of a chat on average).
- 2026-11-26 8f28cc94: step-1 context 82k; first real work at step 15 (0.23% of a week); read before it: notes/next-jobs.md 2.7k, guides/job-packs.md 1.2k, notes/brexit-is-done.md 1.2k, source/preflight.py 1.1k, guides/film-quality-rules.md 1k, story/status.md 0.9k
- 2026-11-26 686ea287: step-1 context 85k; first real work at step 8 (0.13% of a week); read before it: notes/proposals/plain-check.md 3.7k, .claude/settings.json 1.9k, source/propose.py 1.4k, source/words.py 1k, notes/check-audit.md 0.8k, guides/job-packs.md 0.8k
- 2026-11-27 3940790c: step-1 context 85k; first real work at step 11 (0.14% of a week); read before it: source/kitinputs.py 1.6k, notes/check-audit.md 1.2k, guides/job-packs.md 1.2k, source/mhuman.py 0.9k

## Repeated notes (what would have caught them)
- Reopened list offered again after Sam declined it | search Sam's saved messages before any proposal
