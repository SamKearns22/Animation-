# Helper A: chat size and model switching

## Leak
None in the problem file. (A separate chat.md in this folder holds the writing chat's idea; not used.)

## Results
- Protest Tiers cost 101.29% of a week against the 15% aim, 61 chats (notes/ledger/protest-tiers.json). Round 2 was priced 0.865 of the plan and spent 47.6% (stages: 53.21 to 100.78).
- 16 Nov: 24 chats, 39.3%, 1,479 steps: checked (same file). 19 Opus chats: 1,305 steps, 35.18%.
- Chat size: the fit's best length (106 steps) applied to all 1,305 Opus steps gives 33.95%: at most about 1.2% saved on a 39% day (~3%). Size is a small lever.
- Model: Sonnet 64 steps cost 0.8 (1.25 per 100 steps); Opus 60-80 steps 2.7 per 100 (problem file; Sonnet row checked). Routine on Sonnet is about half price: a bigger lever than size.
- Volume: 1,479 steps in one day, mostly rework rounds; the 15 Nov record already found moves "ran as fix rounds on the same faults" (notes/proposals/learn/protest-tiers-costs.md). The biggest lever of the three.
- "Routine on Opus": CLAUDE.md itself says "A round of my notes (deciding, fixing, clips) and building from a clear plan or sound: Opus, medium". France "look, check, clip" and "France sound" on Opus medium followed the rule as written. The check (source/handover.py model_faults, line 317) reads only the Next line, and clips are excluded on purpose: checked.
- Contradictory advice: "too many chats" (notes/budget-job.md line 77) and "split into chats of 200k or less" (notes/cost-diagnosis.md line 45): checked.
- Gap: how many of the 1,305 Opus steps were routine (look, check, render, sound) is not in the record (rows are "auto", no job type).

## The real decision
How a film's chats are priced: steps x price per step. Chat length moves the price ~3%; model moves it ~50% for the routine share; step count (rework) moves it most. The size question is the smallest of these. The rework lever needs its own route; it is named here, not bundled.

## Root cause
1. Sam gets different size answers because size has been set by whichever symptom was measured that day (chat starts on 11 Nov, long history on 13 Nov), and written in several places (CLAUDE.md, rule 85, handovers). No single number owns it.
2. Routine runs on Opus because the model rule puts clips, looks and sound with the Opus round, and a round chat is one bundle; the check only reads the handover line, never the model a chat is actually opened on.

## Approaches weighed
- A. One fixed length (hand over near 100 steps). Saves ~3%; does not touch the model problem.
- B. Reframe: one statement, "a chat is one job; the cost watch alone sets when to hand over", and model enforced at the moment a chat is opened (a hook: an automatic gate that runs when a chat calls create_session and refuses Opus for a job whose words are all routine).
- C. Learn first: tag each 16 Nov chat's steps by job (fix, build, look, check, clip, sound, render, bookkeeping) from its transcript, to find the routine share on Opus and the true Sonnet price for the same jobs.
- D. Reframe wider: cut steps (faults caught before rework). Biggest lever; separate route.
Chosen: C, then B as two separate changes; D proposed on its own.

## Proposal
**Learn (changes nothing):** a Sonnet chat tags the 24 chats of 16 Nov by job, using list_events. Output: routine share of Opus steps and cost; Sonnet cost per 100 steps on look/check/sound. About 1-1.5% of a week (unchecked).
**Change 1, model at the gate (only if the learn step shows routine above ~15% of Opus cost):** rewrite the model line so clips-only, look, check and sound-to-plan go to Sonnet, and the fix chat ends by opening that Sonnet chat. Enforced by the hook on create_session, not by a chat choosing to read it. Number to beat: Opus cost on routine jobs in the next film, against the measured 16 Nov share. About 2% to build.
**Change 2, one size rule:** one line in CLAUDE.md replacing the others: "A chat is one job; it hands over at the cost watch's amber, nowhere else." Amber/red numbers change only through the route on ledger evidence. Number to beat: Opus cost per 100 steps no higher than 2.7, and Sam given no other size advice. Under 0.5%.
Total about 3.5-4% once, against 15% per film; the model change alone pays back on one film if the routine share is as large as it looks.
Sam would notice: shorter Sonnet chats after each fix; one answer on size, never repeated.

## Sam test
- Q1: Yes; route by job and enforce at the gate is standard agent practice.
- Q2: Evidence is the whole film and all 42 step-counted chats; the job tagging widens it.
- Q3: The gate runs on every chat opening; no reading needed. Measured by ledger.
- Q4: Four different levers weighed; the largest (rework) sent to its own route.
- Q5: Each change undone alone; Change 1 waits for its evidence.
- Q6: Sources named; gaps marked.
- Q7: Sized by the result; not the cheap "length number" version.
- Q8: Permanent changes, reviewed at film end.

## Lost / Added
Lost: Opus doing clips and sound; scattered size advice. Added: a gate on opening chats; one size line.

## Unchecked
Routine share of 16 Nov Opus steps; learn-step cost; whether "Sonnet" labels on 72-79-step rows are right; that a hook can read create_session's model field.
