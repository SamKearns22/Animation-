# Helper B: rules without a working check

## Leak
The problem file carries a solution: Sam's Y to item 12 (a CLAUDE.md line, an audit of every rule, a gate on new rules, each check tested on a known-bad example). Treated as Sam's standing yes to honour, not as the answer.

## Results
- Rulebook: 89 table rows, 20 say "by hand" (re-counted; guides/film-quality-rules.md). Line 8 *defines* "by hand" as a check, so every rule meets "a rule only holds if a check enforces it" on paper.
- CLAUDE.md rows (rulebook lines 96-106): 5 of 8 are "by hand" wholly or partly, including "Messages to me", the plain-language rule that failed on 19 Nov (plain-check.md).
- The one coded check on Sam-bound asks (propose.py hook) blocks once, then lets the reply through and logs it: 39 let-throughs, 15-22 Nov (notes/proposals/unrouted.md). A coded check that gives way on the second try still leaves the choice to the chat.
- Milburn: 33 notes, 4 repeats, 22% of a week against the 15% aim (milburn-review.md). Of the 4 faults "checks should have caught": the name card had a coded check that never ran ("COULD NOT TEST"); the brows and 3/4 people had no rule; the mouth had a check that missed. None was a by-hand row failing.
- Checks red or blind for a whole film: 2 kit tests (named-lines.md); 11 failing kit tests fixed 22 Nov, several only stale (check-repairs.md); the per-check catch counter saved nothing in any film (check-catches.md).
- How many checks were ever run on a known-bad example: unchecked. Only one kit test is named as a catch test (watcher_catches_last_weeks_four).
- Gap: nothing maps Sam's notes to the rule that should have stopped them, so the record can't say which kind of failure costs most: by-hand rows, no rule, or a coded check that didn't fire.

## The real decision
Not "give every row a check" but "across a whole film, does every rule fire when it is broken, so no fault a rule covers reaches Sam?" The evidence points to bigger levers than the by-hand rows: coded checks that silently don't run, checks that give way, and Sam's notes not being kept as the test cases (CLAUDE.md "Seeing like Sam" 2 asks for this; nothing stores them).

## Root cause
"Check" was defined as "a name in a column". Nothing proves the named check catches the fault that made the rule, nothing fails when a check can't run, and "by hand" counts as a check. So a rule passes the gate at birth and nobody sees it die.

## Approaches weighed
1. **Sweep:** write a code check for all 89 rows plus CLAUDE.md now. Big, and blind to which failures cost Sam notes; many taste rules can't be coded honestly.
2. **Reframe, proof by example:** a rule is "working" only when its check has caught its own bad example (the note or fault that made it) and runs every film; "by hand" is replaced by a named judge step (a fresh chat or hook that reads the output) tested the same way.
3. **Fail closed:** any check that can't run, or is refused twice, stops the animatic or handover instead of logging.
4. **Learn first:** map Milburn's and Grand Theft Autism's notes to rules and check types before changing anything.
Chosen: 4, then 2, then 3, each its own yes.

## Proposal
**Learn first (changes nothing, Sonnet, ~1.5% of a week):** the audit Sam said Y to, done as a measurement. Every rulebook row and CLAUDE.md rule gets: its check, its kind (code / judge / by hand / none), whether it has ever caught a bad example, and every note in Milburn and GTA it should have stopped. Output: one table and four numbers: notes from by-hand rules, from coded checks that didn't fire, from no rule, from checks that missed.

**Change 1, one rule register with proofs (Opus high, ~4% of a week once, unchecked):** each row's entry holds its bad example (a still, a line of Sam's, a message) and the check run on it, built worst-first by step 1's numbers until every row has one. A row whose check can't yet be built says so plainly, with what the project must learn first (CLAUDE.md honesty rule), and goes to Sam as a list. Enforced by: a kit test running every check on its example; a miss goes on the watcher's existing broken list, read at every chat start; a new row without an example is flagged at every Stop and blocks `handover.py end` (the gate). The CLAUDE.md line Sam approved points to it. Number to beat: next film's notes on a rule-covered fault below Milburn's (measured in step 1), and 0 repeats.

**Change 2, fail closed (separate yes, after step 1):** checks that can't run, and the hook's second-try let-through, stop instead of log. To beat: 39 let-throughs in 8 days, 0 "COULD NOT TEST" lines carried. Shares ground with could-not-test.md; done once, there or here.

Running cost per film: near 0 (kit tests already run in the background at setup). Sam notices: fewer notes on things a rule already covers; one list of rules that can't be checked yet.

## Sam test
Q1 Expert: tested proof per rule, not a column filled in; failures measured before building.
Q2 Best result: two whole films' notes, not one chat's slip.
Q3 Comprehensive: a check is proven on its own fault, runs every chat, a miss is flagged; a gate stops paper compliance.
Q4 Intelligent: four different approaches weighed; the order follows the evidence.
Q5 Risk: step 1 changes nothing; each change undoes alone.
Q6 Checked: sources named; unknowns listed.
Q7 Not cheap: every row ends with a proven check or a plain "can't yet"; worst-first is order, not a cut.
Q8 Nothing temporary: no trial; the register is permanent and reviewed at film end.

## Lost / Added
Lost: "by hand" as a passing check; ~5.5% of a week once. Added: one register of every rule with its proof; a gate on new rules; a list for Sam of rules not yet checkable.

## Unchecked
Count of checks ever run on a bad example; step 1's four numbers; the 4% build cost; which GTA notes map to rules.
