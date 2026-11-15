## Leak
yes: mild. The problem says Sam's messages call first proposals "half-efforts until he pushes" and its only Facts line is the 0 code-tool runs, which nudges helpers away from the three asks and toward the code-reading failure. It does not name a remedy.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 5 | 21 |
| V2 | 4 | 4 | 3 | 2 | 4 | 17 |
| V3 | 2 | 2 | 2 | 1 | 3 | 10 |
## Sam test
Q1: Yes: measure what chats actually run, then enforce at the moment of the work (hook, handover start) rather than add prose; an agent-workflow expert would do exactly this before a sweep or a new rule.
Q2: Whole chats of the last two films (Protest Tiers' 32 and the film before), every tool and check the packs name: the scope Sam asked for, and the right evidence (adoption, not opinions).
Q3: Root cause is evidenced (pack line + tool + rule, 0 of 51 lookups used it; rule 61's only check is a warning). The fix acts in every chat without reading: the page is built at handover start and a hook stops the first hand look. Measured by the hook's own log.
Q4: Four approaches weighed (rule now, full sweep, learn-first, enforce by machine); text-only ones fail the evidence.
Q5: The learning step changes nothing; change 1 is one hook plus one line in handover start, its own Y, removable alone; it is narrow (read-only `grep -n`/`sed -n` on the film's own code) so edits and renders are never blocked. Risk named: it is not yet shown to work, hence its number and review.
Q6: Counts checked against tool-use-29-31.md, the ledger, job-packs.md, rule 61, settings.json, `wc -l`. Cost shares and step costs marked unchecked.
Q7: Not the cheap version: the audit is kept in full where it decides (adoption over two whole films plus notes back-filled), not trimmed to two chats; the prompt-only fix is rejected. Its cost is stated (~3-5%, unchecked).
Q8: Permanent changes, made properly, each reviewed against its number when Sam declares the next film complete; no trial.
## Pick
V1
## Why
V1 and V2 find the same real decision (why named tools and rules are not used, across a whole film) and the same root cause; V3 just forwards the three asks as three Y/Ns, sizes an 8-12% sweep before any result, bundles a change into an in-flight edit, and rests on a wrong fact ("29 chats"; the ledger has 32). V2's change 1 is the risk: a hard block plus pre-flight stops on any film file over 1,000 lines would halt Protest Tiers now (2,283 / 1,666 / 1,564 lines) in the middle of round 2, three changes under one yes. V1's change is narrower and also fixes the missing page at handover start. V1 is weak where its hook only warns (rule 61's warning already failed): I made it stop the first hand look per chat, with the `page.py find` line ready. From V2 I took: back-filling notes and repeated notes from Sam's messages into the ledger, so "fewer notes" can be measured; the pillar rule written as a check, not advice; and asking change 1 now as its own numbered question, since its evidence is already in.
## Faults in the pick
- F1 [fixed] The hook only warned; warnings are what failed. Now it stops the first hand look per chat until `page.py find` has run.
- F2 [fixed] Notes count 0 in all 32 chats, so the "fewer notes" aim could not be checked; the learning step back-fills them.
- F3 [fixed] V1 reads the missing page as the cause; `page.py FILM` writes the page itself, so its absence only shows it was never run. Stated so; building it at handover start still closes that gap.
- F4 [named] Learning-step cost (~3-5% of a week) and the grep cost shares (~27-33% of chats 29 and 31) are estimates, unchecked.
- F5 [named] The ledger's "After the film" line (33.55%) disagrees with its own spend (51.27%); the learning step reports why, it does not fix the ledger.
- F6 [named] The pillar rule Sam had critiqued is not written today; it waits for the audit's results.
## Final version
**Now (Q1, one Y):** the Opus chat editing the code-finding tool stops at a clean commit and pushes; nobody knows yet why the tool goes unused, so improving it waits. Protest Tiers' round 2 carries on unchanged.

**Learning step (changes nothing, Sonnet):** over every chat of Protest Tiers and the film before it: per chat, the pack its handover named, each tool and check that pack names, which ran, hand code looks (grep/sed/cat on film code), and what the chats that skipped a tool spent. Counts Sam's notes and repeated notes per round from his messages and back-fills the ledger; says why the ledger shows 0 and why its closing line says 33.55%. Tests `page.py find` on 10 real notes from round 1. Output: one table, rules and tools ranked by the cost of not being used. ~3-5% of a week (unchecked), filed as tool work (rule 24).

**Change 1 (Q2, its own Y; evidence already in: 0 of 51 lookups used the page):**
- `handover.py start` runs `page.py FILM` so the page always exists at the start of a notes round.
- A PreToolUse hook on Bash: the first read-only `grep -n`/`sed -n`/`cat` on `source/FILM*.py` in a chat is stopped with the ready line `python3 source/page.py FILM find "note words"`; once `page.py find` has run that chat, looks go through. Edits, renders and checks are never touched. Each stop and each look is logged.
- Number to beat: hand code looks per notes-round chat from ~25 to 5 or fewer; their cost share from ~30% to under 10%; read from the log, reviewed when Sam declares the next film complete. ~1% of a week to build (unchecked), with a kittest.

**Then, one at a time:** each unused tool or check the table ranks highest gets its own machine-enforced change, its own number and its own Y.

**Pillar rule last:** written from what worked, as a check: every rule names the machine that makes it happen and the number it must move, verified at film close.
## For Sam
### Option 1: Find out first, then make the code finder impossible to skip
Your tools went unused (0 times in two chats; 51 hand searches instead) because nothing makes a chat use them. First, one chat counts, across every chat of this film and the last one, which tools and checks were really used, and counts your notes properly. Separately, a stop that catches a chat searching film code by hand and points it to the finder. You'd notice cheaper notes rounds and a clear table of what works.
Lost: the full 8-12% sweep as asked (replaced by a usage count over two whole films); the pillar rule today; the code-tool edit pauses.
Added: one counting chat (~3-5% of a week); one automatic stop on hand searches; the finder's page built at every chat start; your notes counted in the ledger.
### Option 2: Enforce everything now, count as well
The same count, but the code rules become hard stops at once: no hand searches at all, and no check passes while a film file is over 1,000 lines. Stronger, but this film's files are over that size, so round 2 would stop until they are split.
Lost: round 2 stalls while files are split; the code-tool edit pauses; the pillar rule today.
Added: the same count; a hard block on hand searches; two new pre-flight stops.
