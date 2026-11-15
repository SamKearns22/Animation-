# Helper B: find out which rules and tools work

## Leak
None. The problem file states the problem and facts only.

## Results
- **The outcome record is empty.** Every ledger reads "0 rounds, 0 notes, 0 repeated": Protest Tiers (32 chats), Blessed (24), Remakes (19) (notes/ledger/*.md). Sam gave Protest Tiers at least note 1 and round-1 notes R1-R5 (notes/protest-tiers.md). So today nothing can say whether any rule cut notes: the measure the question needs is not being kept. This gap is the main finding.
- **Cost, not rules, is where films fail.** Spent vs estimate: Blessed 62.21% vs 19.0; Remakes 35.96% vs 14.5; Protest Tiers 51.27% so far vs 63.51 (ledgers). Against the 15% aim, all three are 2.4-4x.
- **Where Protest Tiers' money went** (stage ends in its ledger): moves 11.30% (planned 3.07), round-1 moves 14.04% (planned 4.45), plan extras 10.08% (planned 0), cast 5.96% (planned 2.09). Moves alone: 25.3 of 51.3%.
- **Inside a chat** (bills-29-31.md): code looks 35% and 27% of calls; start-up reading 11-20 of the first 20 actions; helpers 0. Prescribed tool page.py: 0 runs in chats 29 and 31, 25 and 26 hand greps (tool-use-29-31.md), although job-packs.md line 32 tells chats to use it.
- **What acts by itself:** only setup, cost watch, handover log and ledger auto (.claude/settings.json). Everything else (pre-flight, page.py, critique) waits for a chat to choose it.
- **Rules are adopted untested:** cost stops ran on self-reported figures 20-75% low; a "pillar" rule had 8 faults found only when Sam asked (sam-to-case4.md).
- Counts: 65 numbered rule rows (film-quality-rules.md, grep); about 124 catalogue table rows (kit-catalogue.md, grep, includes headers).

## The real decision
Not "audit 180 rules and tools" but: does the project have a permanent loop that measures, per film, the three aims (cost per stage, Sam's notes, repeats) and ties each bad result to the rule or tool that should have prevented it? Bigger levers than any one rule: the missing outcome record, and the moves stages that cost five times their plan.

## Root cause
Rules and tools are written as instructions a chat must read and choose to follow, with no measure of whether they ran or what they changed. Nothing fails when a rule is ignored (page.py), nothing checks a tool's input against the real record (cost stops), and no rule is tested on a past chat before it is written (pillar rule). Earlier audits failed for the same reason: they judged rules on paper, not against results, so their ideas "sounded great" and the bills did not move.

## Approaches weighed
1. **Sweep audit:** read every rule and tool and grade it. Paper judgement again; huge reading cost; rejected.
2. **Outcome trace (reframe, learn-first):** start from each bad result of the last two films (each of Sam's notes, each stage over plan, each fault that reached him), trace it in the chats to the rule or tool that should have caught it and whether it ran. Only rules that touch real results get looked at.
3. **Automatic meter:** the Stop hook that already reads each chat's record also counts which tools ran, hand code searches, and Sam's notes into the ledger, every chat, no choice involved.
4. **Gate everything:** turn rules into hooks that block. Right for some, but which ones needs 2 first.
5. **Test-before-adopt:** every new rule or tool must be replayed on a past chat and name its number to beat. Good, but it is a change and waits its turn.

Choice: 2, then 3, then one change at a time from what 2 finds.

## Proposal
- **Learn first (changes nothing):** the outcome trace over Protest Tiers and Remakes, whole chats. Helpers dump each chat's record; a script counts tool runs; every note and every stage over plan gets one row: result, cost, rule/tool that should have caught it, ran yes/no, why. Output: one ranked table in the film's ledger folder. Cost about 3-5% of a week (unchecked estimate), a project cost, not a film's.
- **Change 1 (evidence already in: three ledgers read 0 notes):** ledger auto fills notes, repeats and per-tool run counts from the chat record after every reply. Enforced by the existing Stop hook. Number to beat: the counts equal a hand count of chats 29 and 31 (0 page.py, 25/26 greps) and Protest Tiers' notes table. Cost about 1-2%.
- **Changes 2 onward, one per yes,** each from a top row of the trace (likely candidates: moves-stage cost, code looks), each with its own number from the table, reviewed against the next film's ledger when Sam declares it complete. A rule that traced to nothing over three films is offered with a "Lost:" line.
- **What Sam notices:** first a table that shows, in plain lines, which rules saved money or notes and which did not; then films whose ledger shows notes and per-stage costs, so every later yes is judged on real numbers.

## Sam test
- Q1 Expert: outcome-first evaluation plus automatic telemetry is what an agent-workflow expert would do.
- Q2 Best result: whole chats of two films, chosen by results, not one film or the cheapest chats.
- Q3 Comprehensive: root cause named; the meter runs in a hook, not by choice; success is a count that must match a hand count.
- Q4 Most intelligent: five different approaches weighed; the sweep rejected for reason.
- Q5 Risk: the trace changes nothing; change 1 only writes the ledger and is undone alone.
- Q6 Checked: sources named; costs of the work marked unchecked.
- Q7 Not cheap: whole chats of two films, not a sample; costed honestly.
- Q8 Nothing temporary: the meter is permanent; each change is reviewed at film completion, no trials.

## Lost / Added
Lost: nothing now. Added: one trace table; ledger columns that fill themselves.

## Unchecked
The trace's cost; whether chat records of Remakes are still listable; Protest Tiers' full count of Sam's notes (some archived); why the ledger's "After the film" line says 33.55% against 51.27% spent.
