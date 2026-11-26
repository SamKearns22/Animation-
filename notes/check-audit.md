# R8, the check audit (Sam, 26 Nov; job text: notes/next-jobs.md R8)

Kind: tool job. Report for Sam: notes/check-audit.html (published https://claude.ai/artifact/Ltwkh5GG4vT1HxZThJaMH4).
Listing: `python3 source/checkaudit.py` -> notes/checks/audit.tsv (498 checks); `--repeats FILM`; kittest
`check_audit_lists_and_flags_repeats` (passed once, 3 s).

## Evidence (26 Nov)
- Open Wounds "should have caught": none 22, AUDIT pops 1 (note 15), house look 1 (note 16). GTA and Milburn notes
  have no such column (it began 20 Nov).
- notes/ledger/brexit-is-done/checks.jsonl (12 runs from 25 Nov): 372 fault lines, 361 (97%) repeats on 3+ runs:
  layers (viewchecks.layer_faults: ground, frame, pipes, panelling, doors "nearer" than people) 30; captions 8;
  pop-in 4 (doorways); bookcases size 2; benchmark/plan/house-style "film has no X" 1 each; may/blair linecheck
  "edge with no line" 1 each; kit inputs crash (git clone) 1.
- notes/logs/handover-end.log: 430 handovers, 65 refused: kit-test machinery 37 (still running 21, could not run
  16), CAST SHEET 24 (seated 'no bum' and flat leg tone, judge on May 3/4, CROTCH kemi front 0.96 on 26 Nov),
  RULE 8, MOVE TO SHARED 5, UNROUTED 1. No other handover check ever refused.
- kittest reds: body_check_back_view (4, 23 Nov), finished_films_keep_their_bookmark (5): test or kit wrong? unknown.

## Suggestions (report ids; Sam's answers go here)
A prevent in the kit: A1 depth order + flat backdrops never "things" (layer_faults); A2 subtitles auto-split;
A3 acting sizes from camera distance (movesize to kittest); A4 hair/hats open curves, then delete
castsheet.hair_spike_faults, mouth_spike_faults; A5 crotch limit in the body kit (look at kemi front first);
A6 one line weight for every kit (house_ctx like wolf.house_ctx); A7 cuff limit in limbs (confirm what exists);
A8 one ffmpeg join tool at 24 fps (rule S4).
B smarter: B1 say-once (report.group + stills); NO 'Reopened' list: Sam declined that 26 Nov 20:19 (notes/ledger/sam/j4bxb2vq.md: "if something changes, it should just recheck the new film and recognise that it is fine again"); Q2 re-asked in his terms; B2 door-aware
pops (notes/proposals/check-knows-intent.md); B3 bookcases: not its own check, an input fault in sizes.py PROP_SIZES (the film lists a wall of shelves as kind 'bookcase', one 0.8 m bay): describe it as a row of bookcases (fix the input, keep the check); B4 one planning list (preflight.gates,
gate_warnings, benchmark/plan/audits nags, rule 8/61/74 warnings); B5 castsheet_faults only for new/changed cast;
B6 kittest_gate_faults only at film start/end (kitfilm); B7 kitinputs local copy; B8 look at linecheck May/Blair.
C merge: C1 finder (keep finderwarn hook; drop watcher.finder_faults, handover.finder_faults); C2 drop
watcher.guard_faults; C3 drop watcher.saver_faults; C4 kitfilm only (drop watcher.kittest_faults, handover's copy);
C5 watcher.hook_faults + ran_faults into one; rule_faults stays.
D dead: D2 handover.dearest_faults, cost_faults (alarms paused; Q5); D3 kittests of deleted checks go with them.
E keep: kittests; critique and judges (+ column "Sam noted it too?"); R7 seated checks until R7; loss-guards
(sentence, saver, draft, kept_report, tag); old films' own checks.

## Where things stand
- Rules that bite next: 86 (every tool a kittest), 13 (checks in the shared kit), 85.
- Done: listing tool + kittest + catalogue row; evidence gathered; report sent to Sam.
- Next: on Sam's answers, a tool chat (Opus medium) does the Y'd items one at a time, A first, each with its
  kittest and a "Lost:" line; nothing is deleted without his Y.
- Sam's answers: Q1 Y (26 Nov: move group A into the kit, one at a time, each with its kittest).
- Missed (26 Nov): Q2 first offered a 'Reopened' list Sam had already declined; I read only the top of answered-faults-return.md (the decline is its last line) and searched no saved messages. Before any proposal: grep notes/ledger/sam/ and the proposal's last lines.
- Q2 and Q3 merged (26 Nov): Sam asked whether Q2 already had a proposal and whether Q3 was agreed. Chat 36 record (session_01J1JB7YNoonB7shJ4bXB2Vq, read 20:29-22:18): check-knows-intent asked 20:30, re-asked 4 times, never picked (21:00 Sam asked only whether option 1 applies to all films); his 22:14 '1. Y' answered the seeing-tools re-run. Say-once (B1) is part of check-knows-intent option 1 (recheck and recognise meant as fine), so one question.
- Sam's answers: Q2/Q3 option 1 (check-knows-intent, includes say-once B1 and doors B2); resting-hand faults discarded ("I don't see anything wrong their resting hands, discard.").
- Needs Sam: Q4, Q5; seeing-five-candidates 1 or 2 (chat 36) in the report (going one at a time, in simple words, Sam 26 Nov).
- Read: guides/job-packs.md "A tool job"; this file; the report.
- Open rule requests: none.
- COST: a tool job, no film estimate.
- Named: branches claude/gta-v5-sound-draft, claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31
  not merged (outside this job, as named before). Open Wounds chain (chat 39) untouched.
- For Claude: kittest name check_audit_lists_and_flags_repeats; evidence() keys picture-layer faults as
  'layers (drawn over, rule 17)'.
