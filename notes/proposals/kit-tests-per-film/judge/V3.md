## Leak
The problem file gives the answer (start and end of the film, Sam's Y). Weighed below as one option.

## Results
- Sam's complaint came at 17:56 on 25 Nov. The new per-test stamps went in at 17:40 (Sam's log, git log). **Nothing has measured the new system yet.**
- Handover refused 19 times on 23–25 Nov because the tests were still running. Retries re-pay the whole chat (handover-end.log).
- Since the stamps: 3 refusals came from a crashed test. Override then skipped 38 stale tests, 3 times (overrides.log).
- Tests failed ("reds") 12 times in 11 chats over 3 days, in ordinary working chats. 11 of the 12 were in chats that had changed source/ (git log). One test stayed red across 4 chats in a row (kittest-reds.log).
- Usage per wait: unchecked; rough guess 0.05–0.1% of a week a chat (brexit-is-done ledger), about 1–2% a film.

## The real decision
Across all a film's chats: the chat that breaks a check finds out itself, and no other chat waits. The bigger lever is whose change a run tests, not when it runs.

## Root cause
Every chat pays for changes other chats made:
- the start-up run tests every stale file, whoever changed it;
- handover waits for that run (19 refusals plus retries);
- handover also runs every test made stale by other chats.

The stamps cut how many tests run, not who runs them. Film start and end only saves cost by testing less: a check broken mid-film stays broken through every animatic, after the chat that broke it is gone.

## Approaches weighed
1. **Film start and end only** (Sam's draft). Cheapest. Mid-film reds (12 in 3 days) go unseen while Sam watches animatics.
2. **Reframe: each chat tests only its own changes.** A chat that changed no kit file runs nothing. One full sweep runs in the film's first chat (in the background) and one before the final.
3. **Learn first:** measure the new stamps system before changing anything; it may already cost little.
4. **A run outside the chats.** No runner exists for this (unchecked), so it can't be done yet.

Chosen: 3, then 2. It removes the cost from chats that don't touch the kit, keeps faults caught before Sam sees them, and makes "if the kits change" automatic.

## Proposal
**Learn (changes nothing, about 0.3% of a week).** Over the past 7 days and the next 10 chats, find:
- whether each red's files were changed by the chat that saw it;
- the kit-test steps and minutes in each chat (from the transcripts);
- how many chats changed no kit file.

**Change 1 (own yes).** Only a film's first chat runs the tests at start-up, and it blocks nothing. (First chat = no ledger rows yet.) Number to beat: "still running" refusals, from 19 to 0.

**Change 2 (own yes).** At handover, a chat runs only the stale tests that read files it changed itself. Tests made stale by others are listed, not run. Number to beat: kit steps in a chat that changed no kit file, to 0; reds first seen by a later chat, to 0.

**Change 3 (own yes).** The full stale sweep runs before the final. Animatics run only what is stale, which takes seconds once Change 2 is in. Number to beat: animatics or finals on untested files, 0.

Each is enforced in code, and goes ahead only if the learning shows its waste. Cost: about 1.5% of a week once, shared by all films. Saving: about 1–2% a film. Both are unchecked estimates. What Sam would notice: no kit waits in ordinary chats.

## Sam test
- Q1: test where the change is made.
- Q2: every chat over 7 days.
- Q3: in code; three numbers.
- Q4: four approaches; this fixes who pays.
- Q5: learning first; each change undone alone.
- Q6: sources named; guesses unchecked.
- Q7: keeps the mid-film catch that option 1 drops.
- Q8: the changes are permanent and reviewed at the film's end.

## Lost / Added
- Lost: the start-up run in every chat; inherited tests at mid-film handovers.
- Added: each chat tests its own changes; sweeps at the film's first chat and before the final; one learning report.
- This differs from Sam's draft: a chat that changes the kit tests it without asking him.

## Unchecked
- Usage cost per wait.
- Whether each red was the seeing chat's own change.
- Whether the code can tell a film's first chat.
- Whether a fault reached Sam because of a broken check.
- Whether an outside runner exists.
- The cost of the changes.
