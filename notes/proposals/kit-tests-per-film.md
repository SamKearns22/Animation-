# Proposal: The kit tests run in every chat; Sam wants them at each film's start and end

Status: open

## Problem
Sam, 25 Nov (R7 chat 4), word for word: "Make the kit check happen at the beginning and the end of every film. If
something major changes in the kits, then you can manually suggest making one to me. Currently, it is wasting usage and
time to do this with every chat. We do so many chats." Then "1 y y": Y to the rule as drafted in that chat, and Y to
dropping kittest-resume. Today the kit tests (each one checks a fault Sam once caught stays fixed) run in every chat:
in the background when a chat's machine starts, again when a chat hands over, and again before every animatic and
final; a chat cannot hand over while they are running or red. Sam finds this costs usage and time in every chat.

## Facts
- source/kittests.py holds 147 tests (`python3 source/kitstamps.py stale` counts them); a full run took 15 min on a
  fresh machine (notes/proposals/kit-tests-when.md, "Built").
- Built and adopted earlier today (kit-tests-when, Sam's pick 1): each green test leaves a stamp of the files it read
  (notes/kittest-stamps.tsv; source/kitstamps.py); only "stale" tests (files changed since their pass) run. They run at
  three points: (1) every fresh machine, in the background (.claude/hooks/setup.sh last lines -> source/watcher.py
  kittests-bg -> `kittests.py --stale`); (2) every `handover.py end` (kittest_gate_faults, source/handover.py ~574:
  runs the stale ones on the chat's final code; STOPs while the start-up run is busy, when none finished, a test
  crashed, or a test is red at two handovers in a row by different chats; notes/logs/kittest-reds.log); (3) every
  animatic and final (source/finish.py ~216 -> kitstamps.finish_gate: runs the stale ones, refuses while any is stale).
- At this chat's start the background run was running (pgrep) with 28 of 147 tests stale (~5 min estimated).
- notes/logs/handover-end.log, 25 Nov: 10 handover refusals naming the kit tests, across 9 chats' rows that day
  (counted with grep; some refusals are the same chat retrying). 11 chats committed in the last day (git log trailers).
- The replay in kit-tests-when (128 chats in 7 days): per-test stamps waited 636 min in total, median 2.1 min a chat
  (quartiles 0.4 / 2.1 / 11.9). Usage cost of the waiting itself: unchecked.
- Past reds: 7 of 7 caught by the stamps replay; kittest-reds.log has 22 lines. Which of those reds were first seen
  at a chat start (from another chat's change) vs at the chat's own end: unchecked.
- Override (Sam's typed word) already skips the handover kit gate and finish's kit gate, logged (source/override.py).
- A film's chats pass `--film NAME` to handover.py start/end; whether the code can tell a film's FIRST chat, or a
  final from an animatic in finish.py: unchecked (finish.py keeps animatics by "animatic" in the output's name, ~290).
- The rulebook guides/film-quality-rules.md: rule 41 (hands) is where Sam's job asks the new row to follow; rule 59
  names finish's kit gate in its check column. guides/kit-catalogue.md lists kit tools.
- CLAUDE.md: "No rule without a working check" (a rule counts only when its check caught a saved example);
  "Every rule and fix is for all films"; Statement One (cost down only by working smarter, never cutting quality).
- kittest-resume (a proposal to resume a stopped run) is dropped by Sam (notes/proposals/kittest-resume.md, Status).

## Record
source/kittests.py
source/kitstamps.py
source/handover.py
source/watcher.py
source/finish.py
source/override.py
.claude/hooks/setup.sh
notes/proposals/kit-tests-when.md
notes/proposals/kittest-resume.md
notes/next-jobs.md
notes/kittest-stamps.tsv
notes/logs/
guides/film-quality-rules.md
guides/kit-catalogue.md
