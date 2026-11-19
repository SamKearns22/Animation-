# Aim check: helper B

## Leak
Partial: the problem names its own remedy ("say so in its plan and handover", "a check that notices when it is missing"). Ignored here.

## Results
- Milburn's chats did refer to the aim on paper. Every re-estimate ends "over the 15% aim; why: ..." (17.5, ~19, ~24) and none changed how anything was built (notes/archive/milburn.md lines 73, 94, 109). Naming the aim is already happening; it does nothing.
- The one estimate that fell was after Sam pushed (17 Nov: "if these two parts cost 17.5% something has gone terribly wrong"). The rewrite found the people kit drew all five people in about ten steps against 7% priced by hand, and that part fell to about 4-5% (milburn.md 75-79). One challenge, about 12 points of plan.
- Cost: posted at 22% by Sam's app reading against a 24% estimate and a 15% aim (notes/proposals/milburn-review.md). The ledger's app rows add up to 32.85% (notes/ledger/milburn.md). The two figures disagree, and the week's dollar figure behind them is unchecked.
- "Building ran about 8.7 times plan" is weaker than it looks. The stage lines were closed late, so "sets" (16.7) holds the whole plan and cast (milburn-review.md section 2). Those numbers can't show stage overruns.
- Rule 24's budget alarms have been paused since 18 Nov (film-quality-rules.md row 24). The cost line (source/costline.py, 19 Nov) records the forecast after money is spent. Nothing acts before it is spent.
- Gap: the record doesn't count how many build choices (new piece vs kit, 3D vs flat, tier, model) were made without pricing a cheaper way. That count is the number any change must beat.

## The real decision
This isn't "add a line to the plan and handover". It is: who challenges each costly choice, the way Sam did on 17 Nov, before the money is spent, across the whole film? The bigger levers are the estimate itself (Milburn re-estimated up three times and never re-planned the build) and new builds where kit already existed.

## Root cause
The aim is a sentence a chat reads, not a step with an output. When the estimate crosses 15%, the chat that wrote the plan is the one that judges it, and it explains the gap ("the screenplay doubled") instead of looking for a cheaper way. The only challenger has been Sam. Advisory reminders have failed the same way before: the finder reminder (notes/proposals/finder-use.md) and the printed 100.4% forecast that nobody acted on.

## Approaches weighed
1. **A written aim line** in the plan and handover, checked for presence. Milburn already wrote it three times, so this passes on paper and changes nothing.
2. **Reframe: a cold "aim pass" at each cost decision.** A fresh helper that never saw the plan gets each new or dearest row and the ledger's measured costs. It names the cheapest way that keeps the quality (a kit piece, a flat painting, a Glimpse, Sonnet). The chat adopts it or writes why not. This is Sam's 17 Nov push, done by a tool.
3. **Steer on results only:** rely on the cost line after each stage. It is already built, and it acts after the spend.
4. **Learn first:** go back through Milburn and the film before it, and list each costly choice, whether a cheaper way existed, and what it cost.

Chosen: 4, then 2. Approach 2 alone would be guessing at which decisions matter.

## Proposal
**Learn (changes nothing; about 1% of a week; Sonnet):**
- From Milburn and the film before it (plan notes, estimate tables, kit growth, chat records), list every NEW row and every re-estimate.
- Mark each one: was a cheaper means already in the catalogue, did a challenge happen (Sam or a chat), and the points saved or lost.
- Also settle 22% vs 32.85%.
- Output: a count of missed cheaper ways, and the points they cost.

**Change 1 (one yes, only if the learn step finds missed cheaper ways worth at least 2 points per film; about 1% to build, Opus medium):**
- An aim pass runs when an estimate is entered or changed (`ledger.py estimate`, the plan's tool), and at the start of each build stage, for that stage's NEW rows.
- A fresh Sonnet helper (the critique's pattern) gets only those rows, the catalogue's matches and the ledger's measured costs. It answers per row: the cheapest means that keeps the quality, its price, and the measured cost it rests on.
- The tool files the answer, not the chat, so the chat can't write its own pass.
- The chat marks each row adopted, or "kept: why". "Kept" for quality is always allowed. Cutting a joke or content is never offered, and anything Sam added is never nagged about (his 19 Nov answer to search-first).
- Enforced: `ledger.py estimate` refuses to enter stages without a filed pass, and `handover.py end` refuses a build chat whose new rows have no pass.
- Number to beat, measured at the next film's end review: Sam needs to make no cost push, against Milburn's two (17 Nov, 19 Nov); no build stage lands over 1.5 times its plan (the cost line's own test); the plan's estimate is within 15% of the real cost.
- Cost per film: about 0.5% per pass, roughly 2-3 passes, so 1-1.5% against 15%. It pays only if it catches about one Milburn-sized miss. That is what the learn step checks.

**What Sam would notice:** the plan arrives already squeezed, with "Lost/Added" lines only where a cheaper way would change the look. He wouldn't need to ask "why so dear?".

## Sam test
- Q1: An expert puts a cold reviewer at the decision point instead of a reminder, which is the critique pattern that already works here.
- Q2: It looks at the whole film's choices across two films, not one chat's handover.
- Q3: A paper aim line is shown to fail (Milburn wrote it three times). The pass is filed by the tool, refused without it, and measured by Sam's cost pushes.
- Q4: Four different approaches were weighed, and the frame was corrected from "mention the aim" to "challenge each costly choice".
- Q5: Learning changes nothing. Change 1 waits on its evidence and can be undone alone.
- Q6: Sources are named. The 22/32.85 split and the week figure are flagged.
- Q7: It is sized to replace Sam's push, not to be the cheapest line in a template. Its honest cost is stated.
- Q8: It is permanent once yes, and reviewed when Sam declares the next film complete.

## Lost / Added
- Lost: about 1-1.5% of a week per film for the passes, and one extra step at the estimate and at each build-stage start.
- Added: a challenge before the money is spent, a plan that arrives already cheapened where quality allows, and fewer "why so dear" pushes from Sam.

## Unchecked
Which week figure is right (22% vs 32.85%). Whether `ledger.py estimate` can host the refusal cleanly. How many missed cheaper ways the film before Milburn holds.
