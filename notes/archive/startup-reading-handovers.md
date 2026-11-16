
## Startup reading/fixes, handover before chat 4 (archived 16 Nov)
# Startup reading job: Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (each change its own judged yes), 85 (cost watch), 19 (long printouts filtered).
- **Done (chat 1, Opus high):** verdict option 1 (measure first). **(chat 2, Sonnet):** learn table, `learn.md`.
- **Done (chat 3, Opus high, 16 Nov):** proposal `startup-fixes` routed: two helpers, blind judge picked helper B; four
  changes, each its own Y/N, put to Sam with measured savings: (1) cost rows reach the main line (no tokens; complete
  cost totals, 7 of 9 rows missing today); (2) branch printout by the start hook, 2.0k -> under 0.2k tokens a chat,
  ~0.5% a film; (3) notes printout, 3.6k -> under 2.5k, ~0.35%; (4) CLAUDE.md moved word for word, 5.5k -> under 4.8k,
  ~0.2%. Critiqued: 6 found, 3 fixed, 3 named.
- **Sam (16 Nov): "Y to all."** startup-fixes marked adopted.
- **Next (chat 4, Opus, medium):** build changes 1, 2, 3 of the verdict's "Final version" in that order, each with a
  kittest, each pushed and checked before the next; then open chat 5 (Sonnet, medium): change 4's read-only mapping.
- **Needs Sam:** nothing; change 2's first run asks him about the 3 stranded items.
- **Read:** `notes/proposals/startup-fixes.md` (Verdict, "Final version"); `guides/job-packs.md` "A tool job".
- **Open rule requests:** none.
- **For Claude:** the problem file's fact "~1,500 commits = rewritten histories" is wrong: this copy is shallow (history
  from 12 Nov); helper A caught it, the judge used it (F2). Helper A also found Sam-message logs 5t3vj4eb and phxjozvs
  not on the main line: merge them with change 2's first run. Stranded: slurp picture, Blessed WIP, audit branch (F6).

## Chat 4 handover (16 Nov)
# Startup reading job: Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (changes 3-4 as adopted, nothing wider), 85 (cost watch), 19 (filtered printouts).
- **Done (chat 4, Opus medium, 16 Nov):** change 1: cost rows and Sam's saved messages go straight onto the main line
  (own commit, only those files); 18 stranded rows gathered, `ledger.py audit` 0 missing; kittest
  `cost_rows_reach_the_main_line`. Change 2: start hook lists only branches with work the main line lacks (3 lines,
  ~0.1k tokens, was ~2.0k); `handover.py end` refuses an unnamed one; CLAUDE.md line updated; Sam logs 5t3vj4eb and
  phxjozvs merged; kittest `branch_printout_lists_only_real_work`. Handed over at amber.
- **Next (chat 5, Opus, medium):** change 3 (notes printout: `handover.py start --film` prints "Where things stand" and
  the unticked notes; carried() still reads the whole file), with a kittest, pushed and checked; then open chat 6
  (Sonnet, medium): change 4's read-only mapping of CLAUDE.md.
- **Needs Sam:** the 3 stranded branches (asked 16 Nov, chat 4): (1) claude/beautiful-brown-vutd0l, the slurp profile
  picture: pick merge; (2) claude/blessed-c2-mics-wip, Blessed WIP source/blessed.py: pick keep off; (3)
  claude/audit-honest-checker, 12 Nov audit, 16 files incl. CLAUDE.md: pick keep off. His answer comes back to chat 4.
- **Read:** `notes/proposals/startup-fixes.md` ("Final version", change 3); `guides/job-packs.md` "A tool job".
- **Open rule requests:** none.
- **For Claude:** main was rewritten once and this copy is shallow: merged-ness is judged by blob content
  (source/branches.py); fetch uses --shallow-since. Not asked, list at review: Sam's message log also goes via
  mainline.to_main (it stranded the same way); gather keeps non-row keys as main has them (first run revived Blessed's
  alarms_off; put back at once). The ledger .md merge keeps ours until the next row rewrites it.

## Archived by chat 7 (16 Nov)
# Startup reading job: Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (change 4 as adopted, nothing wider), 85 (cost watch), 19 (filtered printouts).
- **Done (chat 5, Opus medium, 16 Nov):** change 3: `handover.py start --film` prints Where things stand + unticked notes
  (protest-tiers ~1.1k tokens vs ~6.3k); Notes round pack reads it. Kittest `notes_printout_reads_only_open_notes`.
  Billing fix (Sam asked): a chat whose task is under notes/proposals/ is billed to proposal-route, never a film; one chat,
  one ledger (this chat's duplicate 0.4% under the paused film removed). Kittest `process_work_is_never_billed_to_a_film`.
- **Done (chat 6, Sonnet medium, 16 Nov):** change 4's read-only map written: `claude-md-map.md` (every sentence -> rule,
  source fault, date, and which move: R tags to rulebook table, P to packs, K stays). No CLAUDE.md edits.
- **Next (chat 7, Opus, medium):** move the text word for word per the verdict (R: 12 dated tags; P: photo search order,
  the finish.py command, My accounts), each leaving a one-line pointer; add the sentence check (every old sentence found
  word for word in CLAUDE.md, rulebook or a pack, else refuse). Rewording of the 5 duplicates is a later proposal.
- **Needs Sam:** the 3 stranded branches (asked chat 4; answer goes to chat 4): claude/beautiful-brown-vutd0l merge;
  claude/blessed-c2-mics-wip keep off; claude/audit-honest-checker keep off (all three left alone by chat 6).
- **Read:** `notes/proposals/startup-fixes.md` ("Final version", change 4); `guides/job-packs.md` "A tool job".
- **Open rule requests:** none.
- **Sam's two cost-estimate asks (11:20, d675uk2u):** "Is any of this relevant to cost ledgers?" and "your estimates in terms of
  week costs (e.g. 3% of a week) are rarely correct". Chat 6's reading: yes, partly. The ledger lost 7 of 9 checked chats' cost
  rows (change 1), so past estimates were compared with incomplete totals; chat 5's billing fix also stops process chats being
  billed to a film. Whether estimates themselves are off is open: a later proposal (after change 1) compares the last films'
  estimates with complete ledger totals. Tell Sam at the next message.
- **For Claude:** shallow copy: fetch, `git checkout -B` the main line. Review list (not asked): job-packs line 32; the
  overnight rule now after the process check; UNROUTED 10:08 was a budget Y/N (Sam told). Failing before chat 5, untouched:
  kittests people_from_a_description, facehouse_whole_head (protest_tiers_cast uses the kit before Sam's OK).

## Chat 7 handover (archived chat 8, 16 Nov)
# Startup reading job: Where things stand (the ONE handover)
- **Rules that bite next:** the proposal route (any next step is a new proposal), 85 (cost watch), 19 (filtered printouts).
- **Done (chat 7, Opus medium, 16 Nov):** change 4 built. 11 dated tags moved word for word to the rulebook's new table
  "Dates moved from CLAUDE.md" (the map's 12th, "Earlier chats can be read", has no date in the text: nothing to move);
  photo search order to the Plan pack, the sign-off command to Checks and animatic, My accounts to Final and posting,
  each with a one-line pointer. `source/sentences.py` refuses any lost sentence (each CLAUDE.md commit since it began,
  and unsaved edits); `handover.py end` runs it; kittest `claude_md_sentences_never_lost` (checks the real move too).
- **Beat:** no sentence lost (checked). Size 12,891 -> 11,726 characters, ~5.0k tokens at learn.md's ratio: **missed the
  4.8k beat by ~0.2k.** The rest needs rewording (the 5 duplicates), which is the later proposal.
- **Startup fixes 1-4 all built.** Sam (16 Nov, chat 7): "Only do Half A" = the 5 duplicates proposal; Half B
  (estimates vs complete ledger) not asked for. **Next (chat 8, Opus, high):** run the proposal route on Half A only
  (`notes/proposals/claude-md-duplicates.md`: helpers, blind judge, top two for Sam with Lost/Added/Critiqued); the guard
  is the 10-situation test (a fresh helper answers 10 past situations with old and new CLAUDE.md; any change refuses).
  sentences.py must gain an allowance for the merged sentences (each removed copy names its kept twin). Build only on
  Sam's Y to the judged proposal. Duplicates: map section "What the map shows chat 7", point 3.
- **Branches settled (Sam, 16 Nov, chat 7):** claude/beautiful-brown-vutd0l: the slurp profile picture merged into
  profile/ beside the eyes-open one; claude/blessed-c2-mics-wip and claude/audit-honest-checker: disregarded (left on
  GitHub, not merged; they drop off the start list within 4 days).
- **Needs Sam:** chat 8's judged proposal (Half A).
- **Read:** `notes/proposals/startup-fixes.md` ("Final version"); this file; the map `claude-md-map.md` (duplicates section).
- **Open rule requests:** none.
- **For Claude:** a rewording must add an allowance to sentences.py first (none exists; the check refuses any loss).
  Failing before chat 5, untouched: kittests people_from_a_description, facehouse_whole_head.
