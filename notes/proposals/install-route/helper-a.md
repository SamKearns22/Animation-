# Helper A: switch on the proposal route?

## Leak
None.

## Results
- The chat's first idea lost to Sam's push 5 of 5 times (notes/proposal-route.md, "The problem").
- Replay 2 passed 4 of 5, which is weak proof. helper.md itself encodes the answers to cases 1, 4 and 5 (steps 3, 2 and 7; checked). The replay tested recall, so this run is the first untuned case.
- Build cost: 21.69% of a week over 6 chats. Helpers 4.41%, judges 2.12%, so one route run is about 1.3-1.4% (notes/ledger/proposal-route.md; estimate).
- Coverage: the hook sees only questions to Sam. Git shows 101 commits that touched system files from 12 to 15 Nov. About 60 of them name no Sam (counted by subject), so no question covered them.
- Bypass (tested with `reply_faults`): "Shall I change the render tool so it reuses cached frames? Y/N" passes, and so does a "clip check" change, because ROUTINE_RE matches. A real change of this kind went in on 15 Nov (commit 0861dd3).
- Results record is blind: both film ledgers say "0 rounds, 0 notes" (notes/ledger/protest-tiers.md, blessed.md). Step 6 `review` reads those zeros.
- Films cost 53.56% (Protest Tiers) and 62.21% (Blessed) against a 15% target. Protest Tiers is topical and on hiatus (story/status.md).
- Gap: nobody has counted how many changes per film reach Sam, so the route's cost per film is unknown.

## The real decision
How system changes made during a film come to improve that film within 15% of a week. Bigger levers than the hook: a results record, the silent changes (most of them), and the hiatus.

## Root cause
Claude's first idea is anchored and sized cheap, and nothing feeds results back to it: notes go unrecorded and step 6 has never run. Sam was the only feedback. The route adds critics before a proposal reaches Sam, but still no feedback after a change is made.

## Approaches weighed
1. **As built, permanent now:** better asks, but the rule is wider than its check, and the bypass and the blind step 6 stay.
2. **Reframe (chosen):** route everything put to Sam, make results recordable, then size coverage of silent changes from the measurements.
3. **Learn first, route off:** drops a guard proven on the known failures (it blocks all 5 replay replies).
4. **Undo, and the chat self-asks Sam's 8 questions:** fails Q3, because it relies on the chat choosing to do it.

## Proposal
**Change 1 (Sam's Y):** the hook stays on as built. The rule is worded to match what it enforces: "every change put to Sam goes through the route; changes made unasked are listed at handover and judged in the end-of-film review". It replaces the 12 Nov search-first bullet, so the rulebook does not grow. Beat: 0 pushes after a verdict, each logged with `propose.py mark replaced`.

**Learning step (read-only, no Y, about 1.5%, estimate):** from git and the Blessed and Protest Tiers transcripts, find:
- notes and repeated notes per round
- changes per film, asked and silent
- how many were later replaced
- asks per film, which sets the route's cost per film

**Then one change at a time, each through the route:**
- **C2:** the ledger counts Sam's notes at each handover. Beat: matches a hand count.
- **C3:** close the bypass. Beat: a kittest blocks the 3 sample questions and the 5 replay replies, and passes routine animatic and render Y/Ns.
- **C4:** silent changes are routed only if the learning step shows they are replaced more often. Beat: replaced rate.

**Cost:** about 1.4% per run, roughly 7% of a week at 5 asks a film (the learning step confirms the count). C2-C4 about 2-4% each (estimate). Protest Tiers resumes now; film work is outside the route.

**What Sam notices:** two options per proposal with a "Critiqued" line; fewer pushes; the film restarts; real note counts in the ledger.

## Sam test
- Q1: adds feedback and coverage.
- Q2: whole-film changes and notes.
- Q3: hook-enforced; gaps named and closed; measured.
- Q4: four approaches weighed.
- Q5: replay overstates proof; each change undoable alone.
- Q6: sources named; estimates marked.
- Q7: sized by result; cost stated.
- Q8: permanent, reviewed at film end.

## Lost / Added
- Lost: about 1.4% per proposal, and a delay before Sam sees wording for his own "I want a rule" asks.
- Added: the hook, the learning chat, note counts, kittest cases.

## Unchecked
- Cost per run (4.41% in the ledger against 4.76% in the notes).
- The commit split (by subject text).
- Asks per film.
- Same-model judge bias.
- Blessed's cost: 62.21% against 80.02% in a compare line.
