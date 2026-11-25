## Leak
yes: Sam's quoted words and his Y to "the rule as drafted" give the answer (a kit run at each film's start and end, a run suggested to him after a major kit change). They are his own request, so they cannot be left out, but they anchor every helper on "when", not "where between a broken tool and Sam's eyes".
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 3 | 2 | 3 | 3 | 4 | 15 |
| V2 | 4 | 4 | 4 | 4 | 4 | 20 |
| V3 | 3 | 4 | 3 | 3 | 4 | 17 |
## Sam test
Q1: Yes, with the patches: an expert tests the shared kit when a film starts and before anything reaches Sam's eyes (animatic, final), not at every worker's step; and fixes the test that crashes and the gate that stopped testing first.
Q2: Scope is the whole film across parallel chains; evidence is the refusal log (19 "still running" refusals 23-25 Nov; 5 kit refusals after the stamps went in, in 2 chats), the reds log (one test red across 4 chats), the stamp file and the code. The usage cost itself is unmeasured; Step 0 measures it.
Q3: Enforced in code (start-up script, handover, finish), with a kit test proving a mid-film chat neither runs nor waits; numbers to beat: mid-film kit refusals to 0, kit waits in mid-film chats to 0, animatics on untested shared code to 0. The "major change" suggestion is printed by the handover from the stamps, not left to a chat's judgment.
Q4: Five approaches weighed (Sam's draft, test at Sam's eyes, repair-first, outside runner, learn-first); V3's "test only your own change" was also weighed and loses because it keeps per-chat runs Sam asked to end.
Q5: Each change and fix is its own commit and undoes alone; nothing Sam sees goes untested, because the final (and, on his Y, every animatic) is still gated. Risk named: a shared-kit break made mid-film is now found at the next animatic, not the next chat.
Q6: Facts checked: the Override-branch regression (handover.py 581-600: without Override the stale run never happens), the crash (next-jobs.md), stamp grain (kitstamps.py 85, ink.py 82, body.py 78 of 147 tests), the refusal counts. Unchecked items are named.
Q7: It keeps the animatic gate that the cheap version drops, and fixes the crash and grain rather than routing round them. Build cost about 1% of a week per piece, unchecked.
Q8: Permanent changes, no trial; Step 0 is a measurement, not a provisional rule; reviewed at the film's end.
## Pick
V2
## Why
V2 is the only version that read the code and found that the problem is partly a broken system, not just a frequent one: a test that has crashed on every fresh machine since 22 Nov (2 of the 5 post-stamps refusals), the handover's own stale run accidentally moved inside the Override branch (so a chat's final code is not tested at all without Override), and the stamp tool itself being read by 85 tests, so editing it reruns most of the kit. It gives Sam exactly what he said Y to (Change 1) while keeping the gate where Sam's eyes meet the work as its own question with a measured count. V1 is Sam's draft unchanged: it drops the animatic gate, runs a full 15-minute set where stale-only would do, and relies on a chat judging "major". V3's idea (a chat tests only what it changed) is clever but keeps per-chat runs Sam asked to end, makes all three changes wait on the learning, and states a wrong fact (stamps "went in at 17:40"; git shows 13:07, last fix 17:23).
Taken from V1: a new tool's own kit test still runs once when it is built. Taken from V3: "first chat = the film has no ledger rows yet"; and the "whose change" idea, used only to print the major-change suggestion from the stamps (V1 step 3, made mechanical).
## Faults in the pick
- F1 [fixed] "Undo c87022ef" would also remove Override's logging; the fix is to move the stale run and the busy wait out of the Override branch.
- F2 [fixed] "Nearly all he saw came before the stamps" overstates: 5 of the 10 kit refusals on 25 Nov came after 13:07.
- F3 [fixed] On Change 2 = N, Sam's own "suggest a run after a major kit change" was lost; restored, printed by the handover from the stamps.
- F4 [fixed] A new tool's own kit test was not mentioned; it still runs when built (V1).
- F5 [named] Whether the code can tell a film's first chat is unchecked (Step 0 c); "no ledger rows" is the proposed marker.
- F6 [named] Stale tests now pile up across mid-film chats; the first animatic after a core drawing change may wait up to a full run (about 15 min) in a Sonnet chat. F3's grain fix shrinks it.
- F7 [named] The usage cost of kit tests per chat and the build costs are unmeasured estimates.
## Final version
**Step 0, learn (changes nothing, about 0.3% of a week).** From the last 3 days of chats: (a) share of a week spent on kit tests (waits, refusals, retries, fixing others' reds); (b) for each past red, the chat that caused it and any animatic made before it was caught; (c) whether handover can tell a film's first chat (marker: the film has no ledger rows yet).

**Change 1 (Sam's Y already given).** The start-up background run happens only in a film's first chat, and the handover kit gate applies only there. Mid-film chats neither run nor wait. A new tool's own kit test still runs once when it is built. A kit test proves a mid-film chat does not run or wait. To beat: mid-film kit refusals to 0; kit waits in mid-film chats to 0.

**Major-change line.** At every handover the chat prints how many kit tests its own commits made stale (from the stamps). Over 20, the message to Sam carries one plain line suggesting a run, run only on his Y.

**Change 2 (own question, asked with Step 0's count b).** Keep the stale-only kit gate before every animatic, as well as the final. On N, only the final is gated. To beat: animatics on untested shared code to 0.

**Fixes (one commit and one kit test each, listed for the end-of-film review):** move the handover's stale run out of the Override branch, keeping Override's skip and log; make the crashing description test run on a fresh machine; stop the stamp tool's own file counting as a read of 85 tests.

**Kept:** final always gated; Override skips as now, logged. **Dropped:** the resume proposal (Sam's Y).
Cost: about 1% of a week per piece, once (unchecked). Reviewed against the film's results at its end.
## For Sam
### Option 1: Check at film start and before you see it
Problem: The kit checks (each re-checks a fault you once caught stays fixed) run in every chat and often stop a chat from finishing while they run. Two of them are also broken: one check crashes on every fresh start, and a recent change stopped the end-of-chat run from testing the chat's own work.
1. First, a short count from the last three days: how much usage the checks cost, and whether a fault ever reached an animatic.
2. The checks run only in each film's first chat; later chats never run or wait for them.
3. When a chat changes a lot of the shared kit, its message to you suggests a check, run only on your yes.
4. The check before the final stays; I'll ask you separately whether to keep it before each animatic too.
5. Fix the crashing check, the broken end-of-chat run, and a fault that makes most checks rerun needlessly.
Why: It does what you asked, and still nothing reaches you on untested tools.
You'd notice: Chats no longer stall at the end; the first animatic after a big drawing change may take up to 15 minutes longer.
Other option: Each chat checks only what it changed itself (option 2).
Lost: The check in every chat, and early warning of a break made by another chat.
Added: One short count, a suggestion line in messages after big kit changes, three repairs.
### Option 2: Each chat checks only its own changes
Problem: Every chat waits for checks on work other chats changed, so most of the cost falls on chats that never touched the shared kit.
1. First, measure over a week which chat caused each failed check and how long checks take.
2. Only a film's first chat runs the checks at start, without holding anything up.
3. At the end of a chat, only the checks touched by that chat's own changes run; others are listed, not run.
4. A full check runs before the final; animatics run only what has changed since.
Why: The chat that breaks something finds out itself, before it ends.
You'd notice: No waiting in chats that only work on the film; a chat that changes the shared kit still waits.
Other option: Check only at film start and before you see it (option 1).
Lost: The start-up check in every chat; checks on other chats' changes at the end of a chat.
Added: Checks in chats that change the kit, without asking you, which is more than you asked for.
