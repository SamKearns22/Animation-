# Helper A: aim-check reviewer, step 2

## Leak
Mild: the title and "what, if anything, Sam should be asked to say yes to" assume a fresh reviewer is the thing being decided. No remedy is given.

## Results
- Missed same-quality kit reuse: 2 clear + 1 partial, all Milburn, about 0.1-0.2% of a week over both films; none challenged (study.md). The verdict's reviewer costs 1-1.5% a film and pays only if it catches about one Milburn-sized miss (aim-check.md, F6). On the target it was built for, it returns about a tenth of its cost.
- Milburn: 21.99% on the ledger at 366 USD = Sam's 22% (ledger/milburn.md; study.md). 33 notes from Sam, 4 repeats, and faults Sam saw that checks should have caught: name card clipping twice, missing mouth, brows, 3/4 people (milburn-review.md). The ledger itself records 0 notes and 0 repeats, and its stage lines were closed late (sets "16.68" holds the whole plan and cast), so per-stage cost is not usable.
- Milburn's 10 Opus chats cost about 67 of the 80.44 USD; most ran 92-136 steps and ended at 200-300k history (ledger/milburn.md).
- The reverse was re-staged because Sam judged the composition "poor" (note 5, chat 6 failed, fixed chat 10; archive/milburn.md line 233): a taste miss, not a cost choice. Lesson 3 (two quick framings first) already has Sam's Y (milburn-review.md).
- Blessed: Walliams' face 10.9%, repeats ~4%, chat 5 bundling ~4% avoidable (cost-diagnosis.md). These are in % of a 290 USD week; at 366 they are about 8.7%, ~3.2%, ~3%. The problem file mixes the two week sizes.
- Across 36 Opus chats, 26 that ended over 200k history cost 158 of 176 USD; re-reading history is 49% of spend (cost-diagnosis.md).
- Gap: no record prices each re-stage, each re-estimate's added scope, or each repeat on its own (unchecked in the problem file too). The decision needs that number.

## The real decision
Not "how should a reviewer question costly choices", but "what is the next change that most moves a whole film from 22-49% to 15% without lowering quality". Bigger levers than a reviewer: faults reaching Sam and coming back (repeats), taste misses on staging, and long Opus chats re-reading big histories. Several already have Sam's Y in the queue.

## Root cause
The overrun is made of rework after Sam sees a fault or a framing he dislikes, and of chats that grow past 200k, not of choosing a dear means when a cheap one existed. The reviewer was aimed on a guess (missed cheaper ways) that the study disproved. F4 already said the mid-stage choices fall between its passes; the study shows that is where the money is.

## Approaches weighed
1. Reviewer as designed (plan and stage start, kit matches): fails its own F6 bar by about ten times. Rejected.
2. Reframe: a reviewer fired by trigger, not schedule: the quiet cost line's existing 1.5x stage flag, a second staging of one shot, an estimate going up. It costs only when money is already going wrong. Unproven: no record shows it would have changed a Milburn or Blessed moment.
3. Reframe wider: drop the reviewer; spend the effort on the queued lessons that hit rework (1, 2, 3, 4, 8) and on chat size. These target the measured causes, but their combined coverage of the overrun is unmeasured.
4. Learn first: price each overrun cause in both films and mark which queued lesson or existing rule already covers it; what is left uncovered decides whether approach 2 is worth a yes.

Chosen: 4, then 2 only if the number calls for it.

## Proposal
- **Step A, learn (changes nothing; about 0.5% of a week; Sonnet).** From the two ledgers' per-chat app figures and step splits, and the two notes tables, price at 366 USD each cause: every re-stage, every re-estimate's added scope (means only, never the joke), every repeat note, every chat over 200k. For each, mark "covered by" (lesson 1, 2, 3, 4, 8, Job C 1-6, or a CLAUDE.md rule) or "uncovered", and whether a cold reader at that moment had a same-quality cheaper means to offer. Output: the uncovered points per film.
- **Step B, the one change, its own yes, only if Step A shows at least 3 uncovered points per film that a trigger moment could have caught:** the trigger-fired reviewer (approach 2). The tool fires it, not the chat; handover.py end refuses a flagged stage without its filed answer; Sam gets no cost messages. Number to beat at the next film's end review: its own cost times three saved, measured by the same pricing as Step A. Cost to build about 1%; to run about 0.3% per trigger.
- **If Step A shows under 3 points:** the reviewer is dropped for good, and the largest uncovered cause goes to the route as its own proposal.
- Sam would notice: one short message with the study's result and this step, then either one yes with a number or a "Lost: the reviewer" line.

## Sam test
Q1: Yes; an expert measures where the money went before adding a checker.
Q2: Yes; both films, every cause, not only kit reuse.
Q3: Step A's output is a number per cause; Step B is enforced by the tool and handover check, not by reading.
Q4: Four different approaches, two reframes; the reviewer is no longer assumed.
Q5: Step A changes nothing; Sam is not asked to trust an unproven reviewer.
Q6: Sources named; week-size mix flagged; gaps marked.
Q7: The reviewer is sized by a 3x return, not by its price; the cheap version (aim at kit only) is rejected.
Q8: No trial: Step B is made properly or the reviewer is dropped for good.

## Lost / Added
Lost: the fresh reviewer as Sam chose it on 19 Nov (it fails its own bar). Added: about 0.5% of a week for Step A; one priced list of where both films' money went.

## Unchecked
Whether a cold reviewer at re-stage time would have changed anything; how much of the overrun the queued lessons already cover; the cost of each re-stage on its own.
