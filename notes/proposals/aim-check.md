# Proposal: Sam wants every planning and building stage to refer back to the cost aim

Status: open

## Problem
Sam, 19 Nov: "If you aren't referring to statement one when you're planning and building, then that needs fixing." Statement one is CLAUDE.md's aim: every stage aims at high quality, fewer notes and faults, and a film within 15% of a week, and every idea for cost or speed makes new things better, cheaper or faster (smarter tools, faults caught before Sam sees them, reading less), never less or worse. Today nothing makes a chat look back at that aim while it plans or builds, or says so in its plan and handover, so cost and quality are weighed only when Sam pushes. Sam wants it to be a habit of every planning and building stage, with a check that notices when it is missing.

## Facts
- The aim is written once in CLAUDE.md ("Every stage aims at three things..." and "The channel is topical..."), not repeated in the plan or the handover (CLAUDE.md, 19 Nov).
- The handover's lines are fixed: Rules that bite next, Done, Next, Needs Sam, Read, Open rule requests, For Claude (CLAUDE.md "Fresh chats and the handover"). None names the aim.
- Milburn: estimate 24% of a week, app's real cost 32.85% over 17 chats; building sets, props and board ran about 8.7 times plan while a forecast of 100.4% was printed and not acted on (notes/ledger/milburn.md; notes/proposals/search-first.md).
- source/handover.py end already runs checks and lists faults a chat must settle before handing over; source/propose.py guards rule proposals the same way.
- Sam's rule: it must be added only through the proposal route and only on his number (CLAUDE.md "Rules are permanent").

## Record
CLAUDE.md
guides/job-packs.md
source/handover.py
notes/ledger/milburn.md
notes/proposals/search-first.md

## Verdict (the judge, word for word)
<!-- verdict-hash: 885daae99333d936 -->
Who wrote which (hidden from the judge): V1 = helper B, V2 = chat, V3 = helper A. Picked: V1 (helper B). Critiqued: 6 found, 3 fixed, 3 named.

## Leak
yes: the problem says the chat should "say so in its plan and handover" and asks for "a check that notices when it is missing", which points straight at a written line plus a presence check.
## Scores
| version | quality | notes | cost | risk | undo | total |
|---|---|---|---|---|---|---|
| V1 | 4 | 4 | 4 | 4 | 4 | 20 |
| V2 | 2 | 1 | 2 | 4 | 5 | 14 |
| V3 | 3 | 3 | 3 | 2 | 4 | 15 |
## Sam test
Q1: Yes. An expert puts a cold challenger with measured numbers at the moment a cost is set, and that is the critique pattern that already works here. Reminders don't do it.
Q2: Yes. It covers every new or costly choice across the whole film, and the learn step reads Milburn and the film before it, not one chat.
Q3: Mostly. The tool files the pass, not the chat, and the estimate and the handover refuse without it. The proof is Sam's cost pushes (Milburn had 2) and stages within 1.5 times plan. Still weak: build choices made mid-stage (staging a shot three times, the one-go 3/4 fix) fall between passes. Named.
Q4: Yes. Four different approaches were weighed (a line, a cold pass, results only, learn first), and the frame moved from "mention the aim" to "challenge each costly choice".
Q5: Learning changes nothing. Change 1 now comes back for its own yes with the learn step's number, so Sam isn't asked to trust it before the evidence exists. It undoes alone.
Q6: The milburn lines (73, 94, 109), 32.85%, 100.4%, the late-closed stages and the paused rule 24 check out against the record. The 22-vs-32.85 gap is partly explained: the review puts the ledger about 10 points high (ratio 0.68). It is still not settled.
Q7: It is sized to replace Sam's push (about 1 to 1.5% a film). It is neither a template line nor a large build ahead of the evidence.
Q8: It is permanent once Sam says yes, and reviewed when he declares the next film complete.
## Pick
V1
## Why
V2 is the leaked remedy. Milburn already wrote "over the 15% aim; why: ..." three times and nothing changed, so a presence-checked line passes on paper and does nothing. V3 rests on a wrong fact: it says nothing prints a forecast or a stage overrun at handover. In fact the quiet cost line (costline.py, 19 Nov) already runs inside handover.py end, records the forecast and flags a stage over 1.5 times its share. So V3's Change A largely repeats it. Its "re-plan when the forecast passes 15%" is also the wording Sam answered on 19 Nov 09:14 with "I don't want to see that message all the time", and it brushes against the paused rule 24. V1 is the only version that acts before the money is spent, at the moment Sam's 17 Nov push acted. It also reads its facts correctly.
Taken from V3: the plan's new items carry routes with a price (V3 Change B), folded into what the pass answers, and V3's point that stages must be closed on time so the pass's measured costs are real. Added by me: the pass weighs all three aims (quality and fewer notes as well as cost), and Change 1 gets its own yes after the learn step.
## Faults in the pick
- F1 [fixed] V1 asked for one yes to a change that only applied if the learn step's threshold was met, which is a yes given before the learning. Now the learn step runs first and Change 1 comes back with its number.
- F2 [fixed] The pass weighed only cost. Statement one has three aims, so it now also names any better-quality way at about the same price and any risky move that needs a rehearsal clip first.
- F3 [fixed] V1 left the 22-vs-32.85 gap fully open. The review's 0.68 ratio is now named and the learn step confirms it.
- F4 [named] Build choices made inside a stage (re-staging, a big fix done in one go) are not covered by a pass. The learn step will show whether they matter.
- F5 [named] Whether `ledger.py estimate` can host the refusal cleanly is unchecked.
- F6 [named] The pass costs about 1 to 1.5% of a week per film. It pays only if it catches about one Milburn-sized miss.
## Final version
**Learn first (changes nothing; about 1% of a week; Sonnet).** From Milburn and the film before it (plan notes, estimate tables, kit growth, chat records), list every NEW row, every re-estimate and every re-stage. For each, mark three things: was a cheaper way of equal quality already in the catalogue, did anyone challenge it (Sam or a chat), and the points saved or lost. Confirm the ledger-to-app ratio (0.68 from the Milburn review). Output: the count of missed cheaper ways, their cost in points, and how many fell mid-stage rather than at the plan or a stage start. That number goes to Sam with Change 1.

**Change 1 (its own yes, after the learn result; about 1% to build; Opus medium).**
- When an estimate is entered or changed, and at the start of each build stage, a fresh Sonnet helper that never saw the plan gets three things: only the stage's NEW rows, the catalogue's matches, and the ledger's measured costs.
- For each row it answers four things: the cheapest way that keeps the quality, its price and the measured cost behind it, any better-quality way at about the same price, and any risky move that should get a rehearsal clip first.
- The tool files the answer, not the chat.
- The chat marks each row "adopted" or "kept: why". Keeping something for quality is always allowed. Cutting a joke or content is never offered, and nothing Sam added is ever questioned.
- The estimate refuses to enter stages without a filed pass. `handover.py end` refuses a build chat whose new rows have no pass, and refuses a stage left unclosed, so the measured costs stay honest.
- It sends Sam no cost messages. The quiet cost line stays as it is.
- If the learn step shows mid-stage misses matter, the pass also runs on any re-stage or re-build.
- Number to beat at the next film's end review: Sam makes no cost push (Milburn had two), no build stage goes over 1.5 times its plan, and the estimate lands within 15% of the real cost.
## For Sam
### Option 1: A fresh reviewer questions each costly choice, after a study
First a short study of the last two films (about 1% of a week, changes nothing). It counts how often a cheaper way of the same quality was already in the kit and was missed, and what that cost. If the misses are worth it, you get one yes: whenever a plan is priced or a build stage starts, a fresh helper that has never seen the plan looks at each new thing. It says the cheapest way that keeps the quality, any better-looking way at the same price, and any risky move to test first. The chat takes the advice or writes why not. You'd notice plans that arrive already tightened, and no more "why so dear?" from you.
Lost: about 1 to 1.5% of a week per film for the helper, and one extra step when a plan is priced and when each build stage starts.
Added: a challenge before the money is spent, not after, and you wouldn't have to be the one doing it.
### Option 2: An "aim" line in every plan and handover
Each plan and handover gets one sentence saying which route was chosen for the best quality at the lowest cost, and a check refuses a handover without it. It's cheap and quick. But Milburn already wrote a line like this three times and nothing changed, so it would probably pass on paper and change little.
Lost: almost nothing, one line per handover.
Added: the aim written down every chat, but no one actually questions the choices.
