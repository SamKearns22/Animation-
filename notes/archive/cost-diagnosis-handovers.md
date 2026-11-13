
# Handover replaced 13 Nov (cost job chat 1)
## Where things stand (the ONE handover)
- **Rules that bite next:** 85 (cost watch: it measures a chat, never a film), 24 (estimates from real costs), 74.
- **Done (13 Nov, diagnosis chat, Sonnet then Opus):** found that the cost record is wrong and the process has grown
  (facts below). Sam: Y to rebuilding the record; NO to "a film cap": "recording and alarming is useful but doesn't
  solve the problem: how do we make each step cost-efficient and high quality."
- **Next: chat 1 of 8, Opus high (building new tools and a new plan).** Jobs A, B, C below, in order.
- **Needs Sam:** nothing until the proposals (job C).
- **Read:** this file only; then the parts named in each job.
- **Open rule requests:** none.
- **For Claude:** real per-chat cost = `get_session(...).external_metadata.usage.cost_usd` (list $), plus
  `modelUsage` in the last `result` event (`list_events kinds=["result"]`) for the split by model. WEEK_USD 290 in
  `.claude/hooks/costwatch.py` is the yardstick (an estimate).



<!-- chat 2 of 8 -->
## Handover, chat 2 of 8 (13 Nov)
- **Rules that bite next:** 19 (short printouts), 85 (cost watch), 89 (critique).
- **Done (13 Nov, chat 2 of 8, Opus high): Jobs B and C; Sam answered (below).**
- **Sam's answers (13 Nov):** Y to 1, 2, 3, 6. **4:** ball hands are the house style (the critique stops listing
  them); no necks and no thighs are FAULTS. **5:** "have we not built this check before?" Answered: yes,
  `clipcheck.py` (18 Oct), run by pre-flight, but only on films that define `solids(t)` or `layers(t)`; Blessed defines
  neither, so it tested nothing and said nothing. New plan for 5 (waiting for Sam's Y): pre-flight says COULD NOT TEST
  when a film with people has no solids, and Blessed gets its list; no new check.
- **Next: chat 3 of 8, Opus MEDIUM (building from this plan):** write and test 1, 2, 3, 6 and 4's checklist line
  (ball hands = house style; necks and thighs stay faults), each in the rule or tool named in "Job C proposals";
  CLAUDE.md wording for 2 and 6 as written there. Test on Blessed's files without rendering a film. Hand over.
- **Needs Sam:** Y/N on 5's new plan; whether necks and thighs are fixed in Blessed now or from the next film.
- **Read:** this file's "Job C proposals" only; then only the lines of each tool it edits (`codemap.py`).
- **Open rule requests:** 1, 2, 3, 4, 6 (Y, to write); 5 (plan, waiting).
- **For Claude:** `ledger.py app` rebuilds film rows from `notes/ledger/app-costs.tsv`. Item 1 = `views.py` ~line 335
  (the 'skeleton arm' allow must not cover "folded back across the body") + `critique.py fixed` printing open faults as
  a "Checks:" line. Item 3 = a round runner in the film kit (fix, `final --small --span`, sheet, checks, commit, one
  printout). Never page a whole chat's events (~1.2k tokens an event).



## Where things stand (chat 3 of 8, 13 Nov)
- **Rules that bite next:** 19 (PASS/FAULT/COULD NOT TEST; one command, short summary), 85 (cost watch), 89.
- **Done (13 Nov, chat 3 of 8, Opus medium): Job C 1, 2, 3, 4, 6 written and tested on Blessed (no film render).**
  1: an elbow folded back across the body stops pre-flight even under the 'skeleton arm' allow (side-on arms excepted:
  no 'across' to read); ARM_FOLD_NAMED faults and `critique.py fixed ... --left N` print a ready "Checks:" line.
  Whole Blessed swept every 0.5 s: clean. 2, 6: CLAUDE.md. 3: rule 19 widened + `source/round.py`. 4: checklist P6,
  P7, P11. Also repaired a half-merged `notes/ledger/blessed.json` on the main line (both entries kept).
- **Sam (13 Nov):** Y to 5's new plan; necks and thighs fixed from the NEXT film, not Blessed. Y to "Never again"
  1-5 (below; rules 24, 85, 19 and CLAUDE.md already written; their tools not built).
- **Next: chat 4 of 8, Opus MEDIUM (building from a clear plan):** build 5 (pre-flight says COULD NOT TEST and stops
  when a film with people has no `solids`/`layers`; give Blessed its list) and the "Never again" tools: the ledger
  stops on real figures at the budget and every 5% (no alarms_off); COULD NOT TEST stops; the after-film comparison
  line. Test on Blessed's files without rendering a film. Hand over.
- **Needs Sam:** nothing.
- **Read:** this file's "Job C proposals" 5 and "Never again"; then only the lines each tool edits (`codemap.py`).
- **Open rule requests:** none unwritten (5 and Never again are written; their tools are chat 4's).
- **For Claude:** figure.NEVER_ALLOWED, figure.named(); preflight sets NAMED_FAULTS_FILE; critique.checks_line();
  `ledger.py app` rebuilds film rows from `notes/ledger/app-costs.tsv`. Never page a whole chat's events.

