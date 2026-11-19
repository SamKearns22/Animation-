# Helper A: check-catches

## Leak
The title gives the answer away ("Record what every check catches"). I set it aside.

## Results
- No check result is on record anywhere. `checks: {}` in all 27 ledgers (counted). No round file has a `#### Round` header or an `== pre-flight` entry. Every round-file entry is a critique pass (notes/ledger/*/round-*.txt). So `ledger.py round` has never run.
- Nothing tells a chat to run it. Its only mention is source/ledger.py's own help text (grep over guides, CLAUDE.md and hooks).
- Only 3 call sites feed the counter (report.summarise in preflight.py, audit.py and film_engine.py). Pre-flight sends about 12 check files through one call titled "pre-flight", so any per-check split comes only from report.kind() guessing from how each fault line starts.
- The miss side is not recorded either. The ledger's "notes" field reads 0 for every chat in every film, Milburn included. Yet notes/archive/milburn.md records Sam's 9 notes on animatic 3, then 4 more and 2 more (18 Nov), and Blessed has 28+ numbered notes (notes/archive/blessed-notes-animatics-1-2.md). The problem file's "Milburn: 0 notes" is a gap in the record, not a fact.
- Some usable record does exist. The critique already counts faults and false alarms per rulebook line (ledger "critique.lines"). preflight-audit.md (13 Nov) sorted pre-flight's results on 10 films by hand into real catches, noise and misses. Example: Blessed had 99 faults, mostly noise, and its animatic-1 stage cost 9.8% against 2% planned. That chat cost 3.24% (ledger preflight-audit.json).
- Milburn's quick checks ended at 13, 11 and 48 faults (ledger), and the film was posted at 22%. How many of those reached Sam: unchecked.

## The real decision
This is not about recording catches. The question is what each check is worth to the whole film: faults it stops before Sam sees them, Sam's notes it should have caught, and what it costs (minutes, false alarms, the chat steps spent answering it). Catches only decide what to retire. Misses and noise move Sam's two other aims (fewer notes, cost) far more.

## Root cause
1. The recorder needs a manual switch (`ledger.py round`) that no pack names. Its marker file is never committed, so each fresh chat starts with it off, and it fails silently.
2. Sam's notes are filed as prose in the film's notes, never as data tied to a check, so a miss cannot be counted.
3. "Would Sam have seen it" cannot be measured directly. Nothing has ever recorded what happened to each fault (fixed, named, or let through).

## Approaches weighed
1. **Learn first, by hand:** score every check on the last three films from the record that exists (round files, quick-check counts, archived handovers, Sam's notes tables, commits), using the 13 Nov method. This gives job 1 its answer now instead of three films from now.
2. **Always-on catch record:** each check run records itself without any switch. Each fault's fate is worked out by comparing one run with the next: gone after a fix counts as a real catch; named or allowed counts as let through.
3. **Reframe to misses:** each of Sam's notes is filed with a column naming the check that should have caught it, or "none covers this". That makes the record show which checks to improve, which is the lever for fewer notes.
4. **Replay:** run today's checks on each past film's code from git history. This measures catches directly but is heavy, and old code often will not run with today's tools. Rejected for now.

Chosen: 1, then 2, then 3, one change at a time.

## Proposal
- **Learn (changes nothing):** one Opus chat scores each check file on the last three finished films: catches, false alarms, Sam's notes it missed, run time, and "could not tell". About 2.5% of a week (the 13 Nov audit did 10 films for pre-flight alone at 3.24%; this estimate is unchecked). **Number to beat:** at least 80% of check-film pairs get a verdict with a named source. It hands job 1 its evidence. The share left "could not tell" is the measured case for change 1.
- **Change 1 (after the learn result, its own Y):** the counter files every run from the film named in the command, with no round switch. Pre-flight files each check under its own name. Each fault's fate is worked out by comparing runs. `handover.py end` reports a fault when a film ran a check with nothing recorded, and a kittest runs it in a fresh copy. About 2% (Opus medium, unchecked). **Number to beat:** 100% of check runs on the next film are recorded (today 0 of 27 ledgers), and every fault has a fate.
- **Change 2 (after one film of change 1, its own Y):** each of Sam's notes rows gets a column naming the check that should have caught it, or "none". `handover.py end` refuses a row left blank, and the ledger's notes count is taken from the rows. About 1% to build, plus seconds per note. **Number to beat:** every note is tagged. A repeat of the same miss on the next film is named in the end-of-film review.
- This is tool work, so it is filed outside each film's 15% (rule 24's cost kinds). The running cost per chat is close to nothing, because it is automatic and nothing extra is read.
- **What Sam would notice:** one Y/N now for the learn step. After that, each "retire" proposal comes with the three-film numbers, and each notes round says which check missed a note and gets improved.

## Sam test
- Q1: An expert would measure value (catches, misses, noise, cost), not catches alone, and would make the recording automatic.
- Q2: It covers all checks on three films, with the critic's and Sam's notes as the evidence of misses.
- Q3: A tool records it and a gate enforces it, so nothing depends on a chat remembering. The root causes (a silent switch, untagged notes) are named.
- Q4: Four different approaches weighed, including a reframe and a learn-first option.
- Q5: The learn step changes nothing. Each change is undone alone, and none is trusted before its number is in.
- Q6: Facts are sourced; estimates are marked unchecked.
- Q7: Sized to give fates and misses, not just a counter that turns on.
- Q8: Each change is permanent once Sam says Y, reviewed at the film's end; no trial.

## Lost / Added
Lost: nothing. Added: a learn chat (about 2.5%); automatic check records; a check column on Sam's notes table; two handover-gate lines.

## Unchecked
The cost estimates. Which film counts as the third finished one. Whether Milburn's 48 final faults reached Sam. Whether report.kind() splits pre-flight's faults by check cleanly enough to name each check.
