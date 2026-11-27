# Ledger: seeing-test

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 4.55%; 3 chats, 0 rounds, 0 notes, 0 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-27 | 8cad9ea9 | est | opus | auto |  | 0.47 |  | 0 | 0 |
| 2026-11-27 | aacaa857 | est | opus | build and score watch test |  | 3.63 |  | 0 | 0 |
| 2026-11-27 | 7a6d1e31 | est | opus | auto |  | 0.45 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-27 8cad9ea9 (auto): 24 steps, history 107k at the end; other 75.5%, tool search 19.6%, renders 3%, pictures 1.9%
- 2026-11-27 7a6d1e31 (auto): 41 steps, history 133k at the end; other 70.2%, tool search 16.2%, pictures 10.9%, renders 2.7%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-27 8cad9ea9 (auto): start-up floor 54.9%, Claude's words 20.4%, new writes 19.4%, carried history 5.4%. Biggest origins: start-up floor 54.9%, Claude's words 27.7%, result: tool search 10.9%. Leftover 0%
- 2026-11-27 7a6d1e31 (auto): start-up floor 47%, new writes 23.5%, Claude's words 18.4%, carried history 11.1%. Biggest origins: start-up floor 47%, Claude's words 26.4%, result: tool search 14.2%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 0% of the film (0.01% of a week over 2 chats: start 0.00, re-learning 0.01; 0.01% a chat; step-1 context re-read is 36% of a chat on average).
- 2026-11-27 8cad9ea9: step-1 context 83k; first real work at step None (None% of a week); read before it: /tmp/claude-0/-home-user-Animation-/8cad9ea9-0602-503b-a4fc-1c432923acb6/scratchpad/gta_21.3.png 1.6k, notes/seeing-test.md 0.5k, notes/seeing-test/key.md 0.3k, notes/seeing-test/findings/plain.md 0.3k, notes/seeing-test/cases.tsv 0.3k, story/status.md 0.1k
- 2026-11-27 7a6d1e31: step-1 context 85k; first real work at step None (None% of a week); read before it: notes/seeing-test/findings/watch.md 2.6k, /tmp/claude-0/-home-user-Animation-/7a6d1e31-c2f2-5172-8b65-d8f842dd67c1/scratchpad/c05b.jpg 3.2k, notes/seeing-test.md 1.9k, notes/seeing-test/scores-watch.md 1.9k, /tmp/claude-0/-home-user-Animation-/7a6d1e31-c2f2-5172-8b65-d8f842dd67c1/scratchpad/c02a.jpg 3.2k, /tmp/claude-0/-home-user-Animation-/7a6d1e31-c2f2-5172-8b65-d8f842dd67c1/scratchpad/c05a.jpg 1.6k
