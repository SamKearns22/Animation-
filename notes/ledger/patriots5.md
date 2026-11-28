# Ledger: patriots5

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate 15.4% of a week; spent 12.5% (-2.90); 6 chats, 0 rounds, 3 notes, 0 repeated.**

**Stages (tracked quietly):**

| stage | planned % | done | spent at its end | steps |
|---|---|---|---|---|
| cast | 3.7 |  |  |  |
| sets | 2.2 |  |  |  |
| board | 1 |  |  |  |
| moves | 5 |  |  |  |
| animatic1 | 0.5 |  |  |  |
| round | 2 |  |  |  |
| final | 1 |  |  |  |

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-27 | 4e93d9da | est | opus | auto |  | 3.22 |  | 0 | 0 |
| 2026-11-28 | 345bd082 | est | opus | plan |  | 3.59 |  | 0 | 0 |
| 2026-11-27 | 22904d63 | est | opus | practice |  | 2.77 |  | 3 | 0 |
| 2026-11-27 | 0b4b259a | est | opus | auto |  | 0.49 |  | 0 | 0 |
| 2026-11-27 | 105b46bb | est | opus | auto |  | 0.7 |  | 0 | 0 |
| 2026-11-27 | b4eecb27 | est | opus | auto |  | 1.73 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-27 4e93d9da (auto): 140 steps, history 296k at the end; other 79.7%, tool search 16.7%, pictures 2.9%, renders 0.7%
- 2026-11-27 22904d63 (practice): 113 steps, history 295k at the end; other 63.3%, tool search 29.1%, pictures 5.9%, renders 1.4%, film-file search 0.2%
- 2026-11-27 0b4b259a (auto): 41 steps, history 115k at the end; start-up reading 39.2%, memory lapses (re-paying for the whole chat after a gap) 19.8%, Claude's words (thinking and writing) 18.2%, tool search 11.2%, messages and reminders 3.5%, renders 1.7%, reading notes 1.7%, app tools (chats, files sent) 1.6%, pictures 1.5%, small shell commands (listing, moving, copying) 0.8%, running checks and tools 0.7%
- 2026-11-27 105b46bb (auto): 59 steps, history 147k at the end; start-up reading 31.4%, Claude's words (thinking and writing) 28.5%, tool search 14%, renders 9.4%, pictures 5.7%, messages and reminders 3%, edit results 2.7%, film-file search 2.6%, small shell commands (listing, moving, copying) 1.5%, app tools (chats, files sent) 0.8%, reading chat records 0.3%, tool lookups 0.1%
- 2026-11-27 b4eecb27 (auto): 76 steps, history 215k at the end; Claude's words (thinking and writing) 32.8%, tool search 21%, start-up reading 16.1%, memory lapses (re-paying for the whole chat after a gap) 14.1%, edit results 4.9%, small shell commands (listing, moving, copying) 3.5%, renders 2.6%, pictures 2.4%, running checks and tools 0.9%, messages and reminders 0.8%, app tools (chats, files sent) 0.4%, reading chat records 0.2%, reading notes 0.1%, tool lookups 0.1%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-27 4e93d9da (auto): new writes 41.3%, carried history 33%, Claude's words 15%, start-up floor 10.7%. Biggest origins: messages and reminders 33.6%, Claude's words 22.5%, cache re-write 16%. Leftover 0%
- 2026-11-27 22904d63 (practice): Claude's words 30%, carried history 29.1%, start-up floor 21.9%, new writes 19%. Biggest origins: Claude's words 51.7%, start-up floor 21.9%, result: tool search 14.5%. Leftover 0%
- 2026-11-27 0b4b259a (auto): start-up floor 43.9%, new writes 35.4%, Claude's words 13.9%, carried history 6.8%. Biggest origins: start-up floor 43.9%, cache re-write 22.2%, Claude's words 20.4%. Leftover 0%
- 2026-11-27 105b46bb (auto): start-up floor 41.5%, Claude's words 25%, new writes 19.4%, carried history 14.1%. Biggest origins: start-up floor 41.5%, Claude's words 37.7%, result: tool search 6.5%. Leftover 0%
- 2026-11-27 b4eecb27 (auto): new writes 34.8%, Claude's words 27.2%, start-up floor 21.2%, carried history 16.9%. Biggest origins: Claude's words 43.1%, start-up floor 21.2%, cache re-write 18.5%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 18% of the film (2.22% of a week over 5 chats: start 2.21, re-learning 0.01; 0.44% a chat; step-1 context re-read is 25% of a chat on average).
- 2026-11-27 4e93d9da: step-1 context 83k; first real work at step 52 (0.8% of a week); read before it: source/patriots3_cast.py 3k, source/facehouse_c.py 2.2k, source/facehouse_b.py 1.8k, guides/job-packs.md 1.7k, /tmp/claude-0/-home-user-Animation-/4e93d9da-64f8-5a9a-be65-cdb7928dda9f/scratchpad/p3.jpg 1.6k, /tmp/claude-0/-home-user-Animation-/4e93d9da-64f8-5a9a-be65-cdb7928dda9f/scratchpad/turns.jpg 1.6k
- 2026-11-27 22904d63: step-1 context 85k; first real work at step 27 (0.59% of a week); read before it: source/mounts.py 2.7k, guides/figure-rig.md 2.4k, source/views.py 2.4k, guides/pose-kits.md 2k, notes/learn/shoulder-tower/refs-sheet.jpg 1.6k, /tmp/claude-0/-home-user-Animation-/22904d63-b565-5dcb-85d6-40d773d90546/scratchpad/tw/pair.png 1.6k
- 2026-11-27 0b4b259a: step-1 context 85k; first real work at step 7 (0.11% of a week); read before it: source/shoulder_tower.py 1.7k, notes/learn/shoulder-tower/lesson.md 0.9k
- 2026-11-27 105b46bb: step-1 context 85k; first real work at step 4 (0.08% of a week); read before it: source/patriots3_cast.py 1.2k
- 2026-11-27 b4eecb27: step-1 context 86k; first real work at step 26 (0.63% of a week); read before it: source/shoulder_tower.py 6.6k, notes/learn/shoulder-tower/lesson.md 3.7k, source/moves.py 2.8k, notes/learn/shoulder-tower/neck-fixed-27nov.png 1.6k, source/views.py 0.8k, guides/job-packs.md 0.2k
