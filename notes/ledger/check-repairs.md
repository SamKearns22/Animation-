# Ledger: check-repairs

Written by `source/ledger.py` (do not edit by hand; the record is the .json beside it). Each round's check results and check sheet text are in the folder of the same name.

**Estimate ?% of a week; spent 2.07%; 1 chats, 0 rounds, 0 notes, 0 repeated.**

Source: **app** = the app’s own figure for that chat (real); **est** = the transcript estimate (chats the app cannot show, or not yet imported with `ledger.py app`).

| date | chat | source | model | stage | round | cost % | $ | notes | repeated |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-21 | 906480b5 | est | opus | auto |  | 2.07 |  | 0 | 0 |

## Cost by kind of step (share of each chat; measured from its transcript)
- 2026-11-21 906480b5 (auto): 123 steps, history 267k at the end; other 77.8%, tool search 17.4%, renders 4.2%, page.py 0.6%

## Where the money went (blocks and origins; leftover = cost nothing explains, aim under 5%)
- 2026-11-21 906480b5 (auto): carried history 31.5%, start-up floor 29.4%, Claude's words 20.8%, new writes 18.3%. Biggest origins: Claude's words 34.9%, start-up floor 29.4%, result: tool search 14.7%. Leftover 0%

## Starting each chat
A new chat's start and re-learning cost 41% of the film (0.84% of a week over 1 chats: start 0.84, re-learning 0.00; 0.84% a chat; step-1 context re-read is 27% of a chat on average). Over 0.5% a chat: a warm handover goes to Sam through the proposal route.
- 2026-11-21 906480b5: step-1 context 91k; first real work at step 54 (0.84% of a week); read before it: story/status.md 2.2k, source/ledger.py 3k, source/handover.py 2.3k, source/kittests.py 1.3k, source/costline.py 0.7k, notes/ledger/grand-theft-autism.md 0.6k
