# Ledger: morning-report

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 51.13%; 21 chats, 0 rounds, 0 notes, 0 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-13 | 8a7d7318 | est | opus | auto |  | 2.59 |  | 0 | 0 |
| 2026-11-13 | 01fccb28 | est | opus | auto |  | 3.12 |  | 0 | 0 |
| 2026-11-13 | ea584b56 | est | opus | auto |  | 2.27 |  | 0 | 0 |
| 2026-11-14 | 03b0b104 | est | opus | auto |  | 2.81 |  | 0 | 0 |
| 2026-11-14 | 51e76e7b | est | opus | auto |  | 1.98 |  | 0 | 0 |
| 2026-11-14 | 3153afb9 | est | opus | auto |  | 1.03 |  | 0 | 0 |
| 2026-11-14 | 373677a3 | est | sonnet | auto |  | 3.4 |  | 0 | 0 |
| 2026-11-14 | 910d15e2 | est | opus | auto |  | 1.73 |  | 0 | 0 |
| 2026-11-14 | 37300ce2 | est | opus | auto |  | 1.69 |  | 0 | 0 |
| 2026-11-14 | 16b5a7e4 | est | sonnet | auto |  | 3.11 |  | 0 | 0 |
| 2026-11-14 | 88fd8879 | est | opus | auto |  | 2.82 |  | 0 | 0 |
| 2026-11-14 | cdb10d78 | est | sonnet | auto |  | 0.3 |  | 0 | 0 |
| 2026-11-14 | 0fb98d3f | est | opus | auto |  | 1.48 |  | 0 | 0 |
| 2026-11-14 | b4547dcd | est | sonnet | auto |  | 0.33 |  | 0 | 0 |
| 2026-11-14 | 0b1357fe | est | opus | auto |  | 3.0 |  | 0 | 0 |
| 2026-11-15 | 13a4cda5 | est | sonnet | auto |  | 1.57 |  | 0 | 0 |
| 2026-11-15 | d58e0dd9 | est | opus | auto |  | 2.33 |  | 0 | 0 |
| 2026-11-16 | 2cec4bf1 | est | sonnet | auto |  | 4.11 |  | 0 | 0 |
| 2026-11-17 | dbebd85f | est | opus | auto |  | 5.21 |  | 0 | 0 |
| 2026-11-17 | 20721d48 | est | opus | auto |  | 3.54 |  | 0 | 0 |
| 2026-11-22 | 3bda3f0b | est | opus | auto |  | 2.71 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-16 2cec4bf1 (auto): 72 steps, history 186k at the end; other 77.7%, tool search 19.5%, renders 2.8%
- 2026-11-17 dbebd85f (auto): 56 steps, history 145k at the end; other 71%, tool search 22.3%, page.py 4%, renders 2.7%
- 2026-11-17 20721d48 (auto): 105 steps, history 224k at the end; other 78.6%, tool search 15.3%, page.py 3.3%, renders 2.5%, routine 0.3%
- 2026-11-22 3bda3f0b (auto): 163 steps, history 266k at the end; other 75.4%, tool search 22.1%, pictures 1.3%, renders 1.2%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-22 3bda3f0b (auto): carried history 34.8%, new writes 26%, start-up floor 21.5%, Claude's words 17.8%. Biggest origins: messages and reminders 32.5%, Claude's words 29.2%, start-up floor 21.6%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 0% of the film (0.18% of a week over 1 chats: start 0.18, re-learning 0.00; 0.18% a chat; step-1 context re-read is 28% of a chat on average).
- 2026-11-22 3bda3f0b: step-1 context 95k; first real work at step 14 (0.18% of a week); read before it: notes/check-repairs.md 1.7k, /tmp/claude-0/-home-user-Animation-/3bda3f0b-5a98-5924-8e3d-d3307fd55bac/scratchpad/s3.png 1.6k, /tmp/claude-0/-home-user-Animation-/3bda3f0b-5a98-5924-8e3d-d3307fd55bac/scratchpad/s3c.png 1.6k, source/kittests.py 0.5k
