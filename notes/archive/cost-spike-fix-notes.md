
# Moved from notes/cost-spike-fix.md (27 Nov, cost tests chat 3)

## Measured on the code (27 Nov)
| what a fix touches | before: one text search | before: searches to trace it to its tests (at least) | after |
|---|---|---|---|
| people.head_faults | 10 lines in 5 files | 1 (2 kit tests; 4 functions lead to it) | 1 step, 7 lines |
| handcheck.head_faults | 10 lines in 5 files | 10 (12 kit tests; 64 functions) | 1 step, 8 lines |
| moves.seated | 446 lines in 90 files | 9 (3 kit tests; 161 functions) | 1 step, 9 lines |
| faces.house_mouth | 5 lines in 2 files | 42 (40 kit tests; 325 functions) | 1 step, 7 lines |
| views.face_box | 4 lines in 2 files | 39 (38 kit tests; 580 functions) | 1 step, 7 lines |
The "before" trace count is a floor (one search per function on the path, none wasted); real chats did worse.

## Kit tests before and after (27 Nov, the whole suite on both copies)
- Old copy (main line before today): 207 passed, 5 failed. New copy: 217 run; 8 failed at first.
- Both copies: head_moves_not_comic, early_move_size, movers_never_meet_head_on, side_by_side_out_of_reach (the
  Brexit film as it stands; not this job's). Old copy only: people_from_a_description (a git name missing in a
  side copy).
- New copy only, all four mine and fixed (each passes now): watcher_catches_last_weeks_four (the new tools had no
  promise line), finished_films_keep_their_bookmark (the freeze count read the 9 topic files as 9 kit files),
  check_audit_lists_and_flags_repeats and critique_saw_it_column (touch.py's own test left a stand-in loaded).
- App figure for this chat: $7.86; the estimate $8.81 (12% over, so not flagged). One chat proves nothing yet.

- 5c (chat 2), the whole suite on both copies: old copy 218 passed, 6 failed; split copy 217 passed, 8 failed at
  first. Both: the four Open Wounds film checks above (not this job's). Old only, fixed here: watcher (three tools had
  no promise line) and maps (a stale MAP). Split copy only, all four the code finder, all fixed and passing:
  page.files followed a module's imports but not its parts' (solid_seat fell out of reach), a page built before that
  fix (the finder now rebuilds its page when it changes itself), and the tool-health replay compared a part's name
  with last week's edit to the whole module.

## Handover check settled (end of chat)
- 95 QUICK CHECK lines on 20 finished films: their code only gained a MAP at the top (no code changed, ast-proved);
  the faults are theirs from before (rule 61: finished films are not retrofitted). Not fixed, on purpose.
- Branches named, not merged (logs and one-off files, none of this job's): claude/jolly-ramanujan-2lcl2o,
  claude/upbeat-dirac-w16tn9, claude/gta-v5-sound-draft, claude/gta-chat46-build, claude/dreamy-fermi-vkhutz,
  claude/gta-chat31.
- RECORD "pre-flight ran on and": a false read of a command line here; no pre-flight ran in this chat.
- PUSH: sent at the handover. COST: recorded (above).

## Replay test (27 Nov)
Kind: tool test. Locked by Sam: no film, shot, camera or beat is touched; the replay is on a throwaway copy (worktrees
at each fix's parent in the scratchpad; none of their code pushed). Widened from 2 to 5 notes by Sam's change (via
the parent chat, 27 Nov).

| note | kind | steps (aim 10-18; chat 30 ~35) | stuck on | vs the original fix |
|---|---|---|---|---|
| 19 Tony's hands hover | touch (hand on armrest) | 19 | 3 steps finding how to draw the shot (frame_image is the action layer; ALONE/blair_shot) | same cure (hand 24 below the forearm line vs 22, onto the front end); chat 30 ALSO added the check `sitting.armrest_faults`: theirs better |
| 21 Kemi's face lines | face / likeness | 16 (incl. ~4 on the test runner) | page.py found the shot but not the face code (`touch "find age"` did) | same look (lines off; mine an `off` list in her pick record, theirs age_boost 0); chat 30 ALSO added `facehouse.line_faults` for any darker skin ranked top: theirs better |
| 24.1 May's sharp head dip | movement / timing | 14 | finished films' moves changed (kit test caught it); copied the posted-films switch pattern | same cure (minimum rise/settle for head moves: mine 0.25 s on nod/roll/lean, chat 38 0.2 s per move); about equal |
| 23.4 wolves/guests clip | meeting / order | 10 | nothing; measured order flips instead of eyeballing | same core (corridor drawn far to near); chat 37 ALSO a guest-before-wolf tie-break and repaired the overlap check (guests merged under one name, wolves unrecorded) as Sam asked: theirs better |
| 28 leap lost off-frame | set / prop | ~8 | nothing; found and fixed a new fault my change made (he vanished mid-air at +0.6 s) | identical numbers (scaffold -5, frame -4, leap 3.88 s); chat 42 ALSO a check that the leap stays in frame |
`notesteps.py report`: 7 marked items, 12 steps each on average; the five notes 19, 16, 14, 10, ~8 (mean ~13). Admin
(choosing notes, comparing): 3 + the write-up. Tool fix: 12.

- Cost: get_session gives no money figure for this chat (only "weekly limit: warning"), so `ledger.py appcost` was
  not run: nothing to record honestly. Steps are the measure here.
- Tools as meant: notesteps (yes; the 12-step nudge fired 4 times, twice on a note that was not stuck), page.py
  (found the film call for 4 of 5; missed the shared face code), touch.py (used before every shared edit; its
  tests list was right; once said 28 tests where the run picked 40), RERUN line after an edit (never appeared: my
  edits were scripted inside the throwaway copies, which the hook does not watch; I used touch.py's line instead).
- Misled: `kittests.py --touching` on an older copy ran 0 tests and printed "all passed"; a word filter did the same.
  Fixed in the shared runner: a filter that picks nothing fails, a missing name is named (kit test `kittests_zero_run`).
- What the test cannot show: the replays knew the notes' history (I saw one-line summaries of chat 30's and the
  others' fixes in the notes archive and commit subjects while finding them); no Sam review; one chat; the main
  quality gap is the same in all five: I fixed the picture but added no check, which the fix pack's step list does
  not ask for (rule 30 / "Seeing like Sam" 3 do). Next: add "name and add the check" as a step in guides/fix-pack.md.
- Kit tests: note 19's 7 (2 failed before the change too); 24.1's 2 and 28's 1 pass; note 21's run
  finished: 28 run, 23 pass, 5 fail (2 failed before, 1 a side-copy git name, 2 hold Kemi's old face on purpose).
- Sam's Y (27 Nov) to "why nobody saw it, on every note": fix pack step 4 added (aim now 12-20 steps a note);
  its check `handover.nocheck_faults` (a fixed note's row must name its check: "Check:", "prevention" or a kittest,
  or "No check: why"), run by `handover.py end`; kit test `fix_names_its_check` (example: the replay's own close
  line). No live film notes flagged.

## Savings 1-4 (Sam's go, 27 Nov), built after the replay
- 1. `source/still.py FILM T [--box] [--after]`: the look cut from the last clean render (the animatic runs on another
  clock: 33.9 s against 35.5 s, its first cut landed 1.9 s off), the code's new frame beside it; `page.py show --at`
  prints the LOOK line. Kit test `still_from_last_render`.
- 2. `page.SAME`: Sam's everyday words -> the code's ("wrinkles" now finds agelines.draw second; it found nothing).
  Kit test `finder_knows_sams_words`. The list grows from notes the finder misses.
- 3. Fix pack step 5: long test runs in the background, the next note started meanwhile.
- 4. `kittests.py`: a pass prints nothing (a count, names if 8 or fewer), failures as before (handover reads them);
  `--verbose` for the old form.
- Not yet measured: the next real notes round is the test (`notesteps.py report`). Cost watch went amber at 160 steps
  (2.3% of the week) in this chat; handed over at the end of this build, nothing left mid-way.

- Handover check answered: finder reach: handover.py, page.py, still.py (tool job: the finder was run on Brexit to
  test the word list, never to find these tools' own code). COST: get_session gives this chat no cost figure (only
  "weekly limit: warning"); the cost watch said about 2.3% of the week at 160 steps. Nothing recorded by guess.

