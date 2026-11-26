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

## Sam's answers (26 Nov)
Q1 Y (group A into the kit); Q2/Q3 merged: option 1 of check-knows-intent (includes say-once B1 and doors B2);
resting-hand faults discarded; Q4 Y (B3-B8, C1-C5); Q5 2: DELETE the paused budget alarms (forecast, stage stop,
dearest weekly list, cost warnings, their kittests; rulebook row 24 reworded to "tracked quietly"); keep the quiet
tracking (costwatch, ledger auto, the cost line recorded).
Work order (each item with its kittest and a Lost/Added line here): Q5 deletions; C1-C5; B6, B5, B7;
check-knows-intent step 1 (sort every Open Wounds flag: meant, real, unclear; nothing changes), then steps 2-3 with
say-once; B4; B3; B8; A2, A6, A4, A5 (Kemi front first), A3, A7 (confirm first), A8. Kit tests at the job's end only.
<<<<<<< HEAD
Plain words (Sam 26 Nov, Y): CLAUDE.md rule rewritten ("checked on every message"); FIRST job of chat 2: build the every-message checker (a Stop hook like propose.py hook: blocks once, never loops, logs a let-through), with a kittest that catches notes/learn/plain-words/bad-1 and bad-2 and passes good-1; Sam's "I don't understand"/"explain" saves the message he replied to as an example (handover.py log sees his words) and adds its words to the list; rule_proofs N8 status owed until then. Still to ask Sam: one question at a time as the normal way (1, my pick) or all in one message (2); the critique column Y/N.
Plain-words checker BUILT (chat 2, 26 Nov): source/plainwords.py, a Stop hook on every reply plus a learn hook on Sam's messages; kittest plain_words_every_message passed once (0 s); rule_proofs N8 now proven. Catches bad-1 (R8, kit, pop-in) and bad-2 (kit tests, R7, critique), passes good-1. On the 19 Nov cases: catches 5 of the 8 Sam was confused by; misses S-cold-start, S-cost-other, S-finder-learn-finish (no code or listed word; dense ideas: only a reader that retells the message can catch those, plain-check Change 3).
Lost: a reply with a code name, label or unexplained project word costs one rewrite before Sam sees it; code names only on a "For Claude:" line.
Added: every reply checked; a log of let-throughs (notes/logs/plainwords.log); Sam's confusion grows the word list itself.
Q5 DONE (chat 2, 26 Nov): deleted the forecast, the budget stop and the stage stop (ledger.py), the cost warnings and the no-estimate nag (costline.py: the line is still recorded, never shown), the weekly dearest list and its handover nag (dearest.py due/week, handover DEAREST; the film-end ranking stays), the STAGES nag; kittests estimate_forecast_and_alarm and stage_share_stop deleted, quiet_cost_line rewritten (recorded, nothing shown), handover_status_checks now expects no stage nag; rulebook row 24 and CLAUDE.md's chain line reworded (no budget stop). Tests passed: quiet_cost_line, dearest_things_named, cost_rows_reach_the_main_line, handover_status_checks, rule_proofs_gate, check_audit.
Lost: any cost reading or stop in chats, and the weekly ranking of the dearest things (Sam can still ask for it).
Added: nothing; the ledger and cost line keep recording quietly.
Sam's words carried (handover start, chat 2): 22:19 "Let's move through these one at a time in simple language" is his reply to bad-1 (saved there) and leans to one question at a time (the parent chat asks it formally); 22:21 "We have discussed reopened as a concept before in another chat": carried as B1 above (no 'Reopened' list; he declined it 26 Nov 20:19).
=======
Plain words (Sam 26 Nov, Y): CLAUDE.md rule rewritten ("checked on every message"); FIRST job of chat 2: build the every-message checker (a Stop hook like propose.py hook: blocks once, never loops, logs a let-through), with a kittest that catches notes/learn/plain-words/bad-1 and bad-2 and passes good-1; Sam's "I don't understand"/"explain" saves the message he replied to as an example (handover.py log sees his words) and adds its words to the list; rule_proofs N8 status owed until then. Sam's answers (26 Nov): one question at a time Y (CLAUDE.md line added; rule_proofs W_one_question owed to the checker: more than one question = send back); the critique column N (dropped).
>>>>>>> origin/claude/create-claude-md-oe8z4g
Extra (Sam 26 Nov): E1 Y: find why body_check_back_view and finished_films_keep_their_bookmark keep going red; fix the test or the kit.
Lesson (Sam 26 Nov): "This is the way you should be explaining things in all messages to me": what a thing is in everyday words, one question at a time, no item codes. My first Q1-Q5 and E1/E2 asks used report labels and jargon; CLAUDE.md names plain-check option 1 as the next step when this slips.
Named branches (not this job, not merged): claude/brexit-chat39 (Open Wounds chat 39, live),
claude/gta-v5-sound-draft, claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31.

## Where things stand
- Rules that bite next: 86 (every tool a kittest), 13 (checks in the shared kit), "Fix the drawing, never the shot".
- Done (chat 1): listing tool, kittest, catalogue row; evidence; report sent; Sam answered all five.
- Next: R8 chat 2 (opened: session_01J1JB7W1VqXUHMQUcpFV4zp, Opus medium, the Animation- project attached): the plain-words checker first, then the work order above, one item at a time.
- Needs Sam: nothing for R8 (seeing-five-candidates 1 or 2 is Open Wounds chat 36's, still open).
- Read: guides/job-packs.md "A tool job"; this file; notes/proposals/check-knows-intent.md option 1.
- Open rule requests: none (Q5 rewords rule 24 on Sam's 2).
- COST: a tool job, no film estimate.
- For Claude: kittest check_audit_lists_and_flags_repeats; chat 36 record session_01J1JB7YNoonB7shJ4bXB2Vq.
