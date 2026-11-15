# Proposal: The guard misses most change questions and stops some routine ones

Status: adopted (2026-11-15)

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

## Verdict (the judge, word for word)
<!-- verdict-hash: 48c523d3ec71d3aa -->
Who wrote which (hidden from the judge): V1 = helper A, V2 = chat, V3 = helper B. Picked: V3 (helper B). Critiqued: 7 found, 3 fixed, 4 named.

## Leak
yes: the problem file says the permanence words ("every film", "from now on", "always", "every round") "are not used" and quotes the install-route verdict calling the "reword" line an invitation to dodge. That points straight at two fixes (add permanence words; drop "reword"); V2, written by the chat before the helpers ran, is exactly those two fixes.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 5 | 21 |
| V2 | 2 | 2 | 3 | 3 | 4 | 14 |
| V3 | 4 | 5 | 4 | 4 | 5 | 22 |
## Sam test
Q1: Yes. An expert would measure a classifier on real, independently labelled asks with a held-out half, guard every road a decision takes to Sam (replies and the morning report), and change one thing per yes; that is the pick.
Q2: The evidence is the real record (notes, archive, morning report, two films' chats via list_events), not 22 lines the guarded chat wrote. Checked: 8 real change asks from notes (morning-report.md 43/71/76/82/94, blessed-handovers.md 66, protest-tiers.md 13, sitting-kit.md 142) are not even seen as asks by today's guard.
Q3: Root cause named and checked: the guard reads only replies, sees only lines with "?" or a leading "Need", lets one judged proposal shield every other ask, and judges by topic words that the routine list overrides. Enforced by the hook and the kittest fixture, not by a chat choosing to comply; the labels come from a blind helper, so the guarded chat cannot grade itself.
Q4: Four approaches weighed (patch the lists, a reach test, a model classifier, guard the writes); the fixture decides between the classifier options, and the write-guard waits for evidence.
Q5: Each change has its own yes, its own kittest case and undoes alone. The learning step changes nothing. Sam is not asked to trust a classifier until it has beaten a held-out half.
Q6: The probe numbers, the ask-detection hole, the shield and the morning-report road are checked (re-run here). All costs, the 76-line count (V1) and the 50-commit count (V3) are unchecked and marked so.
Q7: Sized to zero missed change asks on real wording, not to a word patch; about 5-6% of a week once, stated plainly.
Q8: Every change is permanent on its yes and reviewed against the film's results at the end-of-film review; nothing is a trial.
## Pick
V3
## Why
V2 is the leaked word patch: tested only on the 22 invented lines, it leaves the two biggest holes (most real asks are not detected as asks at all; a judged proposal shields every other ask) and bundles four changes into one yes before anything is measured. V1 and V3 both see that the real decision is whether an unjudged change can reach Sam anywhere in a film, both learn first and both split the changes. V3 goes wider on the unit that sets the result: the morning report, where overnight decisions go to Sam by design (overnight-run.md line 14) and which the Stop hook never reads; 5 of the 8 real asks checked live there. V3 also has the labels made by a blind helper, not by the collecting chat. V3 misses the shield, a confirmed hole (a reply naming a judged proposal with its Critiqued line lets "Shall I add a new rule to the rulebook? Y/N" through; checked). Taken from V1: the shield removal (C1), the reach idea as a candidate classifier (a change outlives this film), and the order that wider ask detection lands only after the classifier, so wrong stops do not multiply.
## Faults in the pick
- F1 [fixed] V3 left the shield in place: one judged proposal named in a reply let every other ask through. Added as its own change (from V1).
- F2 [fixed] V3 widened ask detection before the classifier; with today's lists that risks new wrong stops ("hook" in Hook Text, change words in routine Decide lines). Reordered: classifier first, then wider detection.
- F3 [fixed] The fixture leant on notes copies; the replies' real wording is unchecked. The pick takes list_events replies as the primary source and notes copies only where no reply exists.
- F4 [named] The held-out half may be small; "0 missed" on a handful of cases proves little. If the test half holds fewer than 30 change asks, the probe's 12 and the replay cases are added and the size is said to Sam.
- F5 [named] The write-guard (D) overlaps Sam's adopted rule that unasked changes are judged at the end-of-film review; it is only built if that review finds an unjudged system commit, and then through its own route run.
- F6 [named] Five separate yeses over time; each comes in the one numbered decision message, not as separate interruptions.
- F7 [named] All costs are unchecked estimates.
## Final version
**Learn (changes nothing, no yes needed).** A Sonnet chat collects every decision put to Sam: replies from the Protest Tiers and Blessed chats (list_events, primary), then notes/, notes/archive/ and notes/morning-report.md. A blind helper labels each "change" (rules, tools, checks, kits, how films are built, or anything that outlives this film) or "routine", with a one-line reason. The set becomes a kittest fixture split into a build half and a test half (at least 30 change asks in the test half, topped up with the probe and replay cases if short). Today's guard, a reach test and a small model classifier are scored on it. About 2% of a week (unchecked).

**Then one change per yes, each with its own kittest case and its own undo:**
- **A, no shield.** Each change ask must name its own judged proposal. Beat: a reply with one judged proposal and one unjudged change ask is blocked.
- **B, the refusal names only the route** (no "reword"). Beat: no reworded repeat of a blocked ask in unrouted.md over a film.
- **C, the classifier** (reach-test word rules or the model, whichever wins on the test half). Beat: 0 change asks missed (test half plus the probe's 12); at most 1 in 50 routine asks stopped; the 5 replay replies still blocked.
- **E, wider ask detection, after C:** numbered lines, Y/N without "?", "Needs Sam", "Decide", and lines added this turn to notes/morning-report.md (the hook already sees files touched this turn). Beat: every fixture ask detected, no new routine stops.
- **D, only if the first end-of-film review lists an unjudged system commit:** a check on writes to system files without a verdict, through its own route run. Beat: 0 such commits per film.

Running cost near zero unless the model wins. Total about 5-6% of a week once (unchecked). Each change is reviewed at the film's end.
## For Sam
### Option 1: Measure on real questions, then close every road
First a chat gathers every yes-or-no question really put to you in the last two films, including the morning report, and an outside helper marks which were back-end changes. The guard is tested on that, then fixed one piece at a time, each with your yes: one approved proposal can no longer wave others through; it stops telling chats to just reword; it learns to tell a change from a film question; it reads every way questions reach you, the morning report included. Today it misses nearly all real back-end questions because they are written as "Decide:" or "Y/N" lines it does not read. You would notice: every back-end question arrives already judged, with its plain explanation; film questions pass untouched.
Lost: about 5-6% of a week, once (estimate); a few separate yeses, in one message each time.
Added: a test set of your real questions, a guard proven on it, and the morning report under the guard.
### Option 2: Same, but replies only
The same measure-first plan, but the guard keeps watching only chat replies, not the morning report. Slightly smaller, and it still closes the "one approved proposal waves others through" hole.
Lost: decisions sent through the overnight morning report stay unguarded; about 5% of a week, once (estimate).
Added: a test set of real questions and a guard proven on chat replies.
