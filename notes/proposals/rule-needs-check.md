# Proposal: Rules are written without a working check, so they fail without anyone seeing

Status: open (un-parked 22 Nov, Sam: "Milburn: begin all"; his 19 Nov words below still stand)

## Problem
Several of Sam's rules have nothing that makes them happen; they rely on a chat reading them and choosing to follow
them. The plain-language rule is the latest: no check, and it failed in the review chat (19 Nov). Sam (19 Nov): "A
rule should function. If it doesn't function, you built it wrong." Sam said Y to item 12: no rule without a working
check, an audit of every rule, a gate on new rules, and each check tested on a known-bad example.

## Facts
- guides/film-quality-rules.md has 89 table rows (lines starting "| "); 20 say "by hand" in the check column (counted
  19 Nov with grep). The rows from CLAUDE.md ("Working with Sam" table, lines ~96-106) list several rules per row with
  mixed checks.
- `source/sentences.py` checks the dates table word for word (rulebook line 108).
- The plain-language rule has no check (notes/proposals/plain-check.md).
- Checks that exist but did not work: clipcheck "COULD NOT TEST" on Milburn (notes/proposals/could-not-test.md);
  two kit tests red for the whole film (notes/proposals/named-lines.md).
- Kit tests are in source/kittests.py; the watcher (source/watcher.py PROMISES) lists what each tool promises and
  `handover.py start` prints unlisted ones (19 Nov: "cost_faults has no promise in the watcher").
- CLAUDE.md "Rules are permanent": each rule written once, in the rulebook with its check, or in CLAUDE.md if it is
  about working with Sam (listed in the rulebook's last table).
- How many existing checks have ever been run on a known-bad example: unchecked.

## Record
CLAUDE.md
guides/film-quality-rules.md
source/kittests.py
source/watcher.py
source/sentences.py
source/handover.py
source/propose.py
notes/proposals/milburn-review.md

## Verdict (the judge, word for word)
<!-- verdict-hash: 300b2d54743db644 -->
Who wrote which (hidden from the judge): V1 = chat, V2 = helper A, V3 = helper B. Picked: V3 (helper B). Critiqued: 7 found, 3 fixed, 4 named.

## Leak
yes: the problem file states the solution in full: Sam's Y to item 12 (a CLAUDE.md line "no rule without a working check", an audit of every rule, a gate on new rules, each check tested on a known-bad example). V1 copies it as its whole answer; V2 and V3 name the leak and treat it as Sam's aim, not the method.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 2 | 2 | 2 | 2 | 4 | 12 |
| V2 | 4 | 4 | 3 | 4 | 4 | 19 |
| V3 | 5 | 4 | 4 | 4 | 4 | 21 |
## Sam test
Q1: Yes. An expert proves each control on the fault it exists for, measures which failures actually cost notes before building, and reuses the monitor that already runs in every chat (the watcher's promise list) rather than a new one.
Q2: The evidence is the whole of two films (Milburn's 33 notes and 4 repeats, GTA's notes) plus check-repairs and the 39 let-throughs, mapped rule by rule; not one chat's slip. GTA's note count may be low (named).
Q3: Root cause found with evidence: "check" means a name in a column; "by hand" points at a check sheet that CLAUDE.md turns off by default, so 19 rows have no moment at all; three 21 Nov CLAUDE.md sections have no row; checks were named but never wired. A rule counts as working only when its check has caught its own bad example; a miss lands on the watcher's broken list at every chat start, and the handover check refuses a new rule with no example. It does not rest on a chat choosing to read.
Q4: Four different approaches weighed (sweep, proof by example, fail closed, learn first, plus V2's by-hand judge); learn-first then proof-by-example is the strongest, ordered by evidence.
Q5: The learning step changes nothing. Each later change has its own yes and comes out alone. Risk named: fail-closed could stall an unattended chain; that is why it is a separate yes after the numbers.
Q6: Facts re-checked: 89 rows, 19 rows say "by hand" (20 lines in the file, one is the definition); 6 of 8 Working-with-Sam rows are wholly or partly by hand (V3 said 5); 39 let-throughs in unrouted.md (15-20 Nov); Milburn 33 notes, 4 repeats, 22%; model guard never wired until 21 Nov; no "Locked by Sam" check anywhere. Costs are unchecked and marked so.
Q7: Not cheap: every rule ends with a proven check or a plain "can't yet, needs X"; worst-first is an order, not a cut.
Q8: Nothing provisional; the register and gate are permanent and reviewed against the next film's notes at film end.
## Pick
V3
## Why
V3 answers the real decision (does every rule fire when broken, across a whole film) rather than the wording, measures before building, and its gate blocks the handover instead of only printing, so it does not depend on a chat choosing to act. It also names the second hidden failure V2 misses: checks that give way or cannot run (39 let-throughs, "COULD NOT TEST"). V1 is the leak restated: no learning, no root cause, a commit gate only, cost guessed. V2 is close but its gate only prints louder start lines, and its by-hand judge is a third bundled build with no evidence yet that by-hand rows cause notes (Milburn's four missed faults were none of them by-hand rows).
Taken from V2: hang the register on the watcher's existing promise list (no new monitor); the finding that by-hand rows have no moment because the check sheet is off by default; the three 21 Nov CLAUDE.md sections with no row and the unchecked "Locked by Sam" line, added to the audit; its fresh-eye judge kept as the way a taste rule is proven, not as a separate build.
## Faults in the pick
- F1 [fixed] V3 said 5 of 8 Working-with-Sam rows are by hand; it is 6 of 8. The 20 count is 19 rows plus the definition line.
- F2 [fixed] V3 built a separate register; now it lives in the watcher's existing promise list, so it is read at every chat start with no new tool.
- F3 [fixed] The 21 Nov CLAUDE.md sections (Be honest, Fix the drawing, Seeing like Sam) and the "Locked by Sam" line were missing from the audit; added.
- F4 [named] Build cost (about 4% of a week once, plus 1.5% learning) is unchecked.
- F5 [named] Taste rules can only be proven by a judge step, and a judge's own catch rate on a real bad example is not yet shown.
- F6 [named] Fail-closed can stop an unattended chain; kept as its own yes after the numbers, and it overlaps could-not-test (done once, there or here).
- F7 [named] GTA's note count may be an undercount, so the learning table's numbers may be low.
## Final version
**Step 1, learn (changes nothing; Sonnet; about 1.5% of a week, unchecked).** One table of every rulebook row and every CLAUDE.md rule, including the 21 Nov sections and the "Locked by Sam" line. For each: its check, its kind (code, judge, by hand, none), whether it is switched on, whether it has ever caught a bad example, and every Milburn and GTA note and check-repairs finding it should have stopped. Output: four numbers: notes from by-hand rules, from coded checks that did not fire or gave way, from no rule, from checks that ran and missed. These are the numbers the next steps must beat.

**Step 2, rules as proven promises (own yes; Opus high; about 4% once, unchecked).** The CLAUDE.md line Sam approved: no rule without a working check. Every rule becomes an entry in the watcher's existing promise list, holding its bad example (a still, Sam's words, a message) and the check run on it. A kit test runs each check on its example; a miss goes on the watcher's broken list, printed at every chat start. Taste rules are proven by a fresh-eye judge step tested the same way. "By hand" no longer counts as a check. Built worst-first by step 1's numbers until every rule has one; a rule whose check cannot yet be built says so, with what the project must learn first, and goes to Sam as one list. The gate: the handover check refuses a new rule with no example. To beat: the next film's notes on rule-covered faults below Milburn's (from step 1), and 0 repeats.

**Step 3, fail closed (own yes, after step 1).** A check that cannot run, and the guard's second-try let-through, stop the animatic or handover instead of logging. Built once, shared with the could-not-test proposal. To beat: 39 let-throughs in a week and any "COULD NOT TEST" line carried.

Running cost per film: near zero (kit tests and the watcher already run every chat). Reviewed against the next film's notes at film end.
## For Sam
### Option 1: Measure first, then make every rule prove itself
First, one list (changing nothing) of every rule, its check, and which of your notes on Milburn and Grand Theft Autism it should have stopped. Then, worst first, each rule gets a saved example of the fault it is for, and its check must catch that example or it is shown as broken at the start of every chat. A new rule without an example cannot be handed over. Rules that can't be checked yet come to you as one list saying what's needed. Later, a separate yes: checks that can't run stop the work instead of being skipped.
Lost: about 5.5% of a week once (unchecked); "checked by hand" no longer counts as a check.
Added: every rule with a proven check; a gate on new rules; fewer notes on faults a rule already covers.
### Option 2: Measure first, then flag unproven rules loudly
The same first list. Then every rule without a proven check is printed at the start and end of every chat until fixed, each check is tested on one of your real notes, and a separate fresh-eyes reader checks the hand-checked rules at each handover. Nothing is blocked; the gaps are just loud.
Lost: about 9% of a week once (unchecked); louder start-up lines until every gap is closed.
Added: every gap visible in every chat; a reader for the rules a tool can't check.
