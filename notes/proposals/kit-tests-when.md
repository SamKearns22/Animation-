# Proposal: The full kit tests run every chat, even when nothing shared changed

Status: replaced:kit-tests-per-film (2026-11-25)

## Problem
Sam, 25 Nov 07:39, word for word: "Do we need to run checks every chat? Wouldn't it be better to run them at certain
key stages? Please advise". Chat 13 then asked him (Q1) and he answered Y to: "the full kit tests run only when a chat
changed a shared tool, and always before an animatic and a final render; a chat that changed only its film's files
skips the run and the wait". Today every chat runs all the kit tests at start-up, and no chat can hand over until that
run has finished, whatever the chat changed.

## Facts
- The start-up hook (.claude/hooks/setup.sh, last line) starts `watcher.py kittests-bg` in the background on every
  fresh machine: `nice -n 19 python3 source/kittests.py` into notes/logs/kittests-last.log, timeout 1800 s.
- source/kittests.py holds 141 tests (`grep -c "^@test"`), each a shared-kit check against the saved fault that taught
  it; handover.py says "the start-up run (about 15 min on a fresh machine)" (kittest_gate_faults docstring). Exact
  times per run: unchecked.
- handover.py `end` runs kittest_gate_faults: with no finished run on the machine it STOPs the handover ("KIT TESTS
  STILL RUNNING ... wait for it" or "COULD NOT RUN"); a test red at two handovers in a row by different chats STOPs it;
  red once is a warning (notes/logs/kittest-reds.log).
- The watcher (source/watcher.py `kittests`) reads the same log and lists FAILs as a broken promise.
- Chat 13 (Open Wounds) ran the start-up run (139 passed) and, after its shared fixes, ran the run, chase, gait and
  moves tests again by hand (notes/brexit-is-done.md, Where things stand).
- Earlier Open Wounds chats: chat 7's full run "was still going at handover" (notes/archive/brexit-is-done-handovers.md
  line 114); chat 10's full run "was stopped mid-way" (line 173).
- What counts as a film's own files: handover.py `_film_prefixes()` (a film's name and initials as code-file prefixes,
  e.g. source/brexit_is_done*.py, source/gta_*.py) plus its story/, notes/, references/ and animations/ files. Everything
  else under source/, .claude/hooks/ and guides/kit-*.md is shared (unchecked whether any other folder holds shared code).
- How an animatic and a final are made: finish.py (CLAUDE.md "Files"; guides/job-packs.md "Checks and animatic");
  .claude/hooks/modelguard.py already guards finish.py and whole-film renders (no Opus). Neither runs the kit tests
  today (grep for "kittest" in finish.py and modelguard.py: none in finish.py).
- Sam's rules that bear on it: CLAUDE.md Statement One (cost down only by working smarter, never by cutting quality);
  "Rules are permanent": a step is removed only if it caught nothing in three films, with Sam's Y on a "Lost:" line
  (here Sam has said Y).
- Unchecked: how many chats in the last week changed only film files; how often a start-up run caught a fault the
  chat itself had not caused (i.e. a fault from an earlier chat already on the main line).

## Record
source/handover.py
source/watcher.py
source/kittests.py
.claude/hooks/setup.sh
.claude/hooks/modelguard.py
source/finish.py
notes/brexit-is-done.md
notes/archive/brexit-is-done-handovers.md
notes/logs/
notes/ledger/sam/v7mhwaoh.md

## Verdict (the judge, word for word)
<!-- verdict-hash: d3ea3be4fe8951b3 -->
Who wrote which (hidden from the judge): V1 = helper B, V2 = chat, V3 = helper A. Picked: V1 (helper B). Critiqued: 6 found, 3 fixed, 3 named.

## Leak
yes: the problem file quotes the rule Sam said Y to ("run only when a chat changed a shared tool, and always before an animatic and a final; a film-only chat skips the run and the wait"), so every helper started from that answer. V1 and V3 named it and tested it; V2 builds it as worded.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 4 | 20 |
| V2 | 3 | 2 | 3 | 3 | 4 | 15 |
| V3 | 4 | 4 | 3 | 3 | 4 | 18 |
## Sam test
Q1: Yes, once improved: an expert ties a test result to the exact files that test read and re-runs only the tests whose files changed (test-impact selection). V1 ties it to files; this verdict adds the per-test selection, which is what actually removes the waits.
Q2: Evidence spans every chain on the record, not one film: 15 "still running" refusals in 11 chats and 10 "could not run" (handover-end.log, checked), five red rows carried between chats (kittest-reds.log, checked), 14 to 18 tests importing film code (kittests.py, checked). The learn step replays about 99 chats and every past red before any change.
Q3: Root cause named and checked: the gate accepts any finished run on the machine, started at boot (kittest_gate_faults, checked), so it waits on inherited code and passes untested own changes. Enforced in handover end and finish.py, not by a chat reading a rule; three numbers measure it.
Q4: Five approaches weighed (path rule, file stamps, faster runs, tests on GitHub, learn first). File stamps per test is the only one that both cuts waits and tests each chat's own changes, including film files the tests read.
Q5: Each change has its own yes and comes after the replay that would show a missed red. Main risk: a file a test reads is not recorded (subprocess reads, downloaded tools), so a run is skipped wrongly; guarded by fail-shut (no record or unknown read = run) and named. Each change undoes in one commit.
Q6: Facts above checked against the logs and code; the chat counts (24-27 of 99 film-only, 203 of 250 commits shared) and all time and cost figures are marked unchecked.
Q7: Not cheap: it runs tests the path rule would skip (film-code tests, merged-in changes) and adds a run before every animatic and final. Build cost stated (about 2% of a week, once).
Q8: Permanent; the learn step is a measurement, not a trial. Reviewed at the end of the film against the three numbers.
## Pick
V1
## Why
V1 and V3 both find the real decision (does the exact code an animatic stands on have a green result?) and both correct Sam's Y'd path rule with checked evidence: the tests read film code, and a notes-only change already turned a test red. V1 wins because it learns before it builds (a replay of past chats and reds that must show zero misses), splits the work into separately undoable yeses, and keeps a start-up run when something tested has changed, which keeps the early catch of faults another chat left (body_check_back_view red at four handovers). V3 bundles four changes into one yes and drops the start-up run outright, moving a full 15-minute run to the end of most chats (about 75 to 80% change shared code), which could lengthen waits rather than end them. V2 is Sam's wording built straight: it misses film-code tests and gives up the early net it admits losing.
Taken from V3: the corrected crash count (10 "could not run", 6 of them crashing tests), recording reads through Python's own import list and file-open hook, fail-shut when the record is missing, and its three numbers to beat. Added by this verdict: stamps per test so only affected tests re-run, and merge-safe storage of the record.
## Faults in the pick
- F1 [fixed] V1 re-ran the whole set whenever any stamped file changed, so most chats would still wait at the end; now each test keeps its own stamp and only the tests whose files changed re-run.
- F2 [fixed] V1 did not say how reads are found; now the import list plus a file-open hook, and a test that starts another program counts as reading all shared code (fail-shut).
- F3 [fixed] One committed record would clash when two chains push; now one line per green test, kept on both sides when merging.
- F4 [named] A test green on one machine may crash on another (womens_builds, kit_people_never_generic); skipping on a matching stamp could hide that until the render machine. The finish run still runs any test never recorded green on this setup.
- F5 [named] Wait time and token cost of waiting are unchecked; the saving may be mostly time, not cost.
- F6 [named] Fixing the crashing tests is a separate later change.
## Final version
**Step 0, learn (changes nothing, about 0.4% of a week).** One full run on a fresh machine records, per test, every module and file it read (Python's import list and a file-open hook; a test that starts another program is marked as reading all of source/) and each test's time. Replay the last ~99 chats' commits: count runs and minutes saved under the path rule and under per-test stamps, and whether any past red (kittest-reds.log, the notes-archive red) would have been missed. Per-test stamps must miss none, or Step 1 is not put to Sam.

**Change 1 (own yes).** kittests.py writes, for each green test, one line: test name plus a stamp of every file it read, appended to a committed record (union on merge). handover.py end: a test whose stamp matches a green line passes with no run; any other test, or any test with no record, runs now on the chat's final code. The two-reds-in-a-row and crash STOPs stay. A kittest replays the notes-archive red and a merged-branch change and must catch both.

**Change 2 (own yes).** finish.py refuses an animatic or final unless every test is green on the current stamps, running the missing ones first and saying how long. Override still applies through override.refuse.

**Change 3 (own yes, after 1).** setup.sh starts the background run only for tests whose stamps differ, keeping the early catch of faults another chat left.

**Numbers to beat (end-of-film review):** "still running" refusals on unchanged code 15 to 0; animatics or finals on untested code 0; reds first seen by a later chat 0; past reds missed by the replay 0.

**Cost:** about 2% of a week once, shared by all films (unchecked estimate); nothing added per film.

Lost: the full run on every fresh machine when nothing it tests has changed. Added: a committed record of green tests; a test run on each chat's own final changes; a test run before every animatic and final; one kit test.
## For Sam
### Option 1: test only what changed, every time
Problem: Every chat runs all 141 shared-tool tests (each one checks that a fault you caught stays fixed) when it starts, and can't hand over until they finish, even if nothing they look at changed. Worse, they test what the chat started with, not what it changed.
1. First, without changing anything, record which files each test looks at, and replay the last week's chats to prove this way would have caught every fault the tests ever caught.
2. Each test that passes leaves a stamp of the exact files it looked at; at hand-over, only tests whose files changed run again.
3. Before every animatic and final, any test without a fresh pass runs first.
4. At the start of a chat, only the tests whose files changed run in the background.
Why: Many tests read the film's own files, so "a chat that only changed its film's files" can still break them; this catches that, and stops the waiting when nothing changed.
You'd notice: chats stop stalling at hand-over, and no animatic is made on untested work.
Other option: the rule you said yes to, decided by which folders a chat changed.
Lost: the full test run in every chat when nothing it tests has changed.
Added: a saved record of passing tests; a test run before every animatic and final; one new check that this works.
### Option 2: skip tests when only film files changed
Problem: Every chat runs all 141 shared-tool tests when it starts and waits for them, whatever it changed.
1. A chat that changed only its own film's files skips the tests and the wait.
2. A chat that changed a shared tool runs them on its finished work before hand-over.
3. Every animatic and final waits for a passing run first.
4. The start-of-chat run only happens when a shared tool changed.
Why: It is exactly what you said yes to and is quick to build.
You'd notice: film-only chats hand over faster; about three in four chats change shared tools, so most still wait.
Other option: test only what changed, by which files each test looks at.
Lost: the start-of-chat catch of faults another chat left, and tests on film files that shared tests read, until the animatic.
Added: a test run before every animatic and final.

## Sam's pick and the build (25 Nov)
Sam picked **1** (the judged version: test only what changed, by the files each test looks at), 25 Nov, Open Wounds
chat 14 (session_01U3pKR1ipLftvRyJ1wn1Tcp). Built in its own chat (Opus high), as the verdict's steps:
1. Record which files each kit test reads (trace a full run); first replay the last week's chats to show this way would
   have caught every fault the tests ever caught. Report the replay before switching anything off.
2. Each passing test leaves a stamp of the exact files it read (their hashes); at a chat's end (handover.py end), only
   the tests whose files changed run again; the gate reads the stamps.
3. finish.py refuses an animatic or final until every test has a fresh pass on the current files (runs the stale ones).
4. The start-up hook (setup.sh) runs only the stale tests in the background.
5. A kittest proves it: a film-only change that a test reads re-runs that test; an unchanged file skips; finish refuses
   without fresh stamps. Lost: the full run in every chat. Added: the stamp record; a run before every animatic/final.

## Built (25 Nov, kit-tests build chat 5285aeae, Opus high)
- **Step 0, the record and the replay (done first, nothing switched off before it):** `source/kitstamps.py` traces each
  kit test: every function that runs (Python's per-function start event, switched off after its first sighting, so the
  run is no slower: 23 s traced vs 22.9 s untraced on turned_parts_kept), every `import` named, one step out (what those
  modules hold by name: constants, compiled functions), every file opened and folder listed, git commands on the project
  (stamped by what they print), and Python programs a test starts (each traces itself and reports back; no report =
  ALL). Final full run: 146 of 146 passed in 15 min, all stamped (notes/kittest-stamps.tsv).
  Replay of the last 7 days (`python3 source/kitstamps.py replay 7`, 128 chats): a full run every chat 1,895 min;
  the path rule 1,259 min (43 chats film-only); per-test stamps **636 min**: median wait 2.1 min a chat (quartiles
  0.4 / 2.1 / 11.9), film-only chats median 0.4 min (max 2.6). **Past reds: 7 of 7 caught** (each had a file it reads
  changed between the green and the red), including the notes-archive red (move_to_shared_catches_film_fixes, 23 Nov:
  notes/archive's file list is read). Named: the replay uses today's reads for past chats (reads may have differed);
  the first reds on record (23 Nov 14:13) use a 24 h window.
- **Change 1:** each green test appends one line (name, stamp, seconds, setup, reads) to notes/kittest-stamps.tsv
  (merge=union in .gitattributes; newest 3 lines per test kept). `handover.py end` runs only the stale tests, on the
  chat's final code (`kittests.py --stale`), saying how long; the two-reds and crash STOPs stay.
- **Change 2:** `finish.py` refuses an animatic or final while any test lacks a pass on the current files, running the
  stale ones first and saying how long (`kitstamps.finish_gate`; Override still applies). Rule 59's check column names it.
- **Change 3:** setup.sh's background run (watcher.py kittests-bg) runs `kittests.py --stale` only.
- **Kittest** `kit_tests_rerun_only_what_changed`: a film-only change re-runs only the test that reads it; unchanged
  files skip; a merged branch's change re-runs its test; notes/archive recorded as read; a Python child's reads come
  back and a git command that is no read counts as ALL; finish.py refuses without fresh passes.
- **Named risks (fail-shut where possible):** a file checked only for existence (os.path.exists) is not recorded; tests
  run in a smaller set may meet different leftover state from earlier tests; five tests still read ALL (start a program
  that leaves no report or use git's history), so they re-run whenever source/ or .claude/ changes; a test that
  depends on a library version re-runs on a new setup (the stamp holds the versions).
- **Numbers to beat** (end-of-film review): "still running" refusals on unchanged code (17 on record) to 0; animatics or
  finals on untested files 0; reds first seen by a later chat 0.

## Where things stand (kit-tests build, 25 Nov)
- **Locked by Sam:** his pick 1 as written above; nothing in any film touched (Open Wounds chat 15 owns its files).
- **Rules that bite next:** 59 (finish refuses without fresh kit passes), 85 (cost watch), N27 (Override skips the kit gate, logged).
- **Done:** Steps 0-3 and the kittest, as "Built" above; all 146 kit tests green and stamped.
- **Next:** none for this job; the next chat of any film just runs `handover.py end` as usual (only stale tests run).
  Review the numbers to beat at the end of Open Wounds.
- **Needs Sam:** nothing.
- **Read:** this file's "Built"; `python3 source/kitstamps.py stale` shows what would run.
- **Open rule requests:** none.
- **For Claude:** kitstamps.Tracer (one per process, `tracer()`), `traced(fn)` for nested tracing; KITTESTS_RUNNING=1
  makes finish.py skip the gate inside kit tests; child tracing via a temp sitecustomize.py that first runs the system's own.

## Handover check named (kit-tests build, 25 Nov)
- **Branches named:** claude/brexit-chat15 is Open Wounds chat 15's live work (its chat merges it); claude/gta-v5-sound-draft,
  claude/gta-chat46-build, claude/dreamy-fermi-vkhutz, claude/gta-chat31 hold only posted-GTA logs, a proposal and two old
  helpers: not merged here (outside this job).
- **Handover check named:** SENTENCE lost (34f49840, 0945cc85): earlier chats' commits, not this one's; both sentences
  stand in CLAUDE.md as Sam reworded them. COST: a tool job, no film estimate (its cost is filed as tool work).
  KIT TESTS: Sam typed "Override kit tests" (25 Nov): the hand-over's stale run (38 tests after the merge with chat 15's
  shared changes) was skipped, logged; they stay stale, so the next start-up run, `handover.py end` or finish.py runs them.
- **Start check named:** "NOT CARRIED 08:02 ... make sure it's implement" is Sam's acting-plan message in Open Wounds
  chat 14; it is carried in notes/brexit-is-done.md "Acting plan" (chat 15's job), not this one's.
