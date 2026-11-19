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
