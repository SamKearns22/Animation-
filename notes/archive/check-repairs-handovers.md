# Check repairs: old handovers

## Where things stand (21 Nov, status chat, Opus)

## Where things stand (21 Nov, status chat, Opus)
- Cost audit (21 Nov): done, waits on Sam's picks (see Budget tracker audit). Branch claude/check-repairs-2 = chat 2's
  live work, left alone; check-repairs has no cost estimate (none was set).
- Rules that bite next: 30 (a test failing twice: find why the first fix failed), "Seeing like Sam" 2 (a check is done
  only when it catches the note that taught it), "Rules are permanent" (remove a check only with Sam's Y).
- Done: the seven items ticked above, on the main line; kittests 94 pass / 11 fail before this chat's new test.
- Next: Opus, medium effort. First the 'built but not enabled' fix above (a-d), then one by one, find why each fails, fix the kit or the stale
  test, rerun it and `python3 source/kittests.py` in full at the end: body_check_shot4_v4 (old shot 3 now has 6
  faults, probably real crossed arms the newer check catches: confirm on the picture), focus_front_heads (broken by
  the 20 Nov people-kit default change), pose_gallery, lopsided_invented_only, turned_heads_for_anyone, round_page,
  people_from_a_description (4K vs 1080 image crash), places_ and moves_from_the_acting_list (milburn.py uses the
  kit before Sam's Y: name or fix), facehouse_whole_head, outfit_every_view (officer and scarf missing at 45-180).
- Needs Sam: Y/N to switch the budget alarms back on (paused by him 18 Nov).
- Read: this file only; `python3 source/kittests.py NAME` per test; each test's docstring says what taught it.
- Open rule requests: none from this job (GTA's held-object check stays in its own notes).
- For Claude: new code in source/handover.py (size_faults, ledger_faults, push_faults, turns() failed ids, NOT SENT
  regex), source/watcher.py (hook_faults unwired, PROMISES), .claude/settings.json PreToolUse Bash modelguard.


## Where things stand (22 Nov, cost audit chat 2, Opus medium)
- Rules that bite next: the proposal route (Sam picks only from judged options), 85 (cost watch), 30.
- Done: Sam's picks 1-3 routed and judged (see "Cost audit chat 2 found"); the route costs about 1% of a week per
  proposal; week check: 205% at one week size, cause most likely the week size; dearest_faults promise listed.
- Next: on Sam's answers, Opus medium builds the options he picks (each option 1 is a measuring step first).
- Needs Sam: an option (1 or 2) for each of the three; one reading of his usage meter (% and reset day).
- Read: this file's "Budget tracker audit" only; `propose.py show dearest-grand-theft-autism-N`.
- Open rule requests: none.
- For Claude: still open, dearest.py numbering (save the shown list; --open reads it). Watcher BROKEN saver line
  (20 Nov 03:29) is named in notes/proposal-route.md. claude/check-repairs-2 left alone (another chat's live work). Handover
  flags named: SENTENCE (CLAUDE.md's "Choose views" line still there, now with Sam's 21 Nov aside), COST (no estimate set for this job).

