# Ledger: seeing-test

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 3.56%; 2 chats, 0 rounds, 0 notes, 0 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-27 | 8cad9ea9 | est | opus | auto |  | 0.47 |  | 0 | 0 |
| 2026-11-27 | aacaa857 | est | opus | auto |  | 3.09 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-27 8cad9ea9 (auto): 24 steps, history 107k at the end; other 75.5%, tool search 19.6%, renders 3%, pictures 1.9%
- 2026-11-27 aacaa857 (auto): 80 steps, history 181k at the end; other 80.6%, tool search 12%, pictures 3.8%, renders 3.6%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-27 8cad9ea9 (auto): start-up floor 54.9%, Claude's words 20.4%, new writes 19.4%, carried history 5.4%. Biggest origins: start-up floor 54.9%, Claude's words 27.7%, result: tool search 10.9%. Leftover 0%
- 2026-11-27 aacaa857 (auto): new writes 34.7%, start-up floor 25%, Claude's words 20.7%, carried history 19.6%. Biggest origins: messages and reminders 31.6%, Claude's words 30.4%, start-up floor 25.2%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 7% of the film (0.24% of a week over 2 chats: start 0.23, re-learning 0.01; 0.12% a chat; step-1 context re-read is 31% of a chat on average).
- 2026-11-27 8cad9ea9: step-1 context 83k; first real work at step None (None% of a week); read before it: /tmp/claude-0/-home-user-Animation-/8cad9ea9-0602-503b-a4fc-1c432923acb6/scratchpad/gta_21.3.png 1.6k, notes/seeing-test.md 0.5k, notes/seeing-test/key.md 0.3k, notes/seeing-test/findings/plain.md 0.3k, notes/seeing-test/cases.tsv 0.3k, story/status.md 0.1k
- 2026-11-27 aacaa857: step-1 context 84k; first real work at step 17 (0.23% of a week); read before it: source/seeing.py 3.9k, notes/seeing-test.md 1k, notes/seeing-test/scores.md 0.5k, notes/seeing-test/key.md 0.5k, notes/seeing-test/cases.tsv 0.5k, notes/seeing-test/next-prompt.md 0.5k
