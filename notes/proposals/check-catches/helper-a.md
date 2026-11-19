# Helper A: check-catches

## Leak
The title names the answer (record what every check catches); ignored.

## Results
- No check result is on record. `checks: {}` in all 27 ledgers. No round file has a `#### Round` header or a pre-flight entry; every entry is a critique pass (notes/ledger/*/round-*.txt). `ledger.py round` has never run, and nothing names it outside its own help text.
- Only 3 call sites feed the counter (preflight.py, audit.py, film_engine.py). Pre-flight sends about 12 check files through one "pre-flight" title, so it can only split faults by check from how each fault line starts (report.kind).
- Misses are not recorded either. The ledger "notes" field is 0 for every chat of every film. Yet notes/archive/milburn.md holds Sam's 9 + 4 + 2 notes (18 Nov), and Blessed has 28+ numbered notes. "Milburn: 0 notes" in the problem file is a recording gap, not a fact.
- Some record exists. The critique already counts faults and false alarms per rulebook line (ledger critique.lines). On 13 Nov a chat sorted pre-flight's results on 10 films by hand into real catches, noise and misses (notes/preflight-audit.md), at 3.24% of a week (ledger). Noise costs: Blessed's 99-fault pre-flight stage cost 9.8% against 2% planned.

## The real decision
What each check is worth across the whole film: faults it stops before Sam, notes it missed, and its cost (minutes, false alarms, chat steps). Catches alone only decide what to retire. Misses and noise move "fewer notes" and cost more.

## Root cause
1. Recording depends on a manual switch (`ledger.py round`) that no pack names. Its marker file is never pushed, so each fresh chat starts with it off, silently.
2. Sam's notes are filed as prose, never tied to a check, so a miss cannot be counted.
3. Nothing records what happened to a fault after it was flagged (fixed, named, let through), so "would Sam have seen it" has no evidence.

## Approaches weighed
1. **Learn first, by hand:** score every check on the last three finished films from the existing record with the 13 Nov method. Job 1 gets an answer now.
2. **Automatic catch record:** every check run records itself with no switch. Comparing each run with the next gives each fault's fate: gone after a fix is a real catch; named or allowed means let through.
3. **Reframe to misses:** each of Sam's notes is tagged with the check that should have caught it, or "none". That is the lever for fewer notes.
4. **Replay:** today's checks on past films' code from git. Heavy, brittle. Rejected.

Chosen: 1, then 2, then 3, each on its own Y.

## Proposal
- **Learn (changes nothing):** one Opus chat scores each check file on three finished films: catches, false alarms, misses, run time, could-not-tell. About 2.5% (unchecked; the 13 Nov audit was 3.24% for 10 films, pre-flight only). **To beat:** a sourced verdict for at least 80% of check-film pairs. It goes to job 1; the could-not-tell share is the case for change 1.
- **Change 1:** the counter records every run from the film named in the command, with each check under its own name and each fault's fate from comparing runs. `handover.py end` flags a check that ran with nothing recorded, and a kittest runs it in a fresh copy. About 2% (unchecked). **To beat:** 100% of check runs on the next film recorded (0 of 27 ledgers today), every fault with a fate.
- **Change 2 (after one film of change 1):** each notes row gets a column for the check that should have caught it, or "none". `handover.py end` refuses a blank, and the ledger's notes count comes from the rows. About 1%. **To beat:** every note tagged, and no repeat of the same miss on the next film, checked at the end-of-film review.
- Tool work, filed outside the film's 15% (rule 24). Afterwards about nothing per chat.
- **Sam would notice:** one Y/N now; then retire proposals with three-film numbers, and notes rounds naming the check that missed.

## Sam test
- Q1: measures value, not catches alone; automatic.
- Q2: all checks, three films, Sam's notes as misses.
- Q3: tools and a gate enforce it; root causes named.
- Q4: four different approaches weighed.
- Q5: learning changes nothing; each change undoes alone.
- Q6: sourced; estimates unchecked.
- Q7: sized to fates and misses, not a bare counter.
- Q8: permanent on Y, reviewed at film end.

## Lost / Added
Lost: nothing. Added: a learn chat (about 2.5%); automatic check records; a check column on Sam's notes; two gate lines.

## Unchecked
The costs; which film is the third finished one; whether Milburn's last quick check (48 faults) reached Sam; whether report.kind splits pre-flight's faults cleanly by check.
