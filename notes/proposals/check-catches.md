# Proposal: Record what every check catches, so retiring a check is decided on evidence

Status: adopted (2026-11-19)

## Problem
Sam's rule is to remove a step only if it caught nothing in three films, with his Y. That cannot be followed: there
is no usable record of what each check has caught, in which film, and whether Sam would have seen the fault if the
check had not been there. Without it, checks that never catch anything keep costing every chat, and a check that
saves Sam a note could be retired by mistake. Another job (job 1) is surveying every stage to propose what to
retire, and will need this record.

## Facts
- CLAUDE.md: "remove a step only if it caught nothing in three films, with my Y on a 'Lost:' line."
- Every film ledger's per-check field "checks" is empty: {} in all 27 notes/ledger/*.json (counted 19 Nov,
  including milburn, protest-tiers, blessed).
- A per-check counter exists: source/ledger.py record() (lines 105-126), called by source/report.py:68 for every
  check, counts runs, faults and fault kinds per check. It only works while a round is open: current() reads
  notes/ledger/.current, written only by `ledger.py round FILM N` (ledger.py ~line 890). That file is absent in a
  fresh copy (checked 19 Nov: not on GitHub), so in every new chat (each a fresh container) the counter silently
  saves nothing. Milburn had 0 rounds (milburn.md).
- "quick_checks" (source/handover.py:390-395) stores only a fault total per run, no check names: Milburn 14 runs
  (8, 4, 4, 1, 1, 0, 13, 13, 13, 13, 11, 11, 48, 48); Protest Tiers 13 runs.
- Critique passes (rule 89's fresh-eye critic) are recorded with their fault text: Milburn 6, Protest Tiers 8,
  Blessed 7, remakes_sets 9 (ledger "critique"); round files notes/ledger/milburn/round-1.txt, round-2.txt hold text.
- Chat rows carry "notes" and "repeats" (Sam's notes and repeated notes per chat); Milburn: 0 notes, 0 rounds.
- Nothing records whether a fault a check caught would have reached Sam, or which of Sam's notes a check should
  have caught (a miss).
- Checks in source/: checks.py, clipcheck, handcheck, hookcheck, kitchecks, kittests, linecheck, lookbook_check,
  musiccheck, nametest, posecheck, setcheck, viewchecks, blessed_checks, preflight.py, handover.py's quick checks.
  No "checktests" file found.
- Job 1 (surveying every stage, proposing what to retire): no proposal file in notes/proposals/ yet (checked
  19 Nov ~17:30 UTC on the main line).

## Record
notes/ledger/milburn.json
notes/ledger/milburn/round-1.txt
notes/ledger/protest-tiers.json
source/ledger.py
source/report.py
source/handover.py
source/preflight.py
source/checks.py
guides/film-quality-rules.md
notes/proposals/late-faults.md

## Verdict (the judge, word for word)
<!-- verdict-hash: e4d2b9b772d580e3 -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper A, V3 = helper B. Picked: V3 (helper B). Critiqued: 6 found, 2 fixed, 4 named.

## Leak
yes: the title and the Problem name the answer ("record what every check catches") and the Facts point at the counter's fault (the missing marker file), which anchors toward "fix the counter". V2 and V3 named it and widened the frame; V1 did not.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 3 | 2 | 3 | 3 | 4 | 15 |
| V2 | 4 | 4 | 4 | 4 | 5 | 21 |
| V3 | 5 | 4 | 4 | 4 | 5 | 22 |
## Sam test
Q1: Yes. An expert measures what a check keeps from Sam (catches that would have reached him, misses, noise, time), and measures it now by replaying past films, not by waiting three films for a counter.
Q2: Yes. Today's checks on the last three finished films (64 chat branches exist for Milburn, Protest Tiers, Blessed), with Sam's real notes as the misses. That is the evidence the retire rule asks for.
Q3: Mostly. Root cause shown (record() returns silently without notes/ledger/.current; the kittests fake that file, so they pass; the notes count needs a typed --notes no chat typed). Both changes are enforced by handover refusals and a fresh-copy test, not by a chat choosing to read something. "Would Sam have seen it" stays a proxy (named).
Q4: Yes. Counter fix, notes-first reframe, replay, hand scoring from the record and switching checks off were weighed; replay plus the two fixes is the best of them.
Q5: Low. The replay is read-only and retires nothing; each change is its own Y and undoes alone. Nothing asks Sam to trust an unshown tool: the replay method already ran on 16 Nov (late-faults-replay.md, 149 of 151 faults visible).
Q6: Facts checked: checks {} in all 27 ledgers; notes 0 in every chat row; 15 round files, critique only; record() lines 105-126; kittests 970/2679/2872; Milburn has notes 1-11 in its archive; the 13 Nov audit cost 3.24%. Costs and the proxy are marked unchecked.
Q7: Yes. The counter alone gives no misses, no noise and no evidence for three films; this is sized to deliver a verdict per check now.
Q8: Yes. The replay is a reading, not a trial; both changes are permanent and reviewed at film end.
## Pick
V3
## Why
V3 is the only version that gets three films of evidence today by replaying today's checks on the past films' code (a method already shown to work on 16 Nov), and it fixes both silent records at the root, each on its own Y. V1 bundles four changes into one yes, waits three films for any answer, and leaves miss-tagging to a chat's goodwill. V2 is close but scores from the existing record by hand, which mostly holds critique text, not check results, so its "could not tell" share would be high. Taken from V2: the false-alarm (noise) and run-time columns in the replay table, since noise is a real cost (Blessed's 99-fault pre-flight stage cost 9.8% against 2% planned); each fault's fate (fixed, named, allowed) from comparing runs in change 1; change 2 coming after change 1 has run on one film.
## Faults in the pick
- F1 [fixed] V3's table had no noise or time column, so a noisy, slow check could look as good as a useful one; added from V2.
- F2 [fixed] Change 1 recorded counts but not what happened to each fault; fate from comparing runs added (V2).
- F3 [named] "Would Sam have seen it" is a proxy (visible at phone size in the animatic frame); no record says what Sam would have noted.
- F4 [named] Older branches may say "could not test" (clipcheck did on three Protest Tiers chats); those pairs are counted as unknown, not as clean.
- F5 [named] Replay cost (3-5% of a week) and change costs are unchecked estimates.
- F6 [named] Eye-only faults have no machine check; they show up only as misses with "none".
## Final version
**Learn first (read-only, its own Y).** One Sonnet chat per film, for Milburn, Protest Tiers and Blessed, re-runs today's checks on each chat branch, as the 16 Nov late-faults replay did, and writes one table, one row per check: runs; faults listed; false alarms; faults gone before the animatic Sam saw; faults let through (named or allowed); Sam's notes it should have caught (misses, from each film's notes table); run time; could not test. "Would Sam have seen it" = visible at phone size in the animatic frame (a proxy). Bar to beat: a sourced answer for at least 80% of check-film pairs. The table goes to job 1; a check with nothing caught on three films goes to Sam with a Lost: line. About 3-5% of a week once (unchecked), filed as tool work.

**Change 1: a record that always saves (its own Y).** Each check run saves under the film named in its command, with no marker file, each check under its own name, and each fault's fate from comparing one run with the next (gone after a fix = caught; named or allowed = let through). It prints a line if it cannot save. The handover check refuses when pre-flight ran but the record is empty; a test runs it in a fresh copy with no marker file. Bar to beat: on the next film, every check run has a row (today 0 rows against Milburn's 14 runs). About 1.5-2% once (unchecked).

**Change 2: Sam's notes counted and tagged (its own Y, after one film of change 1).** The handover check counts Sam's numbered notes into the record and refuses while any note lacks "should have caught: CHECK / none". Bar to beat: the count equals the notes table (Milburn today: 0 against 11), and no repeat of a tagged miss on the next film, checked at the end-of-film review. About 1% once.

After these, near nothing per chat. Nothing is retired by this proposal.
## For Sam
### Option 1: Test the checks on the last three films now, then make the record automatic
A short chat per film re-runs today's checks on how Milburn, Protest Tiers and Blessed were built, and makes one table: what each check caught, what it wrongly flagged, how long it took, and which of your notes it should have caught. That tells us now which checks earn their keep, instead of in three films' time. Then two fixes, each on its own yes: the checks save their results every time (today they silently save nothing), and each of your notes is tagged with the check that should have caught it.
Lost: nothing is retired yet; about 3-5% of a week once for the three replays (an estimate).
Added: a per-check table for three films; an automatic record on every film; a "should have caught" tag on each of your notes.
### Option 2: Score the checks from what is already written down, then the same two fixes
One chat reads the notes and records of the last three films and sorts each check's results by hand into real catches, false alarms and misses, the way the 13 Nov pre-flight review did. Cheaper to start, but the records hold little about the checks, so many answers would be "could not tell".
Lost: a firmer answer now; some checks left unjudged until three new films have run.
Added: a hand-made per-check table (about 2.5% of a week, an estimate); the same automatic record and note tags.
