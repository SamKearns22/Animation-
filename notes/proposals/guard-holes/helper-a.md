# Helper A: guard holes

## Leak
Leak: it hints at a fix ("every film" unused); taken as fact only.

## Results
- Probe re-run: 9 of 12 change asks missed, 1 of 10 routine stopped ("hook text"). All invented (probe.py).
- **Untested hole:** `questions()` only sees a line with a "?" or starting with "Need". House-format asks (numbered, "Y/N", CLAUDE.md) are invisible. These pass: "8. New rule 80, in the rulebook: ... Y/N" (real, notes/archive/sitting-kit.md); "- **Needs Sam:** Y/N on the rule wording below"; "1. Y: the critic runs on Sonnet (my pick). Y/N".
- **Real record** (scan of notes/): 76 decision lines; 8 are seen as asks; 0 are blocked. Missed real change asks include the critic on Sonnet, the places kit, rule 80, and "from the next film" (morning-report.md, sitting-kit.md, cost-diagnosis-handovers.md). (Summaries; wording sent unchecked.)
- **Shield** (`reply_faults`): one judged proposal named in a reply lets every other ask through.
- No wrong stops are logged yet (no unrouted.md file). A route run costs about 1.3% of a week (install-route verdict). The cost of a rewrite is unchecked.
- Gap: no labelled set of real asks exists.

## The real decision
Can the guard tell a change from a film question in the words chats really send? Bigger levers than word lists: what counts as an ask, and the shield.

## Root cause
The guard judges by topic words on one line, but a change is defined by its reach: it outlives this film's content. Topic words overlap: "render tool" loses to "render", "hook text" trips "hook", "check sheet step" loses to "sheet". Ask detection expects a "?" that the house format leaves out. Tested only on self-written lines, neither hole showed.

## Approaches weighed
1. **Patch the lists:** add gate, critic and scope words; let change words win over routine ones. Cheap, but it fails on new wording.
2. **Reframe, test reach:** any numbered, Y/N or Need line is an ask. It is a change if it touches a system thing or reaches beyond this film. Proposals are matched per question.
3. **Model judge in the hook:** copes with new wording, but may vary, and costs a call on every stop (unchecked).
4. **Learn first:** label real asks and measure every option against them.
5. **Guard the effect:** block pushes to system files that have no proposal. This conflicts with Sam's adopted rule, so it is a separate decision.

Chosen: 4, then 2. Use 3 only if 2 fails.

## Proposal
**L1, learn (no Y needed):** one Opus-medium chat gathers every ask sent to Sam from notes/, the archive and the Protest Tiers and Blessed chats (`list_events`). It labels each with a reason and splits them into tuning and held-out halves (kittest data). It scores today's guard. About 2% (unchecked).

**Then one change at a time, each with its own Y, its own kittest case and its own undo:**
- **C1, no shield:** each change question names its own judged proposal. Beat: a reply with one judged proposal and one unjudged ask is blocked.
- **C2, refusal names only the route.** Beat: no unrouted.md second try that just rewords the same ask.
- **C3, reach test replaces the word lists.** Beat, on the held-out half: 0 change asks missed, at most 1 routine ask in 20 stopped. The probe and the 5 replay replies must still pass.
- **C4, wider ask detection** (numbered, Y/N, "Needs Sam" and "Decide" lines). After C3, so wrong stops do not multiply. Beat: every ask in the set is detected.
- **C5, only if C3 misses:** the model judge, put through its own route run.

**Enforcement:** the kittest runs the whole set; handover.py flags unrouted lines.

**Cost:** about 2% plus 0.5-1% per change (unchecked). It is paid once, not per film, set against the 15% target.

**Sam notices:** every back-end question comes to him already judged.

## Sam test
- Q1: Yes. An expert measures a classifier on real data with a held-out half.
- Q2: It uses the real record across chats, not invented lines.
- Q3: Root cause named; enforced by the kittest; the held-out half catches tuning to the test.
- Q4: Five different approaches weighed.
- Q5: Each change can be undone alone; C4 waits for C3.
- Q6: Every fact is sourced or marked unchecked.
- Q7: Sized to zero real misses, not a cheap word patch.
- Q8: Permanent on each Y; reviewed at film end.

## Lost / Added
Lost: about 3-6% of a week, once; leaky until C4.
Added: a real labelled set of asks, a guard measured against it, and the shield gone.

## Unchecked
Probe typicality; real wording sent; all costs; the model judge's steadiness.
