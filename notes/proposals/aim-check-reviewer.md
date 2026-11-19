# Proposal: Sam's aim check, step 2: whether and how a fresh reviewer should question costly choices, given the study's numbers

Status: open

## Problem
Sam's aim (CLAUDE.md, "Every stage aims at three things"): high quality, fewer notes and faults, a film within 15% of a week. Sam chose Option 1 of notes/proposals/aim-check.md on 19 Nov: a study first, then one yes on the fresh reviewer with the learned numbers. The study (notes/proposals/aim-check/study.md) found that missed kit reuse cost almost nothing in the last two films, while both films still ran far over 15%. The verdict's reviewer was sized and aimed on the guess that missed cheaper ways were a large share of the overrun. The question now is what, if anything, Sam should be asked to say yes to, given where the money actually went. Jokes and content are never cut; Sam's own additions are never questioned.

## Facts
- Study (notes/proposals/aim-check/study.md): 17 NEW rows in Milburn, 9 in Blessed plus 5 unplanned builds. A same-quality cheaper way already in the kit was missed 2 times clearly, 1 partly, all Milburn, 0 Blessed; together about 0.1 to 0.2% of a week; none challenged; 2 of 3 mid-stage.
- Overruns at 366 USD a week: Milburn 22.0% (80.44 USD) vs 15% aim; Blessed 48.6% (notes/ledger/milburn.md, blessed.md).
- Blessed's spend by cause: rework of returning faults about 15% (Walliams' face 10.9%, repeat notes about 4%); chat 5 bundled four stages to 414k history, 9.6%, about 4% avoidable; animatic 1 stage 7.2% vs 2% planned; critique helpers about a quarter of each build chat (notes/cost-diagnosis.md).
- Milburn's: screenplay doubled 34 s to 68 s; three re-estimates, each up (17.5, ~19, 24); the reverse two-shot staged three times; scene 3 re-staged; the 3/4 fix 3.6% in one chat; searching and re-reading 15-35% of most Opus chats; Sam made two cost pushes (notes/proposals/milburn-review.md; notes/proposals/aim-check.md).
- The verdict's reviewer: about 1 to 1.5% of a week per film; its fault F6 says it pays only if it catches about one Milburn-sized miss; F4 says choices made inside a stage (re-staging, a big fix in one go) fall between its passes (notes/proposals/aim-check.md).
- Ledger-to-app ratio: about 1.00 at 366 USD a week (Milburn ledger 21.99% vs Sam's 22%); the 0.68 came from the old week price (study.md).
- Already in place: the quiet cost line in handover.py end records the forecast and flags a stage over 1.5 times its share, shown to Sam only on a problem (notes/real-cost.md); Sam does not want a cost message every time (19 Nov 09:14, aim-check.md).
- Queued from Milburn's review with Sam's Y: two quick framings before a staging note is built (lesson 3), the guard letting film questions through (lesson 6), and others (milburn-review.md, "Sam's answers").
- Unchecked: the cost of each re-stage on its own; whether a reviewer at re-stage time would have changed Milburn's reverse.

## Record
notes/proposals/aim-check/study.md
notes/proposals/aim-check.md
notes/proposals/milburn-review.md
notes/cost-diagnosis.md
notes/real-cost.md
notes/ledger/milburn.md
notes/ledger/blessed.md
notes/archive/milburn.md
notes/archive/blessed-handovers.md
guides/kit-catalogue.md
CLAUDE.md
source/costline.py
source/handover.py

## Verdict (the judge, word for word)
<!-- verdict-hash: 802a2c9dae7d2bee -->
Who wrote which (hidden from the judge): V1 = helper B, V2 = chat, V3 = helper A. Picked: V0 (the judge (V0: no version passed, so it wrote a better one)). Critiqued: 6 found, 3 fixed, 3 named.

## Leak
yes, mild: the title ("whether and how a fresh reviewer should question costly choices") assumes the reviewer is the thing being decided, and the Facts list F4 ("choices made inside a stage fall between its passes") beside the re-stage and rework costs, which points toward moving the reviewer to re-stages. No remedy is stated outright.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 3 | 4 | 5 | 5 | 21 |
| V2 | 3 | 3 | 2 | 2 | 4 | 14 |
| V3 | 4 | 4 | 4 | 4 | 5 | 21 |
| V0 | 5 | 4 | 4 | 5 | 5 | 23 |
## Sam test
Q1: Yes. An expert stops a checker that fails its own bar (about a tenth of its cost back, study.md line 31) and prices where the money went before adding anything: rework, re-stages and long chats (cost-diagnosis.md lines 40-47, 85-87).
Q2: Yes. Both films, every chat, priced by cause from the ledgers' per-chat app figures and "cost by kind of step" splits (ledger/milburn.md), not kit reuse alone.
Q3: The root cause is shown with evidence (rework, re-stages, chats past 200k; not missed kit). The learn step's output is a number per cause; any later change is enforced by the handover check, not by a chat choosing to read it; success is a number checked at the film's end review.
Q4: Four approaches weighed across V1 and V3: reviewer as built, a trigger-fired reviewer, queued lessons only, and learn-first; plan-time pricing was weighed and left (Sam declined repeated cost messages, aim-check.md 09:14).
Q5: Low risk. Closing the reviewer removes nothing that ever ran; the learn step changes nothing; Sam is not asked to trust an unproven checker.
Q6: Every number checked and sourced; the problem file's mix of week sizes (cost-diagnosis at 290 USD, ledgers at 366) is corrected; re-stage costs remain marked unchecked until the learn step.
Q7: Not the cheap version: the dearer measure is dropped because it buys nothing on the record, and the next change is sized by its measured cause, with its honest cost stated.
Q8: Nothing temporary: the reviewer is closed for good, not trialled; any later change is made properly with its own yes and reviewed at the film's end.
## Pick
V0
## Why
V1 and V3 are close and both right on the real decision (which lever closes a whole film's gap to 15%, not how a reviewer should question choices). Neither passes cleanly as written. V1 rests on an unconverted figure: "rework about 15%" and "Walliams 10.9%" are shares of a 290 USD week; at 366 they are about 8.7% and 3.2% (V3 caught this). V1 also leaves out the biggest measured cause, chats growing past 200k history (26 of 36 Opus chats, 158 of 176 USD, cost-diagnosis.md lines 86-87), and its "Milburn's overrun was set at the plan" glosses that the plan rose three times mid-film (17.5, ~19, 24). V3 has the facts right, including that the reverse was re-staged for taste ("poor", note 5, archive/milburn.md line 233), which a cost reviewer would not have caught, but it keeps the reviewer alive as a conditional Step B, so Sam's one yes still half-commits him to an unproven checker sized before the learning. V2 builds a re-stage reviewer before any measure shows it would have changed a single moment, and folds two changes (plain catalogue search at the plan, reviewer at re-stages) into one yes.
V0 takes V3's facts, cause list (including chat size) and covered/uncovered marking; V1's clean close of the reviewer now and its whole-film success number (rework plus re-stages, plan-set gap against after-plan gap); and drops V3's pre-committed Step B: whatever the table shows uncovered goes to the route as its own proposal, a reviewer only if the table points to one.
## Faults in the pick
- F1 [fixed] Week-size mix: Blessed's cause shares converted to the 366 USD week (rework ~12%, Walliams ~8.7%, bundling ~3%).
- F2 [fixed] Chat size (history re-reading 49% of Opus spend) added as a priced cause; V1 left it out.
- F3 [fixed] No conditional reviewer bundled into this yes; the later change goes through the route on its own.
- F4 [named] The ledgers record 0 notes and 0 repeats and closed Milburn's stage lines late, so the per-cause split leans on the per-chat step splits and the notes tables; it will be rough (upper ends given).
- F5 [named] Whether a reviewer at re-stage time would have changed anything stays unchecked; the evidence so far (the reverse was a taste note) suggests not.
- F6 [named] The learn step costs about 0.5 to 1% of a week and changes nothing on its own; its value is that the next yes is aimed at a measured cause.
## Final version
**Sam's one yes now:** the fresh reviewer (Change 1 of aim-check.md) is closed, unbuilt and for good. The study shows missed kit reuse cost about 0.1-0.2% of a week across both films, against the reviewer's 1-1.5% a film; it fails its own bar (F6) about tenfold. Nothing goes in CLAUDE.md or the rulebook.

**Learn step (changes nothing; about 0.5-1% of a week; Sonnet, routine):** for Milburn and Blessed, price at 366 USD a week, from the ledgers' per-chat app figures and cost-by-step splits, the notes tables and the chat records:
1. each re-stage and each repeated note (rework);
2. each re-estimate's added scope, means only, never the joke;
3. each chat that ended past 200k history, and what it would have cost under 200k;
4. reading and search; checks and critique helpers.
Mark each "covered by" (queued lessons 1, 2, 3, 4, 6, 8, 9, 11, 12, or an existing rule) or "uncovered", and whether a cold reader at that moment had a same-quality cheaper means. Output: points per cause per film, split into plan-set and after-plan, and the uncovered total.

**Then:** the queued lessons go ahead as Sam already ordered. If the table shows an uncovered cause above about 3 points of a week per film, that cause goes to the route as its own proposal with its number (a re-stage reviewer only if the table points there), enforced by the handover check, not by a chat reading it. Sam gets no new cost messages.

**Number at the next film's end review:** rework plus re-stages under 3% of a week (Blessed about 12% at 366), and the film within 15% of a week, or within its estimate where Sam's brief alone sets it over.

Sam would notice: one short message closing the reviewer, then the priced table's result with at most one new numbered ask.
## For Sam
### Option 1: Close the checker, price where the money went
The second-opinion checker we planned would have saved about a tenth of what it costs: the films hardly ever missed a cheaper ready-made piece. So it's closed, unbuilt. Instead, one cheap job (no change to anything) adds up where both films' money really went: redoing things you'd already noted, re-staging shots, and chats that grew too long and kept re-reading themselves. The lessons you already said yes to go ahead; anything left uncovered comes back to you as its own question, with its number.
Lost: the second-opinion checker at planning time (never built; worth about 0.1% of a week a film).
Added: about half to one percent of a week for one priced list of where the money went.
### Option 2: Keep the checker, move it to re-stages
The checker stays, but only wakes up when a shot is about to be staged again or a note comes back, and suggests the cheapest way that keeps the quality, plus a quick still for you first. Nothing yet shows it would have changed a single moment in the last two films: the scene staged three times was a taste call, not a cost one.
Lost: the checker's look at every new piece at planning time.
Added: an extra check at each re-stage or repeated note, about 1% of a week to build and a little each time it runs.
