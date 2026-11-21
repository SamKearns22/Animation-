# Check repairs (Sam, 21 Nov: "Everything else needs step by step checking, fixing, testing, and reporting back to me")

## Brief checklist
- [x] Budget tracker: stages never marked and chats never logging notes. Handover check now flags both (LEDGER, STAGES);
      GTA stages opener..animatic1 marked afterwards from the chat order (approximate). The cost line then showed real
      overruns: board 2.3% against 0.5% planned, moves 19.2% against 11.3%. The budget stop works when tested, but
      Sam paused all budget alarms on 18 Nov (ledger.py ALARMS_PAUSED) "until system fixed": his call to switch back on.
- [x] Renders not handed to Sonnet: the model guard (.claude/hooks/modelguard.py, Sam's Y 17 Nov) was never wired
      into .claude/settings.json, so it never ran. Wired now; the watcher flags any promised hook left unwired.
      In GTA the whole-film animatics did go to Sonnet; Opus chats rendered their own clips, which the rules allow.
- [x] Notes over 4,000 words and handovers over 15 lines: no check existed. size_faults in handover end now
      (also requires the "Open rule requests" line).
- [x] Chat 26 told Sam "I sent you a short clip" but the send was refused (the body check's send gate: faults not
      named). Refused sends no longer count as sent; wider "sent" wording. Chat 27 told to re-send.
- [x] No push notification at handovers: push_faults in handover end.
- [x] kittest handover_status_checks; watcher_catches_last_weeks_four passes again (promises added).
- [ ] The 11 other failing kit tests (below).
- Plain words, one wait per render, repeat notes (rule 30): looked at chat 26's last message and waits; followed.
  Rule 30: the arm note came a fourth time; the chat said why the earlier fix failed (camera fix covered only the
  shooting). The ledger never counted repeats: LEDGER fault now makes each chat log them.

Handover check on this chat (named): three NOT SENT lines are this chat reporting OTHER chats' sends (a status
chat's words; the wider wording catches talk about sending: watch for false flags on film chats); COST: a back-end job
has no estimate; RECORD "pre-flight ran on gta": only test text naming preflight.py, nothing ran; PUSH: sent at the end.

Changes made without a proposal (for the end-of-film review): every item above, all on Sam's 21 Nov instruction.

## Where things stand (21 Nov, status chat, Opus)
- Rules that bite next: 30 (a test failing twice: find why the first fix failed), "Seeing like Sam" 2 (a check is done
  only when it catches the note that taught it), "Rules are permanent" (remove a check only with Sam's Y).
- Done: the seven items ticked above, on the main line; kittests 94 pass / 11 fail before this chat's new test.
- Next: Opus, medium effort (fixes from a clear list). One by one, find why each fails, fix the kit or the stale
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
