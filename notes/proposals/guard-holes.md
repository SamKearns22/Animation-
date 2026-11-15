# Proposal: The guard misses most change questions and stops some routine ones

Status: open

## Problem
The proposal route's guard (the Stop hook, `propose.py hook` / `reply_faults`) is meant to refuse any reply that asks
Sam to approve a change to rules, tools, checks, kits or how films are built without a judge's verdict, and to let
routine film questions (animatic, final render, clip, posting, a note's fix, a picture choice) through. Sam picked
option 1 of notes/proposals/install-route.md (15 Nov), whose first job (C3) is "close the hook's holes". Measured in
chat 6, it misses most change questions and stops at least one routine one. A missed change means Sam is asked to
approve an unjudged change (the failure the route exists to stop); a wrong stop costs a chat a rewrite and teaches
chats to word around the guard. The guard must hold without Sam checking it.

## Facts
- Probe (chat 6, 15 Nov; `notes/proposals/guard-holes/probe.py`, run from the repo root): 12 change questions, 10
  routine ones, written by chat 6 to probe the guard (not drawn from real chats; how typical they are is unchecked).
  Change questions missed: 9 of 12 ("Shall I change the render tool so it reuses cached frames? Y/N"; "Y or N: add a
  new gate before every clip?"; "should every animatic now get a second critic pass?"; "make the subtitles bigger in
  every film from now on?"; "from now on, voices are recorded at 48 kHz?"; "switch every film to 30 fps?"; "update the
  house look so mouths draw at rest?"; "add a check sheet step before every clip?"; "change how the sheet is laid out
  for every round?"). Caught: "add a new gate to pre-flight", "make finish.py add the sign-off twice", "write the
  lesson into the rulebook". Routine questions stopped: 1 of 10 ("Which hook text: 1 or 2?": Hook Text is the TikTok
  caption, CLAUDE.md "TikTok").
- How it decides today (source/propose.py lines ~361-416): a line is an ask if it has "?" or starts "Need" AND an ask
  marker (Y or N, Y/N, "1 or 2", "my pick", approve, go ahead, shall I, ok to, Answer Qn). It is a change if the
  question has a CHANGE_RE word (rule, tool, check (not "check sheet"), kit, hook, guide, pack, .py, helper, pipeline,
  workflow, process, "the system", audit, pre-flight ...) or the 6 lines above it do and the question has an action
  verb; but any ROUTINE_RE word in the question (animatic, render, clip, post, budget, check sheet, sheet, "notes on",
  voice, recording) makes it routine first. Words like "every film", "from now on", "always", "every round" (Sam's
  own markers of a permanent change, CLAUDE.md "Rules are permanent") are not used.
- The 5 original replies from the replay cases are all blocked; kittest `proposal_route_hook` (source/kittests.py)
  covers the 15 Nov asks, 5 routine ones, stale/missing verdicts, stop_hook_active.
- A blocked reply is let through on the second try (stop_hook_active) and logged to notes/proposals/unrouted.md, which
  `handover.py end` flags (chat 6). The refusal text tells the chat it may "reword the question to say what it is"
  (install-route verdict F2: an invitation to dodge).
- The hook also detects proposals written this turn from the chat record (`last_turn`), so a reply naming a judged
  proposal passes if it carries the "Critiqued:" line.
- Cost per route run ~1.3% of a week (install-route verdict). A wrong stop costs one rewrite of the reply (unchecked).
- The hook only loads at chat start; it is live from the chat after chat 6.

## Record
source/propose.py
source/kittests.py
notes/proposals/guard-holes/probe.py
notes/proposals/install-route.md
notes/proposal-route.md
notes/proposals/replay/run2
CLAUDE.md
guides/film-quality-rules.md
